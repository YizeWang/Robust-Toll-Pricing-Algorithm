import csv
import os
import sys
from os.path import join

import matplotlib.pyplot as plt
import numpy as np

pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = join(pathCurrFolder, os.pardir, "DataDemandVariationAndSubsample")

xlim = [0.20, 0.45]
ylim = [1.0, 1.06]
xRange = np.linspace(1, 20, 100, endpoint=True)
eRange = np.linspace(0.2, 0.6, 100, endpoint=True)
demandVariations = [0.05, 0.20]

epsilons = {1: 0.207517101646083,
            2: 0.240255973901323,
            3: 0.269150874312880,
            4: 0.295330961610537,
            5: 0.319424046813630,
            6: 0.341831211355028,
            7: 0.362831102504381,
            8: 0.382628549639911,
            9: 0.401380374073572,
            10: 0.419210394379987,
            11: 0.436218758244360,
            12: 0.452488056294454,
            13: 0.468087497521417,
            14: 0.483075859284717,
            15: 0.497503631263268,
            16: 0.511414611282226,
            17: 0.524847117731315,
            18: 0.537834927191864,
            19: 0.550408010908841,
            20: 0.562593121250870,
            21: 0.574414264443137,
            22: 0.585893085807696,
            23: 0.597049186802088,
            24: 0.607900388258370,
            25: 0.618462950723334,
            26: 0.628751760254123,
            27: 0.638780486144906,
            28: 0.648561715656814,
            29: 0.658107069762125,
            30: 0.667427303102678}

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
    epsilon = [epsilons[len(subsampleList)] for subsampleList in subsampleLists]

    plt.figure(figsize=(13.5, 10), dpi=80)
    plt.scatter(epsilon, lastPoAs, s=75)

    if demandVariation == 0.05:
        x_orange, y_orange = 0.295330961610537, 1.0199250649522302
        plt.scatter([x_orange], [y_orange], s=80, color='orange', zorder=10)
        plt.scatter([x_orange], [y_orange], s=1000, facecolors='none', edgecolors='orange', zorder=10)
        x_magenta, y_magenta = 0.240255973901323, 1.0368548593662308
        plt.scatter([x_magenta], [y_magenta], s=80, color='magenta', zorder=10)
        plt.scatter([x_magenta], [y_magenta], s=1000, facecolors='none', edgecolors='magenta', zorder=10)

    plt.xlabel(r'Reliability Parameter $\epsilon$', fontsize=36)
    plt.ylabel(r'Best Worst-Case PoA $\mathcal{P}^*$', fontsize=36)
    plt.xticks(np.arange(xlim[0], xlim[1] + sys.float_info.epsilon, step=0.05))
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xticks(fontsize=32)
    plt.yticks(fontsize=32)
    plt.legend()

plt.show()
