from loaders.model_loader import (
    movies,
    embeddings,
    index
)


def semantic_search(movie_name, top_k=50):

    movie_index = movies[
        movies["title"] == movie_name
    ].index[0]

    query = embeddings[movie_index].reshape(1, -1)

    scores, indices = index.search(
        query,
        top_k
    )

    return scores, indices
