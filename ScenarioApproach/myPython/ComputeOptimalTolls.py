import gurobipy as gp
from gurobipy import GRB
from GetEqualityConstraints import *
from GetNonZeroDictionary import *
from ComputeSocialCost import *


def ComputeOptimalTolls(G, sampleODs, pathSolFile, verbose=False):

    # create a new model
    m = gp.Model("Toll Calculator")
    m.Params.OutputFlag = verbose
    m.Params.MIPFocus = 0
    m.Params.Heuristics = 0.2
    m.Params.MIPGap = 1e-2
    m.Params.NonConvex = 2

    # extract variable dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    # extract cost coefficients
    C0 = np.min(G.C)  # use min capacity as rescale factor
    regC = C0 / G.C   # reciprocal of regularized capacity

    # coefficients in objective function
    ao = C0 * np.multiply(np.multiply(G.B, G.T), np.power(regC, G.P))
    co = C0 * G.T

    # coefficients in KKT conditions
    ak = np.multiply(np.multiply(G.B, G.T), np.power(regC, G.P))
    ck = G.T

    # compute decision variable dimensions
    hDim = 1
    tDim = M
    xDim = M
    XDim = M + M * K
    uDim = XDim
    lDim = M + N * K
    yDim = xDim
    wDim = xDim
    zDim = XDim

    A, b = GetEqualityConstraints(G, sampleODs)
    AT = np.transpose(A)

    setRowsA, dictColsA = GetNonZeroDictionary(A)
    setRowsAT, dictColsAT = GetNonZeroDictionary(AT)

    h = m.addVars(hDim, vtype=GRB.CONTINUOUS, lb=0,       name='h')
    t = m.addVars(tDim, vtype=GRB.CONTINUOUS, lb=0,       name='t')
    z = m.addVars(zDim, vtype=GRB.CONTINUOUS, lb=0, ub=3, name='z')  # z = x / C0
    u = m.addVars(uDim, vtype=GRB.CONTINUOUS, lb=0,       name='u')
    l = m.addVars(lDim, vtype=GRB.CONTINUOUS,             name='l')
    y = m.addVars(xDim, vtype=GRB.CONTINUOUS, lb=0,       name='y')  # y = z ^ (P + 1)
    w = m.addVars(xDim, vtype=GRB.CONTINUOUS, lb=0,       name='w')  # w = z ^ P

    for i in range(xDim):
        m.addGenConstrPow(z[i], y[i], G.P[i] + 1, options="FuncPieces=-2 FuncPieceError=1e-3")  # y = z ^ (P + 1)
        m.addGenConstrPow(z[i], w[i], G.P[i], options="FuncPieces=-2 FuncPieceError=1e-3")      # w = z ^ P

    m.addConstrs(gp.quicksum(A[row, col] * z[col] for col in dictColsA[row]) == b[row] / C0 for row in setRowsA)  # C0 * A * z = b
    m.addConstrs(ak[i] * w[i] + ck[i] + t[i]        + gp.quicksum(AT[i, j] * l[j] for j in dictColsAT[i]) == 0 for i in range(xDim))
    m.addConstrs(                            - u[i] + gp.quicksum(AT[i, j] * l[j] for j in dictColsAT[i]) == 0 for i in range(xDim, XDim))
    m.addConstrs(z[i] * u[i] == 0 for i in range(xDim, XDim))

    # objective function
    m.setObjective(gp.quicksum(ao[i] * y[i] + co[i] * z[i] for i in range(xDim)))

     # solve optimization
    m.optimize()

    # if model was not solved to optimality
    if m.Status != 2:
        raise Exception("Fail to Solve the Model to Optimality, Error Code: %d" % m.Status)

    # retrieve results
    hVal = [h[i].X for i in range(hDim)]
    tVal = [t[i].X for i in range(tDim)]
    zVal = [z[i].X for i in range(zDim)]
    uVal = [u[i].X for i in range(uDim)]
    lVal = [l[i].X for i in range(lDim)]
    yVal = [y[i].X for i in range(yDim)]
    wVal = [w[i].X for i in range(wDim)]
    xVal = np.array(zVal) * C0

    if verbose:
        print("hVal: ", hVal)
        print("tVal: ", tVal)
        print("zVal: ", zVal)
        print("uVal: ", uVal)
        print("lVal: ", lVal)
        print("yVal: ", yVal)
        print("wVal: ", wVal)
        print("xVal: ", xVal)

    return tVal
