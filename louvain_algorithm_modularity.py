"""This file implements functions to return a graph
on which the modularity-maximizing communities are indicated
by using the Louvain algorithm.
@source https://stackoverflow.com/questions/29897243/graph-modularity-in-python-networkx"""

import community
import matplotlib.pyplot as plt
import networkx as nx
import graphing

def main():
    G = nx.Graph()

    G = graphing.create_graph('115_house.csv')
    nx.transitivity(G)

    # Find modularity
    part = community.best_partition(G)
    print(part)
    mod = community.modularity(part,G)

    # Plot, color nodes using community structure
    values = [part.get(node) for node in G.nodes()]
    nx.draw_spring(G, cmap=plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
    plt.show()

def louvainCluster(g):
    clustering = community.best_partition(g)
    mod = community.modularity(clustering, g)
    num_clusters = max([clustering[key] for key in clustering]) + 1
    return clustering, num_clusters, mod

if __name__ == '__main__':
    main()
