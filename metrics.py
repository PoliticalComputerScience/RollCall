from utils import *
import * from statistics

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

def normalize(input_list):
    temp = [x[4] for x in input_list]
    mid = median(temp)
    new_list = [k / mid for k in temp]
    result = [(input_list[y][0], input_list[y](1), input_list[y](2), input_list[y](3), new_list[y]) for y in range(len(input_list))]
    return result
