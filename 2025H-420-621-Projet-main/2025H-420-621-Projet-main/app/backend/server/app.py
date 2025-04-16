import os
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from game import Game, Board
from game.piece import string_to_piece
from game.rules import validate_move, is_checkmate, is_promotion

players = {}
player_slots = {"white": None, "black": None}
abandon_messages = set()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "../../frontend/templates")
STATIC_DIR = os.path.join(BASE_DIR, "../../frontend/static")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

game = Game()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/initial/board")
def get_board():
    return jsonify(game.board.board)

@socketio.on("connect")
def handle_connect():
    sid = request.sid
    print(f"Connexion détectée: {sid}")
    players[sid] = {"name": None, "color": "spectator"}

    if sid in abandon_messages:
        socketio.emit("opponent_abandoned", room=sid)
        abandon_messages.remove(sid)

    socketio.emit("player_list", players)

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    print(f"Déconnexion: {sid}")

    if sid == player_slots.get("white"):
        player_slots["white"] = None
    elif sid == player_slots.get("black"):
        player_slots["black"] = None

    players.pop(sid, None)
    socketio.emit("player_list", players)

@socketio.on("register_name")
def register_name(data):
    sid = request.sid
    name = data.get("name")

    if sid in players:
        players[sid]["name"] = name

        if player_slots["white"] is None:
            players[sid]["color"] = "white"
            player_slots["white"] = sid
        elif player_slots["black"] is None:
            players[sid]["color"] = "black"
            player_slots["black"] = sid
        else:
            players[sid]["color"] = "spectator"

    socketio.emit("player_list", players)

@socketio.on("move_piece")
def handle_move(data):
    global game
    try:
        from_x = data['from_x']
        from_y = data['from_y']
        to_x = data['to_x']
        to_y = data['to_y']

        valid, reason = validate_move(game, from_x, from_y, to_x, to_y)

        if not valid:
            socketio.emit('move_error', {'error': reason})
            return

        piece_str = game.board.board[from_x][from_y]
        game.board.board[to_x][to_y] = piece_str
        game.board.board[from_x][from_y] = " "

        if is_promotion(piece_str, to_x):
            color = piece_str.split()[0]
            game.board.board[to_x][to_y] = f"{color} queen"

        game.last_move = {
            'piece': piece_str,
            'from': (from_x, from_y),
            'to': (to_x, to_y)
        }
        game.turn = "black" if game.turn == "white" else "white"

        socketio.emit('board_update', {
            'board': game.board.board,
            'from_x': from_x,
            'from_y': from_y,
            'to_x': to_x,
            'to_y': to_y,
            'reason': reason
        })

        if is_checkmate(game):
            socketio.emit('game_over', {'winner': piece_str.split()[0]})
            game = Game()  # Reset du jeu après victoire

    except Exception as e:
        socketio.emit('move_error', {'error': str(e)})

@socketio.on("player_abandon")
def handle_player_abandon():
    global game
    sid = request.sid
    color = players.get(sid, {}).get("color")

    if color == "white":
        opponent_sid = player_slots.get("black")
    elif color == "black":
        opponent_sid = player_slots.get("white")
    else:
        opponent_sid = None

    if opponent_sid:
        if opponent_sid in players:
            socketio.emit("opponent_abandoned", room=opponent_sid)
        else:
            abandon_messages.add(opponent_sid)

    print(f"Player {sid} ({color}) a abandonné.")
    game = Game()  # Reset du jeu après abandon

if __name__ == "__main__":
    print("🚀 Serveur Flask-SocketIO démarré sur http://localhost:5000")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
