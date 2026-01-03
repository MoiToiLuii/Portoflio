from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from mistralai import Mistral
import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash

#ID pour se co testuser, Test1234!


# =======================
# CONFIGURATION BDD
# =======================

# Chemin vers le fichier SQLite (créé automatiquement s'il n'existe pas)
DB_PATH = Path("app.db")

def get_db():
    print("DEBUG DB_PATH =", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Crée les tables de base si elles n'existent pas encore.
    Cette fonction sera appelée au démarrage de l'application.
    """
    conn = get_db()
    cur = conn.cursor()

    # executescript permet d'exécuter plusieurs requêtes SQL d'un coup
    cur.executescript("""
    -- Table des utilisateurs (pour plus tard, même si on ne l'utilise pas encore)
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        role TEXT DEFAULT 'etudiant'
    );

    -- Table des questions posées à l'assistant
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texte TEXT NOT NULL,
        date_pose DATETIME DEFAULT CURRENT_TIMESTAMP,
        utilisateur_id INTEGER,
        FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id)
    );

    -- Table des réponses générées par l'IA (ou autre source)
    CREATE TABLE IF NOT EXISTS reponses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texte TEXT NOT NULL,
        date_reponse DATETIME DEFAULT CURRENT_TIMESTAMP,
        question_id INTEGER NOT NULL,
        source TEXT DEFAULT 'IA',      -- 'IA', 'document', 'contact', etc.
        score_confiance REAL,
        FOREIGN KEY(question_id) REFERENCES questions(id)
    );
    """)

    conn.commit()   # on enregistre les changements sur le fichier app.db
    conn.close()    # on ferme proprement la connexion

# =======================
# APP FLASK
# =======================

app = Flask(__name__, static_url_path="/static")

# app.secret_key sert à sécuriser la session : Flask chiffre/signe 
# les données de session avec cette clé pour qu’un utilisateur ne puisse pas 
# les modifier dans son navigateur.
app.secret_key = "SuperProjet2000"


# =======================
# CONFIGURATION IA
# =======================

# 1) TA CLÉ API (temporaire en dur pour le projet)
API_KEY = "vKbe6c6PedIehpWKAkuhlkKFfD4ADHyE"

# 2) ID DE TON AGENT (celui que tu viens de créer dans la console)
AGENT_ID = "ag_019b178a7be97682af6d52698f525b14"  

# 3) Client Mistral
client = Mistral(api_key=API_KEY)

# =======================
# ROUTES PAGES HTML
# =======================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return "Identifiants invalides", 401

    session["user_id"] = user["id"]
    return index()  # ou vers ta page avec le chatbot


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username or not password:
        return "Champs obligatoires", 400

    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # vérifier si le pseudo existe déjà
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    existing = cur.fetchone()
    if existing:
        conn.close()
        return "Pseudo déjà utilisé", 400

    password_hash = generate_password_hash(password)

    cur.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    conn.commit()
    conn.close()

    return "Compte créé, vous pouvez vous connecter."

# pour ce déco
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/history")
def history():
    """
    Affiche une page avec l'historique des questions / réponses.
    """
    conn = get_db()
    cur = conn.cursor()

    # Jointure simple question ↔ réponse
    cur.execute("""
    SELECT q.id,
           q.texte AS question,
           q.date_pose,
           r.texte AS reponse,
           u.username,
           u.id AS user_id
    FROM questions q
    LEFT JOIN reponses r ON r.question_id = q.id
    LEFT JOIN users u ON u.id = q.utilisateur_id
    ORDER BY q.date_pose DESC
    """)
    rows = cur.fetchall()

    print("DEBUG history, nb lignes :", len(rows))




    return render_template("history.html", interactions=rows)


# =======================
# ROUTE CHATBOT
# =======================

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_msg = (data.get("message") or "").strip()
    if not user_msg:
        return jsonify({"reply": "Message vide"}), 400

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        # 1) Récupérer les 3 dernières interactions pour le contexte
        cur.execute("""
            SELECT q.texte AS question, r.texte AS reponse
            FROM questions q
            JOIN reponses r ON r.question_id = q.id
            ORDER BY q.date_pose DESC
            LIMIT 3
        """)
        dernieres = cur.fetchall()

        contexte = ""
        for row in reversed(dernieres):
            contexte += f"Question précédente : {row['question']}\n"
            contexte += f"Réponse donnée : {row['reponse']}\n\n"

        prompt = contexte + "Nouvelle question : " + user_msg

        # 2) Enregistrer la nouvelle question
        cur.execute(
            "INSERT INTO questions (texte, utilisateur_id) VALUES (?, ?)",
            (user_msg, session.get("user_id"))
        )


        print("DEBUG insert question:", user_msg, "user_id =", session.get("user_id"))


        question_id = cur.lastrowid

        # 3) Appeler l’agent Mistral avec le prompt enrichi
        conv = client.beta.conversations.start(
            agent_id=AGENT_ID,
            inputs=prompt
        )
        print("REPONSE MISTRAL BRUTE:", conv)

        outputs = getattr(conv, "outputs", []) or []
        ai_reply = "Je n'ai pas de réponse pour le moment."

        for out in outputs:
            if isinstance(getattr(out, "content", None), str):
                ai_reply = out.content
                break

            if isinstance(getattr(out, "content", None), list):
                texts = []
                for chunk in out.content:
                    if getattr(chunk, "type", "") == "text":
                        texts.append(chunk.text)
                if texts:
                    ai_reply = " ".join(texts)
                    break

        # 4) Enregistrer la réponse
        cur.execute(
            """
            INSERT INTO reponses (texte, question_id, source, score_confiance)
            VALUES (?, ?, ?, ?)
            """,
            (ai_reply, question_id, "IA", None)
        )

        conn.commit()
        return jsonify({"reply": ai_reply})

    except Exception as e:
        print("ERREUR IA / BDD :", e)
        conn.rollback()
        return jsonify({"reply": "Erreur du serveur IA"}), 500

    finally:
        conn.close()




# =======================
# FICHIERS STATIQUES
# =======================

@app.route("/static/<path:filename>")
def static_files(filename):
    return app.send_static_file(filename)

# =======================
# 404
# =======================

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 — Page non trouvée</h1>", 404

# =======================
# MAIN
# =======================
if __name__ == "__main__":
    # Initialise la base de données (création des tables si besoin),
    # puis lance le serveur Flask en mode debug.
    init_db()
    app.run(debug=True)


