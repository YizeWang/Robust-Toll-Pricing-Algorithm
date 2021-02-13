import numpy as np
from scipy.sparse import csr_matrix
import gurobipy as gp
from gurobipy import GRB

def GetEqualityConstraints(G, ODs):
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    A = csr_matrix(N, M)
    b = csr_matrix(N, K)