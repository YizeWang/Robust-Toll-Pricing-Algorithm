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
from ComputeNashFlowPoly import *
from ComputeOptimalFlowPoly import *
from datetime import datetime
import winsound
from ComputePoA import *


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

    sfs = np.logspace(-1, 0.5, num=30)
    PoAs = []

    for sf in sfs:

        G = ParseTNTP(pathDataFolder, nameNet)
        G = TruncateODs(G, numODs=0, scaleFactor=sf)
        sampleODs = G.dataOD

        PoA = ComputePoA(G, sampleODs)
        PoAs.append(PoA)

    np.savetxt("scaleFactors.csv", sfs, delimiter=",")
    np.savetxt("PoAs.csv", PoAs, delimiter=",")

    logFile.close()

winsound.Beep(frequency=800, duration=2000)

pass