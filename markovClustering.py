#https://github.com/GuyAllard/markov_clustering

import markov_clustering as mc
import networkx as nx
import graphing

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
    matrix = nx.to_scipy_sparse_matrix(graph) #get adjacency matrix in sparse form

    result = mc.run_mcl(matrix) #MCL algorithm with default parameters, inflation of 2
    # result = mc.run_mcl(matrix, inflation=1.5) #MCL algorithm with inflation of 1.5 (coarser clustering)
    clusters =  mc.get_clusters(result) #gets clusters
    mc.draw_graph(matrix, clusters, node_size=50, with_labels=False, edge_color="silver") #display clusters
