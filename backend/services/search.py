import faiss

from loaders import model_loader

from rapidfuzz import process, fuzz


def find_movie_index(movie_name):

    movies = model_loader.movies

    titles = movies["title"].fillna("").tolist()

    query = movie_name.strip().lower()

    normalized_titles = [
        title.lower()
        for title in titles
    ]

    exact_matches = [
        i
        for i, title in enumerate(normalized_titles)
        if title == query
    ]

    if exact_matches:

        return exact_matches[0]

    match = process.extractOne(
        query,
        normalized_titles,
        scorer=fuzz.WRatio
    )

    if match is None:

        return None

    matched_title, score, index = match

    if score >= 70:

        return index

    return None


def semantic_search(movie_name, top_k=50):

    movies = model_loader.movies
    embeddings = model_loader.embeddings
    index = model_loader.index

    movie_index = find_movie_index(
        movie_name
    )

    if movie_index is None:

        return None, None

    query = embeddings[
        movie_index
    ].reshape(1, -1)

    scores, indices = index.search(
        query,
        top_k + 1
    )

    return scores, indices


def semantic_query_search(query, top_k=50):

    semantic_model = model_loader.semantic_model

    index = model_loader.index

    query_embedding = semantic_model.encode(
        [query],
        convert_to_numpy=True
    )

    faiss.normalize_L2(
        query_embedding
    )

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    return scores, indices