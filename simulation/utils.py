import game
import strategy
import math
import os
import datetime
from math import ceil
import vonNeumann

def getTotalGames():
	t = 0
	for n in N:
		t += len(generateNeighSize(n)) + 1

	return runs * t * len(M)

def assignCGameAgents(agents, cgame):
	# print 'assigning agents {} to cgame {}'.format(agents, cgame)
	for ag in agents:
		ag.setCGame(cgame)

def generateFixedGameComunities(N, M, S, nOfNeigh):
	g = game.Game()
	g.addAgents('community', N, M, S)
	cgs = generateFixedCGames(N, nOfNeigh)

	# print len(cgs)

	for i, cg in enumerate(cgs):
		cg.agents = g.agents[i*nOfNeigh:i*nOfNeigh + nOfNeigh]
		assignCGameAgents(cg.agents, cg)

	return g, cgs

def generateFixedCGames(N, nOfNeigh):
	cgs = []
	for c in xrange(int(ceil(float(N)/nOfNeigh))):
		cgs.append(game.CGame())

	return cgs

def generateCenteredGameComunities(N, M, S, nOfNeigh):
	g = game.Game()
	g.addAgents('community', N, M, S)
	cgs = generateCenteredComunities(g.agents, nOfNeigh)

	return g, cgs

def generateCenteredComunities(agents, nOfNeigh):
	cgs = []
	roundAgents = agents[:] + agents[:nOfNeigh]
	for (i,ag) in enumerate(agents):
		cgs.append(game.CGame())
		cgs[i].agents = roundAgents[i:i+nOfNeigh]
		assignCGameAgents(cgs[i].agents, cgs[i])

	return cgs

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

def getSaveNamesCommunity(firstname, nOfAgents, nOfNeigh, run, brainSize):
	name = [firstname, 'M', str(brainSize), 'N', str(nOfAgents), 'neighs', str(nOfNeigh), 'S', str(S), 'rounds', str(nRounds), 'run', str(run)]
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

def generateVonNeumannGameComunities(nOfAgents, brainSize, S, vonNeumannRadius):
	g = game.Game()
	g.addAgents('community', nOfAgents, brainSize, S)

	neigh = vonNeumann.generateVonNeumann(g.agents,vonNeumannRadius)
	cgs = generateVonNeumannCGames(neigh)

	return g, cgs

def generateVonNeumannCGames(neigh):
	cgs = []
	for i, ag in enumerate(neigh):
		cgs.append(game.CGame())
		cgs[i].agents = neigh[ag]
		assignCGameAgents(cgs[i].agents, cgs[i])

	return cgs

# GLOBAL CONFIGURATION
M = range(2,7)
N = [403]
nRounds = 1000
S = 2
i = 0
runs = 10
totalGames = getTotalGames()
dVonNeumann = range(1,7)
totalGamesVonNeumann = runs * len(M) * (len(N)+1) * len(dVonNeumann)