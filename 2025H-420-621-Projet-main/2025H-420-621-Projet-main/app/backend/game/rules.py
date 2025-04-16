from copy import deepcopy
from game.piece import string_to_piece, King, Pawn, Rook

def is_roque_path_under_attack(board, color, from_x, from_y, to_x, to_y):
    if color == "white":
        if (from_x, from_y, to_x, to_y) == (7, 4, 7, 2):
            path = [(7, 3), (7, 2)]
        elif (from_x, from_y, to_x, to_y) == (7, 4, 7, 6):
            path = [(7, 5), (7, 6)]
        else:
            return False
    elif color == "black":
        if (from_x, from_y, to_x, to_y) == (0, 4, 0, 2):
            path = [(0, 3), (0, 2)]
        elif (from_x, from_y, to_x, to_y) == (0, 4, 0, 6):
            path = [(0, 5), (0, 6)]
        else:
            return False

    for x, y in path:
        for i in range(8):
            for j in range(8):
                piece = string_to_piece(board[i][j])
                if piece and piece.color != color:
                    if (x, y) in piece.get_valid_moves(board, i, j):
                        return True
    return False

def king_in_check(board, color):
    king_pos = None
    for x in range(8):
        for y in range(8):
            p = string_to_piece(board[x][y])
            if p and isinstance(p, King) and p.color == color:
                king_pos = (x, y)
                break
    if not king_pos:
        return True

    for x in range(8):
        for y in range(8):
            p = string_to_piece(board[x][y])
            if p and p.color != color:
                if king_pos in p.get_valid_moves(board, x, y):
                    return True
    return False

