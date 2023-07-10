import osmnx as ox
import networkx as nx
import time
import matplotlib.pyplot as plt

start_time = time.time()
Outremont = ox.graph_from_place('Outremont, Montreal, Canada', network_type='drive')
# Verdun =  ox.graph_from_place('Verdun, Montreal, Canada', network_type='drive')
# Montreal = ox.graph_from_place('Montreal, Canada', network_type='drive')

def trajet(city):
    eulerian_graph = nx.eulerize(city.to_undirected())
    euler_circuit = nx.eulerian_circuit(eulerian_graph)
    pos = nx.spring_layout(Outremont)
    nx.draw_networkx_edges(Outremont, pos=pos, edgelist=list(euler_circuit))
    nx.draw_networkx_nodes(Outremont, pos=pos)
    plt.show()
    k = [u for u, v in nx.eulerian_circuit(eulerian_graph)]
    dist = 0
    for i in range(0, len(k) - 1):
        dist += eulerian_graph[k[i]][k[i + 1]][0]["length"]
    print(f"Outremont circuit en km: {dist}")

trajet(Outremont)
print("--- %s seconds ---" % (time.time() - start_time))
