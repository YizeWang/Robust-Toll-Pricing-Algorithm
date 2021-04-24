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
