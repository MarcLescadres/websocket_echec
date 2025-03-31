class Game:
    def __init__(self):
        from .board import Board  # Assuming you have a Board class in board.py
        self.board = Board()  # Initialize the board
        self.current_player = 'white'  # White moves first

    def start_game(self):
        """Starts the game loop, allowing players to make moves."""
        print("Chess game started! Type 'exit' to quit.")
        
        while True:
            self.board.display()  # Print the board (Assuming Board has a display method)
            print(f"{self.current_player.capitalize()}'s turn")

            # Get user input
            move = input("Enter move (e.g., 'e2 e4'): ").strip().lower()
            if move == "exit":
                print("Game exited.")
                break
            
            try:
                start_pos, end_pos = move.split()
                start = self.algebraic_to_index(start_pos)
                end = self.algebraic_to_index(end_pos)

                if self.board.move_piece(start, end, self.current_player):
                    self.switch_turn()
                else:
                    print("Invalid move. Try again.")
            except Exception:
                print("Invalid input format. Use format: 'e2 e4'")

    def switch_turn(self):
        """Switches turn to the other player."""
        self.current_player = "black" if self.current_player == "white" else "white"

    @staticmethod
    def algebraic_to_index(position):
        """Converts chess notation (e.g., 'e2') to board indices (row, col)."""
        col = ord(position[0]) - ord('a')  # 'a' -> 0, 'b' -> 1, ..., 'h' -> 7
        row = 8 - int(position[1])  # '8' -> 0, '7' -> 1, ..., '1' -> 7
        return row, col
