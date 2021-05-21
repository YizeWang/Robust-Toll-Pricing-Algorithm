import os
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder1 = join(join(join(pathCurrFolder, "Figures"), "DataMultiStart", "WithStepSearch"))
pathDataFolder2 = join(join(join(pathCurrFolder, "Figures"), "DataMultiStart", "WithoutStepSearch"))
pathDataPoA1 = join(pathDataFolder1, "PoAsOfMultiStart.csv")
pathDataPoA2 = join(pathDataFolder2, "PoAsOfMultiStart.csv")

with open(pathDataPoA1, 'r') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    PoALists1 = list(reader)

with open(pathDataPoA2, 'r') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    PoALists2 = list(reader)

fig1, ax1 = plt.subplots()
for PoAList in PoALists1:
    ax1.plot(range(len(PoAList)), PoAList)
plt.xlim([0, 50])
plt.ylim([1.0, 1.1])
plt.xlabel("Number of Iterations")
plt.ylabel("Price of Anarchy")

fig2, ax2 = plt.subplots()
for PoAList in PoALists2:
    ax2.plot(range(len(PoAList)), PoAList)
plt.xlim([0, 50])
plt.ylim([1.0, 1.1])
plt.xlabel("Number of Iterations")
plt.ylabel("Price of Anarchy")

plt.show()
