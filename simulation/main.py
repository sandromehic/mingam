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

# nAgents = [101]
# nAgents = range(21,51, 12)
# nAgents.extend(range(51,261,50))
# nAgents.extend(range(51,501,50))
# nAgents.extend(range(501,801,100))
# nAgents.extend(range(1001,2001,250))
memory = [5]
nAgents = [2**a for a in range(4,10)]
# memory = range(2,13)
nRounds = 1000
runs = 6
S = 2

i = 0
totalGames = len(memory) * len(nAgents) * runs
# totalGames2 = len(memory) * len(nAgents[:len(nAgents)-1]) * runs
# totalGames = totalGames + 2*totalGames2	

# for x in range(runs):
# 	print "Starting run number {}".format(x)
# 	for M, N in product(memory, nAgents):

# 		i+=1

# 		g = game.Game()
# 		g.addAgents('classic', N, M, S)
		
# 		# make the last agent verbose so we can debug his decisions
# 		# g.agents[-1].verbose = True

# 		print "Running game {} of {}, memory {}, agents {}, run number {}".format(i, totalGames, M, N, x)
# 		g.runRounds(nRounds)
		
# 		saveDirname = '../data/different_brainsize/'
# 		name = ['M', str(M), 'N', str(N), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), '.game']
# 		g.saveResults('_'.join(name), saveDirname)
		
# 		name = ['M', str(M), 'N', str(N), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), '.agents']
# 		g.saveAgents('_'.join(name), saveDirname)

# 		name = ['M', str(M), 'N', str(N), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), '.score']
# 		g.saveAgentsScores('_'.join(name), saveDirname)
#  		# g.printTest()

# for x in range(runs):
# 	print "Starting run number {}".format(x)
# 	for M, N in product(memory, nAgents):

# 		i+=1

# 		g = game.Game()
# 		# g.addAgents('classic', N-1, M, S)
# 		g.addAgents('producer', N, M, S)
# 		g.addAgents('speculator', N, M, S, 0.01)
# 		# g.addAgents('producer', int((N/2)+1), M)
		
# 		# make the last agent verbose so we can debug his decisions
# 		# g.agents[-1].verbose = True

# 		print "Running game {} of {}, memory {}, agents {}, run number {}".format(i, totalGames, M, N, x)
# 		g.runRounds(nRounds)
		
# 		saveDirname = '../data/same_producers_speculators/'
# 		name = ['M', str(M), 'N', str(N+N), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), 'prod', str(N), 'spec', str(N)]
# 		name.append('.game')
# 		g.saveResults('_'.join(name), saveDirname)
# 		name.remove('.game')
# 		name.append('.agents')
# 		g.saveAgents('_'.join(name), saveDirname)
# 		name.remove('.agents')
# 		name.append('.score')
# 		g.saveAgentsScores('_'.join(name), saveDirname)
# 		name.remove('.score')

for x in range(runs):
	print "Starting run number {}".format(x)
	for M, N in product(memory, nAgents[:len(nAgents)-1]):

		i+=1

		g = game.Game()
		# g.addAgents('classic', N-1, M, S)
		g.addAgents('producer', nAgents[-1], M, S)
		g.addAgents('speculator', N, M, S, 0)
		# g.addAgents('producer', int((N/2)+1), M)
		
		# make the last agent verbose so we can debug his decisions
		# g.agents[-1].verbose = True

		print "Running game {} of {}, memory {}, agents {}, run number {}".format(i, totalGames, M, N, x)
		g.runRounds(nRounds)
		
		saveDirname = '../data/less_speculators_epsilon_zero/'
		name = ['M', str(M), 'N', str(N+nAgents[-1]), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), 'prod', str(nAgents[-1]), 'spec', str(N)]
		name.append('.game')
		g.saveResults('_'.join(name), saveDirname)
		name.remove('.game')
		name.append('.agents')
		g.saveAgents('_'.join(name), saveDirname)
		name.remove('.agents')
		name.append('.score')
		g.saveAgentsScores('_'.join(name), saveDirname)
		name.remove('.score')

# for x in range(runs):
# 	print "Starting run number {}".format(x)
# 	for M, N in product(memory, nAgents[:len(nAgents)-1]):

# 		i+=1

# 		g = game.Game()
# 		# g.addAgents('classic', N-1, M, S)
# 		g.addAgents('producer', N, M, S)
# 		g.addAgents('speculator', nAgents[-1], M, S, 0.01)
# 		# g.addAgents('producer', int((N/2)+1), M)
		
# 		# make the last agent verbose so we can debug his decisions
# 		# g.agents[-1].verbose = True

# 		print "Running game {} of {}, memory {}, agents {}, run number {}".format(i, totalGames, M, N, x)
# 		g.runRounds(nRounds)
		
# 		saveDirname = '../data/more_speculators_less_producers/'
# 		name = ['M', str(M), 'N', str(N+nAgents[-1), 'S', str(S), 'rounds', str(nRounds), 'run', str(x), 'prod', str(N), 'spec', str(nAgents[-1])]
# 		name.append('.game')
# 		g.saveResults('_'.join(name), saveDirname)
# 		name.remove('.game')
# 		name.append('.agents')
# 		g.saveAgents('_'.join(name), saveDirname)
# 		name.remove('.agents')
# 		name.append('.score')
# 		g.saveAgentsScores('_'.join(name), saveDirname)
# 		name.remove('.score')