import os
import sys
import numpy as np
from numpy.random import sample
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
from ComputeOptimalTolls import *
from ComputeFlow import *
from ComputeOptimalTollsApproximate import *
import matplotlib.pyplot as plt


verbose = False

pathCurrFolder = os.path.abspath(os.getcwd())
pathParFolder = os.path.abspath(os.path.join(pathCurrFolder, '..'))
pathDataFolder = os.path.join(pathParFolder, 'myRealData')
pathLogFolder = os.path.join(pathCurrFolder, 'Log')

currentTime = datetime.now()
currentTime = currentTime.strftime("%Y%m%d%H%M%S")

pathLogFile = os.path.join(pathLogFolder, (currentTime + "-Log.txt"))
pathSolFile = os.path.join(pathLogFolder, (currentTime + "-Sol.csv"))

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
nameNet4 = 'SiouxFallsSmall'
nameNet5 = 'Friedrichshain'
nameNet6 = 'Massachusetts'
nameNet7 = 'Pigou'

nameNet = nameNet3
numSmpl = 10000

G = ParseTNTP(pathDataFolder, nameNet)
G = ModifyODs(G, numODs=0, scaleFactor=1)

sampleODs = GenerateSamples(G.dataOD, numSmpl, type='uniform')
costsNash = []

for indSmpl in range(numSmpl):
    od = np.array([sampleODs[0, 0], sampleODs[0, 1], sampleODs[0, 2+indSmpl]]).reshape((1,-1))
    _, costNash, _, _, _, _ = ComputeFlow(G, od, toll=[11, 0, 0, 0, 11], type='Nash', verbose=verbose)
    costsNash.append(costNash)

print("Number of Social Costs Worse than 644: {}".format(str(np.sum(np.array(costsNash)>644))))

plt.hist(costsNash, edgecolor='black', linewidth=0.6)
plt.axvline(644, color="red", linestyle="dashed", alpha=0.4)
plt.xlabel('Social Cost')
plt.ylabel('Number of Samples')
plt.show()
