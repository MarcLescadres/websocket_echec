class Piece:
    def __init__(self, color):
        self.color = color

# -------------------------
# UTILITY: Convertir string → objet Piece
# -------------------------
def string_to_piece(name):
    if name == " " or name is None:
        return None

    color, kind = name.split()
    kind = kind.lower()

    if kind == "pawn":
        return Pawn(color)
    elif kind == "rook":
        return Rook(color)
    elif kind == "knight":
        return Knight(color)
    elif kind == "bishop":
        return Bishop(color)
    elif kind == "queen":
        return Queen(color)
    elif kind == "king":
        return King(color)
    else:
        return None


# -------------------------
# Pièces concrètes
# -------------------------

class Pawn(Piece):
    def get_valid_moves(self, board, x, y):
        moves = []
        direction = -1 if self.color == "white" else 1

        # Avancer d'une case
        if 0 <= x + direction < 8:
            target = string_to_piece(board[x + direction][y])
            if target is None:
                moves.append((x + direction, y))

                # Premier coup : deux cases
                if (self.color == "white" and x == 6) or (self.color == "black" and x == 1):
                    target = string_to_piece(board[x + 2 * direction][y])
                    if target is None:
                        moves.append((x + 2 * direction, y))

        # Captures diagonales
        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = string_to_piece(board[nx][ny])
                if target is not None and target.color != self.color:
                    moves.append((nx, ny))

        return moves


class Rook(Piece):
    def get_valid_moves(self, board, x, y):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = string_to_piece(board[nx][ny])
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves


class Knight(Piece):
    def get_valid_moves(self, board, x, y):
        moves = []
        offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                   (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dx, dy in offsets:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = string_to_piece(board[nx][ny])
                if target is None or target.color != self.color:
                    moves.append((nx, ny))

        return moves


class Bishop(Piece):
    def get_valid_moves(self, board, x, y):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = string_to_piece(board[nx][ny])
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break

        return moves


class Queen(Piece):
    def get_valid_moves(self, board, x, y):
        return Rook(self.color).get_valid_moves(board, x, y) + \
               Bishop(self.color).get_valid_moves(board, x, y)


class King(Piece):
    def get_valid_moves(self, board, x, y):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = string_to_piece(board[nx][ny])
                if target is None or target.color != self.color:
                    moves.append((nx, ny))

        return moves
