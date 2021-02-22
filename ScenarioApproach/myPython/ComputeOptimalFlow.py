import gurobipy as gp
from gurobipy import GRB
from GetEqualityConstraints import *


def ComputeOptimalFlow(G, ODs):

    # create a new model
    m = gp.Model("Optimal Flow Calculator")

    # extract variable dimensions
    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    # extract cost coefficients
    Q = G.Q
    q = G.q

    # compute decision variable dimensions
    xDim = M + M * K

    # create decision variables
    x = m.addMVar(xDim, vtype=GRB.CONTINUOUS, lb=0, name='x')
    xLink = x[:M]

    # specify model
    m.setObjective(xLink @ Q @ xLink + q @ xLink, GRB.MINIMIZE)

    # add constraints
    [A, b] = GetEqualityConstraints(G, ODs)
    m.addConstr(A @ x == b.reshape(-1))

    # gurobi paramters
    m.Params.OutputFlag = 0

    # solve optimization
    m.optimize()

    # print results
    varValues = []

    for var in m.getVars():
        varValues.append(var.X)
    
    xOpt = np.array(varValues)
    xLink = xOpt[:M]
    costOpt = xLink @ Q @ xLink + q @ xLink

    return xOpt, costOpt