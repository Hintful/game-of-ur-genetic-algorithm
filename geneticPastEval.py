import math
import numpy as np
from playUr_GvG import playGame

# global constant
AGENT_DIR = "agentFiles/" # directory for agent files
NUM_GAMES_PER_PAIR = 50 # number of games played between each pair of agents
DEBUG = False
ROUND_DIGIT = 3
WINRATE_THRESHOLD = float(1)

def printWinRate(agentWinRate): # prints out agent winrate
    for i in range(len(agentWinRate)):
        print("Agent " + str(i) + " winrate", end=': ')
        print(str(round(agentWinRate[i] * 100, ROUND_DIGIT)) + "%")

# main ---------------------------
# agentList is a list of genes for each agent
def playGenerationGames(agentList):

    agentWinCount = np.zeros(len(agentList)) # init wincount array
    agentPlayCount = np.zeros(len(agentList)) # init playcount array
    agentWinRate = np.zeros(len(agentList)) # init winrate array

    for indexA in range(len(agentList) - 1): # iterate
        for indexB in range(indexA + 1, len(agentList)):
            genesA = agentList[indexA]
            genesB = agentList[indexB]
            
            for x in range(NUM_GAMES_PER_PAIR): # play x games
                # set player colour
                if x % 2 == 0:
                    colourA, colourB = 'w', 'b'
                else:
                    colourA, colourB = 'b', 'w'

                blackWon = playGame(colourA, genesA, colourB, genesB, 1, DEBUG)
                agentPlayCount[indexA] += 1
                agentPlayCount[indexB] += 1

                if(colourA == 'b'): 
                    agentWinCount[indexA] += blackWon
                    agentWinCount[indexB] += (1 - blackWon)
                else:
                    agentWinCount[indexB] += blackWon
                    agentWinCount[indexA] += (1 - blackWon)

    for i in range(len(agentList)):
        agentWinRate[i] = agentWinCount[i] / agentPlayCount[i]

    return list(agentWinRate)

def normalizeList(listOfNums):
    total = 0
    for value in listOfNums:
        total += value

    normalizedList = list(map(lambda x: round(float(x / total), 5), listOfNums))

    #to be properly normalized we must make sure they sum to 1
    normalizedList[len(normalizedList) - 1] = 1 - sum(normalizedList[:-1])
    return normalizedList


def mutateAgent(genes, rnGenerator):
    #each gene has a 10% chance to mutate by +-25%
    for index in range(len(genes) - 1):
        mutate = rnGenerator.integers(0, 10)
        if mutate == 0 or mutate == 1:
            #1 in 10 chance
            mutationAmount = rnGenerator.choice([1.5, 0.5])
            genes[index] = genes[index] * mutationAmount

def evolveAgents():
    #load the last run's best agent to evaluate against
    priorFinalAgent = []
    with open('FinalAgent', 'r') as f:
        priorFinalAgent = [float(i) for i in f.read().splitlines()]
        f.close()

    #a list of lists of floats, each list corresponding to an agent
    listOfGenes = []
    with open("agentList") as f:
        agentList = f.read().splitlines() # read agent filenames from "/agentList"
        for agentFile in agentList:
            with open(AGENT_DIR + agentFile) as f2:
                #read in the genes as a list and convert each entry to a float
                listOfGenes.append([float(i) for i in f2.read().splitlines()])
    
    generationIndex = 0
    lastBaselineWinRate = 0

    bestWinRate = 0
    bestAgent = []
    # a numpy RNG used for parent selection
    generator = np.random.default_rng()
    while True:
        #each generation we do as follows:
        #increment the index for debugging
        #play the generation games to get all the winrates
        #compute the winrate delta of the best agent
        #if the delta is too small, stop and return the best agent
        #else, normalize the winrates of each agent and use it to pick parents
        #make 7 new kids and take the 4 highest rated agents from last generation
        #repeat
        generationIndex += 1
        print("Beginning generation " + str(generationIndex) + " with baseline winrate " + str(lastBaselineWinRate))

        genWinRates = playGenerationGames(listOfGenes)

        #get the win rate and index of the best agent
        #this is the true winrate in the generation, not agaisnt baseline
        #we use this to track what will become our new final agent
        genWinRate = max(genWinRates)
        bestIndex = genWinRates.index(genWinRate)
        genWinRate = round(genWinRate * 100, 3) #make it nicely formatted now
        genBestAgent = listOfGenes[bestIndex]

        #if its better than the last best agent, save it
        if genWinRate > bestWinRate:
            bestWinRate = genWinRate
            bestAgent = genBestAgent

        genBestAgentWonGames = 0
        #test the best agent in 100 games against last trial's best
        for x in range(100): # play x games
            # set player colour
            if x % 2 == 0:
                colourA, colourB = 'w', 'b'
            else:
                colourA, colourB = 'b', 'w'

            blackWon = playGame(colourA, bestAgent, colourB, priorFinalAgent, 1, DEBUG)

            if ((colourA == 'b' and blackWon)
                    or (colourA == 'w' and not blackWon)):
                genBestAgentWonGames += 1
        

        #if the baseline winrate improved, but not by enough, end the process
        #since we do 100 games, we can directly use the won game count as the winrate
        if ((genBestAgentWonGames > lastBaselineWinRate) and 
                (genBestAgentWonGames - lastBaselineWinRate <= WINRATE_THRESHOLD)):
            #stop now
            f = open("FinalAgent", 'w')
            for gene in bestAgent:
                f.write(str(gene) + '\n')
            f.close()
            print("Final agent discovered, winrate of " + str(genBestAgentWonGames) 
                    + "% was below improvement threshold")
            return
        
        #else, new generation
        lastBaselineWinRate = genBestAgentWonGames
        normalizedList = normalizeList(genWinRates)
        nextGeneration = []
    
        for newChild in range(0, 8):
            child = [0] * 10
            #this chooses 2 parents without replacement, using the final list as probabilities
            parents = generator.choice(listOfGenes, 2, False, normalizedList)
            for gene in range(len(child) - 1):
                #each gene is the average of its parents
                child[gene] = round(parents[0][gene] + parents[1][gene] / 2, 3)
            
            #mutate each child, potentially
            mutateAgent(child, generator)
            nextGeneration.append(child)

        #now we apply our elitism, taking the 4 best members of this generation
        #this sorts the list and produces the 4 highest (original) indices
        eliteIndices = sorted( [(i) for (i,x) in enumerate(genWinRates)], reverse=True )[:3]
        for index in range(3):
            nextGeneration.append(listOfGenes[eliteIndices[index]])

        #the next generation is now complete
        listOfGenes = nextGeneration


evolveAgents()
