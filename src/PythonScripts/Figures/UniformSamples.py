import os
import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
import matplotlib.pyplot as plt
from ParseTNTP import *


verbose = True

pathCurrFolder = os.path.abspath(os.getcwd())
pathParFolder = os.path.abspath(os.path.join(pathCurrFolder, '..'))
pathDataFolder = os.path.join(pathParFolder, 'myRealData')
pathLogFolder = os.path.join(pathCurrFolder, 'Log')

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
nameNet4 = 'SiouxFallsSmall'
nameNet5 = 'Friedrichshain'
nameNet6 = 'Massachusetts'
nameNet7 = 'Pigou'

nameNet = nameNet3
numSmpl = 365

G = ParseTNTP(pathDataFolder, nameNet)
sampleODs = GenerateSamples(G.dataOD, numSmpl, type='uniform')

plt.hist(sampleODs[0, 2:], edgecolor='black', linewidth=0.6)
plt.xlabel('Sampled Demand')
plt.ylabel('Number of Samples')
plt.show()
