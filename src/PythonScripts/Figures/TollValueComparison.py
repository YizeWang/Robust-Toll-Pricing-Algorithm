import os
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = os.path.join(os.path.join(pathCurrFolder, "Figures"), "DataTollValueComparison")

pathDataT0 = os.path.join(pathDataFolder, 'MarginCostToll.csv')
pathDataT1 = os.path.join(pathDataFolder, 'Toll1.csv')
pathDataT2 = os.path.join(pathDataFolder, 'Toll2.csv')

indEdge = np.arange(1, 76+1)
T0 = np.genfromtxt(pathDataT0, delimiter=',')
T1 = np.genfromtxt(pathDataT1, delimiter=',')
T2 = np.genfromtxt(pathDataT2, delimiter=',')
print(np.max(T1))
print(np.max(T2))

plt.figure("Toll Value")
plt.plot(indEdge, T0, label='MCT', color='tab:green')
plt.plot(indEdge, T1, label='Toll1', color='m')
plt.plot(indEdge, T2, label='Toll2', color='orange')
plt.xlim([1, 76])
plt.xticks(np.hstack((np.hstack(([1], np.arange(10,76,10))), 76)))
plt.ylim([0, 60])
plt.yticks(np.arange(0, 60+1, 10))
plt.xlabel("Edge Index")
plt.ylabel("Toll Value")
plt.legend()
plt.show()
