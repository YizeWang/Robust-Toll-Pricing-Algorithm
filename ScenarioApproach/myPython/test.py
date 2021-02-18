import sys
import numpy as np
from ParseTNTP import *
from GetEqualityConstraints import *
from GenerateSamples import *
from ComputeOptimalTolls import *
from datetime import date, datetime


pathDataFolder = '..\\myRealData\\'
pathLogFolder = '.\\Log\\'

currentTime = datetime.now()
currentTime = currentTime.strftime("%Y%m%d%H%M%S")

pathLogFile = pathLogFolder+currentTime+'-Log.txt'

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'

nameNet = nameNet2
numSmpl = 2

with open(pathLogFile, 'w') as logFile:
    
    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    G = TruncateODs(G, numODs=100, scaleFactor=0.001)
    # sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.05)

    ComputeOptimalTolls(G, G.dataOD)

    logFile.close()

pass