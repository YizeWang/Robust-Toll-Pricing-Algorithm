import os
import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
from ComputeOptimalTolls import *
from ComputeFlow import *
from ComputeOptimalTollsApproximate import *
import matplotlib.pyplot as plt


pathCurrFolder = os.path.abspath(os.getcwd())
pathParFolder = os.path.abspath(os.path.join(pathCurrFolder, '..'))
pathDataFolder = os.path.join(pathParFolder, 'myRealData')

nameNet = 'Brasse'

costsNash = []
costsNashToll = []
costsOpt = []
scaleFactors = np.linspace(0.01, 1.2, 120)
tolls = [30.0, 3.0, 3.0, 0.0, 30.0]

for scaleFactor in scaleFactors:
    G = ParseTNTP(pathDataFolder, nameNet)
    G = ModifyODs(G, numODs=0, scaleFactor=scaleFactor)
    xNash, costNashToll, _, _, _, _ = ComputeFlow(G, G.dataOD, tolls, type='Nash', verbose=False)
    xNash, costNash, _, _, _, _ = ComputeFlow(G, G.dataOD, type='Nash', verbose=False)
    xOpt, costOpt, _, _, _, _ = ComputeFlow(G, G.dataOD, type='Optimal', verbose=False)
    costsNash.append(costNash)
    costsNashToll.append(costNashToll)
    costsOpt.append(costOpt)

PoA = np.divide(costsNash, costsOpt)
PoAToll = np.divide(costsNashToll, costsOpt)

fig1 = plt.figure('Social Cost')
plt.xlabel('Scale Factor')
plt.ylabel('Social Cost')
plt.plot(scaleFactors, costsOpt, label='SO')
plt.plot(scaleFactors, costsNashToll, label='UE with Tolls')
plt.plot(scaleFactors, costsNash, label='UE without Tolls')
plt.xlim([0.0, 1.2])
plt.ylim([0.0, 700])

fig2 = plt.figure('Price of Anarchy')
plt.xlabel('Scale Factor')
plt.ylabel('Price of Anarchy')
plt.plot(scaleFactors, PoAToll, label='PoA with Tolls')
plt.plot(scaleFactors, PoA, label='PoA without Tolls')
plt.xlim([0.0, 1.2])
plt.ylim([1.0, 1.25])

plt.legend()
plt.show()
