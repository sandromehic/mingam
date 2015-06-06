import game
import strategy
import math
import os
import datetime
from math import ceil
import vonNeumann
import networkx as nx
import numpy.random as nprnd
import numpy as np

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

def generateHierarchicalGame(N, M, S, nOfNeigh, beta, nOfCommunities):
	g = game.Game()
	g.addAgents('community', N, M, S)
	cgs, meanDegree = generateHierarchicalComunities(g.agents, nOfNeigh, beta, nOfCommunities)

	return g, cgs, meanDegree

def generateHierarchicalComunities(agents, nOfNeigh, beta, nOfCommunities):
	hg = hierarchicalGraph(len(agents), nOfNeigh, beta, nOfCommunities)
	meanDegree = int(round(np.average(hg.degree().values())))
	cgs = getcgamesFromGraph(agents, hg)
	return cgs, meanDegree

def hierarchicalGraph(n, k, beta, nOfCommunities):
	div = getDivArray(n,nOfCommunities)
	print div, k
	graphs = []
	for x in div:
		newG = nx.barabasi_albert_graph(x, k)
		# add edges between initial k nodes, and on the diagonal
		newG = normalizeBarabasi(newG, k)
		graphs.append(newG)

	f = nx.Graph()
	for g in graphs:
		idx = len(f.nodes())
		newNodes = [x+idx for x in g.nodes()]
		newEdges = [(x+idx,y+idx) for (x,y) in g.edges()]
		f.add_nodes_from(newNodes)
		f.add_edges_from(newEdges)

	support_f = f.copy()
	for e in support_f.edges():
		if beta > nprnd.uniform():
			f = changeEdge(f,e)

	return f

def normalizeBarabasi(g, k):
	for i in range(k):
		for j in range(k):
			g.add_edge(i,j)
	for i in g.nodes():
		g.add_edge(i,i)

	return g

def getDivArray(n,k):
	div = n/k
	asd = [div] * k
	if n%k != 0:
		asd[-1] = asd[-1] + (n%k)

	return asd

def changeEdge(g, e):
    x, y = e
    k = nprnd.randint(len(g.nodes()))
    while(k==x or (x,k) in g.edges()):
        k = nprnd.randint(len(g.nodes()))

    g.remove_edge(x,y)
    g.add_edge(x,k)
    return g

def generateBarabasiAlbertGame(N, M, S, nOfNeigh):
	g = game.Game()
	g.addAgents('community', N, M, S)
	cgs = generateBarabasiComunities(g.agents, nOfNeigh)

	return g, cgs

def generateBarabasiComunities(agents, nOfNeigh):
	# here we create a barabasi albert graph with N nodes
	# and nOfNeigh-1 connections per new graph. nOfNeigh
	# passed to the function will be an odd number, so we pass
	# nOfNeigh-1 as barabasi albert graph does not account
	# for the node being added as a part of community
	ba = nx.barabasi_albert_graph(len(agents), nOfNeigh-1)
	cgs = getcgamesFromGraph(agents, ba)
	return cgs

def generateWattsStrogatzGame(N, M, S, nOfNeigh, beta):
	g = game.Game()
	g.addAgents('community', N, M, S)
	cgs = generateWattsStrogatzComunities(g.agents, nOfNeigh-1, beta)

	return g, cgs

def generateWattsStrogatzComunities(agents, nOfNeigh, beta):
	# here we create Watts Strogatz graph with N nodes
	# and each node should have nOfNeigh nearest neighbours
	# that are mixed with p probability
	ws = nx.watts_strogatz_graph(len(agents), nOfNeigh, beta)
	ws = normalizeGraphEdges(ws)
	cgs = getcgamesFromGraph(agents, ws)
	return cgs

# used to make the neighborhood a pair number (odd including the node)
def normalizeGraphEdges(gr):
	upperlimit = 3
	for i in range(upperlimit):
		if checkOddness(gr)>2:
			gr = normalizeGraphEdgesIter(gr)

	return gr

def normalizeGraphEdgesIter(gr):
	oddNeighbors = []
	upperlimit = 5
	for node in gr.nodes():
		if (len(gr.neighbors(node))%2 != 0):
			oddNeighbors.append(node)

	for i, node in enumerate(oddNeighbors):
		if (len(gr.neighbors(node))%2 != 0 and len(oddNeighbors)>2):
			for j in range(upperlimit):
				randomIdx = nprnd.randint(len(oddNeighbors))
				if (randomIdx == i or randomIdx in gr.neighbors(node)):
					randomIdx = nprnd.randint(len(oddNeighbors))
				else:
					gr.add_edge(node, randomIdx)
					break

	return gr

def checkOddness(gr):
	oddNeighbors = []
	for node in gr.nodes():
		if (len(gr.neighbors(node))%2 != 0):
			oddNeighbors.append(node)

	return len(oddNeighbors)

def getcgamesFromGraph(agents, grph):
	cgs = []
	for (i, ag) in enumerate(agents):
		cgs.append(game.CGame())
		cgs[i].agents.append(ag)
		for nIdx in grph.neighbors(i):
			cgs[i].agents.append(agents[nIdx])

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

def getSaveNames(firstname, nOfAgents, run, brainSize):
	name = [firstname, 'M', str(brainSize), 'N', str(nOfAgents), 'S', str(S), 'rounds', str(nRounds), 'run', str(run)]
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

def getComunitySaveName(firstname, nOfAgents, nOfNeigh, run, brainSize):
	name = [firstname, 'M', str(brainSize), 'N', str(nOfAgents), 'neighs', str(nOfNeigh), 'S', str(S), 'rounds', str(nRounds), 'run', str(run)]
	name.append('.comunity')
	saveName = '_'.join(name)
	name.remove('.comunity')
	return saveName

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
M = range(2,5)
N = [403]
nRounds = 10000
S = 2
i = 0
runs = 12
totalGames = getTotalGames()
dVonNeumann = range(1,7)
totalGamesVonNeumann = runs * len(M) * (len(N)+1) * len(dVonNeumann)
