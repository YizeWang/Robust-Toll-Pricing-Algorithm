import os
from os import path
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt
from numpy.core.getlimits import _fr1
from scipy.optimize import curve_fit


pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = os.path.join(os.path.join(pathCurrFolder, "Figures"), "DataDemandVariationAndSubsampleHalfTaxable")
pathDataPoA = os.path.join(pathDataFolder, "PoAsOfMultiStart.csv")
pathDataSubsample = os.path.join(pathDataFolder, "Subsample.txt")

xlim = [1, 20]
ylim = [1.0, 1.06]
xRange = np.linspace(1, 20, 100, endpoint=True)
eRange = np.linspace(0.2, 0.6, 100, endpoint=True)

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

plt.figure('Performance and Robustness (Variation: 5%) - Half Taxable')
plt.scatter(numSubsampleList, lastPoAs, s=4)
plt.scatter(numSubsampleList[47], lastPoAs[47], s=4, color='tab:red')
plt.xlabel('Support Subsample Cardinality')
plt.ylabel(r'Worst-case Price of Anarchy $P$')
plt.xticks(np.arange(1, 20+1, step=1))
plt.xlim(xlim)
plt.ylim(ylim)

plt.show()

epsilons = {1:0.207517101646083,
            2:0.240255973901323,
            3:0.269150874312880,
            4:0.295330961610537,
            5:0.319424046813630,
            6:0.341831211355028,
            7:0.362831102504381,
            8:0.382628549639911,
            9:0.401380374073572,
            10:0.419210394379987,
            11:0.436218758244360,
            12:0.452488056294454,
            13:0.468087497521417,
            14:0.483075859284717,
            15:0.497503631263268,
            16:0.511414611282226,
            17:0.524847117731315,
            18:0.537834927191864,
            19:0.550408010908841,
            20:0.562593121250870,
            21:0.574414264443137,
            22:0.585893085807696,
            23:0.597049186802088,
            24:0.607900388258370,
            25:0.618462950723334,
            26:0.628751760254123,
            27:0.638780486144906,
            28:0.648561715656814,
            29:0.658107069762125,
            30:0.667427303102678}

epsilon = [epsilons[len(subsampleList)] for subsampleList in subsampleLists]

plt.figure('Performance and Robustness (Variation: 5%) - Half Taxable')
plt.scatter(epsilon, lastPoAs, s=4)
plt.scatter(numSubsampleList[47], lastPoAs[47], s=4, color='tab:red')
plt.xlabel(r'Reliability Parameter $\epsilon$')
plt.ylabel(r'Worst-case Price of Anarchy $P$')
plt.xticks(np.arange(0.2, 0.61, step=0.05))
plt.xlim([0.2,0.5])
plt.ylim(ylim)

plt.show()
