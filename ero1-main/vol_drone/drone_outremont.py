import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from chinese_postman import eulerize

O = ox.graph_from_place('Outremont, Montreal, Canada', network_type='drive')

G = eulerize(O)
euler_circuit = nx.eulerian_circuit(G)
pos = nx.spring_layout(O)
k = [u for u, v in nx.eulerian_circuit(G)]
dist = 0
for i in range(0,len(k)-1):
	dist += G[k[i]][k[i+1]][0]["length"]
print(f"Outremont circuit en km: {dist}")
nx.draw_networkx_edges(O, pos=pos, edgelist=list(euler_circuit))
nx.draw_networkx_nodes(O, pos=pos)
plt.show()

