from flask import Flask
from flask_cors import CORS

from routes import movie_routes

app = Flask(__name__)

CORS(app)

app.register_blueprint(movie_routes)


@app.route("/")
def home():
    return {
        "status": "Running",
        "message": "AI Movie Recommendation API"
    }


from loaders.model_loader import load_models

load_models()

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )