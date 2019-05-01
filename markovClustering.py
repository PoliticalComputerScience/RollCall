#https://github.com/GuyAllard/markov_clustering

import pickle
import markov_clustering as mc
import networkx as nx
import graphing
from sklearn.preprocessing import normalize

INFLATION_VALS = [i/10 for i in range(15, 26)]
INFL_VALS = [i / 10 for i in range(12, 23)]
DEBUG = True

""" Using Markov Clustering on NetworkX graph to find clusters

    Can play around with inflation values to determine optimal cluster quality with modularity*:
        - Loop through range of inflation values and create corresponding clusters
        - Q = mc.modularity(matrix=result, clusters=clusters)
        - Find MAX(Q) and use the inflation value for that clustering for highest cluster quality

        * "Briefly, the modularity (Q) can be considered to be the fraction of graph edges which belong to a cluster
        minus the fraction expected due to random chance, where the value of Q lies in the range [-1, 1].
        High, positive Q values suggest higher clustering quality."

"""

#def cluster(csvFileName):
#    graph = graphing.createGraph(csvFileName) #get network from csv data
#    return cluster_graph(graph)

def cluster_graph(graph, infl):
    """
    A naive markov clustering based only on inflation value.
    """
    matrix = nx.to_scipy_sparse_matrix(graph) #get adjacency matrix in sparse form
    m = normalize(matrix, norm='l1', axis=1)
    result = mc.run_mcl(m, inflation=infl) #MCL algorithm with default parameters, inflation of 2
    # result = mc.run_mcl(matrix, inflation=1.5) #MCL algorithm with inflation of 1.5 (coarser clustering)
    clusters =  mc.get_clusters(result) #gets clusters
    return m, clusters, infl

def opt_cluster_graph(graph):
    """
    Finds the best possible clustering of <graph> (optimized over modularity)

    :param graph: (type=NetworkX graph)
    :return: (type=tuple<NumPy Matrix, tuple<NumpyMatrix> >) the matrix representation
    of the graph followed the tuple of cluster matrices
    """
    best_quality = -2
    best_clusters = None
    best_infl = 0
    matrix = nx.to_scipy_sparse_matrix(graph) #get adjacency matrix in sparse form
    for infl in INFLATION_VALS:
        m, clusters, _ = cluster_graph(graph, infl)
        quality = mc.modularity(matrix, clusters) #measure of quality of clustering
        if DEBUG:
            print("inflation: " + str(infl) + ", expansion: " + str(expn) + ", modularity: " + str(quality))
        if quality > best_quality:
            best_clusters = clusters
            best_quality = quality
            best_infl = infl
    return matrix, best_clusters, best_quality, best_infl

def draw_clustering(matrix, clusters):
    mc.draw_graph(matrix, clusters, node_size=4, with_labels=False, edge_color="white") #display clusters

if __name__ == "__main__":
    congress = 115
    chamber = "house"
    metric = "naive"
    g = graphing.create_graph("{}_{}_{}_metric.csv".format(metric, congress, chamber))
    #for infl in INFL_VALS:
    #    print("graphing incl: " + str(infl))
    infl = INFL_VALS[0]
    lst = [e for e in g.edges(data=True)]
    lst.sort(key=lambda x:x[2]['weight'])
    for i in range(int(len(lst)/2)):
        g.remove_edge(lst[i][0], lst[i][1])
    m, c, i = cluster_graph(g, 1.2)#cluster_graph(g, 1.2)
    #i = 1.25
    #with open(str(i) + 'naive_' + str(congress) + '_cluster', 'wb') as outfile:
        #pickle.dump({'matrix': m, 'clusters': c, 'infl': i}, outfile)
    #with open(str(i) + 'naive_' + str(congress) + '_cluster', 'rb') as infile:
        #d = pickle.load(infile)
    #draw_clustering(m, c)
