import os
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

from game import Game, Board  # Ton fichier de logique du jeu
from game.piece import string_to_piece

# Définir les chemins des dossiers frontend
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "../../frontend/templates")
STATIC_DIR = os.path.join(BASE_DIR, "../../frontend/static")

# Initialiser l'application Flask
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialiser SocketIO avec support CORS
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

# Créer une instance du jeu
game = Game()

# Route principale
@app.route("/")
def home():
    return render_template("index.html")

# Route API pour l'état initial du plateau
@app.route("/initial/board")
def get_board():
    return jsonify(game.board.board)

# Événement WebSocket pour déplacer une pièce
@socketio.on('move_piece')
def handle_move(data):
    try:
        from_x = data['from_x']
        from_y = data['from_y']
        to_x = data['to_x']
        to_y = data['to_y']

        # Récupérer la chaîne représentant la pièce
        piece_str = game.board.board[from_x][from_y]

        # Convertir en objet Piece
        piece = string_to_piece(piece_str)

        if piece is None:
            socketio.emit('move_error', {'error': 'Aucune pièce à cet endroit.'})
            return

        valid_moves = piece.get_valid_moves(game.board.board, from_x, from_y)

        if (to_x, to_y) in valid_moves:
            game.board.board[to_x][to_y] = piece_str
            game.board.board[from_x][from_y] = " "

            socketio.emit('board_update', {
                'board': game.board.board,
                'from_x': from_x,
                'from_y': from_y,
                'to_x': to_x,
                'to_y': to_y})
        else:
            socketio.emit('move_error', {'error': 'Mouvement non valide.'})

    except Exception as e:
        socketio.emit('move_error', {'error': str(e)})

# Démarrer le serveur Flask-SocketIO
if __name__ == "__main__":
    print("🚀 Serveur Flask-SocketIO démarré sur http://localhost:5000")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
