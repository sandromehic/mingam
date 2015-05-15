import logging as log
import argparse
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

memory = [5]
nAgents = [100]
nRounds = 1000
epsilon = 0.05
runs = 1
S = 2

i = 0
totalGames = len(memory) * len(nAgents) * runs

for x in range(runs):
	print "Starting run number {}".format(x)
	for M, N in product(memory, nAgents):

		i+=1

		g = game.Game()
		g.addAgents('classic', N-1, M, S)
		g.addAgents('intelligent', 1, M, epsilon)

		print "Running game {} of {}, memory {}, agents {}, run number {}".format(i, totalGames, M, N, x)
		g.runRounds(nRounds)

g.agents[-1].strategy.printInitialAndFinal()
