import sys
from enum import IntEnum

class Piece(IntEnum):
    NoPiece = 0
    Black = 1
    White = 2

"""
STATE:
    the state is a flattened array representing the board. Each index contains
    a Piece object which represents what piece is in the space at the given index
    0, 1, 2, 3 represent the 4 safe white spaces, with 3 being the rosette square
    4, 5, 6, 7 are the 4 safe black spaces, with 7 being the rosette square
    8-15 are the central competitive squares, with 11 being the rosette
    16 and 17 are the white safe goal squares, with 17 being the rosette
    if a white piece would be moved 15 squares total, so onto 18, it is removed
    18 and 19 are the black safe goal squares, with 19 being the rosette
    if a black piece would move onto square 20 it is removed from the board
"""

class Agent:

    #random agent doesnt care about genes, just the colour its playing
    def __init__(self, colour):
        if colour == 'w':
            self.colour = Piece.White
        else:
            self.colour = Piece.Black

    def printState(self, state):
        #prints the state in a non-readable way, to give to another state
        stateAsStrings = [str(int) for int in state]
        stateString = ' '.join(stateAsStrings)
        print(stateString)
        

    def prettyPrintState(self, state):
        #pretty prints the state in a human-readable way
        line = ""
        #print the first 4 backwards, to match the game board
        for index in range(0, 4):
            if state[3 - index] == Piece.White:
                line += 'w'
            elif state[3 - index] == Piece.Black:
                line += 'b'
            elif state[3 - index] == Piece.NoPiece:
                line += 'o'
        line += "  " #spacing
        #print the white safe squares backwards
        for index in range(0, 2):
            if state[17 - index] == Piece.White:
                line += 'w'
            elif state[17 - index] == Piece.Black:
                line += 'b'
            elif state[17 - index] == Piece.NoPiece:
                line += 'o'
        print(line)

        #middle row is easy, print it in order
        line = ""
        for index in range(8, 16):
            if state[index] == Piece.White:
                line += 'w'
            elif state[index] == Piece.Black:
                line += 'b'
            elif state[index] == Piece.NoPiece:
                line += 'o'
        print(line)

        line = ""
        #now print the black safe squares like the white ones
        for index in range(0, 4):
            if state[7 - index] == Piece.White:
                line += 'w'
            elif state[7 - index] == Piece.Black:
                line += 'b'
            elif state[7 - index] == Piece.NoPiece:
                line += 'o'
        line += "  " #spacing
        #print the white safe squares backwards
        for index in range(0, 2):
            if state[19 - index] == Piece.White:
                line += 'w'
            elif state[19 - index] == Piece.Black:
                line += 'b'
            elif state[19 - index] == Piece.NoPiece:
                line += 'o'
        print(line)


    def readNextState(self):
        readState = input()
        stateToReturn = list(map(int, readState.split(' ')))
        return stateToReturn

colourToPlay = sys.argv[1]

#test for IO
agent = Agent(colourToPlay)
inState = agent.readNextState()
agent.printState(inState)
agent.prettyPrintState(inState)
