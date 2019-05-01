from sklearn.cluster import SpectralClustering
import numpy as np
import networkx as nx
import graphing
import math
import utils
import community

CLUSTER_VALS = range(2, 10)

def spectralCluster(G):
	adjMatrix = nx.to_numpy_matrix(G)
	optClusters = None
	optNumClusters = None
	optModularity = -math.inf
	ind_to_node = utils.ind_to_node_map(G)
	for i in CLUSTER_VALS:
		clustering = SpectralClustering(n_clusters=i, assign_labels="discretize")
		affinity = clustering.fit(adjMatrix)
		# print(affinity.labels_, i, "affinity")
		predict = clustering.fit_predict(adjMatrix)
		clustering = {}
		for ind in range(len(predict)):
			node = ind_to_node[ind]
			clustering[node] = predict[ind]
		modularity = community.modularity(clustering, G)
		if modularity > optModularity:
			optClusters = clustering
			optNumClusters = i
			optModularity = modularity
	return optClusters, optNumClusters, optModularity




def test(file):
	G = graphing.create_graph(file)
	spectralCluster(G)

#test('111_senate_metric.csv')
