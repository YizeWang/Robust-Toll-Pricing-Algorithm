import os
import sys
from ParseTNTP import ParseTNTP


nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
pathDataFolder = '..\\myRealData\\'

nameNet = nameNet2

G = ParseTNTP(pathDataFolder, nameNet)

M = G.numEdge
N = G.numNode
K = G.numDmnd

T = G.T
B = G.B
P = G.P
C = G.C





pass