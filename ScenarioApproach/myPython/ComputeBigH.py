import numpy as np
import gurobipy as gp
from gurobipy import GRB


def ComputeBigH(A, bMat, tolls, Q, q):

    m = gp.Model("Big H Calculator")

    halfQ = 0.5 * Q
    qGen = q + tolls

    S = bMat.shape[1]
    M = q.shape[0]
    xDim = A.shape[1]

    x = m.addMVar(xDim, vtype=GRB.CONTINUOUS, name='x')
    xLink = x[:M]

    m.setObjective(xLink @ halfQ @ xLink + qGen @ xLink, GRB.MINIMIZE)
    m.Params.OutputFlag = 0

    costsNash = []

    for s in range(S):

        b = bMat[:, 0]

        m.remove(m.getConstrs())

        m.addConstr(x >= 0)
        m.addConstr(A @ x == b.reshape(-1))

        m.optimize()

        xNash = []

        for var in m.getVars():
            xNash.append(var.X)

        xNash = np.array(xNash)
        xLink = xNash[:M]
        costNash = xLink @ Q @ xLink + q @ xLink

        costsNash.append(costNash)

    return np.max(costsNash)