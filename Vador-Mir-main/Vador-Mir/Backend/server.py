# server.py
# Point d'entrée de l'application backend (Flask)

from flask import Flask, send_from_directory, session, redirect
from pathlib import Path
from config.db import init_db
from routes.auth import auth_bp
from routes.ia import ia_bp
from routes.contact import contact_bp


# Création de l'application Flask
app = Flask(__name__)

# Clé secrète pour les sessions (à changer avant de mettre en prod)
app.secret_key = "change-me-en-cle-secrete-plus-longue"

app.register_blueprint(ia_bp)

# lien entre bp et serv
app.register_blueprint(auth_bp)


app.register_blueprint(contact_bp)

# Répertoire racine du projet (pour servir les fichiers Frontend)
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "Frontend"


# -----------------------------
# Route de test : /ping
# -----------------------------
@app.route("/ping")
def ping():
    # Permet de vérifier que le serveur tourne
    return "pong", 200


# -----------------------------
# Routes pour servir les fichiers statiques du Frontend
# (en dev local, pratique pour tester rapidement)
# -----------------------------

@app.route("/")
def root():
    # Redirige vers la page de login par défaut
    return redirect("/index.html")


@app.route("/<path:filename>")
def static_files(filename):
    """
    Sert les fichiers du Frontend.
    On empêche l'accès direct à certaines pages si l'utilisateur n'est pas connecté.
    """
    protected_pages = {"admin.html"}

    # Si la page demandée est protégée et que l'utilisateur n'est pas connecté,
    # on le renvoie vers la page de login.
    if filename in protected_pages and not is_authenticated():
        return redirect("/login.html")

    return send_from_directory(FRONTEND_DIR, filename)

# petite protection
def is_authenticated():
    """Retourne True si un utilisateur est connecté (présent en session)."""
    return "user_id" in session

# Point d'entrée si on lance "python server.py"
# pour la BDD
if __name__ == "__main__":
    init_db()          # crée les tables si besoin
   
# Pas de app.run() ici : c'est Alwaysdata (uWSGI) qui utilisera wsgi.application/ app.run(host="127.0.0.1", port=5000, debug=True)
