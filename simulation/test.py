import networkx as nx

def normalizeGraphEdges(gr):
	oddNeighbors = []
	for node in gr.nodes():
		print "{}: {}".format(node, gr.neighbors(node))
		if (len(gr.neighbors(node))%2 != 0):
			oddNeighbors.append(node)

	print oddNeighbors

ws = nx.watts_strogatz_graph(43, 3, 0.75)
normalizeGraphEdges(ws)
