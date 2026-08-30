from database.database import (
    initialize_database,
    create_user,
    add_movie_history,
    add_rating,
    add_to_watchlist,
    get_movie_history,
    get_ratings,
    get_watchlist
)


initialize_database()


user_id = create_user(
    "demo_user"
)


print(
    "User ID:",
    user_id
)


add_movie_history(
    user_id,
    "Interstellar"
)


add_rating(
    user_id,
    "Interstellar",
    5
)


add_to_watchlist(
    user_id,
    "Arrival"
)


print("\nHistory:")

print(
    [
        dict(row)
        for row in get_movie_history(
            user_id
        )
    ]
)


print("\nRatings:")

print(
    [
        dict(row)
        for row in get_ratings(
            user_id
        )
    ]
)


print("\nWatchlist:")

print(
    [
        dict(row)
        for row in get_watchlist(
            user_id
        )
    ]
)