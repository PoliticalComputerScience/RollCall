import networkx as nx
import utils

def createGraph(csvFileName):
    tupleList = utils.from_csv(csvFileName)
    graphyBoi = nx.Graph()
    for tupleBoi in tupleList:
        graphyBoi.add_edge(tupleBoi[0],tupleBoi[1],tupleBoi[2])
    return graphyBoi
