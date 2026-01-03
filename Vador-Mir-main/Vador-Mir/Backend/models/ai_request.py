# models/ai_request.py
# Accès à la table ai_requests

from datetime import datetime
from config.db import get_connection


def create_ai_request(user_id: int, question: str, answer_short: str = "") -> int:
    """
    Enregistre une requête IA dans la base.
    - user_id : id de l'utilisateur ayant posé la question.
    - question : texte complet de la question.
    - answer_short : réponse courte stockée (facultatif).
    Retourne l'id de la ligne créée.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO ai_requests (user_id, question, answer_short, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, question, answer_short, datetime.utcnow().isoformat()),
    )

    req_id = cur.lastrowid
    conn.commit()
    conn.close()
    return req_id


def list_ai_requests(limit: int = 50):
    """
    Retourne les dernières requêtes IA (pour l'admin).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT ar.id, ar.question, ar.answer_short, ar.created_at,
               u.email AS user_email
        FROM ai_requests ar
        JOIN users u ON u.id = ar.user_id
        ORDER BY ar.created_at DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cur.fetchall()
    conn.close()
    return rows

