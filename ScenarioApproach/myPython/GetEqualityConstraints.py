import numpy as np
from scipy.sparse import csr_matrix
import gurobipy as gp
from gurobipy import GRB

def GetEqualityConstraints(G, ODs):
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    A = np.zeros((N, M), dtype=np.double)
    for idxLink, link in enumerate(G.dataNet):
        print(link[0])
        idxInit = int(link[0]) - 1 # index starts from 0
        idxTerm = int(link[1]) - 1 # index starts from 0
        A[idxInit][idxLink] = A[idxInit][idxLink] - 1
        A[idxTerm][idxLink] = A[idxTerm][idxLink] + 1

    A11 = np.eye(M, dtype=np.double) * -1
    A12 = np.matlib.repmat(np.eye(M, dtype=np.double), 1, K)
    A21 = np.zeros((N*K, M), dtype=np.double)
    A22 = np.kron(np.eye(K, dtype=np.double), A)

    A1   = np.concatenate((A11, A12), axis=1)
    A2   = np.concatenate((A21, A22), axis=1)
    ABig = np.concatenate((A1,  A2 ), axis=0)

    b = np.zeros((N, K), vtype=np.double)
    for k in range(K):
        idxInit = ODs[k][1]
        idxTerm = ODs[k][2]
        demand  = ODs[k][3]

        b[idxInit][k] = -demand
        b[idxTerm][k] =  demand
    
    bBigLow = b.reshape((N*K, 1))
    bBigUp = np.zeros((M, 1), vtype=np.double)
    bBig = np.concatenate((bBigUp, bBigLow), axis=0)

    return [ABig, bBig]