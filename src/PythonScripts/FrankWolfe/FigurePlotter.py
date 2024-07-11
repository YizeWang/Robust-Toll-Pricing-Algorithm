import os
import sys
import csv
import numpy as np
from os.path import join
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


class FigurePlotter:

    def __init__(self, pathFolder):
        self.__pathFolder = pathFolder

    def PlotPoAsOfMultiStart(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        PoAsOfMultiStart = []
        with open(join(self.__pathFolder, 'PoAsOfMultiStart.csv'), 'r') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            PoAsOfMultiStart = list(reader)

        for PoAs in PoAsOfMultiStart:
            numIteration = len(PoAs)
            ax.plot(range(numIteration), PoAs)

        ax.set_xlabel("Number of Iteration")
        ax.set_ylabel("Price of Anarchy")
        plt.show()

    def PlotConfidence(self):
        numSubsamples = []
        PoAs = []

        with open(join(self.__pathFolder, 'Subsample.txt'), 'r') as f:
            txt = f.readlines()
            txt = [line.strip('{}\n') for line in txt]
            reader = csv.reader(txt, quoting=csv.QUOTE_NONNUMERIC)
            subsampleLists = list(reader)
        for subsamples in subsampleLists:
            numSubsamples.append(len(subsamples))

        with open(join(self.__pathFolder, 'PoAsOfMultiStart.csv'), 'r') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            PoALists = list(reader)
        for PoAList in PoALists:
            PoAs.append(PoAList[-1])

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.scatter(PoAs, numSubsamples)

        ax.set_xlabel("PoA")
        ax.set_ylabel("Number of Subsamples")
        plt.show()
