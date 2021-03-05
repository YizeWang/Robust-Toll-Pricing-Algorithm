import gurobipy as gp
from gurobipy import GRB
from GetEqualityConstraints import *
from scipy import sparse
from GetRowColDict import *
from ComputeSocialCost import *


def ComputeNashFlowPoly(G, ODs):

    # create a new model
    m = gp.Model("Nash Flow Calculator")
    m.Params.OutputFlag = 0

    # extract network dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    # regularize capacity
    C0 = np.min(G.C) # use min capacity as rescale factor
    normC = C0 / G.C # reciprocal of normalized capacity

    PPlus = G.P + 1

    a = np.multiply(G.T, G.B)
    a = np.multiply(a, np.power(normC, G.P))
    a = a * C0
    a = np.divide(a, PPlus)
    c = G.T * C0

    # compute decision variable dimensions
    xDim = M
    XDim = M + M * K

    A, b = GetEqualityConstraints(G, ODs)

    sparseA = sparse.csc_matrix(A)
    rows, cols = sparseA.nonzero()
    setRows, dictCols = GetRowColDict(rows, cols)

    x = m.addVars(XDim, vtype=GRB.CONTINUOUS, lb=0, name='x')
    y = m.addVars(xDim, vtype=GRB.CONTINUOUS, lb=0, name='y')

    m.addConstrs(gp.quicksum(A[row, col] * x[col] for col in dictCols[row]) == b[row]/C0 for row in setRows) # Ax == b

    for i in range(xDim):
        m.addGenConstrPow(x[i], y[i], PPlus[i]) # y = x ^ (P + 1)

    m.setObjective(gp.quicksum(a[i] * y[i] + c[i] * x[i] for i in range(xDim)))

    # solve optimization
    m.optimize()

    # print results
    varValues = []
    idxZero = []

    for idx, var in enumerate(m.getVars()):
        realFlow = var.X * C0
        varValues.append(realFlow)

        if idx >= M and realFlow < np.finfo(np.float64).eps: # keep track of indices of zero-valued elements
            idxZero.append(idx)

    xNash = varValues[:M]
    costNash = ComputeSocialCost(xNash, G)

    return xNash, costNash, idxZero, varValues