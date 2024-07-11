import os
import sys
import csv
import time
import numpy as np
from os.path import join
from TrafficAssigner import *


numSample = 1000
maxIteration = 200
objective = 'user_eq'
pathCurrFolder = os.path.abspath(os.getcwd())
pathExecutable = "/home/onion/Repo/frank-wolfe-traffic/Build/Release/Launchers/AssignTraffic"
pathDataFolder = "/home/onion/Repo/Differential_Pricing/Locations/SiouxFalls"
pathTempFolder = os.path.join(pathCurrFolder, "Temp")
pathTollFolder = join(join(pathCurrFolder, 'Figures'), 'DataPerformanceComparison')

TA = TrafficAssigner()
TA.SetDataFolderPath(pathDataFolder)
TA.SetTempFolderPath(pathTempFolder)
TA.SetExecutablePath(pathExecutable)
TA.SetMaxIteration(maxIteration)

toll0 = np.zeros(76)
toll1 = np.genfromtxt(join(pathTollFolder, 'Toll1.csv'))
toll2 = np.genfromtxt(join(pathTollFolder, 'Toll2.csv'))
MCT = np.genfromtxt(join(pathTollFolder, 'MarginCostToll.csv'))

SysOptCost = []
UserEqCost = []
Toll1Cost = []
Toll2Cost = []
MCTCost = []

tStart = time.time()
TA.GenSample(numSample, 0.05)
for i in range(numSample):
    flow = TA.AssignTraffic(toll0, i, objective)
    cost = TA.SocialCost(flow)
    UserEqCost.append(cost)

    SysOptCost = TA.optCosts

    flow = TA.AssignTraffic(toll1, i, objective)
    cost = TA.SocialCost(flow)
    Toll1Cost.append(cost)

    flow = TA.AssignTraffic(toll2, i, objective)
    cost = TA.SocialCost(flow)
    Toll2Cost.append(cost)

    flow = TA.AssignTraffic(MCT, i, objective)
    cost = TA.SocialCost(flow)
    MCTCost.append(cost)
tElapsed = time.time()-tStart
print('Elpased time: {}, sample average time: {}'.format(tElapsed, tElapsed/numSample))

np.savetxt(join(pathTempFolder, 'CostSysOpt.csv'), SysOptCost)
np.savetxt(join(pathTempFolder, 'CostUserEq.csv'), UserEqCost)
np.savetxt(join(pathTempFolder, 'CostToll1.csv'), Toll1Cost)
np.savetxt(join(pathTempFolder, 'CostToll2.csv'), Toll2Cost)
np.savetxt(join(pathTempFolder, 'CostMCT.csv'), MCTCost)