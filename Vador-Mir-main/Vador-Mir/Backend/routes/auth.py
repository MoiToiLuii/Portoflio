# routes/auth.py
# Routes d'authentification (login / logout)

from flask import Blueprint, request, redirect, url_for, session, flash
from models.user import verify_user_credentials, create_user, get_user_by_email

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return redirect("/signup.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    password_confirm = request.form.get("password_confirm", "")

    print("DEBUG email:", repr(email))
    print("DEBUG password_len:", len(password), "confirm_len:", len(password_confirm))

    if not email or not password or not password_confirm:
        print("DEBUG -> champs vides")
        flash("Veuillez remplir tous les champs.", "error")
        return redirect("/signup.html")

    if password != password_confirm:
        print("DEBUG -> mdp différents")
        flash("Les mots de passe ne correspondent pas.", "error")
        return redirect("/signup.html")

    existing = get_user_by_email(email)
    print("DEBUG existing:", existing)
    if existing:
        print("DEBUG -> email déjà utilisé")
        flash("Un compte existe déjà avec cet e-mail.", "error")
        return redirect("/signup.html")

    user_id = create_user(email=email, password=password, role="user")
    print("DEBUG -> create_user id", user_id)

    flash("Votre compte a été créé. Vous pouvez vous connecter.", "success")
    return redirect("/login.html")



@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect("/login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        flash("Veuillez renseigner votre e-mail et votre mot de passe.", "error")
        return redirect("/login.html")

    user = verify_user_credentials(email, password)
    if not user:
        flash("Identifiants invalides.", "error")
        return redirect("/login.html")

    session["user_id"] = user["id"]
    session["user_email"] = user["email"]
    session["user_role"] = user["role"]

    return redirect("/index.html")


