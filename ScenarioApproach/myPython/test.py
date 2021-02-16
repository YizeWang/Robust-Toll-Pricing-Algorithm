import os
import sys
import numpy as np
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
h = m.addVar(hDim, 1, vtype=GRB.CONTINUOUS)
t = m.addVars(xDim, 1, lb=0, vtype=GRB.CONTINUOUS)
x = m.addVars(xDim, 1, lb=0, vtype=GRB.CONTINUOUS)
u = m.addVars(uDim, 1, lb=0, vtype=GRB.CONTINUOUS)
l = m.addVars(lDim, 1, vtype=GRB.CONTINUOUS)

m.setObjective(h, GRB.MINIMIZE)




pass