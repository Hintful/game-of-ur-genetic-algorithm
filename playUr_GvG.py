import sys
import math
from enum import IntEnum
from copy import deepcopy
# Local Imports
from agent import *
from winGame import *

def playGame(agentFile1, colourToPlay1, genes1, agentFile2, colourToPlay2, genes2)):

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

    while not win:
        
        state = blackTeam.playTurn()

        if winGame(state): #checks if black's last turn won the game
            blackWon = True
            win = True
            break
        
        state = whiteTeam.playTurn()

        if winGame(state): #checks if white's last turn won the game
            whiteWon = True
            win = True
            break

    if blackWon:
        print("Black Genetic Agent Won")
    else: #whiiteWon
        print("White Genetic Agent Won")

    return
        

def main():

    agentFile1 = sys.argv[1]
    colourToPlay1 = sys.argv[2]
    agentFile2 = sys.argv[3]
    colourToPlay2 = sys.argv[4]

    with open(agentFile1) as f:
        genes1 = f.read().splitlines()

    with open(agentFile2) as f:
        genes2 = f.read().splitlines()

    playGame(agentFile1, colourToPlay1, genes1, agentFile2, colourToPlay2, genes2)
