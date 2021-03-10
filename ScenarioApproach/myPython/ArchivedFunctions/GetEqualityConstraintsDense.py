import numpy as np
from numpy import matlib


def GetEqualityConstraints(G, sampleODs):

    # extract dimensions
    M = G.numEdge              # number of edges
    N = G.numNode              # number of nodes
    K = G.numDmnd              # number of demands
    S = sampleODs.shape[1] - 2 # number of samples

    # compute net in-flow of each node
    A = np.zeros((N, M), dtype=np.byte)
    for idxLink, link in enumerate(G.dataNet):
        idxInit = int(link[0]) - 1 # index starts from 0
        idxTerm = int(link[1]) - 1 # index starts from 0
        A[idxInit][idxLink] = A[idxInit][idxLink] - 1
        A[idxTerm][idxLink] = A[idxTerm][idxLink] + 1

    A11 = -np.eye(M, dtype=np.byte)
    A12 = np.matlib.repmat(np.eye(M, dtype=np.byte), 1, K)
    A21 = np.zeros((N*K, M), dtype=np.byte)
    A22 = np.kron(np.eye(K, dtype=np.byte), A) # arrange matrix A along diagonal

    A1   = np.concatenate((A11, A12), axis=1) #        | A11 | A12 |   | A1 |
    A2   = np.concatenate((A21, A22), axis=1) # ABig = |-----+-----| = |----|
    ABig = np.concatenate((A1,  A2 ), axis=0) #        | A21 | A22 |   | A2 |

    # initialize empty bBig
    bBig = np.zeros((M+N*K, S), dtype=np.double)

    # construct bBig columns
    for s in range(S):

        b = np.zeros((N, K), dtype=np.double)

        for k in range(K):
            idxInit = int(sampleODs[k][0]) - 1 # index starts from 0
            idxTerm = int(sampleODs[k][1]) - 1 # index starts from 0
            demand  = sampleODs[k][s+2]

            b[idxInit][k] = -demand # net out-flows equal demand
            b[idxTerm][k] =  demand # net in-flows equal demand
        
        bVecLow = np.reshape(b, (N*K, 1), order='F')        #        |    0    |
        bVecUp  = np.zeros((M, 1), dtype=np.double)         # bVec = |---------|
        bVec    = np.concatenate((bVecUp, bVecLow), axis=0) #        | bVecLow |

        bBig[:, s:s+1] = bVec

    return [ABig, bBig]