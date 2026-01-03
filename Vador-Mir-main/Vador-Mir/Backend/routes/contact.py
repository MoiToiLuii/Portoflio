# routes/contact.py
# Traitement du formulaire "Nous contacter"

from flask import Blueprint, request, redirect, jsonify, session
from config.db import get_connection
from datetime import datetime

contact_bp = Blueprint("contact", __name__)


def _insert_contact_message(name: str, email: str, subject: str, message: str):
    """Insère le message de contact dans une table dédiée."""
    conn = get_connection()
    cur = conn.cursor()

    # Crée la table si elle n'existe pas encore
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )

    cur.execute(
        """
        INSERT INTO contact_messages (name, email, subject, message, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, subject, message, datetime.utcnow().isoformat()),
    )

    conn.commit()
    conn.close()


@contact_bp.route("/contact", methods=["POST"])
def handle_contact():
    """
    Traite le formulaire de contact.
    - Vérifie les longueurs côté serveur (sécurité).
    - Stocke le message dans la base.
    - Redirige vers contact.html avec un indicateur de succès.
    """
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    subject = (request.form.get("subject") or "").strip()
    message = (request.form.get("message") or "").strip()

    # Vérifications simples côté serveur (toujours, même si le front en fait déjà)
    if not name or not email or not subject or not message:
        return redirect("/contact.html?error=missing")

    if len(name) > 50 or len(email) > 100 or len(subject) > 100 or len(message) > 1000:
        return redirect("/contact.html?error=too_long")

    _insert_contact_message(name, email, subject, message)

    # On pourrait afficher un vrai message de succès côté front en lisant ?success=1
    return redirect("/contact.html?success=1")


