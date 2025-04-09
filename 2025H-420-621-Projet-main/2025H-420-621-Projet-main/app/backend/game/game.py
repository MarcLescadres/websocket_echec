from .board import Board  # <- importe seulement Board ici
from .rules import validate_move, is_checkmate, is_promotion
from .piece import string_to_piece

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 'white'
        self.last_move = None
        self.white_can_castle_kingside = True
        self.white_can_castle_queenside = True
        self.black_can_castle_kingside = True
        self.black_can_castle_queenside = True

    def start_game(self):
        print("Chess game started! Type 'exit' to quit.")
        while True:
            self.board.display()
            print(f"{self.turn.capitalize()}'s turn")

            move = input("Enter move (e.g., 'e2 e4'): ").strip().lower()
            

            try:
                start_pos, end_pos = move.split()
                from_x, from_y = self.algebraic_to_index(start_pos)
                to_x, to_y = self.algebraic_to_index(end_pos)

                valid, reason = validate_move(self, from_x, from_y, to_x, to_y)
                if not valid:
                    print("Invalid move:", reason)
                    continue

                piece_str = self.board.board[from_x][from_y]
                self.board.board[to_x][to_y] = piece_str
                self.board.board[from_x][from_y] = " "

                if is_promotion(piece_str, to_x):
                    color = piece_str.split()[0]
                    self.board.board[to_x][to_y] = f"{color} queen"
                    print("Promotion to queen!")

                self.last_move = {
                    'piece': piece_str,
                    'from': (from_x, from_y),
                    'to': (to_x, to_y)
                }

                if is_checkmate(self):
                    self.board.display()
                    print(f"Checkmate! {self.turn.capitalize()} loses.")
                    break

                self.switch_turn()
            except Exception:
                print("Invalid input format. Use format: 'e2 e4'")

    def switch_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'

    @staticmethod
    def algebraic_to_index(position):
        col = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        return row, col
