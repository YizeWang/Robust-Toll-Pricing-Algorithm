import os
import sys
import numpy as np
import time
from TrafficAssigner import TrafficAssigner
from os.path import join


maxIteration = 200
pathCurrFolder = os.path.abspath(os.getcwd())
pathExecutable = "/home/onion/Repo/frank-wolfe-traffic/Build/Release/Launchers/AssignTraffic"
pathDataFolder = "/home/onion/Repo/Differential_Pricing/Locations/SiouxFalls"
pathTempFolder = os.path.join(pathCurrFolder, "Temp")
objective = 'user_eq'
# objective = 'sys_opt'

TA = TrafficAssigner()
TA.SetDataFolderPath(pathDataFolder)
TA.SetTempFolderPath(pathTempFolder)
TA.SetExecutablePath(pathExecutable)
TA.SetMaxIteration(maxIteration)
TA.SetObjective(objective)

TA.GenSample(100, 0.01)

Hs, tolls, gammas, times, hLists = TA.GreedyGradientDescent()

np.savetxt(join("Temp", "Hs.csv"),     Hs,     delimiter=',')
np.savetxt(join("Temp", "tolls.csv"),  tolls,  delimiter=',')
np.savetxt(join("Temp", "gammas.csv"), gammas, delimiter=',')
np.savetxt(join("Temp", "times.csv"),  times,  delimiter=',')
np.savetxt(join("Temp", "hLists.csv"), hLists, delimiter=',')