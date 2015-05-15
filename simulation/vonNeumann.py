import numpy as np
import collections
from scipy.spatial.distance import cityblock as cityblock
import game

def intFactorize(n, d):
	# return closest factorization, if the number cannot be factorized, return the one with smallest rest
	sn = np.sqrt(n)
	if sn.is_integer():
		# already found factorization, it is the square root
		return (int(sn), int(sn))
	else:
		div = int(sn)
		while div>d-2:
			if n%div == 0:
				return (div, n/div)
			else:
				div -= 1

	return (n, 1)

def intFactorizeRestfull(n, d):
	# return closest factorization, if the number cannot be factorized, return the one with smallest rest
	sn = np.sqrt(n)
	if sn.is_integer():
		# already found factorization, it is the square root
		return (int(sn), int(sn))
	else:
		restfull = collections.defaultdict(list)
		div = int(sn)
		while div>d+1:
			if n%div == 0:
				return (div, n/div)
			else:
				restfull[n%div].append((div, n/div))
				div -= 1

	od = collections.OrderedDict(sorted(restfull.items()))
	# return the biggest factorization possible
	return od[od.keys()[0]][0]

def generateSupportGrid(lst, d):
	n = len(lst)
	(p,q) = intFactorize(n,d)
	if (p == n and q == 1):
		print "Integer factorization of {} not possible!".format(n)
	else:
		# print (p,q)
		supportGrid = np.empty((p+(2*d), q+2*d), dtype=object)
		# supportGrid = generate from agents
		width = range(d, (d+p))
		height = range(d, (d+q))
		# print width, height
		for i,x in enumerate(width):
			for j,y in enumerate(height):
				supportGrid[x][y] = lst[i*q + j]

		supportGrid[d+p:, d:d+q] = supportGrid[d:d+d, d:d+q]
		supportGrid[:d, d:d+q] = supportGrid[p:p+d, d:d+q]
		supportGrid[d:d+p, d+q:] = supportGrid[d:d+p, d:d+d]
		supportGrid[d:d+p, :d] = supportGrid[d:d+p, q:q+d]
		supportGrid[:d, :d] = supportGrid[p:d+p, q:d+q]
		supportGrid[:d, d+q:] = supportGrid[p:d+p, d:d+d]
		supportGrid[d+p:, :d] = supportGrid[d:d+d, q:q+d]
		supportGrid[d+p:, d+q:] = supportGrid[d:d+d, d:d+d]
		return supportGrid, p, q

def getVonNeumannNeigh(supportNeigh, d):
	neighbourhood = []
	# print "support neighbourhood"
	# print supportNeigh
	for i,row in enumerate(supportNeigh):
		for j,elem in enumerate(row):
			# print i,j, d
			if cityblock([i,j], [d,d]) <= d:
				neighbourhood.append(elem)

	return neighbourhood

def generateVonNeumann(lst, d):
	neighs = {}
	supportGrid, p, q = generateSupportGrid(lst, d)
	width = range(d, (d+p))
	height = range(d, (d+q))
	# print width, height
	for i,x in enumerate(width):
		for j,y in enumerate(height):
			neighs[supportGrid[x][y]] = getVonNeumannNeigh(supportGrid[x-d:x+d+1, y-d:y+d+1], d)

	return neighs


# g = game.Game()
# g.addAgents('community', 20, 3, 2)
# neigh = generateVonNeumann(g.agents,1)
# for x in neigh:
# 	print "neighbourhood of {}:".format(x)
# 	print neigh[x]
