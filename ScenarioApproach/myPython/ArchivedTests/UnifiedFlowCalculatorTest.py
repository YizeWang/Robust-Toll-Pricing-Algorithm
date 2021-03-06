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
from ComputeFlowPoly import *


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

nameNet = nameNet1
numSmpl = 5

with open(pathLogFile, 'wt') as logFile:
    
    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    G = TruncateODs(G, numODs=0, scaleFactor=1)
    # G = TruncateODs(G, numODs=0, scaleFactor=0.853)
    sampleODs = G.dataOD

    xNash1, costNash1, idxZeroNash1, _, _, _ = ComputeNashFlowPoly(G, G.dataOD)
    print("Nash Flow Cost: %f" % costNash1)

    xOpt1, costOpt1 = ComputeOptimalFlowPoly(G, G.dataOD)
    print("Optimal Flow Cost: %f" % costOpt1)

    xNash2, costNash2, idxZeroNash2, _, _, _ = ComputeFlowPoly(G, G.dataOD, type='Nash')
    print("Nash Flow Cost: %f" % costNash2)

    xOpt2, costOpt2, idxZeroOpt2, _, _, _ = ComputeFlowPoly(G, G.dataOD, type='Optimal')
    print("Optimal Flow Cost: %f" % costOpt2)  


    # tOpt = ComputeOptimalTollsPolyNew(G, G.dataOD, pathSolFile)
    # xToll, costToll, idxZeroToll, _, _, _ = ComputeNashFlowPoly(G, sampleODs, tOpt)

    # print("costNash: %f, costOpt: %f, costToll: %f" % (costNash, costOpt, costToll))
    # print("tOpt: ", tOpt)

    logFile.close()

winsound.Beep(frequency=800, duration=1000)

pass