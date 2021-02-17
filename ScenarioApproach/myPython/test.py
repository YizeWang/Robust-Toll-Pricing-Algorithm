import numpy as np
import gurobipy as gp
from gurobipy import GRB
from ParseTNTP import *
from GetEqualityConstraints import *

pathDataFolder = '..\\myRealData\\'

nameNet1     = 'SimpleGeneralNetwork'
nameNet2     = 'SiouxFalls'
nameNet3     = 'Brasse'

nameNet = nameNet2

G = ParseTNTP(pathDataFolder, nameNet)
G = TruncateODs(G, numODs=0, scaleFactor=0.001)
[A, b] = GetEqualityConstraints(G, G.dataOD)

# # create a new model
# m = gp.Model("Toll-Calculator")

# # extract variable dimensions
# M = G.numEdge
# N = G.numNode
# K = G.numDmnd

# # extract cost coefficients
# Q = G.Q
# q = G.q
# T = G.T
# a = G.a

# # compute decision variable dimensions
# tDim = M
# hDim = 1
# xDim = M + M * K
# uDim = xDim
# lDim = M + N * K

# # create decision variables
# h = m.addVar(vtype=GRB.CONTINUOUS)
# t = m.addMVar(tDim, vtype=GRB.CONTINUOUS, lb=0)
# x = m.addMVar(xDim, vtype=GRB.CONTINUOUS, lb=0)
# u = m.addMVar(uDim, vtype=GRB.CONTINUOUS, lb=0)
# l = m.addMVar(lDim, vtype=GRB.CONTINUOUS)
# xLink = x[:M]

# # specify model
# m.setObjective(xLink@Q@xLink+q@xLink, GRB.MINIMIZE)
# m.addConstr(A@x == b.reshape(-1))

# m.optimize()

pass