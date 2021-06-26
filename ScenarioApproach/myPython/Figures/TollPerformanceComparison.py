import os
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


variation = 0.05
areAllTaxable = False

pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = join(join(pathCurrFolder, "Figures"), "DataTollPerformanceComparison")

if variation == 0.05:
    pathDataFolder = join(pathDataFolder, "Variation005")
elif variation == 0.20:
    pathDataFolder = join(pathDataFolder, "Variation020")
else:
    raise Exception("Invalid variation {}".format(str(variation)))

lb = 1.015
ub = 1.045

if variation == 0.05:
    divider1 = 1.037
    divider2 = 1.020
    ylim = [0, 2000]
elif variation == 0.20:
    divider1 = 1.034
    divider2 = 1.024
    ylim = [0, 600]

pathDataT1 = os.path.join(pathDataFolder, 'CostToll1.csv')
pathDataT2 = os.path.join(pathDataFolder, 'CostToll2.csv')
pathDataUE = os.path.join(pathDataFolder, 'CostUserEq.csv')
pathDataSO = os.path.join(pathDataFolder, 'CostSysOpt.csv')

CostToll1 = np.genfromtxt(pathDataT1, delimiter=',')
CostToll2 = np.genfromtxt(pathDataT2, delimiter=',')
CostUserEq = np.genfromtxt(pathDataUE, delimiter=',')
CostSysOpt = np.genfromtxt(pathDataSO, delimiter=',')

PoAToll1 = np.divide(CostToll1, CostSysOpt)
PoAToll2 = np.divide(CostToll2, CostSysOpt)
PoAUserEq= np.divide(CostUserEq, CostSysOpt)

PoAToll1 = np.delete(PoAToll1, PoAToll1<lb)
PoAToll2 = np.delete(PoAToll2, PoAToll2<lb)
PoAUserEq = np.delete(PoAUserEq, PoAUserEq<lb)

PoAToll1 = np.delete(PoAToll1, PoAToll1>ub)
PoAToll2 = np.delete(PoAToll2, PoAToll2>ub)
PoAUserEq = np.delete(PoAUserEq, PoAUserEq>ub)

print(np.sum(PoAToll1>divider1))
print(np.sum(PoAToll2>divider2))

plt.figure()

if not areAllTaxable and variation == 0.05:
    pathDataTH = os.path.join(pathDataFolder, 'CostTollH.csv')
    CostTollH = np.genfromtxt(pathDataTH, delimiter=',')
    PoAHalf = np.divide(CostTollH, CostSysOpt)
    PoAHalf = np.delete(PoAHalf, PoAHalf<lb)
    PoAHalf = np.delete(PoAHalf, PoAHalf>ub)
    dividerHalf = 1.03152
    print(np.sum(PoAHalf>dividerHalf))
    plt.hist(PoAHalf, bins=500, alpha=0.8, label="Toll (Half Tollable)", color='green', zorder=3)
    plt.axvline(dividerHalf, color="green", linestyle="dashed", alpha=0.5)

plt.hist(PoAToll1, bins=500, alpha=0.8, label="Toll1", color='m', zorder=1)
plt.hist(PoAToll2, bins=500, alpha=0.8, label="Toll2", color='orange', zorder=2)
plt.hist(PoAUserEq, bins=500, alpha=0.8, label="Toll-Free", color='tab:blue', zorder=0)
plt.axvline(divider1, color="m", linestyle="dashed", alpha=0.5)
plt.axvline(divider2, color="orange", linestyle="dashed", alpha=0.5)
plt.xlabel('Price of Anarchy')
plt.ylabel('Number of Samples')
plt.xlim([lb, ub])
plt.ylim(ylim)
plt.legend()
plt.show()
