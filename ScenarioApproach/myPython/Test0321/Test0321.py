import os
import sys
import numpy as np
import matplotlib.pyplot as plt


sys.path.insert(1, os.path.abspath(os.path.curdir))

from ParseTNTP import *
from ComputeSocialCost import *
from GetEqualityConstraints import *

xNash001        = np.genfromtxt(os.path.join("Test0321", "xNash0.01.csv"),       delimiter=',')
xNash0001       = np.genfromtxt(os.path.join("Test0321", "xNash0.001.csv"),      delimiter=',')
xNash00001      = np.genfromtxt(os.path.join("Test0321", "xNash0.0001.csv"),     delimiter=',')
xNash000001     = np.genfromtxt(os.path.join("Test0321", "xNash0.00001.csv"),    delimiter=',')
xNash0005       = np.genfromtxt(os.path.join("Test0321", "xNash0.005.csv"),      delimiter=',')
xNash00005      = np.genfromtxt(os.path.join("Test0321", "xNash0.0005.csv"),     delimiter=',')
xNash000005     = np.genfromtxt(os.path.join("Test0321", "xNash0.00005.csv"),    delimiter=',')
xNashAquilibrae = np.genfromtxt(os.path.join("Test0321", "xNashAquilibrae.csv"), delimiter=',')

pathCurrFolder = os.path.abspath(os.getcwd())
pathParFolder  = os.path.abspath(os.path.join(pathCurrFolder, '..'))
pathDataFolder = os.path.join(pathParFolder, 'myRealData')
pathLogFolder  = os.path.join(pathCurrFolder, 'Log')

nameNet = 'SiouxFalls'
G = ParseTNTP(pathDataFolder, nameNet)

a = np.divide(np.multiply(G.T, G.B), (G.P+1))
c = G.T

NashCost = lambda x: np.sum(np.multiply(c, x) + np.multiply(np.multiply(a, x), np.power(np.divide(x, G.C), G.P)))

yNash001        = NashCost(xNash001[0:76])
yNash0001       = NashCost(xNash0001[0:76])
yNash00001      = NashCost(xNash00001[0:76])
yNash000001     = NashCost(xNash000001[0:76])
yNash0005       = NashCost(xNash0005[0:76])
yNash00005      = NashCost(xNash00005[0:76])
yNash000005     = NashCost(xNash000005[0:76])
yNashAquilibrae = NashCost(xNashAquilibrae[0:76])

A, b = GetEqualityConstraints(G, G.dataOD)

Violation = lambda x : np.linalg.norm(A@(np.reshape(x,(-1,1))) - b)

eNash001    = Violation(xNash001)
eNash0001   = Violation(xNash0001)
eNash00001  = Violation(xNash00001)
eNash000001 = Violation(xNash000001)
eNash0005   = Violation(xNash0005)
eNash00005  = Violation(xNash00005)
eNash000005 = Violation(xNash000005)

ySocial001        = ComputeSocialCost(xNash001[0:76], G)
ySocial0001       = ComputeSocialCost(xNash0001[0:76], G)
ySocial00001      = ComputeSocialCost(xNash00001[0:76], G)
ySocial000001     = ComputeSocialCost(xNash000001[0:76], G)
ySocial0005       = ComputeSocialCost(xNash0005[0:76], G)
ySocial00005      = ComputeSocialCost(xNash00005[0:76], G)
ySocial000005     = ComputeSocialCost(xNash000005[0:76], G)
ySocialAquilibrae = ComputeSocialCost(xNashAquilibrae[0:76], G)

precision = [0.01, 0.001, 0.0001, 0.00001, 0.005, 0.0005, 0.00005]
costNash = [yNash001, yNash0001, yNash00001, yNash000001, yNash0005, yNash00005, yNash000005]
error = [eNash001, eNash0001, eNash00001, eNash000001, eNash0005, eNash00005, eNash000005]
socialCost = [ySocial001, ySocial0001, ySocial00001, ySocial000001, ySocial0005, ySocial00005, ySocial000005]

costNashR = costNash / np.min(costNash)
socialCostR = socialCost / np.min(socialCost)

yNashAquilibraeR = yNashAquilibrae / np.min(costNash)
ySocialAquilibraeR = ySocialAquilibrae / np.min(socialCost)

order = np.argsort(precision)
precisionInOrder  = [precision[i] for i in order]
costNashInOrder   = [costNashR[i] for i in order]
errorInOrder      = [error[i] for i in order]
socialCostInOrder = [socialCostR[i] for i in order]

fig = plt.figure(1)
ax1 = fig.add_subplot(111)
ax1.plot(precisionInOrder, costNashInOrder, color='b', label='Gurobi Nash Cost')
ax1.set_xscale('log')
ax1.hlines(yNashAquilibraeR, np.min(precision), np.max(precision), color='b', linestyle='dashed', label='AquilibreE Nash Cost')
ax2 = ax1.twinx()
ax2.plot(precisionInOrder, socialCostInOrder, color='r', label='Gurobi Optimal Cost')
ax2.hlines(ySocialAquilibraeR, np.min(precision), np.max(precision), color='r', linestyle='dashed', label='AquilibreE Optimal Cost')
ax1.ticklabel_format(axis='y', style='plain', useOffset=False)
ax2.ticklabel_format(axis='y', style='plain', useOffset=False)
ax1.tick_params(axis='y', colors='b')
ax2.tick_params(axis='y', colors='r')
ax1.yaxis.label.set_color('b')
ax2.yaxis.label.set_color('r')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.set_xlabel("Max Piece Relative Error")
ax1.set_ylabel("Nash Cost")
ax2.set_ylabel("Optimal Cost")
ax1.set_title("Max Piece Relative Error Impact")

ax2.legend(lines1+lines2, labels1+labels2, loc=0)

plt.show()