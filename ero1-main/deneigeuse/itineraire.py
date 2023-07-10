import osmnx as ox
import networkx as nx
import collections
import numpy as np
import matplotlib.pyplot as plt

def length_path(P,city):
	length = 0
	for i in range(0,len(P)-1):
		length+=city.edges[P[i],P[i+1],0]["length"]
	return length
def eulerize(city):
	copy = nx.MultiDiGraph(city)
	while(not nx.is_eulerian(copy)):
		in_degree_nodes = []
		out_degree_nodes = []
		for n,d in copy.out_degree():
			a = copy.in_degree(n)
			if(a<d):
				in_degree_nodes.append(n)
			if(a>d):
				out_degree_nodes.append(n)
		G = nx.MultiDiGraph(copy)
		for i in out_degree_nodes:
			minimum = -1
			p_min = []
			k = 0
			for j in in_degree_nodes:
				P = nx.shortest_path(city, source=i, target=j,weight="length")
				l = length_path(P,city)
				if (minimum < 0 or l < minimum):
					minimum = l
					p_min = P
					k=j
			G.add_edges_from(nx.utils.pairwise(p_min))
			if(k in in_degree_nodes):
				in_degree_nodes.remove(k)
		copy = G
	return copy

#Outremont = ox.graph_from_place('Outremont, Montreal, Canada', network_type='drive')
#Montreal = ox.graph_from_place('Montreal, Canada', network_type='drive')
#ox.plot_graph(Montreal)
#Verdun = ox.graph_from_place('Verdun, Montreal, Canada', network_type='drive')
#Riv = ox.graph_from_place('Rivière-des-prairies-pointe-aux-trembles, Montreal, Canada', network_type='drive')
#Saint = ox.graph_from_place('Saint-Léonard, Montreal, Canada', network_type='drive')
#Plateau = ox.graph_from_place('Plateau-Mont-Royal, Montreal, Canada', network_type='drive')
#comp_outr = [[n for n in item] for item in nx.strongly_connected_components(Outremont)]
#comp_ver = [[n for n in item] for item in nx.strongly_connected_components(Verdun)]
#comp_riv = [[n for n in item] for item in nx.strongly_connected_components(Riv)]
#comp_saint = [[n for n in item] for item in nx.strongly_connected_components(Saint)]
#comp_plat = [[n for n in item] for item in nx.strongly_connected_components(Plateau)]
#comp_Mont = [[n for n in item] for item in nx.strongly_connected_components(Montreal)]

#P = Outremont.subgraph(max(nx.strongly_connected_components(Outremont),key=len))
#h = eulerize(P)
#d = [u for u, v in nx.eulerian_circuit(h)]

def length_boucle(city,base,Path,nb_den1,nb_den2):
	c = collections.Counter(Path)
	a,b=c.most_common()[0]
	i = 0
	start = Path.index(a)
	l = [a]
	total = 0
	while i < b:
		length = 0
		p = []
		while True:
			p.append(Path[start])
			if start+1 == len(Path):
				length+= city.edges[Path[start],Path[0],0]["length"]
				start = 0
			else:
				length+= city.edges[Path[start],Path[start+1],0]["length"]
				start+=1
			if Path[start] == a:
				break
		i+=1
		if(nb_den2>0):
			if(length>160000 and nb_den2 > 0):
				nb_den2 -=1
				_,nb_den1,nb_den2 = length_boucle(city,base,p,nb_den1,nb_den2)
			else:
				p.append(a)
				total+=length
				l.append((p,length))
		else:
			if(length>80000 and nb_den1 > 0):
				nb_den1 -=1
				_,nb_den1,nb_den2 = length_boucle(city,base,p,nb_den1,nb_den2)
			else:
				p.append(a)
				total+=length
				l.append((p,length))
	l.append(total)
	base.append(l)
	return base,nb_den1,nb_den2
def reduce_graph(city,all_comp):
	G = nx.MultiDiGraph()
	for i in all_comp:
		for node in i:
			for lien in city.adj[node]:
				for j in all_comp:	
					if j[0]!=i[0] and lien in j:
						G.add_edge(i[0],j[0])
	return G

def parcours_den(circuit,type1,type2):
	den = [[-1,[],0,2] for k in range(type2)]
	for k in range(type1):
		den.append([-1,[],0,1])
	nb_den = 0
	for i in circuit:
		k = 1
		while k < len(i)-1:
			print(i[k][1])
			if(den[nb_den][3] == 2):
				if(den[nb_den][2]+i[k][1]<160000 or nb_den+1==len(den)):
					den[nb_den][0] = i[0]
					den[nb_den][1].append(i[k][0])
					den[nb_den][2] += i[k][1]
					k+=1
				else:
					nb_den+=1
			else:
				if(den[nb_den][2]+i[k][1]<80000 or nb_den+1==len(den)):
					den[nb_den][0] = i[0]
					den[nb_den][1].append(i[k][0])
					den[nb_den][2] += i[k][1]
					k+=1
				else:
					nb_den+=1
		nb_den+=1
	return den
#ox.plot_graph(Outremont)
#h = eulerize(h)
#ox.plot_graph(Outremont)
#print(nx.is_eulerian(h))
#print(nx.is_strongly_connected(Montreal))
