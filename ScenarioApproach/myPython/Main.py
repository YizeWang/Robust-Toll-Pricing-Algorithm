import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
import winsound
from ComputeOptimalTolls import *
from ComputeFlow import *
from ComputeOptimalTollsApproximate import *


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
nameNet5 = 'Friedrichshain'
nameNet6 = 'Massachusetts'

nameNet = nameNet2
numSmpl = 0

with open(pathLogFile, 'wt') as logFile:

    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    G = ModifyODs(G, numODs=0, scaleFactor=1.2)

    sampleODs = G.dataOD
    # sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.05)

    xNash, costNash, idxZeroFlowNash, idxNonZeroFlowNash, idxUsedNash, flowNash = ComputeFlow(G, G.dataOD, type='Nash')
    print("Nash Flow Cost: %f" % costNash)

    xOpt, costOpt, idxZeroFlowOpt, idxNonZeroFlowOpt, idxUsedOpt, flowOpt = ComputeFlow(G, G.dataOD, type='Optimal')
    print("Optimal Flow Cost: %f" % costOpt)

    tOpt1 = ComputeOptimalTollsApproximate(G, sampleODs, pathSolFile, idxZeroFlowNash, idxNonZeroFlowNash, idxUsedNash)
    xToll1, costToll1, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt1, type='Nash')

    tOpt2 = ComputeOptimalTollsApproximate(G, sampleODs, pathSolFile, idxZeroFlowOpt, idxNonZeroFlowOpt, idxUsedOpt)
    xToll2, costToll2, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt2, type='Nash')

    print("costNash: %f, costOpt: %f, costToll1: %f, costToll2: %f" % (costNash, costOpt, costToll1, costToll2))
    print("tOpt1: ", tOpt1, " tOpt2: ", tOpt2)

    logFile.close()

winsound.Beep(frequency=800, duration=1000)

pass
