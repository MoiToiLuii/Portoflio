
# config/db.py
# Connexion à la base SQLite et création des tables de base

import sqlite3
from pathlib import Path

# Fichier de base de données SQLite (local)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database.db"


def get_connection():
    """
    Ouvre une connexion vers la base SQLite.
    À utiliser dans les models (user.py, ai_request.py).
    """
    conn = sqlite3.connect(DB_PATH)
    # Permet de récupérer les résultats sous forme de dictionnaire-like (accès par nom de colonne)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Crée les tables si elles n'existent pas encore.
    À appeler une fois au démarrage (par exemple depuis server.py).
    """
    conn = get_connection()
    cur = conn.cursor()

    # Table users : email unique, password_hash, role, created_at
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        );
        """
    )

    # Table ai_requests : historique des requêtes IA (on l'utilisera plus tard)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ai_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer_short TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )

    conn.commit()
    conn.close()
