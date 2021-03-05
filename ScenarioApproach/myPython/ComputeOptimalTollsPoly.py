import numpy as np
import gurobipy as gp
from gurobipy import GRB
from ParseTNTP import *
from GetEqualityConstraints import *
import csv
from scipy import sparse
from GetRowColDict import *
from ComputeSocialCost import *


def ComputeOptimalTollsPoly(G, sampleODs, pathSolFile):

    # create a new model
    m = gp.Model("Toll-Calculator")

    # extract variable dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    # extract cost coefficients
    minC = np.min(G.C)
    normC = minC / G.C

    PPlus = G.P + 1

    # coefficients in objective function
    ao = np.multiply(G.T, G.B) * minC
    ao = np.multiply(ao, np.power(normC, G.P))
    co = G.T * minC

    # coefficients in KKT conditions
    ak = np.multiply(G.T, G.B)
    ak = np.multiply(ak, np.power(normC, G.P))
    ck = G.T

    # compute decision variable dimensions
    tDim = M
    hDim = 1
    xDim = M
    XDim = M + M * K
    uDim = XDim
    lDim = M + N * K

    A, b = GetEqualityConstraints(G, sampleODs)
    AT = np.transpose(A)

    sparseA = sparse.csc_matrix(A)
    rows, cols = sparseA.nonzero()
    setRows, dictCols = GetRowColDict(rows, cols)

    h = m.addVars(hDim, vtype=GRB.CONTINUOUS, lb=0, name='h')
    t = m.addVars(tDim, vtype=GRB.CONTINUOUS, lb=0, name='t')
    z = m.addVars(XDim, vtype=GRB.CONTINUOUS, lb=0, name='z')
    u = m.addVars(uDim, vtype=GRB.CONTINUOUS, lb=0, name='u')
    l = m.addVars(lDim, vtype=GRB.CONTINUOUS,       name='l')
    y = m.addVars(xDim, vtype=GRB.CONTINUOUS,       name='y')

    m.addConstrs(gp.quicksum(A[row, col] * z[col] for col in dictCols[row]) == b[row]/minC for row in setRows)

    for i in range(xDim):
        m.addGenConstrPow(z[i], y[i], G.P[i])

    m.addConstrs(ak[i]*y[i]+ck[i]+t[i]-u[i]+gp.quicksum(AT[i, j] * l[j] for j in range(lDim)) == 0 for i in range(xDim))
    m.addConstrs(                     -u[i]+gp.quicksum(AT[i, j] * l[j] for j in range(lDim)) == 0 for i in range(xDim, XDim))
    m.addConstr(gp.quicksum(z[i]*u[i] for i in range(XDim)) == 0)

    m.setObjective(gp.quicksum(ao[i]*y[i]*z[i]+co[i]*z[i] for i in range(xDim)))

    # gurobi paramters
    m.Params.OutputFlag = 1
    # m.Params.MIPGap = 1e-2
    # m.Params.MIPFocus = 1
    m.Params.NonConvex = 2

    # solve optimization
    m.optimize()

    # print results
    varNames = []
    varValues = []

    for var in m.getVars():
        varNames.append(str(var.varName))
        varValues.append(var.X * minC)

    with open(pathSolFile, 'wt') as solFile:
        wr = csv.writer(solFile, quoting=csv.QUOTE_ALL)
        wr.writerows(zip(varNames, varValues))
        solFile.close()