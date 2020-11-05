import sys
import math
from random import randint
from enum import IntEnum
from copy import deepcopy
# Local Imports
from agent import *
from winGame import *

def playGame(colourToPlay1, genes1, colourToPlay2, genes2, gamesToPlay, debug):

    win = False
    blackWon = False
    whiteWon = False
    board = []

    if colourToPlay1 == Piece.Black:
        blackTeam = Agent(genes1, colourToPlay1)
        whiteTeam = Agent(genes2, colourToPlay2)
    else:
        whiteTeam = Agent(genes1, colourToPlay1)
        blackTeam = Agent(genes2, colourToPlay2)

    for gameIndex in range(0, gamesToPlay):
        #initialize empty board
        state = [[0] * 20, 7, 7, 0]

        while not win:
            
            #roll the die and return the move
            #it's possible to have no moves, in this case
            #return the current state so as to not take a turn
            state[3] = rollDie()
            blackMove = blackTeam.playTurn(state, debug)
            state = blackMove if blackMove is not None else state

            if winGame(state): #checks if black's last turn won the game
                blackWon = True
                win = True
                break
        
            state[3] = rollDie()
            whiteMove = whiteTeam.playTurn(state, debug)
            state = whiteMove if whiteMove is not None else state

            if winGame(state): #checks if white's last turn won the game
                whiteWon = True
                win = True
                break
        
        #for sake of fairness, swap agents after each game
        temp = whiteTeam
        whiteTeam = blackTeam
        blackTeam = temp

        if blackWon:
            print("Black Genetic Agent Won Game " + str(gameIndex))
        else: #whiiteWon
            print("White Genetic Agent Won Game " + str(gameIndex))
        

def rollDie():
    #helper to generate a game of ur die roll
    dieRoll = 0
    for index in range(0, 4):
        dieRoll += randint(0, 1)

    return dieRoll

def main():

    agentFile1 = sys.argv[1]
    colourToPlay1 = sys.argv[2]
    agentFile2 = sys.argv[3]
    colourToPlay2 = sys.argv[4]
    gamesToPlay = int(sys.argv[5])

    with open(agentFile1) as f:
        genes1 = f.read().splitlines()

    with open(agentFile2) as f:
        genes2 = f.read().splitlines()

    playGame(colourToPlay1, genes1, colourToPlay2, genes2, gamesToPlay, True)

main()
