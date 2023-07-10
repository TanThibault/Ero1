import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

O = ox.graph_from_place('Outremont, Montreal, Canada', network_type='drive')
# Verdun =  ox.graph_from_place('Verdun, Montreal, Canada', network_type='drive')
# Montreal = ox.graph_from_place('Montreal, Canada', network_type='drive')

def length_path(P,city):
	length = 0
	for i in range(0,len(P)-1):
		length += city.edges[P[i], P[i+1], 0]["length"]
	return length
def eulerize(city):
	city = city.to_undirected()
	odd_degree_nodes = [n for n, d in city.degree() if d % 2 == 1]
	G = nx.MultiGraph(city)
	if len(odd_degree_nodes) == 0:
		return G
	odd_deg_pairs_paths = [
		(m, {n: nx.shortest_path(G, source=m, target=n, weight="length")})
		for m, n in combinations(odd_degree_nodes, 2)
	]
	Gp = nx.Graph()
	for n, Ps in odd_deg_pairs_paths:
		for m, P in Ps.items():
			if n != m:
				Gp.add_edge(
					m, n, weight=length_path(P, G), path=P
				)
	best_matching = nx.Graph(list(nx.min_weight_matching(Gp)))
	for m,n in best_matching.edges():
		path = Gp[m][n]["path"]
		G.add_edges_from(nx.utils.pairwise(path))
	return G


def eule_broken(city):
	odd_degree_nodes = [n for n, d in city.degree() if d % 2 == 1]
	undirected = nx.MultiGraph(city)
	if len(odd_degree_nodes) == 0:
		return undirected
	odd_comb = []
	for m, n in combinations(odd_degree_nodes, 2):
		odd_comb.append((m, n))
	pairings = []
	while len(odd_comb) != 0:
		i = 0
		pairs = []
		while i < len(odd_comb):
			(a,b) = odd_comb[i]
			if not a in pairs and not b in pairs:
				pairs.append(a)
				pairs.append(b)
				odd_comb.pop(i)
			else:
				i += 1
		pairings.append(pairs)
	short = []
	nb = 0
	min_weight = 0
	index = 0
	for pairs in pairings:
		path = []
		i = 0
		bigweight = 0
		while i < len(pairs):
			p = nx.shortest_path(undirected,source=pairs[i], target=pairs[i+1],weight="length")
			t = 0
			while t < len(p)-1:
				bigweight += undirected.edges[p[t], p[t+1], 0]["length"]
				t += 1
			path.append(p)
			i += 2
		short.append(path)
		if bigweight < min_weight or min_weight == 0:
			min_weight = bigweight
			nb = index
		index+=1
	for i in short[nb]:
		j = 0
		while j < len(i)-1:
			undirected.add_edge(i[j],i[j+1],color = "r",length=undirected.edges[i[j],i[j+1],0]["length"])
			j+=1
	return undirected
