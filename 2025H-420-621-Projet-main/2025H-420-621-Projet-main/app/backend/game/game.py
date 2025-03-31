class Game:
    def __init__(self):
        from .board import Board
        self.board = Board()  # Initialisation du plateau
        self.current_player = 'white'

    def start_game(self):
        # Logique pour démarrer une nouvelle partie
        pass