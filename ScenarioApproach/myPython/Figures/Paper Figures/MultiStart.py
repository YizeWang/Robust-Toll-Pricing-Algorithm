import csv
import os
from os.path import join

import matplotlib.pyplot as plt
import numpy as np

pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = join(pathCurrFolder, os.pardir, "DataMultiStart")
pathDataPoA1 = join(pathDataFolder, "PoAsOfMultiStartwithoutSearch.csv")
pathDataPoA2 = join(pathDataFolder, "PoAsOfMultiStartwithSearch.csv")

with open(pathDataPoA1, 'r') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    PoALists1 = list(reader)

with open(pathDataPoA2, 'r') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    PoALists2 = list(reader)

fig1, ax1 = plt.subplots(figsize=(16, 12), dpi=80)
for PoAList in PoALists1:
    ax1.plot(range(len(PoAList)), PoAList, linewidth=2)
plt.xlim([0, 30])
plt.ylim([1.015, 1.05])
plt.xlabel("Number of Iterations", fontsize=36)
plt.ylabel("Price of Anarchy", fontsize=36)
plt.xticks(fontsize=32)
plt.yticks(fontsize=32)

fig2, ax2 = plt.subplots(figsize=(16, 12), dpi=80)
for PoAList in PoALists2:
    ax2.plot(range(len(PoAList)), PoAList, linewidth=2)
plt.xlim([0, 30])
plt.ylim([1.015, 1.05])
plt.xlabel("Number of Iterations", fontsize=36)
plt.ylabel("Price of Anarchy", fontsize=36)
plt.xticks(fontsize=32)
plt.yticks(fontsize=32)

plt.show()
