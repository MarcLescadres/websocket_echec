import random
from game.rules import validate_move
from .piece import string_to_piece

def get_random_move(game, color):
    valid_moves = []
    
    # Chercher toutes les pièces de la couleur de l'IA
    for x in range(8):
        for y in range(8):
            piece_str = game.board.board[x][y]
            piece = string_to_piece(piece_str)
            
            if piece and piece.color == color:
                # Ajouter tous les coups valides de cette pièce
                valid_moves.extend([(x, y, to_x, to_y) for (to_x, to_y) in piece.get_valid_moves(game.board.board, x, y)])
    
    # Choisir un coup au hasard parmi les coups valides
    if valid_moves:
        return random.choice(valid_moves)
    return None