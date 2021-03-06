import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
import winsound
from ComputeOptimalTolls import *
from ComputeFlow import *

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

nameNet = nameNet2
numSmpl = 0

with open(pathLogFile, 'wt') as logFile:
    
    sys.stdout = logFile

    resMat = np.array([[], [], [], [], []])
    scaleFactors = np.logspace(-1, 0.5, num=50)
    # scaleFactors = [3.5]

    for scaleFactor in scaleFactors:

        G = ParseTNTP(pathDataFolder, nameNet)
        G = TruncateODs(G, numODs=0, scaleFactor=scaleFactor)

        sampleODs = G.dataOD

        xNash, costNash, _, _, _, _ = ComputeFlow(G, G.dataOD, type='Nash')
        print("Nash Flow Cost: %f" % costNash)

        xOpt, costOpt, _, _, _, _ = ComputeFlow(G, G.dataOD, type='Optimal')
        print("Optimal Flow Cost: %f" % costOpt)

        tOpt1 = ComputeOptimalTolls(G, G.dataOD, pathSolFile, baseType='Nash')
        xToll1, costToll1, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt1, type='Nash')

        tOpt2 = ComputeOptimalTolls(G, G.dataOD, pathSolFile, baseType='Optimal')
        xToll2, costToll2, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt2, type='Nash')

        newCol = np.array([[scaleFactor], [costNash], [costOpt], [costToll1], [costToll2]])
        resMat = np.hstack((resMat, newCol))

    logFile.close()

np.savetxt("TempData\\resMat.csv", resMat, delimiter=",")

winsound.Beep(frequency=800, duration=1000)

pass