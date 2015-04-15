import logging as log
import argparse
import utils
import game
from itertools import product
import os
import datetime
from math import ceil

''' parse input arguments
	mainly for verbose option
	and use log to output info to screen for debugging
'''
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()
if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose mode turned on!")


'''
usage to addAgents, pass a tuple as arguments

to add classical agents call Game method addAgents like this
gameInstance.addAgents('classic', numberOfAgents, brainSize, numberOfStrategies)

to add producers (agents with only one strategy and always active) call this
gameInstance.addAgents('producer', numberOfAgents, brainSize, 1)

to add speculators (agents with S strategies and a Zero Strategy that prevents
them from participating in the market if their virtual score are not high enough,
epsilon is the controll parameter, usually 0.01 or 0.1)
gameInstance.addAgents('speculator', numberOfAgents, brainSize, numberOfStrategies, epsilon)
'''

# memory = [2]
# nAgents = [101]
M = 2
N = 101
# communities go from 2 to 64 by the power of 2
neighSize = range(3,33,2)
nRounds = 10000
S = 5
i = 0
runs = 10
totalGames = runs * len(neighSize)

saveDirname = generateFolderName('../data/', 'neighSize_' + str(neighSize))

for run in range(runs):
	for nOfNeigh in neighSize:
		i+=1
		g, cgs = generateGameComunities(N, M, S, nOfNeigh)
		printAgentsAndGames(g, cgs)

		# make the last agent verbose so we can debug his decisions
		# g.agents[-1].verbose = True

		print "Starting the Game {} of total: {}".format(i, totalGames)
		runComunityRound(g, cgs, nRounds)
		
		(gameName, agentsName, scoreName) = getSaveNamesCommunity('game_'+str(i))
		g.saveResults(gameName, saveDirname)
		g.saveAgents(agentsName, saveDirname)
		# g.saveAgentsScores(scoreName, saveDirname)
		for j,cg in enumerate(cgs):
			(gameName, agentsName, scoreName) = getSaveNamesCommunity('nOfNeigh_' + str(nOfNeigh) + '_comunities_' + str( ceil(float(N)/nOfNeigh) ))
			cg.saveResults(gameName, saveDirname)
			cg.saveAgents(agentsName, saveDirname)
			# cg.saveAgentsScores(scoreName, saveDirname)
