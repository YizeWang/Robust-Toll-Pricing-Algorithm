import os
import sys
import time
import numpy as np
from os.path import join
from FrankWolfe.TrafficAssigner import TrafficAssigner


maxIteration = 300
pathCurrFolder = os.path.abspath(os.getcwd())
pathExecutable = "/home/onion/Repo/frank-wolfe-traffic/Build/Release/Launchers/AssignTraffic"
pathDataFolder = "/home/onion/Repo/Differential_Pricing/Locations/SiouxFalls"
pathTempFolder = os.path.join(pathCurrFolder, "Temp")
objective = 'user_eq'

TA = TrafficAssigner()
TA.SetDataFolderPath(pathDataFolder)
TA.SetTempFolderPath(pathTempFolder)
TA.SetExecutablePath(pathExecutable)
TA.SetMaxIteration(maxIteration)
TA.SetObjective(objective)

TA.GenSample(50, 0.02)

PoAs, tolls, gammas, times, PoALists = TA.GreedyGradientDescentPoA()

np.savetxt(join("Temp", "PoAs.csv"),     PoAs,     delimiter=',')
np.savetxt(join("Temp", "tolls.csv"),    tolls,    delimiter=',')
np.savetxt(join("Temp", "gammas.csv"),   gammas,   delimiter=',')
np.savetxt(join("Temp", "times.csv"),    times,    delimiter=',')
np.savetxt(join("Temp", "PoALists.csv"), PoALists, delimiter=',')
