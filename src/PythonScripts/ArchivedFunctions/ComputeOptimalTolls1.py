import numpy as np
import gurobipy as gp
from gurobipy import GRB
from ParseTNTP import *
from GetEqualityConstraints import *
import csv


def ComputeOptimalTolls1(G, sampleODs, pathSolFile):

    # create a new model
    m = gp.Model("Toll-Calculator")

    # extract variable dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd
    S = sampleODs.shape[1] - 2

    # extract cost coefficients
    Q = G.Q
    q = G.q
    T = G.T
    a = G.a

    # compute decision variable dimensions
    hDim = 1
    tDim = M
    xDim = M + M * K
    uDim = xDim
    lDim = M + N * K

    # create decision variables
    h = m.addMVar(hDim,      vtype=GRB.CONTINUOUS,       name='h')
    t = m.addMVar(tDim,      vtype=GRB.CONTINUOUS, lb=0, name='tau')
    x = m.addMVar((xDim, S), vtype=GRB.CONTINUOUS, lb=0, name='x')
    u = m.addMVar((uDim, S), vtype=GRB.CONTINUOUS, lb=0, name='mu')
    l = m.addMVar((lDim, S), vtype=GRB.CONTINUOUS,       name='lambda')

    # specify model
    m.setObjective(h, GRB.MINIMIZE)

    # add constraints sample by sample
    for s in range(S):
        xs = x[:, s]
        us = u[:, s]
        ls = l[:, s]
        xLink = xs[:M]

        ODs = np.concatenate((sampleODs[:, 0:2], sampleODs[:, 2+s:2+s+1]), axis=1)
        [A, bs] = GetEqualityConstraints(G, ODs)

        m.addConstr(A @ xs == bs.reshape(-1))
        m.addConstr(xLink @ Q @ xLink + q @ xLink <= h)
        m.addConstr(us @ xs == 0)
        m.addConstrs(T[i] + t[i] + a[i] * xs[i] - us[i] + (np.transpose(A)[i]) @ ls == 0 for i in range(0, M   ))
        m.addConstrs(                           - us[i] + (np.transpose(A)[i]) @ ls == 0 for i in range(M, xDim))

    # gurobi paramters
    m.Params.NonConvex = 2
    m.Params.OutputFlag = 1
    m.Params.MIPGap = 1e-2
    m.Params.MIPFocus = 1

    # solve optimization
    m.optimize()

    # print results
    varNames = []
    varValues = []

    for var in m.getVars():
        varNames.append(str(var.varName))
        varValues.append(var.X)

    with open(pathSolFile, 'wt') as solFile:
        wr = csv.writer(solFile, quoting=csv.QUOTE_ALL)
        wr.writerows(zip(varNames, varValues))
        solFile.close()

    hOpt = varValues[0]
    tOpt = varValues[1:tDim+1]

    return hOpt, tOpt