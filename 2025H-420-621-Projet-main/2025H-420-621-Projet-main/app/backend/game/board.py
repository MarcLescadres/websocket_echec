class Board:
    def __init__(self):
        self.board = self.create_initial_board()  # Initialise le plateau d'échecs

    def create_initial_board(self):
        """ Créer un plateau de 8x8 avec les positions initiales des pièces """
        # Le plateau est une liste de listes représentant chaque ligne du plateau
        initial_board = []

        # Lignes 1 et 2 (pions noirs)
        initial_board.append(['black rook', 'black knight', 'black bishop', 'black king', 'black queen', 'black bishop', 'black knight', 'black rook'])  # Ligne des pièces noires
        initial_board.append(['black pawn', 'black pawn', 'black pawn', 'black pawn', 'black pawn', 'black pawn', 'black pawn', 'black pawn'])  # Ligne des pions noirs

        # Lignes 3 à 6 (cases vides)
        for _ in range(4):
            initial_board.append([' ']*8)  # Cases vides

        # Lignes 7 et 8 (pions blancs)
        initial_board.append(['white pawn', 'white pawn', 'white pawn', 'white pawn', 'white pawn', 'white pawn', 'white pawn', 'white pawn'])
        initial_board.append(['white rook', 'white knight', 'white bishop', 'white king', 'white queen', 'white bishop', 'white knight', 'white rook'])  # Ligne des pièces blanches

        return initial_board
