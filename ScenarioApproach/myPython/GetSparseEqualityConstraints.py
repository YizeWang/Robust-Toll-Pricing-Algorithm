import numpy as np
from scipy import sparse
from numpy import matlib


def GetSparseEqualityConstraints(G, sampleODs):

    # extract network dimensions
    M = G.numEdge               # number of edges
    N = G.numNode               # number of nodes
    K = G.numDmnd               # number of demands
    S = sampleODs.shape[1] - 2  # number of samples

    # compute net in-flow of each node
    A = sparse.csc_matrix((N, M), dtype=np.byte)
    for idxLink, link in enumerate(G.dataNet):
        idxInit = np.byte(link[0]) - 1  # index starts from 0
        idxTerm = np.byte(link[1]) - 1  # index starts from 0
        A[idxInit, idxLink] = A[idxInit, idxLink] - 1
        A[idxTerm, idxLink] = A[idxTerm, idxLink] + 1

    # construct ABig blocks
    A11 = -sparse.eye(M, dtype=np.byte)
    A12 = sparse.csc_matrix(np.matlib.repmat(np.eye(M, dtype=np.byte), 1, K))
    A21 = sparse.csc_matrix((N*K, M), dtype=np.byte)
    A22 = sparse.kron(sparse.eye(K, dtype=np.byte), A)  # arrange matrix A along diagonal

    # constract ABig
    A1   = sparse.hstack((A11, A12))  #        | A11 | A12 |   | A1 |
    A2   = sparse.hstack((A21, A22))  # ABig = |-----+-----| = |----|
    ABig = sparse.vstack((A1,  A2 ))  #        | A21 | A22 |   | A2 |

    # initialize empty bBig
    bBig = sparse.csc_matrix((M+N*K, 0), dtype=np.double)

    # construct bBig columns
    for s in range(S):

        b = sparse.csc_matrix((N, K), dtype=np.double)

        for k in range(K):
            idxInit = int(sampleODs[k][0]) - 1  # index starts from 0
            idxTerm = int(sampleODs[k][1]) - 1  # index starts from 0
            demand  = sampleODs[k][s+2]

            b[idxInit, k] = -demand  # net out-flows equal demand
            b[idxTerm, k] =  demand  # net in-flows equal demand
        
        bVecLow = b.reshape((N*K, 1), order='F')              #        |    0    |
        bVecUp  = sparse.csc_matrix((M, 1), dtype=np.double)  # bVec = |---------|
        bVec    = sparse.vstack((bVecUp, bVecLow))            #        | bVecLow |

        bBig = sparse.hstack((bBig, bVec))

    return sparse.csc_matrix(ABig), sparse.csc_matrix(bBig)