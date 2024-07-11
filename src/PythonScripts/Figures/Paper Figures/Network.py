import os
from os.path import join

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

pathCurrFolder = os.path.abspath(os.getcwd())
pathRepoFolder = join(pathCurrFolder, os.pardir, os.pardir, os.pardir)
pathNetworkFolder = join(pathRepoFolder, "myRealData", "SiouxFalls")
pathNode = join(pathNetworkFolder, "SiouxFalls_node.tntp")
pathOD = join(pathNetworkFolder, "SiouxFalls_net.tntp")

node_df = pd.read_csv(pathNode, delimiter='\t')
demand_df = pd.read_csv(pathOD, delimiter='\t')

G = nx.Graph()

for idx, node in node_df.iterrows():
    Node = int(node['Node'])
    X = float(node['X'])
    Y = float(node['Y'])
    G.add_node(Node, pos=(X, Y))

for idx, edge in demand_df.iterrows():
    init_node = edge['init_node']
    term_node = edge['term_node']
    G.add_edge(init_node, term_node)

pos_nodes = nx.get_node_attributes(G, 'pos')

pos_labels = {}
labels = {}
for node, pos in pos_nodes.items():
    pos_labels[node] = (pos[0] - 0.003, pos[1] + 0.0025)
    labels[node] = str(node)
pos_labels[2] = (pos_labels[2][0], pos_labels[2][1] + 0.001)
pos_labels[4] = (pos_labels[4][0] + 0.006, pos_labels[4][1] + 0.001)
pos_labels[10] = (pos_labels[10][0], pos_labels[10][1] - 0.007)
pos_labels[17] = (pos_labels[17][0] + 0.006, pos_labels[17][1] - 0.0025)
pos_labels[21] = (pos_labels[21][0] + 0.006, pos_labels[21][1] - 0.007)

nx.draw(G, pos_nodes, node_size=30)
nx.draw_networkx_labels(G, pos_labels, labels, font_size=12)
plt.show()
