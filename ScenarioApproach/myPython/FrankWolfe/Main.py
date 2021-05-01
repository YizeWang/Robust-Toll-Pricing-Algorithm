import os
import sys
import csv
import time
import numpy as np
from os.path import join
from TrafficAssigner import TrafficAssigner
from FigurePlotter import FigurePlotter


maxIteration = 200
numMultiStart = 50
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

TA.GenSample(100, 0.02)

# PoAs, tolls, gammas, times, PoALists = TA.GreedyGradientDescentPoA()

# np.savetxt(join("Temp", "PoAs.csv"),     PoAs,     delimiter=',')
# np.savetxt(join("Temp", "tolls.csv"),    tolls,    delimiter=',')
# np.savetxt(join("Temp", "gammas.csv"),   gammas,   delimiter=',')
# np.savetxt(join("Temp", "times.csv"),    times,    delimiter=',')
# np.savetxt(join("Temp", "PoALists.csv"), PoALists, delimiter=',')

start = time.time()
TA.GenerateMultiStart(numMultiStart)
PoAsOfMultiStart, subsamples, PoABest, subsampleBest = TA.MultiStart()
print('Best PoA: {}, Subsample: {}'.format(PoABest, subsampleBest))
time = time.time() - start

with open(join("Temp", "PoAsOfMultiStart.csv"), "w") as f:
    writer = csv.writer(f)
    writer.writerows(PoAsOfMultiStart)

with open(join("Temp", "ElapsedTime.txt"), 'w') as f:
    f.write(str(time))

with open(join("Temp", "Subsample.txt"), 'w') as f:
    for subsample in subsamples:
        f.write(str(subsample)+'\n')

# fp = FigurePlotter("Temp")
# fp.PlotPoAsOfMultiStart()

os.system('shutdown -t 5')
