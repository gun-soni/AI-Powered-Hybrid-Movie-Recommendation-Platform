from loaders import model_loader


def hybrid_score(candidate_movies,
                 semantic_scores,
                 user_id=1):
    svd_model = model_loader.svd_model

    collab_scores = []

    for movie_id in candidate_movies["id"]:

        prediction = svd_model.predict(
            user_id,
            movie_id
        )

        collab_scores.append(
            prediction.est / 5
        )

    candidate_movies["semantic_score"] = semantic_scores

    candidate_movies["collab_score"] = collab_scores

    candidate_movies["vote_score"] = (
        candidate_movies["vote_average"] / 10
    )

    candidate_movies["final_score"] = (

        0.50 * candidate_movies["semantic_score"]

        +

        0.30 * candidate_movies["collab_score"]

        +

        0.20 * candidate_movies["vote_score"]

    )

    candidate_movies = candidate_movies.sort_values(

        by="final_score",

        ascending=False

    )

    return candidate_movies