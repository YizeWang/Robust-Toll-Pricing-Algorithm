import os
import sys
import numpy as np
import numpy.matlib
import pandas as pd
import networkx as nx
from scipy import sparse
import matplotlib.pyplot as plt


nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
pathDataFolder = '..\\myRealData\\'

nameNet = nameNet2

pathDataPrefix = pathDataFolder + nameNet + '\\' + nameNet + '_'

pathDataNode = pathDataPrefix + 'node' + '.tntp'
pathDataNet  = pathDataPrefix +  'net' + '.tntp'
pathDataOD   = pathDataPrefix +  'ODs' + '.tntp'

dataOD   = np.genfromtxt(pathDataOD,   delimiter='\t', skip_header=0)
dataNet  = np.genfromtxt(pathDataNet,  delimiter='\t', skip_header=1)
dataNode = np.genfromtxt(pathDataNode, delimiter='\t', skip_header=1)

M = dataNet.shape[0]
N = dataNode.shape[0]
K = dataOD.shape[0]

A11 = -np.eye(3, dtype=np.double)
A12 = np.matlib.repmat(np.eye(3, dtype=np.double), 1, 3)
A1 = np.concatenate((A11, A12), axis=1)
# A = sparse.bmat([A11, A12])


# G.nameNet = nameNet
# G.numEdge = len(G.dataNet)
# G.numNode = len(G.dataNode)
# G.numDmnd = len(G.dataOD)

# G.T = G.dataNet.free_flow_time
# G.B = G.dataNet.b
# G.P = G.dataNet.power
# G.C = G.dataNet.capacity

# G.initNode = G.dataNet.init_node
# G.termNode = G.dataNet.term_node









pass