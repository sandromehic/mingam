import game

def generateGameComunities(N, M, S, nOfNeigh):
	g = game.Game()
	g.addAgents('community', N, M, S)
	cgs = []
	for c in xrange((N + nOfNeigh // 2) // nOfNeigh):
		cgs.append(game.CGame())

	print len(cgs)

	for i, cg in enumerate(cgs):
		cg.agents = g.agents[i*nOfNeigh:i*nOfNeigh + nOfNeigh]

	return g, cgs

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

M = 2
N = 101
neighSize = range(3,19,2)
S = 5

for nOfNeigh in neighSize:
	g, cgs = generateGameComunities(N, M, S, nOfNeigh)
	printAgentsAndGames(g, cgs)