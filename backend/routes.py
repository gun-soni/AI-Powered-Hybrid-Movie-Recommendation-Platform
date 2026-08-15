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

    movie = data["movie"]

    result = recommend_movie(movie)

    return jsonify(result)