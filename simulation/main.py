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

nAgents = [101]
# nAgents = range(21,51, 12)
# nAgents.extend(range(51,261,50))
# nAgents.extend(range(51,501,50))
# nAgents.extend(range(501,801,100))
# nAgents.extend(range(1001,2001,250))
# memory = range(2,7)
memory = [4]
nRounds = 10000
runs = 3
S = 2

i = 0
totalGames = len(memory) * len(nAgents) * runs

for x in range(runs):
	print "Starting run number {}".format(x)
	for M, N in product(memory, nAgents):

		i+=1

		g = game.Game()
		# g.addAgents('classic', N-1, M, S)
		g.addAgents('producer', 64, M, S)
		g.addAgents('speculator', 11, M, S, 0.01)
		# g.addAgents('producer', int((N/2)+1), M)
		
		# make the last agent verbose so we can debug his decisions
		# g.agents[-1].verbose = True

		print "Running game {} of {}, memory {}, agents {}, run number {}".format(i, totalGames, M, N, x)
		g.runRounds(nRounds)
		
		saveDirname = '../data/test2/'
		name = ['M', str(M), 'N', str(N), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), '.game']
		g.saveResults('_'.join(name), saveDirname)
		
		name = ['M', str(M), 'N', str(N), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), '.agents']
		g.saveAgents('_'.join(name), saveDirname)

		name = ['M', str(M), 'N', str(N), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), '.score']
		g.saveAgentsScores('_'.join(name), saveDirname)
		# g.printTest()
