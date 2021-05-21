import os
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = join(join(join(pathCurrFolder, "Figures"), "DataMultiStart", "WithStepSearch"))
pathDataPoA = join(pathDataFolder, "PoAsOfMultiStart.csv")

with open(pathDataPoA, 'r') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    PoALists = list(reader)

for PoAList in PoALists:
    plt.plot(range(len(PoAList)), PoAList)

plt.xlim([0, 50])
plt.ylim([1.0, 1.1])
plt.xlabel("Number of Iterations")
plt.ylabel("Price of Anarchy")
plt.show()
