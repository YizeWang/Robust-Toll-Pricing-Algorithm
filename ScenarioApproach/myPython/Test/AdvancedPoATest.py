import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
import winsound
from ComputeOptimalTollsSparse import *
from ComputeFlowSparse import *


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

    resMat = np.array([[], [], [], [], []])
    # scaleFactors = np.logspace(-1, 0.7, num=10)
    scaleFactors = [1]

    for scaleFactor in scaleFactors:

        G = ParseTNTP(pathDataFolder, nameNet)
        G = ModifyODs(G, numODs=0, scaleFactor=scaleFactor)

        sampleODs = G.dataOD

        xNash, costNash, idxZeroNash, idxNonZeroNash, idxUsedNash, xFlowNash = ComputeFlowSparse(G, G.dataOD, type='Nash')

        xOpt, costOpt, idxZeroOpt, idxNonZeroOpt, idxUsedOpt, xFlowOpt = ComputeFlowSparse(G, G.dataOD, type='Optimal')

        tOpt1 = ComputeOptimalTollsSparse(G, G.dataOD, pathSolFile, baseType='Nash', idxZero=idxZeroNash, idxNonZero=idxNonZeroNash, idxUsed=idxUsedNash)
        xToll1, costToll1, _, _, _, _ = ComputeFlowSparse(G, sampleODs, tOpt1, type='Nash')

        tOpt2 = ComputeOptimalTollsSparse(G, G.dataOD, pathSolFile, baseType='Optimal', idxZero=idxZeroOpt, idxNonZero=idxNonZeroOpt, idxUsed=idxUsedOpt)
        xToll2, costToll2, _, _, _, _ = ComputeFlowSparse(G, sampleODs, tOpt2, type='Nash')

        print("Scale Factor: %f" % scaleFactor)
        print("Nash Flow Cost: %f" % costNash)
        print("Optimal Flow Cost: %f" % costOpt)
        print("Toll Flow 1 Cost: %f" % costToll1)
        print("Toll Flow 2 Cost: %f" % costToll2)

        newCol = np.array([[scaleFactor], [costNash], [costOpt], [costToll1], [costToll2]])
        resMat = np.hstack((resMat, newCol))

    logFile.close()

np.savetxt("TempData\\resMat.csv", resMat, delimiter=",")

winsound.Beep(frequency=800, duration=1000)

pass