"""
You can add metrics to this file. New metrics should take in a list of Pairs
and output a dictionary mapping from pair -> metric_value. Once you write the
function, add it to the metrics list defined above calculate_metric().
"""

from utils import *
import statistics
from Pair import *

"""
Given a list of pairs, a list of dictionaries mapping from pair -> metric_value,
and a list of weights corresponding to the order of the list of dictionaries.
Calculates and returns a weighted sum of the metrics for each pair and returns
a new dictionary mapping from pair -> metric_value.
"""
def weighted_metric(pairs, metrics, weights):
    assert len(metrics) == len(weights)
    result = dict()
    for p in pairs:
        final = 0
        for i in range(len(metrics)):
            final += weights[i] * metrics[i].get(p)
        result[p] = final
    return result

"""
Calculates the naive metric for each pair. Takes in a list of pair objects.
Outputs a dictionary mapping Pair -> naive_metric_value.
"""
def naive_metric(pairs):
    def f(data):
        return data['votes_same'] / (data['votes_total'] + 1)
    result = dict()
    for p in pairs:
        result[p] = p.calc(f)
    return result

"""
Calculates the sponsorship metric for each pair. Takes in a list of pairs.
Outputs a dictionary mapping Pair -> sponsorship_metric_value.
"""
def sponsorship_metric(pairs):
    def f(data):
        return data.get('mutual_sponsorships')
    result = dict()
    vals = []
    for p in pairs:
        val = p.calc(f)
        vals.append(val)
        result[p] = val
    median = statistics.median(vals)
    for k in result.keys():
        result[p] /= (median + 1)
    return result

metrics = [naive_metric, sponsorship_metric]

"""
Calculates metric and writes a list of tuples (member_a, member_b, metric)
to file. Takes in a list of weights corresponding to the metrics array above.
"""
def calculate_metric(congress, chamber, weights):
    filename = str(congress) + '_' + chamber + '.csv'
    data = from_csv(filename)
    pairs = [Pair(None, None, tup) for tup in data]
    metric_list = [metric(pairs) for metric in metrics]
    final_metric_values = weighted_metric(pairs, metric_list, weights)
    new_filename = str(congress) + '_' + chamber + '_metric.csv'
    new_header = ('member_a', 'member_b', 'metric')
    data = [(pair.id_a, pair.id_b, metric) for pair, metric in final_metric_values.items()]
    to_csv(new_header, data, new_filename)
