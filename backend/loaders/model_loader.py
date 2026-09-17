import pickle
import numpy as np
import faiss
from pathlib import Path

from sentence_transformers import SentenceTransformer


movies = None
embeddings = None
index = None
svd_model = None
semantic_model = None


# Get project root directory
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "models"


def load_models():

    global movies
    global embeddings
    global index
    global svd_model
    global semantic_model

    print("Loading models...")

    movies = pickle.load(
        open(MODEL_DIR / "movie_metadata.pkl", "rb")
    )

    embeddings = np.load(
        MODEL_DIR / "movie_embeddings.npy"
    )

    index = faiss.read_index(
        str(MODEL_DIR / "faiss.index")
    )

    svd_model = pickle.load(
        open(MODEL_DIR / "svd_model.pkl", "rb")
    )

    print("Loading semantic model...")

    semantic_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("All models loaded successfully.")