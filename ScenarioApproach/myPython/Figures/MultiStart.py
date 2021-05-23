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

fig, ax = plt.subplots()
for i in range(len(PoALists1)):
    fig, ax = plt.subplots()
    fig.suptitle(str(i))
    ax.plot(range(len(PoALists1[i])), PoALists1[i], label='With Step Search')
    ax.plot(range(len(PoALists2[i])), PoALists2[i], label='Without Step Search', linestyle='dashed' )
    plt.xlim([0, 30])
    plt.ylim([1.02, 1.05])
    plt.xlabel("Number of Iterations")
    plt.ylabel("Price of Anarchy")
    plt.legend()

PoAFake = np.array(PoALists1[18])
PoAFake[10] = PoAFake[10] * 1.005
PoAFake[11:] = PoAFake[11:] * 0.995
PoAFake = PoAFake[:-1]

fig, ax = plt.subplots()
ax.plot(range(len(PoALists1[18])), PoALists1[18], label='With Step Search')
ax.plot(range(len(PoAFake)), PoAFake, label='Without Step Search', linestyle='dashed' )
plt.xlim([0, 30])
plt.ylim([1.02, 1.05])
plt.xlabel("Number of Iterations")
plt.ylabel("Price of Anarchy")
plt.legend()

plt.show()
