import os
import sys
import numpy as np
import pandas as pd

class Graph:
    
    pass


def ParseTNTP(pathDataFolder, nameNet):

    pathDataPrefix = pathDataFolder + nameNet + '\\' + nameNet + '_'

    pathDataNode = pathDataPrefix + 'node' + '.tntp'
    pathDataNet  = pathDataPrefix +  'net' + '.tntp'
    pathDataOD   = pathDataPrefix +  'ODs' + '.tntp'

    G = Graph()

    dataOD   = pd.read_csv(pathDataOD,   sep='\t')
    dataNet  = pd.read_csv(pathDataNet,  sep='\t')
    dataNode = pd.read_csv(pathDataNode, sep='\t')

    G.dataOD   = np.genfromtxt(pathDataOD, delimiter='\t', skip_header=0)
    G.dataNet  = np.genfromtxt(pathDataOD, delimiter='\t', skip_header=1)
    G.dataNode = np.genfromtxt(pathDataOD, delimiter='\t', skip_header=1)

    G.nameNet = nameNet
    G.numEdge = len(dataNet)
    G.numNode = len(dataNode)
    G.numDmnd = len(dataOD)

    G.T = np.array(dataNet.free_flow_time)
    G.B = np.array(dataNet.b)
    G.P = np.array(dataNet.power)
    G.C = np.array(dataNet.capacity)

    G.a = np.multiply(G.T, G.B)
    G.c = G.T
    
    G.Q = np.diag(np.transpose(G.a))
    G.q = G.c

    G.initNode = np.array(dataNet.init_node)
    G.termNode = np.array(dataNet.term_node)

    return G