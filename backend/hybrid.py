import ast

from loaders import model_loader


def to_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):

        try:
            parsed = ast.literal_eval(value)

            if isinstance(parsed, list):
                return parsed

        except (ValueError, SyntaxError):
            pass

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


def contains_value(movie_value, search_values):

    movie_items = [
        str(item).strip().lower()
        for item in to_list(movie_value)
    ]

    search_items = [
        str(item).strip().lower()
        for item in search_values
    ]

    for search_item in search_items:

        for movie_item in movie_items:

            if (
                search_item == movie_item
                or search_item in movie_item
                or movie_item in search_item
            ):
                return True

    return False


def get_column_value(movie, column):

    if column in movie.index:
        return movie[column]

    return []


def calculate_preference_score(
    candidate_movies,
    intent
):

    scores = []

    requested_genres = intent.genres or []

    requested_actors = intent.actors or []

    requested_director = intent.director

    requested_year = intent.year

    mood = (
        intent.mood.lower()
        if intent.mood
        else None
    )


    for _, movie in candidate_movies.iterrows():

        preference_score = 0.0


        # -----------------------------
        # Genre
        # -----------------------------

        if requested_genres:

            genres = get_column_value(
                movie,
                "genres"
            )

            if contains_value(
                genres,
                requested_genres
            ):
                preference_score += 0.30


        # -----------------------------
        # Actors
        # -----------------------------

        if requested_actors:

            cast = get_column_value(
                movie,
                "cast"
            )

            if contains_value(
                cast,
                requested_actors
            ):
                preference_score += 0.20


        # -----------------------------
        # Director
        # -----------------------------

        if requested_director:

            crew = get_column_value(
                movie,
                "crew"
            )

            if contains_value(
                crew,
                [requested_director]
            ):
                preference_score += 0.25


        # -----------------------------
        # Year
        # -----------------------------

        if requested_year:

            release_date = str(
                movie.get(
                    "release_date",
                    ""
                )
            )

            if release_date.startswith(
                str(requested_year)
            ):
                preference_score += 0.15


        # -----------------------------
        # Mood
        # -----------------------------

        if mood:

            genres = get_column_value(
                movie,
                "genres"
            )

            genres = [
                str(item).lower()
                for item in to_list(genres)
            ]


            mood_genres = {

                "emotional": [
                    "drama",
                    "romance"
                ],

                "romantic": [
                    "romance"
                ],

                "funny": [
                    "comedy"
                ],

                "scary": [
                    "horror",
                    "thriller"
                ],

                "exciting": [
                    "action",
                    "adventure",
                    "thriller"
                ],

                "dark": [
                    "crime",
                    "thriller",
                    "horror"
                ],

                "family": [
                    "family",
                    "animation"
                ],

                "relaxing": [
                    "comedy",
                    "romance",
                    "family"
                ]
            }


            matching_genres = mood_genres.get(
                mood,
                []
            )


            if any(
                genre in genres
                for genre in matching_genres
            ):
                preference_score += 0.10


        scores.append(
            min(preference_score, 1.0)
        )


    return scores


def hybrid_score(
    candidate_movies,
    semantic_scores,
    intent=None,
    user_id=1
):

    svd_model = model_loader.svd_model


    # ---------------------------------
    # Semantic Score
    # ---------------------------------

    semantic_scores = semantic_scores.astype(
        float
    )

    semantic_min = semantic_scores.min()

    semantic_max = semantic_scores.max()


    if semantic_max != semantic_min:

        semantic_scores = (
            semantic_scores - semantic_min
        ) / (
            semantic_max - semantic_min
        )

    else:

        semantic_scores = (
            semantic_scores * 0
        ) + 1


    candidate_movies[
        "semantic_score"
    ] = semantic_scores


    # ---------------------------------
    # Collaborative Filtering
    # ---------------------------------

    collab_scores = []


    for movie_id in candidate_movies["id"]:

        try:

            prediction = svd_model.predict(
                user_id,
                movie_id
            )

            score = prediction.est / 5.0

        except Exception:

            score = 0.0


        collab_scores.append(score)


    candidate_movies[
        "collab_score"
    ] = collab_scores


    # ---------------------------------
    # Rating
    # ---------------------------------

    if "vote_average" in candidate_movies.columns:

        candidate_movies[
            "vote_score"
        ] = (
            candidate_movies[
                "vote_average"
            ].fillna(0) / 10.0
        )

    else:

        candidate_movies[
            "vote_score"
        ] = 0.0


    # ---------------------------------
    # Gemini Preferences
    # ---------------------------------

    if intent is not None:

        preference_scores = (
            calculate_preference_score(
                candidate_movies,
                intent
            )
        )

    else:

        preference_scores = [
            0.0
            for _ in range(
                len(candidate_movies)
            )
        ]


    candidate_movies[
        "preference_score"
    ] = preference_scores


    # ---------------------------------
    # Final Score
    # ---------------------------------

    candidate_movies[
        "final_score"
    ] = (

        0.40
        * candidate_movies[
            "semantic_score"
        ]

        +

        0.25
        * candidate_movies[
            "collab_score"
        ]

        +

        0.15
        * candidate_movies[
            "vote_score"
        ]

        +

        0.20
        * candidate_movies[
            "preference_score"
        ]

    )


    return candidate_movies.sort_values(
        by="final_score",
        ascending=False
    )