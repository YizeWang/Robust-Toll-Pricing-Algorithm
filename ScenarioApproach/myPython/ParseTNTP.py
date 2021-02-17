import numpy as np
import pandas as pd


class Graph:
    
    pass


def ParseTNTP(pathDataFolder, nameNet):

    pathDataPre  = pathDataFolder + nameNet + '\\' + nameNet + '_'

    pathDataNode = pathDataPre + 'node' + '.tntp'
    pathDataNet  = pathDataPre +  'net' + '.tntp'
    pathDataOD   = pathDataPre +  'ODs' + '.tntp'

    G = Graph()

    dataOD   = pd.read_csv(pathDataOD,   sep='\t')
    dataNet  = pd.read_csv(pathDataNet,  sep='\t')
    dataNode = pd.read_csv(pathDataNode, sep='\t')

    G.dataOD   = dataOD.to_numpy(dtype=np.double)
    G.dataNet  = dataNet.to_numpy(dtype=np.double)
    G.dataNode = dataNode.to_numpy(dtype=np.double)

    G.nameNet = nameNet
    G.numEdge = len(dataNet)
    G.numNode = len(dataNode)
    G.numDmnd = len(dataOD)

    G.T = np.array(dataNet.free_flow_time, dtype=np.double)
    G.B = np.array(dataNet.b, dtype=np.double)
    G.P = np.array(dataNet.power, dtype=np.double)
    G.C = np.array(dataNet.capacity, dtype=np.double)

    G.a = np.multiply(G.T, G.B)
    G.c = G.T
    
    G.Q = np.diag(G.a)
    G.q = G.c

    return G


def TruncateODs(G, numODs=0, scaleFactor=1.0):

    if numODs != 0:
        G.dataOD = G.dataOD[:numODs] # truncate OD pairs
        G.numDmnd = numODs # update number of demands

    G.dataOD[:, 2] = G.dataOD[:, 2] * scaleFactor # scale demands

    return G