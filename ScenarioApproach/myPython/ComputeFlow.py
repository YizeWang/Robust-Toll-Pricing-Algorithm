import gurobipy as gp
from gurobipy import GRB
from GetEqualityConstraints import *
from scipy import sparse
from GetNonZeroDictionary import *
from ComputeSocialCost import *


eps = np.finfo(np.float64).eps


def ComputeFlow(G, ODs, toll=None, type='Nash', verbose=False):

    # create a new model
    nameModel = type + ' Flow Calculator'
    m = gp.Model(nameModel)
    m.Params.OutputFlag = verbose
    m.Params.Presolve = 0
    m.Params.Aggregate = 0

    # extract network dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    # regularize capacity
    C0 = np.min(G.C)  # use min capacity as rescale factor
    regC = C0 / G.C   # reciprocal of regularized capacity

    PPlusOne = G.P + 1

    if type == 'Nash':
        a = np.divide(np.multiply(np.multiply(G.T, G.B), np.power(regC, G.P)), PPlusOne) * C0
        c = G.T * C0 if toll is None else (G.T + toll) * C0
    elif type == 'Optimal':
        a = np.multiply(np.multiply(G.T, G.B), np.power(regC, G.P)) * C0
        c = G.T * C0
    else:
        raise Exception("Invalid Type Input")

    # compute decision variable dimensions
    xDim = M
    XDim = M + M * K

    A, b = GetEqualityConstraints(G, ODs)
    setRows, dictCols = GetNonZeroDictionary(A)

    z = m.addVars(XDim, vtype=GRB.CONTINUOUS, lb=0, ub=10, name='z')  # z = x / C0
    y = m.addVars(xDim, vtype=GRB.CONTINUOUS, lb=0,       name='y')  # y = z ^ (P + 1)

    m.addConstrs(gp.quicksum(A[row, col] * z[col] for col in dictCols[row]) == b[row] / C0 for row in setRows)

    for i in range(xDim):
        m.addGenConstrPow(z[i], y[i], PPlusOne[i], options="FuncPieces=-2 FuncPieceError=1e-3")  # y = z ^ (P + 1)

    # obj = a * z ^ (P + 1) + c * z
    m.setObjective(gp.quicksum(a[i] * y[i] + c[i] * z[i] for i in range(xDim)))

    # solve optimization
    m.optimize()

    # if model was not solved to optimality
    if m.Status != 2:
        raise Exception("Fail to Solve the Model to Optimality, Error Code: %d" % m.Status)

    # print results
    flow = []            # flow values
    idxZeroFlow = []     # indicies of zero-flow links, range: [M, M+M*K]
    idxNonZeroFlow = []  # indicies of non-zero-flow links, range: [M, M+M*K]
    idxUsed = []         # indicies of used links, range: [0, M]

    for idx, var in enumerate(m.getVars()):
        x = var.X * C0 if idx < XDim else var.X * (C0 ** (G.P[idx-XDim] + 1))  # x = z * C0
        flow.append(x)

        if idx >= M and idx < XDim:
            idxZeroFlow.append(idx) if x < eps else idxNonZeroFlow.append(idx)  # keep track of indices of zero-valued elements
            continue

        if idx < M and x > eps:
            idxUsed.append(idx)

    xLink = flow[:M]
    cost = ComputeSocialCost(xLink, G)

    return xLink, cost, idxZeroFlow, idxNonZeroFlow, idxUsed, flow
