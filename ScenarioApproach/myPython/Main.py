import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
import winsound
from ComputeOptimalTolls import *
from ComputeFlow import *
from ComputeOptimalTollsApproximate import *


verbose = True

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

nameNet = nameNet3             
numSmpl = 0

with open(pathLogFile, 'wt') as logFile:

    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    # G = ModifyODs(G, numODs=0, scaleFactor=0.853)
    G = ModifyODs(G, numODs=0, scaleFactor=1)

    sampleODs = G.dataOD
    # sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.05)
    
    xNash, costNash, idxZeroFlowNash, idxNonZeroFlowNash, idxUsedNash, flowNash = ComputeFlow(G, G.dataOD, type='Nash', verbose=verbose)
    print("Nash Flow Cost: %f" % costNash)
    print("xNash: ", xNash)

    # xOpt, costOpt, idxZeroFlowOpt, idxNonZeroFlowOpt, idxUsedOpt, flowOpt = ComputeFlow(G, G.dataOD, type='Optimal', verbose=False)
    # print("Optimal Flow Cost: %f" % costOpt)


    # tOpt1 = ComputeOptimalTollsApproximate(G, sampleODs, pathSolFile, idxZeroFlowNash, idxNonZeroFlowNash, idxUsedNash, verbose=verbose)
    # xToll1, costToll1, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt1, verbose=verbose)
    # print("costToll1: %f" % costToll1)
    # print("tOpt1: ", tOpt1)

    # tOpt2 = ComputeOptimalTollsApproximate(G, sampleODs, pathSolFile, idxZeroFlowOpt, idxNonZeroFlowOpt, idxUsedOpt, verbose=verbose)
    # xToll2, costToll2, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt2, verbose=verbose)
    # print("costToll2: %f" % costToll2)
    # print("tOpt2: ", tOpt2)

    # tOpt = ComputeOptimalTolls(G, sampleODs, pathSolFile, verbose=True)
    # xToll, costToll, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt, verbose=verbose)
    # print("costToll: %f" % costToll)
    # print("tOpt: ", tOpt)

    logFile.close()

winsound.Beep(frequency=800, duration=1000)

pass
