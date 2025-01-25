import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

G = nx.Di_graph()
G.add_nodes_from([1,4,5,7,11,10])
G.add_weighted_edges_from([(1,5,3)])
G.add_weighted_edges_from([(5,1,2)])
G.add_weighted_edges_from([(1,10,2)])
G.add_weighted_edges_from([(1,4,1)])
G.add_weighted_edges_from([(5,4,2)])
G.add_weighted_edges_from([(4,5,3)])
G.add_weighted_edges_from([(4,7,3)])
G.add_weighted_edges_from([(7,4,3)])
G.add_weighted_edges_from([(4,10,2)])
G.add_weighted_edges_from([(10,4,2)])
G.add_weighted_edges_from([(4,11,1)])
G.add_weighted_edges_from([(11,4,2)])
G.add_weighted_edges_from([(5,7,2)])
G.add_weighted_edges_from([(5,10,1)])
G.add_weighted_edges_from([(10,5,2)])
G.add_weighted_edges_from([(5,11,8)])
G.add_weighted_edges_from([(11,5,5)])
G.add_weighted_edges_from([(7,10,2)])
G.add_weighted_edges_from([(10,7,4)])
G.add_weighted_edges_from([(7,11,1)])
G.add_weighted_edges_from([(11,7,3)])
G.add_weighted_edges_from([(10,11,3)])
G.add_weighted_edges_from([(11,10,4)])


# Create position dictionary for plotting the graph
pos = {}
pos[1] = np.array([0.5,0.1])
pos[4] = np.array([0.75,0.35])
pos[5] = np.array([0.25,0.35])
pos[7] = np.array([0.9,0.85])
pos[10] = np.array([0.5, 0.6])
pos[11] = np.array([0.1,0.85])

nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
plt.show()

