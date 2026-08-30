from flask import Blueprint
from flask import jsonify
from flask import request

from recommender import recommend_movie

from database.database import (
    initialize_database,
    add_movie_history,
    add_rating,
    add_to_watchlist,
    get_movie_history,
    get_ratings,
    get_watchlist,
    delete_movie_history,
    delete_from_watchlist
)
from services.tmdb import get_movie_details

movie_routes = Blueprint(
    "movie_routes",
    __name__
)


initialize_database()


# =========================================
# RECOMMEND MOVIES
# =========================================

@movie_routes.route(
    "/recommend",
    methods=["POST"]
)
def recommend():

    data = request.get_json()

    movie = data.get("movie")

    if not movie:

        return jsonify({
            "error":
            "Movie name or query is required."
        }), 400


    try:

        result = recommend_movie(movie)


        if (
            isinstance(result, dict)
            and "error" in result
        ):

            return jsonify(result), 404


        # Save searched movie

        user_id = 1

        searched_movie = result.get(
            "searched_movie"
        )


        if searched_movie:

            movie_title = searched_movie.get(
                "title"
            )

            if movie_title:

                add_movie_history(
                    user_id,
                    movie_title
                )


        return jsonify(result)


    except Exception as error:

        print(
            "Recommendation Error:",
            error
        )

        return jsonify({
            "error":
            "Internal server error."
        }), 500


# =========================================
# RATE MOVIE
# =========================================

@movie_routes.route(
    "/rate",
    methods=["POST"]
)
def rate_movie():

    data = request.get_json()

    movie_title = data.get(
        "movie_title"
    )

    rating = data.get(
        "rating"
    )


    if not movie_title:

        return jsonify({
            "error":
            "movie_title is required."
        }), 400


    if rating is None:

        return jsonify({
            "error":
            "rating is required."
        }), 400


    try:

        rating = float(rating)


    except (TypeError, ValueError):

        return jsonify({
            "error":
            "Rating must be a number."
        }), 400


    if rating < 1 or rating > 5:

        return jsonify({
            "error":
            "Rating must be between 1 and 5."
        }), 400


    try:

        user_id = 1

        add_rating(
            user_id,
            movie_title,
            rating
        )


        return jsonify({

            "message":
            "Movie rated successfully.",

            "movie_title":
            movie_title,

            "rating":
            rating

        })


    except Exception as error:

        print(
            "Rating Error:",
            error
        )

        return jsonify({
            "error":
            "Could not save rating."
        }), 500


# =========================================
# ADD TO WATCHLIST
# =========================================

@movie_routes.route(
    "/watchlist",
    methods=["POST"]
)
def add_watchlist():

    data = request.get_json()

    movie_title = data.get(
        "movie_title"
    )


    if not movie_title:

        return jsonify({
            "error":
            "movie_title is required."
        }), 400


    try:

        user_id = 1

        add_to_watchlist(
            user_id,
            movie_title
        )


        return jsonify({

            "message":
            "Movie added to watchlist.",

            "movie_title":
            movie_title

        })


    except Exception as error:

        print(
            "Watchlist Error:",
            error
        )

        return jsonify({
            "error":
            "Could not add movie to watchlist."
        }), 500


# =========================================
# GET SEARCH HISTORY
# =========================================

@movie_routes.route(
    "/history",
    methods=["GET"]
)
def history():

    user_id = 1

    history_data = get_movie_history(
        user_id
    )


    return jsonify([
        dict(row)
        for row in history_data
    ])


# =========================================
# GET RATINGS
# =========================================

@movie_routes.route(
    "/ratings",
    methods=["GET"]
)
def ratings():

    user_id = 1

    rating_data = get_ratings(
        user_id
    )


    return jsonify([
        dict(row)
        for row in rating_data
    ])


# =========================================
# GET WATCHLIST
# =========================================

@movie_routes.route(
    "/watchlist",
    methods=["GET"]
)
def watchlist():

    user_id = 1

    watchlist_data = get_watchlist(
        user_id
    )

    movies = []

    for row in watchlist_data:

        movie_title = row["movie_title"]

        movie_details = get_movie_details(
            movie_title
        )

        movie = {

            "id": row["id"],

            "title": movie_title,

            "poster":
                movie_details.get("poster"),

            "overview":
                movie_details.get("overview"),

            "tmdb_rating":
                movie_details.get("tmdb_rating"),

            "release_date":
                movie_details.get("release_date"),

            "rating":
                movie_details.get("tmdb_rating")
                if movie_details.get("tmdb_rating") is not None
                else "N/A",

            "added_at":
                row["added_at"]

        }

        movies.append(movie)

    return jsonify(movies)

# =========================================
# DELETE HISTORY ITEM
# =========================================

@movie_routes.route(
    "/history/<int:history_id>",
    methods=["DELETE"]
)
def delete_history(history_id):

    try:

        user_id = 1

        deleted = delete_movie_history(
            user_id,
            history_id
        )

        if deleted == 0:

            return jsonify({
                "error":
                "History item not found."
            }), 404

        return jsonify({

            "message":
            "History item deleted successfully.",

            "id":
            history_id

        })

    except Exception as error:

        print(
            "Delete History Error:",
            error
        )

        return jsonify({
            "error":
            "Could not delete history item."
        }), 500


# =========================================
# DELETE WATCHLIST ITEM
# =========================================

@movie_routes.route(
    "/watchlist/<int:watchlist_id>",
    methods=["DELETE"]
)
def delete_watchlist(watchlist_id):

    try:

        user_id = 1

        deleted = delete_from_watchlist(
            user_id,
            watchlist_id
        )

        if deleted == 0:

            return jsonify({
                "error":
                "Watchlist item not found."
            }), 404

        return jsonify({

            "message":
            "Watchlist item deleted successfully.",

            "id":
            watchlist_id

        })

    except Exception as error:

        print(
            "Delete Watchlist Error:",
            error
        )

        return jsonify({
            "error":
            "Could not delete watchlist item."
        }), 500