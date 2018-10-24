from utils import *
def weighted_sum(m1, m2, w1, w2):
    return w1*m1 + w2*m2

""" Calculates the metric with the given weighted sums. """
def metric(filename, a, b):
    data = from_csv(filename)
    naive = naive_metric(data)
    sponsorship = normalize(data)
    pairs = []
    for i in range(len(data)):
        pairs.append((data[i][0], data[i][1], weighted_sum(naive[i][2], sponsorship[i][2], a, b)))
    return pairs
