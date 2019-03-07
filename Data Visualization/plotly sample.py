import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
G.add_node(1)
G.add_node(2)
G.add_node(4)
G.add_edge(1, 2, weight=4)
G.add_edge(2, 4, weight=2)
G.add_edge(1, 4, weight= 20)


nx.draw(G)
plt.show()