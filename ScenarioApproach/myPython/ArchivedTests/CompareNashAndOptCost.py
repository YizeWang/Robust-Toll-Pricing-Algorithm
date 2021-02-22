from ComputeOptimalFlow import ComputeOptimalFlow
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

nameNet = nameNet2
numSmpl = 5

with open(pathLogFile, 'wt') as logFile:
    
    sys.stdout = logFile

    scaleFactorList = [1, 0.1, 0.01, 0.001]
    numODsList = range(1, 528, 10)

    costsOpt = np.zeros((len(scaleFactorList), len(numODsList)), dtype=np.double)
    costsNash = np.zeros((len(scaleFactorList), len(numODsList)), dtype=np.double)

    for scaleFactorIndex in range(len(scaleFactorList)):

        for numODsIndex in range(len(numODsList)):

            scaleFactor = scaleFactorList[scaleFactorIndex]
            numODs = numODsList[numODsIndex]

            G = ParseTNTP(pathDataFolder, nameNet)
            G = TruncateODs(G, numODs, scaleFactor)

            xNash, costNash = ComputeNashFlow(G, G.dataOD, pathSolFile)
            print("Nash Flow Cost: %f" % costNash)

            xOpt, costOpt = ComputeOptimalFlow(G, G.dataOD, pathSolFile)
            print("Optimal Flow Cost: %f" % costOpt)

            costsOpt[scaleFactorIndex, numODsIndex] = costOpt
            costsNash[scaleFactorIndex, numODsIndex] = costNash

    logFile.close()

    np.savetxt('costsOpt.csv', costsOpt, delimiter=',')
    np.savetxt('costsNash.csv', costsNash, delimiter=',')

winsound.Beep(frequency=800, duration=2000)

pass