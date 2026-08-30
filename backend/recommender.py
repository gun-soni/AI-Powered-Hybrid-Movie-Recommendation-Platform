from services.search import (
    semantic_search,
    semantic_query_search
)

from services.gemini import understand_query

from hybrid import hybrid_score

from loaders import model_loader

from services.tmdb import get_movie_details


def build_movie_details(movie):

    title = movie["title"]

    tmdb_data = get_movie_details(title)

    return {
        "title": title,

        "rating": float(
            movie["vote_average"]
        ),

        "release_date": movie["release_date"],

        "poster": tmdb_data["poster"],

        "overview": tmdb_data["overview"],

        "tmdb_rating": tmdb_data["tmdb_rating"]
    }


def recommend_movie(user_query):

    # -----------------------------
    # Gemini
    # -----------------------------

    intent = understand_query(
        user_query
    )

    print("\nGemini Intent:")
    print(
        intent.model_dump()
    )


    # -----------------------------
    # Search
    # -----------------------------

    if intent.movie:

        scores, indices = semantic_search(
            intent.movie
        )

    else:

        scores, indices = semantic_query_search(
            user_query
        )


    # -----------------------------
    # Validate
    # -----------------------------

    if scores is None or indices is None:

        return {
            "error":
            "Could not understand the movie request."
        }


    # -----------------------------
    # Candidate movies
    # -----------------------------

    candidate_movies = (
        model_loader.movies.iloc[
            indices[0]
        ].copy()
    )

    semantic_scores = scores[0]


    # -----------------------------
    # Hybrid ranking
    # -----------------------------

    recommendations = hybrid_score(
        candidate_movies,
        semantic_scores,
        intent=intent
    )


    # -----------------------------
    # Searched movie
    # -----------------------------

    searched_movie = None


    if intent.movie:

        searched_title = (
            intent.movie
            .strip()
            .lower()
        )

        matching_movies = (
            model_loader.movies[
                model_loader.movies["title"]
                .fillna("")
                .str.lower()
                == searched_title
            ]
        )


        if not matching_movies.empty:

            searched_movie_data = (
                matching_movies.iloc[0]
            )

            searched_movie = (
                build_movie_details(
                    searched_movie_data
                )
            )


    # -----------------------------
    # Remove searched movie
    # from recommendations
    # -----------------------------

    if intent.movie:

        searched_title = (
            intent.movie
            .strip()
            .lower()
        )

        recommendations = (
            recommendations[
                recommendations["title"]
                .fillna("")
                .str.lower()
                != searched_title
            ]
        )


    # -----------------------------
    # Top 10
    # -----------------------------

    recommendations = (
        recommendations.head(10)
    )


    # -----------------------------
    # Build output
    # -----------------------------

    recommendation_output = []


    for _, movie in (
        recommendations.iterrows()
    ):

        recommendation_output.append(
            build_movie_details(movie)
        )


    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------

    return {

        "searched_movie":
            searched_movie,

        "recommendations":
            recommendation_output

    }