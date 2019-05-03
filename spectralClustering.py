from sklearn.cluster import SpectralClustering
import numpy as np
import networkx as nx
import graphing
import math
import utils
import community

CLUSTER_VALS = range(2, 10)
GAMMA_VALS = [10**i * j for i in range(-3, 4) for j in [0.5, 1]]
# GAMMA_VALS = [1]

def spectralCluster(G):
	# graphing.pad_graph(G)
	adjMatrix = nx.to_numpy_matrix(G)
	optClusters = None
	optNumClusters = None
	optModularity = -math.inf
	ind_to_node = utils.ind_to_node_map(G)
	for n in CLUSTER_VALS:
		for g in GAMMA_VALS:
			clustering = SpectralClustering(n_clusters=n, gamma=g, assign_labels="discretize")
			# affinity = clustering.fit(adjMatrix)
			# print(affinity.labels_, i, "affinity")
			predict = clustering.fit_predict(adjMatrix)
			clustering = {}
			for ind in range(len(predict)):
				node = ind_to_node[ind]
				clustering[node] = predict[ind]
			modularity = community.modularity(clustering, G)
			if modularity > optModularity:
				optClusters = clustering
				optNumClusters = n
				optGamma = g
				optModularity = modularity
	return optClusters, optNumClusters, optGamma, optModularity




def test(file):
	G = graphing.create_graph(file)
	print(spectralCluster(G))

# test('naive_110_house_metric.csv')
