import os
import sys
from flask import Flask, render_template,jsonify
from game import Game,Board
from flask_socketio import SocketIO


# Définir les chemins des dossiers
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # backend/server/
TEMPLATES_DIR = os.path.join(BASE_DIR, "../../frontend/templates")
STATIC_DIR = os.path.join(BASE_DIR, "../../frontend/static")

# Créer l'application Flask
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

@app.route("/")
def home():
    """Affiche la page principale du jeu."""
    return render_template("index.html")

@app.route("/api/board")
def get_board():
    board = Board()  # Crée un objet Board
    return jsonify(board.board)  # Renvoie le plateau au format JSON

from .websockets import register_websocket_events #Faire ce import après l'initialisation de socketio

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)