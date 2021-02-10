import os
import sys
import numpy as np
import pandas as pd
from Graph import Graph

def ParseTNTP(pathDataFolder, nameNet):

    pathDataPrefix = pathDataFolder + nameNet + '\\' + nameNet + '_'

    pathDataNode = pathDataPrefix + 'node' + '.tntp'
    pathDataNet  = pathDataPrefix +  'net' + '.tntp'
    pathDataOD   = pathDataPrefix +  'ODs' + '.tntp'

    G = Graph()

    G.dataOD   = pd.read_csv(pathDataOD,   sep='\t')
    G.dataNet  = pd.read_csv(pathDataNet,  sep='\t')
    G.dataNode = pd.read_csv(pathDataNode, sep='\t')

    G.nameNet = nameNet
    G.numEdge = len(G.dataNet)
    G.numNode = len(G.dataNode)
    G.numDmnd = len(G.dataOD)

    G.T = G.dataNet.free_flow_time
    G.B = G.dataNet.b
    G.P = G.dataNet.power
    G.C = G.dataNet.capacity
    
    G.initNode = G.dataNet.init_node
    G.termNode = G.dataNet.term_node

    return G