import os
import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
from ComputeOptimalTolls import *
from ComputeFlow import *
from ComputeOptimalTollsApproximate import *


verbose = False

pathCurrFolder = os.path.abspath(os.getcwd())
pathParFolder = os.path.abspath(os.path.join(pathCurrFolder, '..'))
pathDataFolder = os.path.join(pathParFolder, 'myRealData')
pathLogFolder = os.path.join(pathCurrFolder, 'Log')

currentTime = datetime.now()
currentTime = currentTime.strftime("%Y%m%d%H%M%S")

pathLogFile = os.path.join(pathLogFolder, (currentTime + "-Log.txt"))
pathSolFile = os.path.join(pathLogFolder, (currentTime + "-Sol.csv"))

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
nameNet4 = 'SiouxFallsSmall'
nameNet5 = 'Friedrichshain'
nameNet6 = 'Massachusetts'
nameNet7 = 'Pigou'

nameNet = nameNet7
numSmpl = 0

with open(pathLogFile, 'wt') as logFile:

    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    G = ModifyODs(G, numODs=0, scaleFactor=1)

    sampleODs = G.dataOD
    
    xNash, costNash, idxZeroFlowNash, idxNonZeroFlowNash, idxUsedNash, flowNash = ComputeFlow(G, G.dataOD, type='Nash', verbose=verbose)
    print("Nash Flow Cost: %f" % costNash)

    xOpt, costOpt, idxZeroFlowOpt, idxNonZeroFlowOpt, idxUsedOpt, flowOpt = ComputeFlow(G, G.dataOD, type='Optimal', verbose=verbose)
    print("Optimal Flow Cost: %f" % costOpt)

    tOpt = ComputeOptimalTolls(G, sampleODs, pathSolFile, verbose=verbose)
    xToll, costToll, _, _, _, flowNash = ComputeFlow(G, sampleODs, tOpt, verbose=verbose)
    print("costToll: %f" % costToll)

    logFile.close()

os.system('shutdown -t 5')
