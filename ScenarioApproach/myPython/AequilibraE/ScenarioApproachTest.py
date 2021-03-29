import os
import time
import numpy as np
from os.path import join
from InitProject import *
from GraphManager import *
from ScenarioApproachManager import *


pathFolder = '/home/onion/SiouxFalls'
nameProject = 'SiouxFalls.sqlite'

project, demand = InitProject(pathFolder, nameProject)
SAM = ScenarioApproachManager(project, demand, 3)
Hs, tolls, gammas, times, hLists = SAM.GradientDescent(np.ones(76)*0)
np.savetxt(join("TempData", "Hs.csv"),     Hs,     delimiter=',')
np.savetxt(join("TempData", "tolls.csv"),  tolls,  delimiter=',')
np.savetxt(join("TempData", "gammas.csv"), gammas, delimiter=',')
np.savetxt(join("TempData", "times.csv"),  times,  delimiter=',')
np.savetxt(join("TempData", "hLists.csv"), hLists, delimiter=',')
print("Total Time %.1fs" % np.sum(times))

project.close()
