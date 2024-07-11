import os
import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
import gurobipy as gp
from gurobipy import GRB
from GetEqualityConstraints import *
from GetNonZeroDictionary import *
import matplotlib.pyplot as plt


verbose = True

pathCurrFolder = os.path.abspath(os.getcwd())
pathParFolder = os.path.abspath(os.path.join(pathCurrFolder, '..'))
pathDataFolder = os.path.join(pathParFolder, 'myRealData')
pathLogFolder = os.path.join(pathCurrFolder, 'Log')

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
nameNet4 = 'SiouxFallsSmall'
nameNet5 = 'Friedrichshain'
nameNet6 = 'Massachusetts'
nameNet7 = 'Pigou'

nameNet = nameNet3
numSmpl = 10

G = ParseTNTP(pathDataFolder, nameNet)
sampleODs = GenerateSamples(G.dataOD, numSmpl, type='uniform')
tUpperbound = np.full(G.numEdge, np.inf)

# create a new model
m = gp.Model("Robust Toll Calculator")
m.Params.OutputFlag = verbose
m.Params.NonConvex = 2
m.Params.Presolve = 2

# extract variable dimensions
M = G.numEdge
N = G.numNode
K = G.numDmnd

# # extract cost coefficients
C0 = np.max(G.C)
regC = C0 / G.C   # reciprocal of regularized capacity

# # coefficients in objective function
ao = C0 * np.multiply(np.multiply(G.B, G.T), np.power(regC, G.P))
co = C0 * G.T
co[co<1e-6] = 0

# # coefficients in KKT conditions
ak = np.multiply(np.multiply(G.B, G.T), np.power(regC, G.P))
ck = G.T
ck[ck<1e-6] = 0

# compute decision variable dimensions
xDim = M
XDim = M + M * K
lDim = M + N * K

t, h, z, y, w, u, l = {}, {}, {}, {}, {}, {}, {}

H = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="H")

for indEdge in range(xDim):
    t[indEdge] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="t({})".format(str(indEdge)))
    
for indSmpl in range(numSmpl):
    h[indSmpl] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="h({})".format(str(indSmpl)))
    for indX in range(XDim):
        z[indX, indSmpl] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=10, name="z({},{})".format(str(indX), str(indSmpl)))
        u[indX, indSmpl] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,        name="u({},{})".format(str(indX), str(indSmpl)))
    for indL in range(lDim):
        l[indL, indSmpl] = m.addVar(vtype=GRB.CONTINUOUS,              name="l({},{})".format(str(indL), str(indSmpl)))
    for indx in range(xDim):
        y[indx, indSmpl] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="y({},{})".format(str(indx), str(indSmpl)))
        w[indx, indSmpl] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="w({},{})".format(str(indx), str(indSmpl)))

A, b = GetEqualityConstraints(G, sampleODs)
AT = np.transpose(A)
setRowsA, dictColsA = GetNonZeroDictionary(A)
setRowsAT, dictColsAT = GetNonZeroDictionary(AT)

for indSmpl in range(numSmpl):
    m.addConstrs(gp.quicksum(A[row, col] * z[col, indSmpl] for col in dictColsA[row]) == b[row, indSmpl] / C0 for row in setRowsA)  # C0 * A * z = b
    m.addConstrs(ak[i] * w[i, indSmpl] + ck[i] + t[i]                 + gp.quicksum(AT[i, j] * l[j, indSmpl] for j in dictColsAT[i]) == 0 for i in range(xDim))
    m.addConstrs(                                     - u[i, indSmpl] + gp.quicksum(AT[i, j] * l[j, indSmpl] for j in dictColsAT[i]) == 0 for i in range(xDim, XDim))
    m.addConstrs(z[i, indSmpl] * u[i, indSmpl] == 0 for i in range(xDim, XDim))
    for indEdge in range(xDim):
        m.addGenConstrPow(z[indEdge, indSmpl], y[indEdge, indSmpl], G.P[indEdge]+1, options="FuncPieces=-2 FuncPieceError=1e-3")  # y = z ^ (P + 1)
        m.addGenConstrPow(z[indEdge, indSmpl], w[indEdge, indSmpl], G.P[indEdge],   options="FuncPieces=-2 FuncPieceError=1e-3")  # w = z ^ P

m.setObjective(H)
m.addConstrs(h[indSmpl] == (gp.quicksum(ao[i] * y[i, indSmpl] + co[i] * z[i, indSmpl] for i in range(xDim))) for indSmpl in range(numSmpl))
m.addConstr(H == gp.max_([h[indSmpl] for indSmpl in range(numSmpl)]))

m.optimize()

with open('Result.txt', 'w') as f:
    for v in m.getVars():
        f.write('%s = %g\n' % (v.varName, v.x))
