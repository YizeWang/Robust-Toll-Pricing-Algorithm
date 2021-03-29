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
from ComputeGradient import *
from datetime import datetime
import winsound


pathDataFolder = '..\\myRealData\\'
pathLogFolder = '.\\Log\\'

currentTime = datetime.now()
currentTime = currentTime.strftime("%Y%m%d%H%M%S")

pathLogFile = pathLogFolder + currentTime + "-Log.txt"
pathSolFile = pathLogFolder + currentTime + "-Sol.csv"

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
nameNet4 = 'SiouxFallsSmall'

nameNet = nameNet4
numSmpl = 4

with open(pathLogFile, 'wt') as logFile:
    
    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    G = TruncateODs(G, numODs=3, scaleFactor=1)
    sampleODs = G.dataOD
    sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.15)

    Q = G.Q
    q = G.q
    [A, bMat] = GetEqualityConstraints(G, sampleODs)

    xOpt, costOpt = ComputeOptimalFlow(G, G.dataOD)
    print("Optimal Flow Cost: %f" % costOpt)

    xNash, costNash = ComputeNashFlow(G, G.dataOD)
    print("Nash Flow Cost: %f" % costNash)

    maxIteration = 1000
    currIteration = 1
    tolls = np.zeros(G.numEdge, dtype=np.double)
    H = -1

    while currIteration < maxIteration:

        currIteration = currIteration + 1
        grad = ComputeGradient(tolls, A, bMat, Q, q, deltaToll=0.01)
        gamma = 1 / currIteration
        tolls = tolls - grad * gamma
        tolls[tolls<0] = 0
        prevH = H + 0
        H = ComputeBigH(A, bMat, tolls, Q, q)
        if abs(prevH - H) < 0.01:
            break
        print("H: %s" % (H))
    
    H1 = H
    tOpt1 = tolls

    xMax = np.max(xNash)
    bigM = np.ceil(15 * xMax)
    print("big-M: %d" % bigM)
    H2, tOpt2 = ComputeOptimalTolls5(G, sampleODs, pathSolFile, bigM)

    logFile.close()

winsound.Beep(frequency=500, duration=1000)

pass