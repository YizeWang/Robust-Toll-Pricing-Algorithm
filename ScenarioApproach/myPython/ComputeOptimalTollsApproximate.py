import gurobipy as gp
from gurobipy import GRB
from GetEqualityConstraints import *
from scipy import sparse
from GetNonZeroDictionary import *
from ComputeSocialCost import *
from ComputeFlow import *


def ComputeOptimalTollsApproximate(G, sampleODs, pathSolFile, idxZero=None, idxNonZero=None, idxUsed=None):

    # create a new model
    m = gp.Model("Toll Calculator")
    m.Params.OutputFlag = 1

    # extract variable dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    # extract cost coefficients
    C0 = np.min(G.C)  # use min capacity as rescale factor
    normC = C0 / G.C  # reciprocal of normalized capacity

    # coefficients in objective function
    ao = C0 * np.multiply(np.multiply(G.B, G.T), np.power(normC, G.P))
    co = C0 * G.T

    # coefficients in KKT conditions
    ak = np.multiply(np.multiply(G.B, G.T), np.power(normC, G.P))
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
    AT = A.transpose()

    setRowsA, dictColsA = GetNonZeroDictionary(A)
    setRowsAT, dictColsAT = GetNonZeroDictionary(AT)

    h = m.addVars(hDim, vtype=GRB.CONTINUOUS,       name='h')
    t = m.addVars(tDim, vtype=GRB.CONTINUOUS, lb=0, name='t')
    z = m.addVars(zDim, vtype=GRB.CONTINUOUS,       name='z') # z = x / C0
    u = m.addVars(uDim, vtype=GRB.CONTINUOUS,       name='u')
    l = m.addVars(lDim, vtype=GRB.CONTINUOUS,       name='l')
    y = m.addVars(xDim, vtype=GRB.CONTINUOUS,       name='y') # y = z ^ (P + 1)
    w = m.addVars(xDim, vtype=GRB.CONTINUOUS,       name='w') # w = z ^ P

    for i in range(xDim):
        m.addGenConstrPow(z[i], y[i], G.P[i] + 1) # y = z ^ (P + 1)
        m.addGenConstrPow(z[i], w[i], G.P[i])     # w = z ^ P

    for row in setRowsA:
        rowA = A[row, :].toarray()[0]
        m.addConstr(gp.quicksum(rowA[col] * z[col] for col in dictColsA[row]) == b[row] / C0)  # C0 * A * z = b

    # stationarity
    m.addConstrs(ak[i] * w[i] + ck[i] + t[i] - u[i] + gp.quicksum(AT[i, j] * l[j] for j in dictColsAT[i]) == 0 for i in range(xDim))  # xLink
    m.addConstrs(                                     gp.quicksum(AT[i, j] * l[j] for j in dictColsAT[i]) == 0 for i in idxNonZero)   # u = 0
    m.addConstrs(                            - u[i] + gp.quicksum(AT[i, j] * l[j] for j in dictColsAT[i]) == 0 for i in idxZero)      # x = 0

    # primal feasibility
    m.addConstrs(z[i] >= 0 for i in idxUsed)
    m.addConstrs(z[i] >= 0 for i in idxNonZero)
    m.addConstrs(z[i] == 0 for i in idxZero)

    # dual feasibility
    m.addConstrs(u[i] == 0 for i in idxUsed)
    m.addConstrs(u[i] == 0 for i in idxNonZero)
    m.addConstrs(u[i] >= 0 for i in idxZero)

    # objective function
    m.setObjective(gp.quicksum(ao[i] * y[i] + co[i] * z[i] for i in range(xDim)))

    # solve optimization
    m.optimize()

    # print results
    varNames = []
    varValues = []

    for var in m.getVars():
        varNames.append(str(var.varName))
        varValues.append(var.X)

    hPos = range(0, hDim)
    tPos = range(np.max(hPos) + 1, np.max(hPos) + tDim + 1)
    zPos = range(np.max(tPos) + 1, np.max(tPos) + zDim + 1)
    uPos = range(np.max(zPos) + 1, np.max(zPos) + uDim + 1)
    lPos = range(np.max(uPos) + 1, np.max(uPos) + lDim + 1)
    yPos = range(np.max(lPos) + 1, np.max(lPos) + yDim + 1)
    wPos = range(np.max(yPos) + 1, np.max(yPos) + wDim + 1)

    hVal = [varValues[i] for i in hPos]
    tVal = [varValues[i] for i in tPos]
    zVal = [varValues[i] for i in zPos]
    uVal = [varValues[i] for i in uPos]
    lVal = [varValues[i] for i in lPos]
    yVal = [varValues[i] for i in yPos]
    wVal = [varValues[i] for i in wPos]
    xVal = np.array(zVal) * C0

    return tVal
