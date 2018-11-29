import networkx as nx
import utils

""" Creates a list of tuples of voting data from a CSV and creates a NetworkX graph with the according nodes and edge weights """
def createGraph(csvFileName):
    tupleList = utils.from_csv(csvFileName)
    graphyBoi = nx.Graph()
    for tupleBoi in tupleList:
        graphyBoi.add_edge(tupleBoi[0],tupleBoi[1],tupleBoi[4])
    return graphyBoi
