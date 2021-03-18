import numpy as np


def ImposeToll(graph, t):

    graph.graph['free_flow_time'] = graph.network['free_flow_time'] + t
    graph.graph['b'] = np.divide(np.multiply(graph.network['b'], graph.network['free_flow_time']), graph.graph['free_flow_time'])
