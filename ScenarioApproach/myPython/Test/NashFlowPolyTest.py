import sys
import numpy as np
from ParseTNTP import *
from GetEqualityConstraints import *
from GenerateSamples import *
from ComputeNashFlowPoly import *
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

nameNet = nameNet2
numSmpl = 5

with open(pathLogFile, 'wt') as logFile:
    
    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    G = TruncateODs(G, numODs=0, scaleFactor=0.853)
    sampleODs = G.dataOD
    # sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.05)

    xNash, costNash, idxZeroNash, idxNonZeroNash, xAllNash = ComputeNashFlowPoly(G, G.dataOD)
    print("Nash Flow Cost: %f" % costNash)

    np.savetxt("TempData\\xNash.csv", xNash, delimiter=',')
    np.savetxt("TempData\\idxZeroNash.csv", idxZeroNash, delimiter=',', fmt='%u')
    np.savetxt("TempData\\xAllNash.csv", xAllNash, delimiter=',')

    logFile.close()

winsound.Beep(frequency=800, duration=2000)

pass