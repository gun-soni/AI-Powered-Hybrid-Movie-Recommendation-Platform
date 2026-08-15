from services.search import semantic_search

from hybrid import hybrid_score

from loaders import model_loader

from services.tmdb import get_movie_details


def recommend_movie(movie_name):

    scores, indices = semantic_search(
        movie_name
    )

    if scores is None or indices is None:

        return {
            "error": "Movie could not be identified."
        }

    candidate_movies = model_loader.movies.iloc[
        indices[0]
    ].copy()

    semantic_scores = scores[0]

    recommendations = hybrid_score(
        candidate_movies,
        semantic_scores
    )

    recommendations = recommendations[
        recommendations["title"].str.lower()
        != movie_name.strip().lower()
    ]

    output = []

    for _, movie in recommendations.head(10).iterrows():

        title = movie["title"]

        tmdb_data = get_movie_details(title)

        output.append({

            "title": title,

            "rating": float(
                movie["vote_average"]
            ),

            "release_date": movie["release_date"],

            "poster": tmdb_data["poster"],

            "overview": tmdb_data["overview"],

            "tmdb_rating":
                tmdb_data["tmdb_rating"]

        })

    return output