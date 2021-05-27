import os
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


lb = 1.015
ub = 1.0425

pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = os.path.join(os.path.join(pathCurrFolder, "Figures"), "DataTollPerformanceComparison")

pathDataT0 = os.path.join(pathDataFolder, 'CostMCT.csv')
pathDataT1 = os.path.join(pathDataFolder, 'CostToll1.csv')
pathDataT2 = os.path.join(pathDataFolder, 'CostToll2.csv')
pathDataUE = os.path.join(pathDataFolder, 'CostUserEq.csv')
pathDataSO = os.path.join(pathDataFolder, 'CostSysOpt.csv')

indEdge = np.arange(1, 76+1)
CostMCT = np.genfromtxt(pathDataT0, delimiter=',')
CostToll1 = np.genfromtxt(pathDataT1, delimiter=',')
CostToll2 = np.genfromtxt(pathDataT2, delimiter=',')
CostUserEq = np.genfromtxt(pathDataUE, delimiter=',')
CostSysOpt = np.genfromtxt(pathDataSO, delimiter=',')

PoAMCT = np.divide(CostMCT, CostSysOpt)
PoAToll1 = np.divide(CostToll1, CostSysOpt)
PoAToll2 = np.divide(CostToll2, CostSysOpt)
PoAUserEq= np.divide(CostUserEq, CostSysOpt)

PoAToll1 = np.delete(PoAToll1, PoAToll1<lb)
PoAToll2 = np.delete(PoAToll2, PoAToll2<lb)
PoAUserEq = np.delete(PoAUserEq, PoAUserEq<lb)

PoAToll1 = np.delete(PoAToll1, PoAToll1>ub)
PoAToll2 = np.delete(PoAToll2, PoAToll2>ub)
PoAUserEq = np.delete(PoAUserEq, PoAUserEq>ub)

print(np.sum(PoAToll1>1.037))
print(np.sum(PoAToll2>1.020))

plt.figure()
plt.hist(PoAToll1, bins=500, alpha=0.8, label="Toll1", color='m')
plt.hist(PoAToll2, bins=500, alpha=0.8, label="Toll2", color='orange')
plt.hist(PoAUserEq, bins=500, alpha=0.8, label="Toll-Free", color='tab:blue')
plt.axvline(1.037, color="m", linestyle="dashed", alpha=0.5)
plt.axvline(1.020, color="orange", linestyle="dashed", alpha=0.5)
plt.xlabel('Price of Anarchy')
plt.ylabel('Number of Samples')
plt.xlim([lb, ub])
plt.legend(loc='upper center')
plt.show()
