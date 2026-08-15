from flask import Blueprint
from flask import jsonify
from flask import request

from recommender import recommend_movie


movie_routes = Blueprint(
    "movie_routes",
    __name__
)


@movie_routes.route(
    "/recommend",
    methods=["POST"]
)
def recommend():

    data = request.get_json()

    movie = data.get("movie")

    if not movie:

        return jsonify({
            "error": "Movie name is required."
        }), 400

    try:

        result = recommend_movie(movie)

        if isinstance(result, dict) and "error" in result:

            return jsonify(result), 404

        return jsonify(result)

    except Exception as error:

        print("Recommendation Error:", error)

        return jsonify({
            "error": "Internal server error."
        }), 500