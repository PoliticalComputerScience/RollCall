# RollCall

The clusters directory stores dictionaries in the form of {"matrix": matrix,
"clusters": clusters, "infl": inflation_value} serialized using the Python
pickle library. An example of using pickle can be seen in markovClustering.py.

The data directory stores csv's that contain pairs of congress members along with
the relevant data between them that are used for calculating metrics. It also
stores pairs of congress members with metric values.

Pair.py contains an abstraction for two members of Congress that stores a data
dictionary to store data values. If you pass in a tuple, then the pair will be
created based on the tuple, otherwise the pair will be created based on the rest
of the constructor args. These pairs are hashable. Two Pairs will return the
same hash if each represents the same two congress members.

graphing.py contains create_graph, which takes a metric csv and returns a
NetworkX graph.

propublica_api.py contains code that creates all pairs of congress members from
a given session and chamber of Congress and writes them to file. Feel free to
augment these tuples using data from other apis.

utils.py contains functions to get data from ProPublica as well as functions
to write to and from csv's. Currently, those functions write to and from the
directory data/.

metrics.py is where metrics are calculated. calculate_metric calculates metric
values based on a weighted sum of the metric functions. You can add metrics by
defining a metric function and adding the function to the list of metrics.
    Each metric function takes in a list of Pair objects and returns a
dictionary mapping Pair -> metric_value.

markovClustering contains functions to perform Markov clustering on graphs of
congress members connected by edges that represent a metric value. See the file
to see more detailed descriptions of Markov clustering.
