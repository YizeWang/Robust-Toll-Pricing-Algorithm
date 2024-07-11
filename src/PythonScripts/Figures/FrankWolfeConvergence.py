import os
from os import path
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = os.path.join(os.path.join(pathCurrFolder, "Figures"), "DataFrankWolfe")

pathDataFW = os.path.join(pathDataFolder, "RelativeGapFW.csv")
pathDataCFW = os.path.join(pathDataFolder, "RelativeGapCFW.csv")
pathDataBFW = os.path.join(pathDataFolder, "RelativeGapBFW.csv")

RGapFW = np.genfromtxt(pathDataFW)
RGapCFW = np.genfromtxt(pathDataCFW)
RGapBFW = np.genfromtxt(pathDataBFW)

plt.plot(range(1, 60), RGapFW[:60-1], label='Vanilla Frank-Wolfe')
plt.plot(range(1, 60), RGapCFW[:60-1], label='Conjugate Frank-Wolfe')
plt.plot(range(1, 60), RGapBFW[:60-1], label='Biconjugate Frank-Wolfe')
plt.xlim([0, 60])
plt.ylim([0, 1])
plt.xlabel('Number of Iterations')
plt.ylabel('Relative Gap between Iterations')
plt.legend()
plt.show()

plt.plot(range(60, 120), RGapFW[60:120], label='Vanilla Frank-Wolfe')
plt.plot(range(60, 120), RGapCFW[60:120], label='Conjugate Frank-Wolfe')
plt.plot(range(60, 120), RGapBFW[60:120], label='Biconjugate Frank-Wolfe')
plt.xlim([60, 120])
plt.ylim([0, 0.01])
plt.xlabel('Number of Iterations')
plt.ylabel('Relative Gap between Iterations')
plt.legend()
plt.show()
