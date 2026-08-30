import sqlite3


DATABASE_NAME = "users.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            movie_title TEXT NOT NULL,

            searched_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            movie_title TEXT NOT NULL,

            rating REAL NOT NULL,

            rated_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            movie_title TEXT NOT NULL,

            added_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)


    connection.commit()

    connection.close()


def create_user(username):

    connection = get_connection()

    cursor = connection.cursor()


    try:

        cursor.execute(
            """
            INSERT INTO users (username)
            VALUES (?)
            """,
            (username,)
        )

        connection.commit()

        user_id = cursor.lastrowid

    except sqlite3.IntegrityError:

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user_id = cursor.fetchone()["id"]


    connection.close()

    return user_id


def add_movie_history(
    user_id,
    movie_title
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO movie_history
        (user_id, movie_title)
        VALUES (?, ?)
        """,
        (
            user_id,
            movie_title
        )
    )


    connection.commit()

    connection.close()


def add_rating(
    user_id,
    movie_title,
    rating
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO ratings
        (user_id, movie_title, rating)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            movie_title,
            rating
        )
    )


    connection.commit()

    connection.close()


def add_to_watchlist(
    user_id,
    movie_title
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO watchlist
        (user_id, movie_title)
        VALUES (?, ?)
        """,
        (
            user_id,
            movie_title
        )
    )


    connection.commit()

    connection.close()


# =========================================
# DELETE HISTORY ITEM
# =========================================

def delete_movie_history(
    user_id,
    history_id
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM movie_history
        WHERE id = ?
        AND user_id = ?
        """,
        (
            history_id,
            user_id
        )
    )


    deleted = cursor.rowcount


    connection.commit()

    connection.close()

    return deleted


# =========================================
# DELETE WATCHLIST ITEM
# =========================================

def delete_from_watchlist(
    user_id,
    watchlist_id
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM watchlist
        WHERE id = ?
        AND user_id = ?
        """,
        (
            watchlist_id,
            user_id
        )
    )


    deleted = cursor.rowcount


    connection.commit()

    connection.close()

    return deleted


# =========================================
# GET MOVIE HISTORY
# =========================================

def get_movie_history(user_id):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            id,
            movie_title,
            searched_at

        FROM movie_history

        WHERE user_id = ?

        ORDER BY searched_at DESC
        """,
        (user_id,)
    )


    history = cursor.fetchall()

    connection.close()

    return history


# =========================================
# GET RATINGS
# =========================================

def get_ratings(user_id):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            movie_title,
            rating,
            rated_at

        FROM ratings

        WHERE user_id = ?

        ORDER BY rated_at DESC
        """,
        (user_id,)
    )


    ratings = cursor.fetchall()

    connection.close()

    return ratings


# =========================================
# GET WATCHLIST
# =========================================

def get_watchlist(user_id):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            id,
            movie_title,
            added_at

        FROM watchlist

        WHERE user_id = ?

        ORDER BY added_at DESC
        """,
        (user_id,)
    )


    watchlist = cursor.fetchall()

    connection.close()

    return watchlist


if __name__ == "__main__":

    initialize_database()

    print(
        "Database initialized successfully."
    )