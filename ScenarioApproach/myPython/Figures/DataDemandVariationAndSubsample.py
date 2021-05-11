import os
from os import path
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = os.path.join(os.path.join(pathCurrFolder, "Figures"), "DataDemandVariationAndSubsample")

popt1List = np.zeros((0, 3))
popt2List = np.zeros((0, 3))
demandVariations = [0.01, 0.02, 0.05, 0.10, 0.20]

xlim = [1, 15]
ylim = [1.0, 1.06]
xRange = np.linspace(1, 15, 100)

for i, demandVariation in enumerate(demandVariations):
    pathCurrDataFolder = os.path.join(pathDataFolder, "DemandVariation{:.2f}".format(demandVariation))
    pathDataPoA = os.path.join(pathCurrDataFolder, "PoAsOfMultiStart.csv")
    pathDataSubsample = os.path.join(pathCurrDataFolder, "Subsample.txt")

    with open(pathDataSubsample, 'r') as f:
        txt = f.readlines()
        txt = [line.strip('{}\n') for line in txt]
        reader = csv.reader(txt, quoting=csv.QUOTE_NONNUMERIC)
        subsampleLists = list(reader)
        subsampleLists = [[int(indSubsample) for indSubsample in subsampleList] for subsampleList in subsampleLists]

    with open(pathDataPoA, 'r') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        PoALists = list(reader)

    lastPoAs = [PoAList[-1] for PoAList in PoALists]
    numSubsampleList = [len(subsampleList) for subsampleList in subsampleLists]
    

    def f1(x, a, b, c):
        return b/(np.array(x)+a)+c
    popt1, pcov1 = curve_fit(f1, numSubsampleList, lastPoAs)
    popt1List = np.vstack((popt1List, np.array(popt1)))

    def f2(x, a, b, c):
        return a*np.exp(-b*x)+c
    popt2, pcov2 = curve_fit(f2, numSubsampleList, lastPoAs)
    popt2List = np.vstack((popt2List, np.array(popt2)))

    plt.figure()
    plt.scatter(numSubsampleList, lastPoAs, s=4)
    plt.plot(xRange, f1(xRange, *popt1), label=r'$y_1=\frac{b}{x+a}+c$', color='r')
    plt.plot(xRange, f2(xRange, *popt2), label=r'$y_2=ae^{-bx}+c$', color='g')
    plt.title('Performance and Robustness (Variation: {}%)'.format(int(demandVariation*100)), fontweight="bold")
    plt.xlabel('Support Subsample Cardinality')
    plt.ylabel('Price of Anarchy')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.legend()

plt.figure()
for i in range(5): plt.plot(xRange, f1(xRange, *popt1List[i, :]), label='Demand Variation: {}%'.format(int(demandVariations[i]*100)))
plt.title(r"Demand Variation's Impact ($y=\frac{b}{x+a}+c$)", fontweight="bold")
plt.xlabel('Support Subsample Cardinality')
plt.ylabel('Price of Anarchy')
plt.xlim(xlim)
plt.ylim(ylim)
plt.legend()

plt.figure()
for i in range(5): plt.plot(xRange, f2(xRange, *popt2List[i, :]), label='Demand Variation: {}%'.format(int(demandVariations[i]*100)))
plt.title(r"Demand Variation's Impact ($y=ae^{-bx}+c$)", fontweight="bold")
plt.xlabel('Support Subsample Cardinality')
plt.ylabel('Price of Anarchy')
plt.xlim(xlim)
plt.ylim(ylim)
plt.legend()

plt.show()
