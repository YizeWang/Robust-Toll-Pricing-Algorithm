import os
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = join(join(pathCurrFolder, "Figures"), "DataMultiStart")
pathDataPoA1 = join(pathDataFolder, "PoAsOfMultiStartwithoutSearch.csv")
pathDataPoA2 = join(pathDataFolder, "PoAsOfMultiStartwithSearch.csv")

with open(pathDataPoA1, 'r') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    PoALists1 = list(reader)

with open(pathDataPoA2, 'r') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    PoALists2 = list(reader)

fig1, ax1 = plt.subplots()
for PoAList in PoALists1:
    ax1.plot(range(len(PoAList)), PoAList, linewidth=0.5)
plt.xlim([0, 30])
plt.ylim([1.02, 1.05])
plt.xlabel("Number of Iterations")
plt.ylabel("Price of Anarchy")

fig2, ax2 = plt.subplots()
for PoAList in PoALists2:
    ax2.plot(range(len(PoAList)), PoAList, linewidth=0.5)
plt.xlim([0, 30])
plt.ylim([1.02, 1.05])
plt.xlabel("Number of Iterations")
plt.ylabel("Price of Anarchy")

numCurve = 0
colors = ['r', 'b', 'g', 'orange']
fig3, ax3 = plt.subplots()
for i in range(len(PoALists1)):
    if PoALists1[i] == PoALists2[i]: continue
    if numCurve != 2:
        ax3.plot(range(len(PoALists1[i])), PoALists1[i], color=colors[numCurve], label='Init Toll {} with Step Search'.format(min(2, numCurve)))
        ax3.plot(range(len(PoALists2[i])), PoALists2[i], color=colors[numCurve], label='Init Toll {} without Step Search'.format(min(2, numCurve)), linestyle='dashed' )
    numCurve = numCurve + 1
    if numCurve > 3: break
plt.xlim([0, 30])
plt.ylim([1.02, 1.05])
plt.xlabel("Number of Iterations")
plt.ylabel("Price of Anarchy")
plt.legend(prop={'size': 8})
plt.show()
