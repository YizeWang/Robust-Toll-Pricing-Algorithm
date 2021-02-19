import numpy as np
from numpy import matlib


def GetEqualityConstraints(G, ODs):

    M = G.numEdge # number of edges
    N = G.numNode # number of nodes
    K = G.numDmnd # number of demands

    # compute net in-flow of each node
    A = np.zeros((N, M), dtype=np.double)
    for idxLink, link in enumerate(G.dataNet):
        idxInit = int(link[0]) - 1 # index starts from 0
        idxTerm = int(link[1]) - 1 # index starts from 0
        A[idxInit][idxLink] = A[idxInit][idxLink] - 1
        A[idxTerm][idxLink] = A[idxTerm][idxLink] + 1

    A11 = -np.eye(M, dtype=np.double)
    A12 = np.matlib.repmat(np.eye(M, dtype=np.double), 1, K)
    A21 = np.zeros((N*K, M), dtype=np.double)
    A22 = np.kron(np.eye(K, dtype=np.double), A) # arrange matrix A along diagonal

    A1   = np.concatenate((A11, A12), axis=1) #        | A11 | A12 |   | A1 |
    A2   = np.concatenate((A21, A22), axis=1) # ABig = |-----+-----| = |----|
    ABig = np.concatenate((A1,  A2 ), axis=0) #        | A21 | A22 |   | A2 |

    b = np.zeros((N, K), dtype=np.double)
    for k in range(K):
        idxInit = int(ODs[k][0]) - 1 # index starts from 0
        idxTerm = int(ODs[k][1]) - 1 # index starts from 0
        demand  = ODs[k][2]

        b[idxInit][k] = -demand # net out-flows equal demand
        b[idxTerm][k] =  demand # net in-flows equal demand
    
    bBigLow = np.reshape(b, (N*K, 1), order='F')        #        |    0    |
    bBigUp  = np.zeros((M, 1), dtype=np.double)         # bBig = |---------|
    bBig    = np.concatenate((bBigUp, bBigLow), axis=0) #        | bBigLow |

    return [ABig, bBig]