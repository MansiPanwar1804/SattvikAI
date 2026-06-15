import sqlite3
from pathlib import Path

DB_PATH = Path("data/sattvikai.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_users_table():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            name TEXT,
            age INTEGER,
            gender TEXT,
            weight_kg REAL,
            height_cm REAL,
            activity_level TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, name, age, gender, weight_kg, height_cm, activity_level):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute('SELECT username FROM users WHERE username = ?', (username,))
        if c.fetchone():
            return False, "Username already exists."
        c.execute('''
            INSERT INTO users (username, password, name, age, gender, weight_kg, height_cm, activity_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, password, name, age, gender, weight_kg, height_cm, activity_level))
        conn.commit()
        return True, "User registered successfully."
    except Exception as e:
        print(f"Database error: {e}")
        return False, "An error occurred during registration."
    finally:
        conn.close()

def validate_user(username, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT username FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None
