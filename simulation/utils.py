import game
import strategy
import math
import os
import datetime
from math import ceil

def getTotalGames():
	t = 0
	for n in N:
		t += len(generateNeighSize(n))

	return runs * t

def assignCGameAgents(agents, cgame):
	# print 'assigning agents {} to cgame {}'.format(agents, cgame)
	for ag in agents:
		ag.setCGame(cgame)

def generateGameComunities(N, M, S, nOfNeigh):
	g = game.Game()
	g.addAgents('community', N, M, S)
	cgs = []
	for c in xrange(int(ceil(float(N)/nOfNeigh))):
		cgs.append(game.CGame())

	# print len(cgs)

	for i, cg in enumerate(cgs):
		cg.agents = g.agents[i*nOfNeigh:i*nOfNeigh + nOfNeigh]
		assignCGameAgents(cg.agents, cg)

	return g, cgs

def runComunityRound(g, cgs, nRounds):
	for k in range(nRounds):
		g.runRound()
		for cg in cgs:
			cg.runRound()

def printAgentsAndGames(game, cgames):
	print "Main game: {} agents".format(len(game.agents))
	for a in game.agents:
		# print a
		pass

	for i, cg in enumerate(cgames):
		print "Cgame number {}: {} agents".format(i, len(cg.agents))
		for a in cg.agents:
			# print a
			pass

def getSaveNamesCommunity(firstname, nOfAgents, nOfNeigh, run):
	name = [firstname, 'M', str(M), 'N', str(nOfAgents), 'neighs', str(nOfNeigh), 'S', str(S), 'rounds', str(nRounds), 'run', str(run)]
	name.append('.game')
	gameName = '_'.join(name)
	name.remove('.game')
	name.append('.agents')
	agentsName = '_'.join(name)
	name.remove('.agents')
	name.append('.score')
	scoreName = '_'.join(name)
	name.remove('.score')
	return (gameName, agentsName, scoreName)

def generateFolderName(base, name):
	dirname = base + str(datetime.datetime.now()) + '_' + name
	os.mkdir(dirname)
	return dirname + '/'

def generateNeighSize(N):
	neighs = []
	for x in range(3,N,2):
		if (N/x not in [N/y for y in neighs]):
			neighs.append(x)

	return neighs

def getHalfStrategy(strat):
	# input - strategy with M brainSize to be cut in equal getHalfStrategy
	# output - strategy with M/2 brainSize

	# if we have a pair brainSize
	brainSize = int(math.log(len(strat.strat),2))
	if ((brainSize%2) == 0):
		newStrat = []
		for i in range(2**(brainSize/2)):
			newStrat.append(strat.strat[i*(2**(brainSize/2) + 1)])

		returnStrat = strategy.ClassicStrat(brainSize/2)
		returnStrat.strat = np.array(newStrat)
		return returnStrat
	else:
		return False


# GLOBAL CONFIGURATION
M = 3
N = [201]
# neighSize = [3,5]
nRounds = 10000
S = 2
i = 0
runs = 10
totalGames = getTotalGames()