import sys
import numpy as np
from ParseTNTP import *
from GetEqualityConstraints import *
from GenerateSamples import *
from ComputeNashFlow import *
from ComputeOptimalFlow import *
from datetime import datetime
import winsound
from ComputeOptimalTollsPoly import *
from ComputeOptimalFlowPoly import *
from ComputeNashFlowPoly import *
from ComputeOptimalTollsPolyNew import *
from ComputeOptimalTolls1 import *


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

with open(pathLogFile, 'wt') as logFile:
    
    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    G = TruncateODs(G, numODs=0, scaleFactor=1)
    sampleODs = G.dataOD
    # sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.05)

    tVal = ComputeOptimalTollsPolyNew(G, sampleODs, pathSolFile)
    xNash, costNash, _, _, _, _ = ComputeNashFlowPoly(G, sampleODs)
    xOpt, costOpt = ComputeOptimalFlowPoly(G, sampleODs)
    xToll, costToll, _, _, _, _ = ComputeNashFlowPoly(G, sampleODs, tVal)
    _, toll2 = ComputeOptimalTollsPoly(G, sampleODs, pathSolFile)
    xToll2, costToll2, _, _, _, _ = ComputeNashFlowPoly(G, sampleODs, toll2)

    logFile.close()

winsound.Beep(frequency=800, duration=2000)

pass