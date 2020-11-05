import sys
import math
from enum import IntEnum
from copy import deepcopy

# constant definition
NUM_TOTAL_PIECES = 7
NUM_GENES = 10
BOARD_SIZE = 20

# debug flag
DEBUG = False

def debug(s):
    print(s) if DEBUG == True else ''

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
        # self.g1 = genes[0]
        # self.g2 = genes[1]
        # self.g3 = genes[2]
        # self.g4 = genes[3]
        # self.g5 = genes[4]
        # self.g6 = genes[5]
        # self.g7 = genes[6]
        # self.g8 = genes[7]
        # self.g9 = genes[8]
        # self.g10 = genes[9]
        self.g = [0] * NUM_GENES # init list containing genes

        for i in range(NUM_GENES):
            self.g[i] = float(genes[i])

        self.numHand = NUM_TOTAL_PIECES # number of pieces yet to be played

        if colour == 'w':
            self.colour = Piece.White
        else:
            self.colour = Piece.Black

    #pass this the full list of states
    def printState(self, stateList):
        #prints the state in a non-readable way, to give to another state
        stateAsStrings = [str(int) for int in stateList[0]]
        stateString = ' '.join(stateAsStrings)
        for index in range(1, 4):
            stateString += " " + str(stateList[index])
        print(stateString)
        

    def prettyPrintState(self, stateList):
        if not stateList: # empty state
            return
        #pretty prints the state in a human-readable way
        line = ""
        state = stateList[0]

        #print the white pieces above their home
        print(str(stateList[2]))

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

        #print the black pieces below theirs
        print(str(stateList[1]))


    def readNextState(self):
        readState = input()
        ints = list(map(int, readState.split(' ')))
        state = ints[:20] #the first 20, indexes 0 to 19
        blackPieces = ints[20]
        whitePieces = ints[21]
        dieRoll = ints[22]
        return [state, blackPieces, whitePieces, dieRoll]

    def getNumPiecesOnBoard(self, state, player): # get number of specified player's pieces on the board
        num = 0 # init

        for i in state[0]: # iterate through the board
            if(i == player):
                num += 1

        return num


    def getNextIndex(self, curIndex, roll, player): # gets next index for the given player on the board after moving "roll" squares
        if(player == Piece.White):
            if(curIndex == -1): # playing from hand
                # print("1", roll - 1)
                return max(0, roll - 1) # takes care of cases where roll = 0
            elif(curIndex + roll >= 4 and curIndex + roll <= 7):
                # print("2", curIndex + roll + 4)
                return curIndex + roll + 4
            else:
                # print("3", min(curIndex + roll, 18))
                return min(curIndex + roll, 18)
        elif(player == Piece.Black):
            if(curIndex == -1):
                return roll + 3
            elif(curIndex + roll <= 15):
                return curIndex + roll
            else: # curIndex + roll >= 16
                return min(curIndex + roll + 2, 20)

    def enemyCapturable(self, board, roll, minIndex, maxIndex): # True if enemy capturing move exists within given board index from given board and die roll, False otherwise
        for i in range(minIndex, maxIndex + 1 - roll): # from minIndex to (maxIndex - roll), inclusive
            if(board[i] == self.colour):
                nextIndex = self.getNextIndex(i, roll, self.colour)
                if((nextIndex == 18 and self.colour == Piece.White) or (nextIndex == 20 and self.colour == Piece.Black)): # exiting cases shouldn't be considered
                    continue
                elif((board[nextIndex] == (3 - self.colour)) and nextIndex != 11):
                    return True
        return False

    def allyCapturable(self, board, roll, minIndex, maxIndex): # True if an enemy move that captures ally piece exists within given board index from given board and die roll, False otherwise
        for i in range(minIndex, maxIndex + 1 - roll):
            if(board[i] == (3 - self.colour)):
                nextIndex = self.getNextIndex(i, roll, 3 - self.colour)
                if((nextIndex == 18 and (3 - self.colour) == Piece.White) or (nextIndex == 20 and (3 - self.colour) == Piece.Black)): # exiting cases shouldn't be considered
                    continue
                if((board[nextIndex] == self.colour) and nextIndex != 11):
                    return True
        return False

    def extraTurn(self, board, oldBoard):
        return ((oldBoard[3] == 0 and board[3] == self.colour) or (oldBoard[7] == 0 and board[7] == self.colour) or (oldBoard[11] == 0 and board[11] == self.colour) \
                or (oldBoard[17] == 0 and board[17] == self.colour) or (oldBoard[19] == 0 and board[19] == self.colour))

    def getSuccessors(self, state):
        successors = [] # list containing possible successor states

        # reference var
        board = state[0]
        roll = state[3]

        for i in range(len(board)): # search through the board
            if(board[i] == self.colour):
                nextIndex = self.getNextIndex(i, roll, self.colour)
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
            nextIndex = self.getNextIndex(-1, roll, self.colour)
            if(board[nextIndex] == 0):
                newState = deepcopy(state)
                newBoard = newState[0]
                newBoard[nextIndex] = self.colour
                newState[self.colour] -= 1 # decrease number of unplayed pieces

                successors.append(newState)

        return successors

    # > State Evaluation Variables

    # v[0]  Number of Pieces Not on the board
    # v[1]  Number of Pieces on the board
    # v[2]  Number of Pieces Scored (Removed from Board)
    # v[3]  1 if there is a friendly piece on the central rosette, 0 otherwise
    # v[4]  Probability of jumping an Enemy Piece BEFORE the central rosette (index 11)
    # v[5]  Probability of jumping an Enemy Piece AFTER the central rosette (index 11)
    # v[6]  Probability of losing a friendly piece BEFORE the central rosette
    # v[7]  Probability of losing a friendly piece AFTER the central rosette
    # v[8]  1 if the state of the board earns a bonus turn (a piece landed on a rosette), 0 otherwise
    # v[9] Number of opponent pieces on the board


    # > Roll Chances

    # 0   1 in 16
    # 1   4 in 16
    # 2   6 in 16
    # 3   4 in 16
    # 4   1 in 16


    def getBestSuccessor(self, states, old_state): # evaluates the best state from the given list of states
        max_S = (-math.inf) # init
        bestState = None

        oldBoard = old_state[0]

        for state in states:
            board = state[0]
            v = [0] * NUM_GENES # init

            v[0] = -(state[self.colour])
            v[1] = self.getNumPiecesOnBoard(state, self.colour)
            v[2] = NUM_TOTAL_PIECES - (-v[0] + v[1])
            v[3] = 1 if board[11] == self.colour else 0
            v[4] = float(4/16) * self.enemyCapturable(board, 1, 0, 10) + float(6/16) * self.enemyCapturable(board, 2, 0, 10) + float(4/16) * self.enemyCapturable(board, 3, 0, 10) \
                + float(1/16) * self.enemyCapturable(board, 4, 0, 10)
            v[5] = float(4/16) * self.enemyCapturable(board, 1, 12, 19) + float(6/16) * self.enemyCapturable(board, 2, 12, 19) + float(4/16) * self.enemyCapturable(board, 3, 12, 19) \
                + float(1/16) * self.enemyCapturable(board, 4, 12, 19)
            v[6] = -(float(4/16) * self.allyCapturable(board, 1, 0, 10) + float(6/16) * self.allyCapturable(board, 2, 0, 10) + float(4/16) * self.allyCapturable(board, 3, 0, 10) \
                + float(1/16) * self.allyCapturable(board, 4, 0, 10))
            v[7] = -(float(4/16) * self.allyCapturable(board, 1, 12, 19) + float(6/16) * self.allyCapturable(board, 2, 12, 19) + float(4/16) * self.allyCapturable(board, 3, 12, 19) \
                + float(1/16) * self.allyCapturable(board, 4, 12, 19))
            v[8] = 1 if self.extraTurn(board, oldBoard) else 0
            v[9] = self.getNumPiecesOnBoard(state, 3 - self.colour)

            S = 0 # init

            debug(state)

            for i in range(NUM_GENES):
                debug("v" + str(i) + ": " + str(v[i]))
                S += v[i] * self.g[i] # evaluate state value S

            debug(S)

            if(S > max_S):
                max_S = S
                bestState = state

        return bestState, self.extraTurn(bestState[0], oldBoard) # extraTurn == True if extra turn is granted after this turn, and False otherwise


    def playTurn(self, currentState, debug):
        # play turn reads the next state of the board, 
        # analyzes and computes the successor moves, 
        # and then determines the best successor
        # if debug is set to true, it will pretty print its moves for tracing
        
        successors = self.getSuccessors(currentState)
        bestSuccessor, extraTurn = self.getBestSuccessor(successors, currentState)
       
        if (debug):
            self.prettyPrintState(bestSuccessor if bestSuccessor else currentState)

        return bestSuccessor, extraTurn




# agentFile = sys.argv[1]
# colourToPlay = sys.argv[2]
# agentFile
# with open(agentFile) as f:
#     genes = f.read().splitlines()

# # test for IO
# agent = Agent(genes, colourToPlay)
# inState = agent.readNextState()
# agent.printState(inState)
# agent.prettyPrintState(inState)

# agent.getBestSuccessor(agent.getSuccessors(inState), inState) # test
