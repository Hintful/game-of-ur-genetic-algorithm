import sys
import math
from randomagent import *
from enum import IntEnum
from copy import deepcopy
# Local Imports
from agent import *
from winGame import *

def playGame(colourToPlay, genes):

    win = False
    blackWon = False
    whiteWon = False
    agentColour = ""
    board = []

    if colourToPlay == Piece.Black:
        blackTeam = Agent(genes, colourToPlay)
        whiteTeam = RandomAgent(Piece.White)
        agentColour = "Black"

    else:
        blackTeam = RandomAgent(Piece.Black)
        whiteTeam = Agent(genes, colourToPlay) 
        agentColour = "White"

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

    if (blackWon and agentColour == "Black") or (whiteWon and agentColour == "White"):
        print("Agent Wins")
    else:
        print("Random Agent Wins")

    return
        

def main():

    agentFile = sys.argv[1]
    colourToPlay = sys.argv[2]

    with open(agentFile) as f:
        genes = f.read().splitlines()

    playGame(colourToPlay, genes)
