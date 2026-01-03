import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "app.db"

username = "testuser"
password = "Test1234!"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

password_hash = generate_password_hash(password)

cur.execute(
    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
    (username, password_hash)
)

conn.commit()
conn.close()
print("Utilisateur testuser / Test1234! créé.")
