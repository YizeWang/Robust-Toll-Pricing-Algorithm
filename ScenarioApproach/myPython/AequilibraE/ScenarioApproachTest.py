import os
import time
import numpy as np
from os.path import join
from ScenarioApproachManager import *


numSample = 10

pathFolder = '/home/onion/SiouxFalls'
nameProject = 'SiouxFalls.sqlite'
os.makedirs("TempData", exist_ok=True) 

pathDmndDir = join(pathFolder, '0_tntp_data')
pathProjDir = join(pathFolder, '1_project')

SAM = ScenarioApproachManager(pathDmndDir, pathProjDir, numSample)

Hs, tolls, gammas, times, hLists = SAM.GreedyGradientDescent(np.zeros(76))

np.savetxt(join("TempData", "Hs.csv"),     Hs,     delimiter=',')
np.savetxt(join("TempData", "tolls.csv"),  tolls,  delimiter=',')
np.savetxt(join("TempData", "gammas.csv"), gammas, delimiter=',')
np.savetxt(join("TempData", "times.csv"),  times,  delimiter=',')
np.savetxt(join("TempData", "hLists.csv"), hLists, delimiter=',')

print("Total Time %.1fs" % np.sum(times))