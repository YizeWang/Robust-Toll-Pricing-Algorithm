import sys
import numpy as np
from ParseTNTP import *
from GetEqualityConstraints import *
from GenerateSamples import *
from ComputeOptimalTolls1 import *
from ComputeOptimalTolls2 import *
from ComputeOptimalTolls4 import *
from ComputeOptimalTolls5 import *
from ComputeNashFlow import *
from ComputeOptimalFlow import *
from GetRowColDict import *
from ComputeSocialCost import *
from datetime import datetime
import winsound
import gurobipy as gp
from gurobipy import GRB
from scipy import sparse
import time
from ComputeNashFlowPoly import *


pathDataFolder = '..\\myRealData\\'
pathLogFolder = '.\\Log\\'

startTime = time.time()
currentTime = datetime.now()
currentTime = currentTime.strftime("%Y%m%d%H%M%S")

pathLogFile = pathLogFolder + currentTime + "-Log.txt"
pathSolFile = pathLogFolder + currentTime + "-Sol.csv"

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
nameNet4 = 'SiouxFallsSmall'

nameNet = nameNet2

with open(pathLogFile, 'wt') as logFile:
    
    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    G = TruncateODs(G, numODs=0, scaleFactor=1)
    sampleODs = G.dataOD

    m = gp.Model("Equilibrium-Calculator")

    minC = np.min(G.C)
    normC = minC / G.C

    PPlus = G.P + 1

    a = np.multiply(G.T, G.B)
    a = np.multiply(a, np.power(normC, G.P))
    a = a * minC
    a = np.divide(a, PPlus)
    c = G.T * minC

    M = G.numEdge
    N = G.numNode
    K = G.numDmnd

    xDim = M
    XDim = M + M * K
    bDim = M + N * K

    A, b = GetEqualityConstraints(G, sampleODs)

    sparseA = sparse.csc_matrix(A)
    sparseb = sparse.csc_matrix(b)
    rows, cols = sparseA.nonzero()
    setRows, dictCols = GetRowColDict(rows, cols)

    z = m.addVars(XDim, vtype=GRB.CONTINUOUS, lb=0, name='zAll')
    y = m.addVars(xDim, vtype=GRB.CONTINUOUS, lb=0, name='ySoc')
    
    m.addConstrs(gp.quicksum(A[row, col] * z[col] for col in dictCols[row]) == b[row]/minC for row in setRows)

    for i in range(xDim):
        m.addGenConstrPow(z[i], y[i], PPlus[i])

    m.setObjective(gp.quicksum(a[i]*y[i]+c[i]*z[i] for i in range(xDim)))

    # solve optimization
    m.optimize()

    # print results
    varNames = []
    varValues = []

    for var in m.getVars():
        varNames.append(str(var.varName))
        varValues.append(var.X*minC)

    with open(pathSolFile, 'wt') as solFile:
        wr = csv.writer(solFile, quoting=csv.QUOTE_ALL)
        wr.writerows(zip(varNames, varValues))
        solFile.close()

    xLink = varValues[:M]
    objVal = np.multiply(G.T, G.B)
    objVal = np.divide(objVal, PPlus)
    objVal = np.multiply(objVal, np.power(np.divide(xLink, G.C), G.P))
    objVal = np.multiply(objVal, xLink) + np.multiply(G.T, xLink)
    objVal = np.sum(objVal)
    print("Objective Value: %f" % objVal)

    logFile.close()

winsound.Beep(frequency=800, duration=2000)

pass