import networkx as nx
import utils
import csv
from math import sqrt

""" Creates a list of tuples of voting data from a CSV and creates a NetworkX graph with the according nodes and edge weights """
def create_graph(csvFileName):
	tupleList = utils.from_csv(csvFileName)
    graphyBoi = nx.Graph()
    for tupleBoi in tupleList:
        graphyBoi.add_edge(tupleBoi[0], tupleBoi[1], weight=float(tupleBoi[4]))
    return graphyBoi

def extract_member_map(file="data/115nom.csv"):
	"""
	returns a dictionary from member bioguide_id's to dw_nominate tuples 
	"""
    f = open(file, "r")
    csv_reader = csv.DictReader(f)
    member_map = {}
    for row in csv_reader:
        bioguide_id = row["bioguide_id"]
        if (row["bioname"] and row["nominate_dim1"] and row["nominate_dim2"]):
            member_map[bioguide_id] = (float(row["nominate_dim1"]), float(row["nominate_dim2"]))
    f.close()
    return member_map

def create_dw_graph():
	"""
	creates a graph with dw_nominate similarity scores
	"""
	g = nx.Graph()
	euclid = lambda pair1,pair2: sqrt((pair1[0]-pair2[0])**2 + (pair1[1]-pair2[1])**2)
	member_map = extract_member_map()
	for memb in member_map:
		g.add_node
	for memb1 in member_map:
		for memb2 in member_map:
			if memb1 != memb2:
				scores1, scores2 = member_map[memb1], member_map[memb2]
				dist = euclid(scores1,scores2)
				if dist != 0:
					weight = 1/dist
				else:
					weight = 1/(2*(.001**2))
				#if weight > .5:
				g.add_edge(memb1, memb2, weight=weight)
	return g

