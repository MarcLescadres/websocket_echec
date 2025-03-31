import pygame

class Piece:
    def __init__(self, color):
        self.color = color

    def get_valid_moves(self, board, x, y):
        """To be implemented by subclasses"""
        pass

class Pawn(Piece):
    def get_valid_moves(self, board, x, y):
        """Moves one step forward (two if first move), and captures diagonally"""
        moves = []
        direction = -1 if self.color == "white" else 1  # White moves up, Black moves down
        
        # Normal move
        if 0 <= x + direction < 8 and board[x + direction][y] is None:
            moves.append((x + direction, y))
            
            # First move allows 2-step advance
            if (self.color == "white" and x == 6) or (self.color == "black" and x == 1):
                if board[x + 2 * direction][y] is None:
                    moves.append((x + 2 * direction, y))
        
        # Capture diagonally
        for dy in [-1, 1]:  
            if 0 <= y + dy < 8 and 0 <= x + direction < 8:
                if board[x + direction][y + dy] and board[x + direction][y + dy].color != self.color:
                    moves.append((x + direction, y + dy))
        
        return moves
    pass

class Rook(Piece):
    def get_valid_moves(self, board, x, y):

        moves = []
        
        # Directions: Up, Down, Left, Right
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:  # Stay within bounds
                    if board[nx][ny] is None:
                        moves.append((nx, ny))  # Empty square
                    elif board[nx][ny].color != self.color:
                        moves.append((nx, ny))  # Capture enemy piece
                        break
                    else:
                        break  # Blocked by own piece
                else:
                    break
        return moves
    pass

class Knight(Piece):
    def get_valid_moves(self, board, x, y):
        """Moves in L-shapes"""
        moves = []
        offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                   (1, 2), (1, -2), (-1, 2), (-1, -2)]
        
        for dx, dy in offsets:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None or board[nx][ny].color != self.color:
                    moves.append((nx, ny))
        return moves
    pass

class Bishop(Piece):
    def get_valid_moves(self, board, x, y):
        """Moves diagonally"""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            nx, ny = x, y
            while True:
                nx, ny = nx + dx, ny + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if board[nx][ny] is None:
                        moves.append((nx, ny))
                    elif board[nx][ny].color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves
    pass

class Queen(Piece):
    def get_valid_moves(self, board, x, y):
        """Combines Rook and Bishop movements"""
        return Rook(self.color).get_valid_moves(board, x, y) + \
               Bishop(self.color).get_valid_moves(board, x, y)

    pass

class King(Piece):
    def get_valid_moves(self, board, x, y):
        """Moves one square in any direction"""
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None or board[nx][ny].color != self.color:
                    moves.append((nx, ny))
        return moves
    pass


