"""
Represents a pair of congress members. Contains the IDs of both and the data
points relevant to calculating the metric between them. Each pair is hashable
(the hash is based on the id's of the two members).
"""

keys = ['votes_same', 'votes_total', 'mutual_sponsorships']

class Pair:

    """
        If a tuple is passed in, the class members are based off of the tuple.
        Otherwise, class members are based on the other arguments. The names
        are optional arguments in case you want to create a dummy Pair using
        just the id's (which is what the hash is based on).
    """
    def __init__(self, id1, id2, name_1=None, name_2=None, tup=None):
        if not tup: #create Pair directly
            self.id_a = id1
            self.id_b = id2
            self.name_a = name_1
            self.name_b = name_2
            self.data = dict()
            for k in keys:
                self.data[k] = 0
        else: #create Pair from tuple of data values (id_a, id_b, k_0, .., k_n)
            self.id_a = tup[0]
            self.id_b = tup[1]
            self.name_a = tup[2]
            self.name_b = tup[3]
            self.data = dict()
            for i in range(len(keys)):
                self.data[keys[i]] = int(tup[i + 4])

    """ Equality is based on ID values. """
    def __eq__(self, other):
        return (self.id_a == other.id_a and self.id_b == other.id_b) or \
        (self.id_a == other.id_b and self.id_b == other.id_a)

    def __hash__(self):
        return hash(self.id_a) ^ hash(self.id_b)

    """
    Gets data value for calcualting metrics from dictionary. The list of keys
    is stored in the keys list at the top of the file.
    """
    def getVal(self, key):
        return self.data.get(key)

    """
    Returns a value for the metric based on the function f. f takes in the
    Pair.data dictionary and calculates the value. The value returned
    does not necessarily need to be the value of the metric itself, but can be
    used in intermediary calculations for the metric.
    For example, if you require a comparison with other pairs, you can fetch the
    the data for all pairs using calc and then calculate the metric from those.
    """
    def calc(self, f):
        return f(self.data)

    def toTuple(self):
        return tuple([self.id_a, self.id_b, self.name_a, self.name_b] + [v for k, v in self.data.items()])

def get_pair_hash(id_a, id_b):
    return hash(id_a) ^ hash(id_b)
