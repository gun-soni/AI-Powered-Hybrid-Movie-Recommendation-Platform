import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


movies = None
embeddings = None
index = None
svd_model = None
semantic_model = None


def load_models():

    global movies
    global embeddings
    global index
    global svd_model
    global semantic_model

    print("Loading models...")

    movies = pickle.load(
        open("../models/movie_metadata.pkl", "rb")
    )

    embeddings = np.load(
        "../models/movie_embeddings.npy"
    )

    index = faiss.read_index(
        "../models/faiss.index"
    )

    svd_model = pickle.load(
        open("../models/svd_model.pkl", "rb")
    )

    print("Loading semantic model...")

    semantic_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("All models loaded successfully.")