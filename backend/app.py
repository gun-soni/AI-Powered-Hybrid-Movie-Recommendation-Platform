import os

from flask import (
    Flask,
    send_from_directory
)

from flask_cors import CORS

from routes import movie_routes

from loaders.model_loader import load_models


# =========================================
# PATHS
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "..",
    "frontend"
)


# =========================================
# FLASK APP
# =========================================

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

CORS(app)


# =========================================
# REGISTER API ROUTES
# =========================================

app.register_blueprint(
    movie_routes
)


# =========================================
# FRONTEND
# =========================================

@app.route("/")
def serve_frontend():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.route("/<path:path>")
def serve_frontend_files(path):

    file_path = os.path.join(
        FRONTEND_DIR,
        path
    )

    if os.path.isfile(file_path):

        return send_from_directory(
            FRONTEND_DIR,
            path
        )

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# =========================================
# LOAD MODELS
# =========================================

load_models()


# =========================================
# LOCAL DEVELOPMENT
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )