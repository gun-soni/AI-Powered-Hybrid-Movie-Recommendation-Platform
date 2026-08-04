import pickle
import numpy as np
import faiss

# Global Variables
movies = None
embeddings = None
index = None
svd_model = None


def load_models():

    global movies
    global embeddings
    global index
    global svd_model

    print("Loading Models...")

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

    print("Models Loaded Successfully")