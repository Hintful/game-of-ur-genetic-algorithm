import sys
from enum import IntEnum
from copy import deepcopy

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

    > Visual Representation of index on the board

    * White side *

    < 3> [ 2] [ 1] [ 0]           <17> [16]
    [ 8] [ 9] [10] <11> [12] [13] [14] [15]
    < 7> [ 6] [ 5] [ 4]           <19> [18]

    * Black side *

    4-tuple: (board, # of unplayed black pieces, # of unplayed white pieces, die roll)
"""

class Agent:

    #The file corresponding to an agent will contain the 10 genes, and the colour
    #is provided by the manager that makes 2 agents compete
    def __init__(self, genes, colour):
        self.g1 = genes[0]
        self.g2 = genes[1]
        self.g3 = genes[2]
        self.g4 = genes[3]
        self.g5 = genes[4]
        self.g6 = genes[5]
        self.g7 = genes[6]
        self.g8 = genes[7]
        self.g9 = genes[8]
        self.g10 = genes[9]

        self.numHand = 4 # number of pieces yet to be played

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

    def getNextIndex(self, curIndex, roll): # gets next index on the board after moving "roll" squares
        if(self.colour == Piece.White):
            if(curIndex == -1): # playing from hand
                return roll - 1
            elif(curIndex + roll >= 4 and curIndex + roll <= 7):
                return curIndex + roll + 4
            else:
                return min(curIndex + roll, 18)
        elif(self.colour == Piece.Black):
            if(curIndex == -1):
                return roll + 3
            elif(curIndex + roll <= 15):
                return curIndex + roll
            else: # curIndex + roll >= 16
                return min(curIndex + roll + 2, 20)

    def getSuccessors(self, state):
        successors = [] # list containing possible successor states

        # reference var
        board = state[0]
        roll = state[3]

        for i in range(len(board)): # search through the board
            if(board[i] == self.colour):
                nextIndex = self.getNextIndex(i, roll)
                if((nextIndex == 18 and self.colour == Piece.White) or (nextIndex == 20 and self.colour == Piece.Black)): # piece can exit
                    newState = deepcopy(state)
                    newBoard = newState[0]
                    newBoard[i] = 0

                    successors.append(newState)
                elif(board[nextIndex] == 0 or (board[nextIndex] == (3 - self.colour) and nextIndex != 11)): # sqaure unoccupied OR taken by enemy but not rosette
                    newState = deepcopy(state)
                    newBoard = newState[0]
                    newBoard[i] = 0
                    newBoard[nextIndex] = self.colour
                    
                    if(board[nextIndex] == (3 - self.colour)): # taking enemy piece
                        newState[3 - self.colour] += 1 # increase number of opponent's unplayed pieces

                    successors.append(newState)
                # elif(state[nextIndex] == self.colour):
                #   continue
                # else: 

        if(state[self.colour] > 0): # number of unplayed pieces > 0
            nextIndex = self.getNextIndex(-1, roll)
            if(board[nextIndex] == 0):
                newState = deepcopy(state)
                newBoard = newState[0]
                newBoard[nextIndex] = self.colour
                newState[self.colour] -= 1 # decrease number of unplayed pieces

                successors.append(newState)

        return successors




agentFile = sys.argv[1]
colourToPlay = sys.argv[2]
with open(agentFile) as f:
    genes = f.read().splitlines()

# test for IO
agent = Agent(genes, colourToPlay)
inState = agent.readNextState()
agent.printState(inState)
agent.prettyPrintState(inState)
