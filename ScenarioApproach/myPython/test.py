import os
import sys
import numpy as np
from numpy.core.fromnumeric import reshape
from numpy.lib.function_base import quantile
from numpy.ma.core import concatenate
import numpy.matlib
import pandas as pd
import networkx as nx
from scipy import sparse
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB
from ParseTNTP import ParseTNTP
from GetEqualityConstraints import GetEqualityConstraints


nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
pathDataFolder = '..\\myRealData\\'

nameNet = nameNet1

G = ParseTNTP(pathDataFolder, nameNet)
[A, b] = GetEqualityConstraints(G, G.dataOD)

# create a new model
m = gp.Model("Toll-Calculator")

# extract variable dimensions
M = G.numEdge
N = G.numNode
K = G.numDmnd

# compute decision variable dimensions
tDim = M
hDim = 1
xDim = M + M * K
uDim = xDim
lDim = M + N * K

# create decision variables
h = m.addMVar((hDim,), vtype=GRB.CONTINUOUS)
t = m.addMVar((tDim,), vtype=GRB.CONTINUOUS, lb=0)
x = m.addMVar((xDim,), vtype=GRB.CONTINUOUS, lb=0)
u = m.addMVar((uDim,), vtype=GRB.CONTINUOUS, lb=0)
l = m.addMVar((lDim,), vtype=GRB.CONTINUOUS)

m.setObjective(h, GRB.MINIMIZE)
m.addMConstr(A, x, '=', b)

Q = np.diag(np.concatenate((G.a.reshape(-1), [0])))
q = np.concatenate((G.q.reshape(-1), [0]))
v = np.hstack((x, h))


# m.addMQConstr(G.Q, G.q.reshape(-1), '<', 0.0, v, v, v)