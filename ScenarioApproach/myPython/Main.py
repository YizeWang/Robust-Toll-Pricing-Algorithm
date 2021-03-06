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
from ComputeOptimalTollsPolyNew import *
from datetime import datetime
import winsound
from ComputeOptimalFlowPoly import *
from ComputeOptimalTollsPoly import *


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
    # G = TruncateODs(G, numODs=0, scaleFactor=1)
    sampleODs = G.dataOD
    # sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.05)

    xNash, costNash, idxZeroNash, _, _, _ = ComputeNashFlowPoly(G, G.dataOD)
    print("Nash Flow Cost: %f" % costNash)

    xOpt, costOpt = ComputeOptimalFlowPoly(G, G.dataOD)
    print("Optimal Flow Cost: %f" % costOpt)

    # xMax = np.max(xNash)
    # bigM = np.ceil(15 * xMax)
    # print("big-M: %d" % bigM)

    tOpt = ComputeOptimalTollsPolyNew(G, G.dataOD, pathSolFile)
    xToll, costToll, idxZeroToll, _, _, _ = ComputeNashFlowPoly(G, sampleODs, tOpt)

    print("costNash: %f, costOpt: %f, costToll: %f" % (costNash, costOpt, costToll))
    print("tOpt: ", tOpt)

    logFile.close()

winsound.Beep(frequency=800, duration=1000)

pass