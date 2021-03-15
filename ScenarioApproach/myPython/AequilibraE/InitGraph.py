import numpy as np


def InitGraph(project):

    project.network.build_graphs()
    graph = project.network.graphs['c']
    graph.set_graph('distance')
    graph.set_blocked_centroid_flows(False)
    
    return graph
