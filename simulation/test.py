import networkx as nx
import copy
import numpy.random as nprnd

def normalizeGraphEdges(gr):
	upperlimit = 3
	i = 0
	while(checkOddness(gr)>2 or i<upperlimit):
		gr = normalizeGraphEdgesIter(gr)
		i += 1

	return gr

def normalizeGraphEdgesIter(gr):
	oddNeighbors = []
	upperlimit = 5
	i = 0
	for node in gr.nodes():
		if (len(gr.neighbors(node))%2 != 0):
			oddNeighbors.append(node)

	for i, node in enumerate(oddNeighbors):
		if (len(gr.neighbors(node))%2 != 0 and len(oddNeighbors)>2):
			randomIdx = nprnd.randint(len(oddNeighbors))
			while ((randomIdx == i or randomIdx in gr.neighbors(node)) or i<upperlimit):
				randomIdx = nprnd.randint(len(oddNeighbors))
				i+=1

			print "adding edge to node {}, node {}".format(node, randomIdx)
			gr.add_edge(node, randomIdx)

	return gr

def checkOddness(gr):
	oddNeighbors = []
	for node in gr.nodes():
		if (len(gr.neighbors(node))%2 != 0):
			oddNeighbors.append(node)

	return len(oddNeighbors)

gr = nx.watts_strogatz_graph(43, 3, 0.75)
gr = normalizeGraphEdges(gr)

print "length of odd neighbours {}".format(checkOddness(gr))

for node in gr.nodes():
	if (len(gr.neighbors(node))%2 != 0):
		print "{}: {}".format(node, gr.neighbors(node))
