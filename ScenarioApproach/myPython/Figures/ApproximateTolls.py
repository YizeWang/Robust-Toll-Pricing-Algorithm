import os
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


xRange = np.linspace(0.1, 2.5, num=100, endpoint=True)

pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = os.path.join(os.path.join(pathCurrFolder, "Figures"), "DataApproximateTolls")

pathDataUE = os.path.join(pathDataFolder, 'nashCosts.csv')
pathDataSO = os.path.join(pathDataFolder, 'optCosts.csv')
pathDataToll = os.path.join(pathDataFolder, 'tollCosts.csv')

CostUE = np.genfromtxt(pathDataUE, delimiter=',')
CostSO = np.genfromtxt(pathDataSO, delimiter=',')
CostToll = np.genfromtxt(pathDataToll, delimiter=',')

PoAUE = np.divide(CostUE, CostSO)
PoAToll = np.divide(CostToll, CostSO)

plt.figure()
plt.plot(xRange, PoAUE, label='Without Tolls')
plt.plot(xRange, PoAToll, label='With Tolls')
plt.xlabel('Scale Factor')
plt.ylabel('Price of Anarchy')
plt.xlim([xRange[0], 2])
plt.legend()
plt.show()
