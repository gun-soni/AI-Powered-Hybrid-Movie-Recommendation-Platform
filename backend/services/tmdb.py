import requests

from config import TMDB_API_KEY


BASE_URL = "https://api.themoviedb.org/3"

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def get_movie_details(movie_name):

    url = f"{BASE_URL}/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_name
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return {
                "poster": None,
                "overview": None,
                "tmdb_rating": None,
                "release_date": None,
                "genres": []
            }

        movie = results[0]

        poster_path = movie.get("poster_path")

        poster = None

        if poster_path:
            poster = IMAGE_BASE_URL + poster_path

        return {
            "poster": poster,
            "overview": movie.get("overview"),
            "tmdb_rating": movie.get("vote_average"),
            "release_date": movie.get("release_date"),
            "genres": []
        }

    except requests.RequestException as error:

        print("TMDB API Error:", error)

        return {
            "poster": None,
            "overview": None,
            "tmdb_rating": None,
            "release_date": None,
            "genres": []
        }