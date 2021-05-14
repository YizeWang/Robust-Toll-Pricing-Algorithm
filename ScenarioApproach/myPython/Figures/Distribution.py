import os
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = os.path.join(os.path.join(pathCurrFolder, "Figures"), "DataDistribution")

pathDataUniform = os.path.join(pathDataFolder, 'yUniform.csv')
pathDataGaussian = os.path.join(pathDataFolder, 'yGaussian.csv')
pathDataPoisson = os.path.join(pathDataFolder, 'yPoisson.csv')

x = np.arange(800, 1200+1, 1)
yUniform = np.genfromtxt(pathDataUniform, delimiter=',')
yGaussian = np.genfromtxt(pathDataGaussian, delimiter=',')
yPoisson= np.genfromtxt(pathDataPoisson, delimiter=',')

plt.plot(x, yUniform, label='Uniform')
plt.plot(x, yGaussian, label='Gaussian')
plt.plot(x, yPoisson, label='Poisson')
plt.axvline(1000, color="red", linestyle="dashed", alpha=0.4)

plt.xlabel('Demand')
plt.ylabel('Probability')
plt.xlim([800, 1200])
plt.ylim([0, 0.014])
plt.legend()
plt.show()
