from sklearn.cluster import SpectralClustering
import numpy as np
import networkx as nx
import graphing
import math

CLUSTER_VALS = range(2, 10)

def spectralCluster(G):
	adjMatrix = nx.to_numpy_matrix(G)
	optClusters = None
	optNumClusters = None
	optModularity = -math.inf
	for i in CLUSTER_VALS:
		clustering = SpectralClustering(n_clusters=i, assign_labels="discretize")
		affinity = clustering.fit(adjMatrix)
		# print(affinity.labels_, i, "affinity")
		predict = clustering.fit_predict(adjMatrix)
		# print(predict, i, "predict")
		


def test(file):
	G = graphing.create_graph(file)
	spectralCluster(G)

test('115_house.csv')