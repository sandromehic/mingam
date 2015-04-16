import logging as log
import argparse
from utils import *
import game
from itertools import product

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

saveDirname = generateFolderName('../data/', '')
for run in range(runs):
	for nOfAgents in N:
		neighSize = generateNeighSize(nOfAgents)
		print nOfAgents, neighSize
		for nOfNeigh in neighSize:
			i+=1
			g, cgs = generateGameComunities(nOfAgents, M, S, nOfNeigh)

			print "Starting the Game {} of total: {}".format(i, totalGames)
			runComunityRound(g, cgs, nRounds)
			
			(gameName, agentsName, scoreName) = getSaveNamesCommunity('game_'+str(i), nOfAgents, nOfNeigh, run)
			g.saveResults(gameName, saveDirname)
