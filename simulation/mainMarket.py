import logging as log
import argparse
import game
from itertools import product
from utils import *
import datetime

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

memory = [5]
nOfSpeculators = 300
nOfProducers = 10
epsilon = 0.01
nRounds = 100000
runs = 3
S = 2

saveDirname =  generateFolderName('../data/', '')

i = 0
totalGames = len(memory) * runs

for x in range(runs):
	print "{} - Starting run number {}".format(datetime.datetime.now(), x)
	for M in memory:
		i+=1

		g = game.Game()
		g.addAgents('producer', nOfProducers, M, S)
		g.addAgents('speculator', nOfSpeculators, M, S, epsilon)

		print "Running game {} of {}, memory {}, run number {}".format(i, totalGames, M, x)
		g.runRounds(nRounds)

		(gameName, agentsName, scoreName) = getSaveNamesCommunity('game_'+str(i), nOfProducers, nOfSpeculators, x, brainSize)
		g.saveResults(gameName, saveDirname)
