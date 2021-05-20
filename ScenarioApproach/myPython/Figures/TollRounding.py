import os
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = os.path.join(os.path.join(pathCurrFolder, "Figures"), "DataTollRounding")

pathDataRoundNo = os.path.join(os.path.join(pathDataFolder, 'Decimal-1'), 'PoAs.csv')
pathDataRound0 = os.path.join(os.path.join(pathDataFolder, 'Decimal0'), 'PoAs.csv')
pathDataRound1 = os.path.join(os.path.join(pathDataFolder, 'Decimal1'), 'PoAs.csv')
pathDataRound2 = os.path.join(os.path.join(pathDataFolder, 'Decimal2'), 'PoAs.csv')

it = np.arange(0, 51)
roundNo = np.genfromtxt(pathDataRoundNo, delimiter=',')
round0 = np.genfromtxt(pathDataRound0, delimiter=',')
round1 = np.genfromtxt(pathDataRound1, delimiter=',')
round2 = np.genfromtxt(pathDataRound2, delimiter=',')

plt.plot(it, roundNo, label='No Rounding')
plt.plot(it, round0, label='0 Decimal')
plt.plot(it, round1, label='1 Decimal')
plt.plot(it, round2, label='2 Decimal')

plt.xlabel('Number of Iteration')
plt.ylabel('Price of Anarchy')
plt.xlim([0, 50])
plt.ylim([1, 1.1])
plt.legend()
plt.show()
