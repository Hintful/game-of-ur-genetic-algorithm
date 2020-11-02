from enum import Enum

class Piece(Enum):
    NoPiece = 1
    Black = 2
    White = 3

class Agent:

    def __init__(self, g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, colour):
        self.g1 = g1
        self.g2 = g2
        self.g3 = g3
        self.g4 = g4
        self.g5 = g5
        self.g6 = g6
        self.g7 = g7
        self.g8 = g8
        self.g9 = g9
        self.g10 = g10

        if colour == 'w':
            self.colour = Piece.White
        else:
            self.colour = Piece.Black
