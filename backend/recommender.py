from services.search import semantic_search

from hybrid import hybrid_score

from loaders import model_loader


def recommend_movie(movie_name):

    scores, indices = semantic_search(
        movie_name
    )

    candidate_movies = model_loader.movies.iloc[
    indices[0]
    ].copy()
    semantic_scores = scores[0]

    recommendations = hybrid_score(
        candidate_movies,
        semantic_scores
    )

    output = []

    for _, movie in recommendations.head(10).iterrows():

        output.append({

            "title": movie["title"],

            "rating": float(movie["vote_average"]),

            "release_date": movie["release_date"]

        })

    return output