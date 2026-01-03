
# create_test_user.py
# Script à lancer une fois pour créer un utilisateur de test dans la base.
# À exécuter depuis le dossier Backend avec :  python create_test_user.py

from models.user import create_user
from config.db import init_db


def main():
    # On s'assure que la base et les tables existent
    init_db()

    # Coordonnées du compte de test
    email = "test@test.com"
    password = "Test1234!"   # Mot de passe que tu taperas dans login.html
    role = "admin"           # On crée un admin pour pouvoir tester l'espace admin

    # create_user s'occupe de hacher le mot de passe avant de l'enregistrer
    user_id = create_user(email, password, role=role)

    print(f"Utilisateur créé : id={user_id}, email={email}, rôle={role}")


if __name__ == "__main__":
    main()
