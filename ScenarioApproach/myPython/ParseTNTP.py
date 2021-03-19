import os
import numpy as np
import pandas as pd


class Graph:
    
    pass


def ParseTNTP(pathDataFolder, nameNet):

    pathDataPre  = os.path.join(pathDataFolder, nameNet)

    pathDataNode = os.path.join(pathDataPre, nameNet + '_' + 'node' + '.tntp')
    pathDataNet  = os.path.join(pathDataPre, nameNet + '_' + 'net'  + '.tntp')
    pathDataOD   = os.path.join(pathDataPre, nameNet + '_' + 'ODs'  + '.tntp')

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
    G.B = np.array(dataNet.b,              dtype=np.double)
    G.P = np.array(dataNet.power,          dtype=np.double)
    G.C = np.array(dataNet.capacity,       dtype=np.double)

    return G


def ModifyODs(G, numODs=0, scaleFactor=1.0):

    if scaleFactor < 0.0:
        scaleFactor = 1.0
        print('Invalid Negative Scale Factor, Reset to 1')

    if numODs < 0 or numODs > G.numDmnd:
        print('Invalid Number of Demands, Reset to All Demands')
    elif numODs != 0:
        G.dataOD = G.dataOD[:numODs, :]  # truncate OD pairs
        G.numDmnd = numODs               # update number of demands

    G.dataOD[:, 2] = G.dataOD[:, 2] * scaleFactor  # scale demands
    print('Considering %d Demands with Scale Factor %f' % (G.numDmnd, scaleFactor))

    return G
