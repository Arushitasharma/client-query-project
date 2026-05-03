import sqlite3
import os
from flask import current_app
from werkzeug.security import generate_password_hash

def get_db():
    db_path = os.path.join(current_app.instance_path, "queries.db")
    return sqlite3.connect(db_path)

def init_db(app):
    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, "queries.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # queries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            query TEXT,
            status TEXT
        )
    """)

    # users table (for login)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # default admin (username: admin, password: admin123)
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", generate_password_hash("admin123"))
        )

    conn.commit()
    conn.close()