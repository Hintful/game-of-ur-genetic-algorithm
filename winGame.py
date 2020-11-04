import math
from agent import Piece


def winGame(state):
    # needs to determine if the board is a win-state or not
    # search through board array, set boolean values
    board = state[0]
    win = False
    blackEmpty = False #No more captured pieces
    whiteEmpty = False #No more captured pieces

    unplayedBlackPices = state[1]
    unplayedWhitePices = state[2]


    if unplayedBlackPices == 0:
        blackEmpty = True
    if unplayedWhitePices == 0:
        whiteEmpty = True


    boardEmptyOfBlackTiles = True
    boardEmptyOfWhiteTiles = True

    # Finds any pieces on board
    for i in board:
        if i == Piece.Black:
            boardEmptyOfBlackTiles = False
        elif i == Piece.White:
            boardEmptyOfWhiteTiles = False

    if blackEmpty and boardEmptyOfBlackTiles:
        win = True
        print("Black Won")
    elif whiteEmpty and boardEmptyOfWhiteTiles:
        print("White Won")
        win = True
    else: #no win
        print("No Winner Yet")
        win = False

    return win
