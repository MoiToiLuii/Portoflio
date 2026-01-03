# models/user.py
# Fonctions d'accès à la table "users"

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from config.db import get_connection


def create_user(email: str, password: str, role: str = "user") -> int:
    """
    Crée un utilisateur dans la base.
    - email : sert d'identifiant unique.
    - password : mot de passe en clair reçu, que l'on VA hacher.
    - role : 'user' par défaut, 'admin' pour un compte admin.

    Retourne l'id de l'utilisateur créé.
    """
    # Génère un hash sécurisé à partir du mot de passe en clair
    password_hash = generate_password_hash(password)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users (email, password_hash, role, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (email, password_hash, role, datetime.utcnow().isoformat()),
    )

    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_user_by_email(email: str):
    """
    Récupère un utilisateur par son email.
    Retourne un objet de type Row (ou None si non trouvé).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, email, password_hash, role, created_at
        FROM users
        WHERE email = ?
        """,
        (email,),
    )

    row = cur.fetchone()
    conn.close()
    return row
def list_users(limit: int = 50):
    """
    Retourne la liste des utilisateurs (pour l'admin).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, email, role, created_at
        FROM users
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cur.fetchall()
    conn.close()
    return rows


def verify_user_credentials(email: str, password: str):
    """
    Vérifie si l'email et le mot de passe correspondent à un utilisateur existant.
    - Si OK, retourne le Row de l'utilisateur.
    - Sinon, retourne None.
    """
    user = get_user_by_email(email)
    if not user:
        return None

    # user["password_hash"] contient le hash stocké dans la BDD
    if not check_password_hash(user["password_hash"], password):
        return None

    return user

