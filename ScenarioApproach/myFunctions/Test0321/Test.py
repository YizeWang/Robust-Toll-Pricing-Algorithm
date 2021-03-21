import os
import numpy as np
from ParseTNTP import *
from GetEqualityConstraints import *
from ComputeSocialCost import *

xNash001   = np.genfromtxt("xNash0.01.csv",    delimiter=',')
xNash0001  = np.genfromtxt("xNash0.001.csv",   delimiter=',')
xNash00001  = np.genfromtxt("xNash0.0001.csv",  delimiter=',')
xNash000001 = np.genfromtxt("xNash0.00001.csv", delimiter=',')
xNash0005    = np.genfromtxt("xNash0.005.csv",    delimiter=',')
xNash00005  = np.genfromtxt("xNash0.0005.csv",  delimiter=',')
xNash000005 = np.genfromtxt("xNash0.00005.csv", delimiter=',')
xNashAquilibrae = np.genfromtxt("xNashAquilibrae.csv", delimiter=',')

pathCurrFolder = os.path.abspath(os.getcwd())
pathParFolder = os.path.abspath(os.path.join(pathCurrFolder, '..'))
pathDataFolder = os.path.join(pathParFolder, 'myRealData')
pathLogFolder = os.path.join(pathCurrFolder, 'Log')

nameNet = 'SiouxFalls'
G = ParseTNTP(pathDataFolder, nameNet)

a = np.divide(np.multiply(G.T, G.B), (G.P+1))
c = G.T

NashCost = lambda x: np.sum(np.multiply(c, x) + np.multiply(np.multiply(a, x), np.power(np.divide(x, G.C), G.P)))

yNash001   = NashCost(xNash001[0:76])
yNash0001  = NashCost(xNash0001[0:76])
yNash00001  = NashCost(xNash00001[0:76])
yNash000001 = NashCost(xNash000001[0:76])
yNash0005  = NashCost(xNash0005[0:76])
yNash00005  = NashCost(xNash00005[0:76])
yNash000005 = NashCost(xNash000005[0:76])
yNashAquilibrae = NashCost(xNashAquilibrae[0:76])

A, b = GetEqualityConstraints(G, G.dataOD)

Violation = lambda x : np.linalg.norm(A@(np.reshape(x,(-1,1))) - b)

eNash001   = Violation(xNash001)
eNash0001  = Violation(xNash0001)
eNash00001  = Violation(xNash00001)
eNash000001 = Violation(xNash000001)
eNash0005  = Violation(xNash0005)
eNash00005  = Violation(xNash00005)
eNash000005 = Violation(xNash000005)

print(yNash001, yNash0001, yNash00001, yNash000001, yNash0005, yNash00005, yNash000005)
print(eNash001, eNash0001, eNash00001, eNash000001, eNash0005, eNash00005, eNash000005)

print("Aquilibrae Nash: %f, Aquilibrae Social Cost: %f" % (yNashAquilibrae, ComputeSocialCost(xNashAquilibrae, G)))