def validate_move(game, from_x, from_y, to_x, to_y):
    board = game.board.board
    piece_str = board[from_x][from_y]
    piece = string_to_piece(piece_str)
    if piece is None:
        return False, "Aucune pièce à cet endroit."

    if piece.color != game.turn:
        return False, "Ce n'est pas le tour de ce joueur."

    if isinstance(piece, Rook):
        if piece.color == "white":
            if board[7][0] != "white rook":
                game.white_can_castle_queenside = False
            if board[7][7] != "white rook":
                game.white_can_castle_kingside = False
        elif piece.color == "black":
            if board[0][0] != "black rook":
                game.black_can_castle_queenside = False
            if board[0][7] != "black rook":
                game.black_can_castle_kingside = False

    # Roques personnalisés pour le roi blanc (rangée 7) ou noir (rangée 0)
    if isinstance(piece, King):
        if not ((from_x == 7 and from_y == 4 and to_x == 7 and to_y == 2) or
                (from_x == 7 and from_y == 4 and to_x == 7 and to_y == 6) or
                (from_x == 0 and from_y == 4 and to_x == 0 and to_y == 2) or
                (from_x == 0 and from_y == 4 and to_x == 0 and to_y == 6)):
            if piece.color == "white":
                game.white_can_castle_kingside = False
                game.white_can_castle_queenside = False
            else:
                game.black_can_castle_kingside = False
                game.black_can_castle_queenside = False

        if piece.color == "white":
            if board[7][0] != "white rook":
                game.white_can_castle_queenside = False
            if board[7][7] != "white rook":
                game.white_can_castle_kingside = False
        elif piece.color == "black":
            if board[0][0] != "black rook":
                game.black_can_castle_queenside = False
            if board[0][7] != "black rook":
                game.black_can_castle_kingside = False

        if (from_x, from_y, to_x, to_y) == (7, 4, 7, 2) and not is_roque_path_under_attack(board, "white", from_x, from_y, to_x, to_y):
            if game.white_can_castle_queenside and not king_in_check(board, "white"):
                if board[7][3] == " " and board[7][2] == " ":
                    game.board.board[7][3] = game.board.board[7][0]
                    game.board.board[7][0] = " "
                    game.white_can_castle_queenside = False
                    game.white_can_castle_kingside = False
                    return True, "roque"
                else:
                    return False, "Cases bloquées pour le roque."
            else:
                return False, "Grand roque blanc non autorisé."

        elif (from_x, from_y, to_x, to_y) == (7, 4, 7, 6) and not is_roque_path_under_attack(board, "white", from_x, from_y, to_x, to_y):
            if game.white_can_castle_kingside and not king_in_check(board, "white"):
                if board[7][6] == " " and board[7][5] == " ":
                    game.board.board[7][5] = game.board.board[7][7]
                    game.board.board[7][7] = " "
                    game.white_can_castle_kingside = False
                    game.white_can_castle_queenside = False
                    return True, "roque"
                else:
                    return False, "Cases bloquées pour le roque."
            else:
                return False, "Petit roque blanc non autorisé."

        elif (from_x, from_y, to_x, to_y) == (0, 4, 0, 6) and not is_roque_path_under_attack(board, "black", from_x, from_y, to_x, to_y):
            if game.black_can_castle_kingside and not king_in_check(board, "black"):
                if board[0][6] == " " and board[0][5] == " ":
                    game.board.board[0][5] = game.board.board[0][7]
                    game.board.board[0][7] = " "
                    game.black_can_castle_kingside = False
                    game.black_can_castle_queenside = False
                    return True, "roque"
                else:
                    return False, "Cases bloquées pour le roque."
            else:
                return False, "Petit roque noir non autorisé."

        elif (from_x, from_y, to_x, to_y) == (0, 4, 0, 2) and not is_roque_path_under_attack(board, "black", from_x, from_y, to_x, to_y):
            if game.black_can_castle_queenside and not king_in_check(board, "black"):
                if board[0][3] == " " and board[0][2] == " ":
                    game.board.board[0][3] = game.board.board[0][0]
                    game.board.board[0][0] = " "
                    game.black_can_castle_kingside = False
                    game.black_can_castle_queenside = False
                    return True, "roque"
                else:
                    return False, "Cases bloquées pour le roque."
            else:
                return False, "Grand roque noir non autorisé."

    valid_moves = piece.get_valid_moves(board, from_x, from_y)

    if isinstance(piece, Pawn):
        if (to_x, to_y) not in valid_moves:
            can_en_pass, reason = can_en_passant(game, from_x, from_y, to_x, to_y)
            if can_en_pass:
                direction = 1 if piece.color == "white" else -1
                captured_x = to_x + direction
                captured_y = to_y
                game.board.board[captured_x][captured_y] = " "
                game.board.board[to_x][to_y] = piece_str
                game.board.board[from_x][from_y] = " "
                return True, reason
            return False, "Coup illégal pour un pion"

    if (to_x, to_y) not in valid_moves:
        return False, "Coup non valide pour cette pièce."

    temp_board = deepcopy(board)
    temp_board[to_x][to_y] = piece_str
    temp_board[from_x][from_y] = " "

    if king_in_check(temp_board, piece.color):
        return False, "Ce coup met votre roi en échec."

    return True, "OK"

def handle_castling(game, from_x, from_y, to_x, to_y):
    return False, "Roque invalide."

def can_en_passant(game, fx, fy, tx, ty):
    last = game.last_move
    if not last:
        return False

    piece = string_to_piece(game.board.board[fx][fy])
    if not isinstance(piece, Pawn):
        return False

    if abs(fy - ty) != 1 or tx - fx != (-1 if piece.color == "white" else 1):
        return False

    last_piece = string_to_piece(last['piece'])
    if not isinstance(last_piece, Pawn):
        return False

    if last['to'] != (fx, ty):
        return False

    if abs(last['from'][0] - last['to'][0]) == 2:
        return True, "prise en passant"

    return False

def is_checkmate(game):
    color = "black" if game.turn == "white" else "white"  # Vérifie l’adversaire du joueur courant
    board = game.board.board

    for x in range(8):
        for y in range(8):
            piece = string_to_piece(board[x][y])
            if piece and piece.color == color:
                for move in piece.get_valid_moves(board, x, y):
                    temp_board = deepcopy(board)
                    temp_board[move[0]][move[1]] = board[x][y]
                    temp_board[x][y] = " "
                    if not king_in_check(temp_board, color):
                        return False
    return True

def is_promotion(piece_str, to_x):
    piece = string_to_piece(piece_str)
    if isinstance(piece, Pawn):
        if (piece.color == "white" and to_x == 0) or (piece.color == "black" and to_x == 7):
            return True
    return False