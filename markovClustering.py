#https://github.com/GuyAllard/markov_clustering

import markov_clustering as mc
import networkx as nx
import graphing

INFLATION_VALS = [i/10 for i in range(15, 26)]
DEBUG = False

""" Using Markov Clustering on NetworkX graph to find clusters

    Can play around with inflation values to determine optimal cluster quality with modularity*:
        - Loop through range of inflation values and create corresponding clusters
        - Q = mc.modularity(matrix=result, clusters=clusters)
        - Find MAX(Q) and use the inflation value for that clustering for highest cluster quality

        * "Briefly, the modularity (Q) can be considered to be the fraction of graph edges which belong to a cluster
        minus the fraction expected due to random chance, where the value of Q lies in the range [-1, 1].
        High, positive Q values suggest higher clustering quality."

"""

def cluster(csvFileName):
    graph = graphing.createGraph(csvFileName) #get network from csv data
    return cluster_graph(graph)

def cluster_graph(graph):
    """
    Finds the best possible clustering of <graph> (optimized over modularity)

    :param graph: (type=NetworkX graph)
    :return: (type=tuple<NumPy Matrix, tuple<NumpyMatrix> >) the matrix representation
    of the graph followed the tuple of cluster matrices 
    """
    best_quality = -2
    best_clusters = None
    matrix = nx.to_scipy_sparse_matrix(graph) #get adjacency matrix in sparse form
    for infl in INFLATION_VALS:
        result = mc.run_mcl(matrix, inflation=infl)
        if DEBUG:
            print("mcl run")
        clusters = mc.get_clusters(result)
        if DEBUG:
            print("clusters found")
        quality = mc.modularity(matrix, clusters) #measure of quality of clustering
        if DEBUG:
            print("inflation: " + str(infl) + ", expansion: " + str(expn) + ", modularity: " + str(quality))
        if quality > best_quality:
            best_clusters = clusters
            best_quality = quality
    return matrix, best_clusters

def draw_clustering(matrix, clusters):
    mc.draw_graph(matrix, clusters, node_size=50, with_labels=False, edge_color="silver") #display clusters

if __name__ == "__main__":
    g = graphing.create_dw_graph()
    matrix, clusters = cluster_graph(g)

