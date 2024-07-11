import os
from os.path import join

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import numpy as np

variation = 0.05
areAllTaxable = False

pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = join(pathCurrFolder, os.pardir, "DataTollPerformanceComparison")

if variation == 0.05:
    pathDataFolder = join(pathDataFolder, "Variation005")
elif variation == 0.20:
    pathDataFolder = join(pathDataFolder, "Variation020")
else:
    raise Exception("Invalid variation {}".format(str(variation)))

lb = 1.015
ub = 1.045

divider1 = None
divider2 = None
ylim = [0, 2250]
if variation == 0.05:
    divider1 = 1.037
    divider2 = 1.020
elif variation == 0.20:
    divider1 = 1.034
    divider2 = 1.024

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
PoAUserEq = np.divide(CostUserEq, CostSysOpt)

PoAToll1 = np.delete(PoAToll1, PoAToll1 < lb)
PoAToll2 = np.delete(PoAToll2, PoAToll2 < lb)
PoAUserEq = np.delete(PoAUserEq, PoAUserEq < lb)

PoAToll1 = np.delete(PoAToll1, PoAToll1 > ub)
PoAToll2 = np.delete(PoAToll2, PoAToll2 > ub)
PoAUserEq = np.delete(PoAUserEq, PoAUserEq > ub)

print(np.sum(PoAToll1 > divider1))
print(np.sum(PoAToll2 > divider2))

plt.figure(figsize=(15, 11), dpi=80)

if variation == 0.05:
    plt.hist(PoAToll1, bins=500, alpha=0.8, label="Toll1", color='m', zorder=1)
    plt.hist(PoAToll2, bins=500, alpha=0.8, label="Toll2", color='orange', zorder=2)
    plt.hist(PoAUserEq, bins=500, alpha=0.8, label="Toll-Free", color='tab:blue', zorder=0)
    plt.axvline(divider1, color="m", linestyle="dashed", alpha=0.5, lw=5)
    plt.axvline(divider2, color="orange", linestyle="dashed", alpha=0.5, lw=5)
    if not areAllTaxable:
        pathDataTH = os.path.join(pathDataFolder, 'CostTollH.csv')
        CostTollH = np.genfromtxt(pathDataTH, delimiter=',')
        PoAHalf = np.divide(CostTollH, CostSysOpt)
        PoAHalf = np.delete(PoAHalf, PoAHalf < lb)
        PoAHalf = np.delete(PoAHalf, PoAHalf > ub)
        dividerHalf = 1.03152
        print(np.sum(PoAHalf > dividerHalf))
        plt.hist(PoAHalf, bins=500, alpha=0.8, label="Toll (Half Tollable)", color='tab:red', zorder=3)
        plt.axvline(dividerHalf, color="tab:red", linestyle="dashed", alpha=0.5, lw=5)

if variation == 0.20:
    plt.hist(PoAToll1, bins=500, alpha=0.8, label="Toll3", color='tab:green', zorder=1)
    plt.hist(PoAToll2, bins=500, alpha=0.8, label="Toll4", color='tab:brown', zorder=2)
    plt.hist(PoAUserEq, bins=500, alpha=0.8, label="Toll-Free", color='tab:blue', zorder=0)
    plt.axvline(divider1, color="tab:green", linestyle="dashed", alpha=0.5, lw=5)
    plt.axvline(divider2, color="tab:brown", linestyle="dashed", alpha=0.5, lw=5)

plt.xlabel('Price of Anarchy $\mathcal{P}$', fontsize=36)
plt.ylabel('Number of Scenarios $N$', fontsize=36)
plt.xlim([lb, ub])
plt.ylim(ylim)
plt.xticks(fontsize=32)
plt.yticks(fontsize=32)
legend_font = font_manager.FontProperties(size=32)
plt.legend(prop=legend_font, loc='upper right', framealpha=1)
plt.show()
