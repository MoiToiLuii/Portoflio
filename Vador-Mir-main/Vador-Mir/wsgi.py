# wsgi.py
# Point d'entrée WSGI pour Alwaysdata

import os
import sys
from pathlib import Path

# Ajoute le chemin du projet au PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "Backend"
sys.path.append(str(BACKEND_DIR))

from server import app  # importe l'objet Flask défini dans Backend/server.py

# WSGI attend une variable "application"
application = app
