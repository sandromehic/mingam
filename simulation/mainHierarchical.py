import logging as log
import argparse
from utils import *
import game
from itertools import product
import datetime
import numpy as np

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

def generateBarabasiNeighSize(n):
	k = []
	md = []
	for x in range(1,n):
		g = nx.barabasi_albert_graph(n,x)
		for i in range(x):
			for j in range(x):
				g.add_edge(i,j)

		for i in g.nodes():
			g.add_edge(i,i)

		meanD = int(round(np.average(g.degree().values())))
# 		if x<7:
# 				k.append(x)
# 				md.append(meanD)
# 				continue

		if meanD%2!=0 and meanD not in md:
				k.append(x)
				md.append(meanD)

	return k

# boltzmann folder
saveDirname = generateFolderName('data/', '')
# saveDirname = generateFolderName('../data/', '')
beta = 0.15
nOfCommunities = 10
M = [2]
N = [401]
nRounds = 10000
S = 2
i = 0
runs = 16
totalHierarchicalGames = runs * len(M) * len(N) * len(generateBarabasiNeighSize(N[0]/nOfCommunities))

for run in range(runs):
	for brainSize in M:
		for nOfAgents in N:
			k = generateBarabasiNeighSize(nOfAgents/nOfCommunities)
			print nOfAgents, k
			for nOfNeigh in k:
				i+=1
				g, cgs, meanDegree = generateHierarchicalGame(nOfAgents, brainSize, S, nOfNeigh, beta, nOfCommunities)

				print "{} - Starting the Game {} of total: {}, number of cgames: {}".format(datetime.datetime.now(), i, totalHierarchicalGames, len(cgs))
				runComunityRound(g, cgs, nRounds)

				(gameName, agentsName, scoreName) = getSaveNamesCommunity('game_'+str(i), nOfAgents, meanDegree, run, brainSize)
				g.saveResults(gameName, saveDirname)
