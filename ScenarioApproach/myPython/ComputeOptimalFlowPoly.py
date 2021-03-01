import gurobipy as gp
from gurobipy import GRB
from GetEqualityConstraints import *
from scipy import sparse
from GetRowColDict import *
from ComputeSocialCost import *


def ComputeOptimalFlowPoly(G, ODs):

    # create a new model
    m = gp.Model("Optimal Flow Calculator")
    m.Params.OutputFlag = 0

    # extract variable dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    # regularize capacity
    minC = np.min(G.C)
    normC = minC / G.C

    PPlus = G.P + 1

    a = np.multiply(G.T, G.B)
    a = np.multiply(a, np.power(normC, G.P))
    a = a * minC
    c = G.T * minC

    # compute decision variable dimensions
    xDim = M
    XDim = M + M * K

    A, b = GetEqualityConstraints(G, ODs)

    sparseA = sparse.csc_matrix(A)
    rows, cols = sparseA.nonzero()
    setRows, dictCols = GetRowColDict(rows, cols)

    z = m.addVars(XDim, vtype=GRB.CONTINUOUS, lb=0, name='zAll')
    y = m.addVars(xDim, vtype=GRB.CONTINUOUS, lb=0, name='ySoc')

    m.addConstrs(gp.quicksum(A[row, col] * z[col] for col in dictCols[row]) == b[row]/minC for row in setRows)

    for i in range(xDim):
        m.addGenConstrPow(z[i], y[i], PPlus[i])

    m.setObjective(gp.quicksum(a[i]*y[i]+c[i]*z[i] for i in range(xDim)))

    # solve optimization
    m.optimize()

    # print results
    varValues = []

    for var in m.getVars():
        varValues.append(var.X*minC)
    
    xOpt = varValues[:M]
    costOpt = ComputeSocialCost(xOpt, G)

    return xOpt, costOpt