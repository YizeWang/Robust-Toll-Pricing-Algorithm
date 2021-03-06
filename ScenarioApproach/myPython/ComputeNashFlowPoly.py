import gurobipy as gp
from gurobipy import GRB
from GetEqualityConstraints import *
from scipy import sparse
from GetRowColDict import *
from ComputeSocialCost import *


eps = np.finfo(np.float64).eps


def ComputeNashFlowPoly(G, ODs, toll=None, type='Nash'):

    # create a new model
    nameModel = type + 'Flow Calculator'
    m = gp.Model(nameModel)
    m.Params.OutputFlag = 0

    # extract network dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    # regularize capacity
    C0 = np.min(G.C)  # use min capacity as rescale factor
    normC = C0 / G.C  # reciprocal of normalized capacity

    PPlus = G.P + 1

    a = np.multiply(G.T, G.B)
    a = np.multiply(a, np.power(normC, G.P))
    a = a * C0
    a = np.divide(a, PPlus)
    c = G.T * C0 if toll == None else (G.T + toll) * C0

    # compute decision variable dimensions
    xDim = M
    XDim = M + M * K

    A, b = GetEqualityConstraints(G, ODs)

    sparseA = sparse.csc_matrix(A)
    rows, cols = sparseA.nonzero()
    setRows, dictCols = GetRowColDict(rows, cols)

    z = m.addVars(XDim, vtype=GRB.CONTINUOUS, lb=0, name='z')  # z = x / C0
    y = m.addVars(xDim, vtype=GRB.CONTINUOUS, lb=0,
                  name='y')  # y = z ^ (P + 1)

    m.addConstrs(gp.quicksum(A[row, col] * z[col]
                             for col in dictCols[row]) == b[row]/C0 for row in setRows)  # Ax == b

    for i in range(xDim):
        m.addGenConstrPow(z[i], y[i], PPlus[i])

    m.setObjective(gp.quicksum(a[i] * y[i] + c[i] * z[i] for i in range(xDim)))

    # solve optimization
    m.optimize()

    # print results
    varValues = []
    idxZero = []
    idxNonZero = []
    idxUsed = []

    for idx, var in enumerate(m.getVars()):
        x = var.X * C0  # x = z * C0
        varValues.append(x)

        if idx >= M and idx < XDim:
            idxZero.append(idx) if x < eps else idxNonZero.append(
                idx)  # keep track of indices of zero-valued elements

        if idx < M and x > eps:
            idxUsed.append(idx)

    xNash = varValues[:M]
    costNash = ComputeSocialCost(xNash, G)

    return xNash, costNash, idxZero, idxNonZero, idxUsed, varValues
