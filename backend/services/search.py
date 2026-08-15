from loaders import model_loader


def semantic_search(movie_name, top_k=50):

    movies = model_loader.movies
    embeddings = model_loader.embeddings
    index = model_loader.index

    movie_index = movies[
        movies["title"] == movie_name
    ].index[0]

    query = embeddings[movie_index].reshape(1, -1)

    scores, indices = index.search(query, top_k)

    return scores, indices