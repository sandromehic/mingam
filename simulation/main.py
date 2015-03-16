import logging as log
import argparse
import game
from itertools import product

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
'''

''' run simulation for classical game
	n will be in [51, 101, 201, 401, 801, 1601, 3201]
	m will be in [2,3,4,5]
'''

nAgents = [101]
# nAgents = range(21,51, 5)
# nAgents.extend(range(51,501,25))
# nAgents.extend(range(501,1001,100))
# nAgents.extend(range(1001,3001,250))
memory = range(2,13)
# memory = [5]
nRounds = 10000
runs = 32
S = 2

# reset log files
f = open('../agent', 'w')
f.close()

totalGames = len(memory) * len(nAgents) * runs

i = 0
for x in range(runs):
	for M, N in product(memory, nAgents):
		g = game.Game()
		g.addAgents('classic', N, M, S)
		# make the last agent verbose so we can debug his decisions
		# g.agents[-1].verbose = True
		i+=1
		print "Running game {} of {}, memory {}, agents {}, run number {}".format(i, totalGames, M, N, x)
		g.runRounds(nRounds)
		name = ['M', str(M), 'N', str(N), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), '.csv']
		g.saveResults('_'.join(name), '../data/n101s2_04/')
		name = ['M', str(M), 'N', str(N), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), '.game']
		g.saveAgents('_'.join(name), '../data/n101s2_04_agents/')
		# g.printTest()
