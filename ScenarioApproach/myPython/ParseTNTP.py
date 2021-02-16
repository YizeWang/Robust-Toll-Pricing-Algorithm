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

    G.dataOD   = dataOD.to_numpy()
    G.dataNet  = dataNet.to_numpy()
    G.dataNode = dataNode.to_numpy()

    G.nameNet = nameNet
    G.numEdge = len(dataNet)
    G.numNode = len(dataNode)
    G.numDmnd = len(dataOD)

    G.T = np.array(dataNet.free_flow_time).reshape(-1, 1)
    G.B = np.array(dataNet.b).reshape(-1, 1)
    G.P = np.array(dataNet.power).reshape(-1, 1)
    G.C = np.array(dataNet.capacity).reshape(-1, 1)

    G.a = np.multiply(G.T, G.B)
    G.c = G.T
    
    G.Q = np.diag(G.a.reshape(-1))
    G.q = G.c

    return G