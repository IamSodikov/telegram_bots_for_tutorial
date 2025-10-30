import sqlite3
import os 


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "users.db")
def get_connection():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        age INTEGER,
        phone TEXT            
)
""")
    
    conn.commit()
    conn.close

def save_user_data(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, name, surname, age, phone)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        data.get("name"),
        data.get("surname"),
        data.get("age"),
        data.get("phone")
    ))

    conn.commit()
    conn.close()


def get_user_data(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, surname, age, phone FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close

    if result:
        name, surname, age, phone = result
        return {
            "name": name,
            "surname": surname,
            "age": age,
            "phone": phone
        }
    return None