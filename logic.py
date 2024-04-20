import sqlite3

def connect_to_db():
    conn = sqlite3.connect('movie.db')
    return conn

def get_top_movies_by_genre(genre, limit=5):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.title, m.vote_average
        FROM movies m
        JOIN movies_genres mg ON m.id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.genre_id
        WHERE g.genre = ?
        ORDER BY m.vote_average DESC
        LIMIT ?
    """, (genre, limit))
    top_movies = cursor.fetchall()
    conn.close()
    return top_movies

def get_top_movies_by_year(year, limit=5):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, vote_average
        FROM movies
        WHERE strftime('%Y', release_date) = ?
        ORDER BY vote_average DESC
        LIMIT ?
    """, (str(year), limit))
    top_movies = cursor.fetchall()
    conn.close()
    return top_movies

def get_random_genres(num_genres=5):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT genre FROM genres ORDER BY RANDOM() LIMIT ?", (num_genres,))
    genres = [row[0] for row in cursor.fetchall()]
    conn.close()
    return genres