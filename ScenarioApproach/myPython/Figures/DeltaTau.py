import os
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = os.path.join(os.path.join(pathCurrFolder, "Figures"), "DataDeltaTau")

pathDataTau001 = os.path.join(os.path.join(pathDataFolder, 'DeltaTau0.01'), 'PoAs.csv')
pathDataTau005 = os.path.join(os.path.join(pathDataFolder, 'DeltaTau0.05'), 'PoAs.csv')
pathDataTau010 = os.path.join(os.path.join(pathDataFolder, 'DeltaTau0.10'), 'PoAs.csv')
pathDataTau050 = os.path.join(os.path.join(pathDataFolder, 'DeltaTau0.50'), 'PoAs.csv')
pathDataTau100 = os.path.join(os.path.join(pathDataFolder, 'DeltaTau1.00'), 'PoAs.csv')

it = np.arange(0, 51)
tau001 = np.genfromtxt(pathDataTau001, delimiter=',')
tau005 = np.genfromtxt(pathDataTau005, delimiter=',')
tau010 = np.genfromtxt(pathDataTau010, delimiter=',')
tau050 = np.genfromtxt(pathDataTau050, delimiter=',')
tau100 = np.genfromtxt(pathDataTau100, delimiter=',')

plt.plot(it, tau001, label=r'$\delta\tau=0.01$')
plt.plot(it, tau005, label=r'$\delta\tau=0.05$')
plt.plot(it, tau010, label=r'$\delta\tau=0.10$')
plt.plot(it, tau050, label=r'$\delta\tau=0.50$')
plt.plot(it, tau100, label=r'$\delta\tau=1.00$')

plt.xlabel('Number of Iteration')
plt.ylabel('Price of Anarchy')
plt.xlim([0, 50])
plt.ylim([1, 1.1])
plt.legend()
plt.show()
