import os
import sys
import numpy as np
import time
from TrafficAssigner import TrafficAssigner


maxIteration = 100
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

print(TA.AssignTraffic(np.zeros(76)))
