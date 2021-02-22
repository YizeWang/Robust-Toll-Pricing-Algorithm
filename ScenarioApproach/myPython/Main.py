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

nameNet = nameNet3
numSmpl = 5

with open(pathLogFile, 'wt') as logFile:
    
    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    G = TruncateODs(G, numODs=0, scaleFactor=1)
    sampleODs = G.dataOD
    # sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.05)

    xNash, costNash = ComputeNashFlow(G, G.dataOD)
    print("Nash Flow Cost: %f" % costNash)

    xOpt, costOpt = ComputeOptimalFlow(G, G.dataOD)
    print("Optimal Flow Cost: %f" % costOpt)

    xMax = np.max(xNash)
    bigM = np.ceil(15 * xMax)
    print("big-M: %d" % bigM)

    # ComputeOptimalTolls1(G, G.dataOD, pathSolFile)
    # ComputeOptimalTolls2(G, G.dataOD, pathSolFile)
    # ComputeOptimalTolls4(G, G.dataOD, pathSolFile, bigM)
    # ComputeOptimalTolls5(G, G.dataOD, pathSolFile, bigM)

    logFile.close()

winsound.Beep(frequency=800, duration=2000)

pass