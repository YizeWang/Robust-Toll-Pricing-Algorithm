import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
import winsound
from ComputeOptimalTolls import *
from ComputeFlowSparse import *
from ComputeFlow import *
from GetSparseEqualityConstraints import *
import time


pathDataFolder = '..\\myRealData\\'
pathLogFolder = '.\\Log\\'

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
nameNet4 = 'SiouxFallsSmall'

nameNet = nameNet2
numSmpl = 0

G = ParseTNTP(pathDataFolder, nameNet)
sampleODs = G.dataOD

G = ParseTNTP(pathDataFolder, nameNet)

start = time.time()
xNash, costNash, _, _, _, _ = ComputeFlowSparse(G, G.dataOD, type='Nash')
print("Nash Flow Cost (Sparse): %f, Time: %f" % (costNash, time.time()-start))

start = time.time()
xNash, costNash, _, _, _, _ = ComputeFlow(G, G.dataOD, type='Nash')
print("Nash Flow Cost: %f, Time: %f" % (costNash, time.time()-start))

start = time.time()
xOpt, costOpt, _, _, _, _ = ComputeFlowSparse(G, G.dataOD, type='Optimal')
print("Optimal Flow Cost (Sparse): %f, Time: %f" % (costOpt, time.time()-start))

start = time.time()
xOpt, costOpt, _, _, _, _ = ComputeFlow(G, G.dataOD, type='Optimal')
print("Optimal Flow Cost: %f, Time: %f" % (costOpt, time.time()-start))

pass


