import gurobipy as gp
from gurobipy import GRB
from GetEqualityConstraints import *
import csv


def ComputeNashFlow(G, ODs, pathSolFile, tolls=-1):

    # create a new model
    m = gp.Model("Nash Flow Calculator")

    # extract variable dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    # extract cost coefficients
    Q = G.Q
    q = G.q
    halfQ = 0.5 * Q

    # if tolls are imposed
    if tolls != -1:
        q = q + tolls

    # compute decision variable dimensions
    xDim = M + M * K

    # create decision variables
    x = m.addMVar(xDim, vtype=GRB.CONTINUOUS, lb=0, name='x')
    xLink = x[:M]

    # specify model
    m.setObjective(xLink @ halfQ @ xLink + q @ xLink, GRB.MINIMIZE)

    # add constraints
    [A, b] = GetEqualityConstraints(G, ODs)
    m.addConstr(A @ x == b.reshape(-1))

    # gurobi paramters
    m.Params.OutputFlag = 1

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
    