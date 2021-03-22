import os
import time
import numpy as np
from os.path import join
from InitProject import *
from GraphManager import *


pathFolder = '/home/onion/SiouxFalls'
nameProject = 'SiouxFalls.sqlite'

project, demand = InitProject(pathFolder, nameProject)
graphManager = GraphManager(project, demand)

Hs, tolls, gammas, times = graphManager.GradientDescent(np.ones(76)*0)
np.savetxt(join("TempData", "Hs0.csv"),     Hs,     delimiter=',')
np.savetxt(join("TempData", "tolls0.csv"),  tolls,  delimiter=',')
np.savetxt(join("TempData", "gammas0.csv"), gammas, delimiter=',')
np.savetxt(join("TempData", "times0.csv"),  times,  delimiter=',')
print("Total Time %.1fs" % np.sum(times))
project.close()

project, demand = InitProject(pathFolder, nameProject)
graphManager = GraphManager(project, demand)

Hs, tolls, gammas, times = graphManager.GradientDescent(np.ones(76)*1)
np.savetxt(join("TempData", "Hs1.csv"),     Hs,     delimiter=',')
np.savetxt(join("TempData", "tolls1.csv"),  tolls,  delimiter=',')
np.savetxt(join("TempData", "gammas1.csv"), gammas, delimiter=',')
np.savetxt(join("TempData", "times1.csv"),  times,  delimiter=',')
print("Total Time %.1fs" % np.sum(times))
project.close()

project, demand = InitProject(pathFolder, nameProject)
graphManager = GraphManager(project, demand)

Hs, tolls, gammas, times = graphManager.GradientDescent(np.ones(76)*2)
np.savetxt(join("TempData", "Hs2.csv"),     Hs,     delimiter=',')
np.savetxt(join("TempData", "tolls2.csv"),  tolls,  delimiter=',')
np.savetxt(join("TempData", "gammas2.csv"), gammas, delimiter=',')
np.savetxt(join("TempData", "times2.csv"),  times,  delimiter=',')
print("Total Time %.1fs" % np.sum(times))
project.close()

project, demand = InitProject(pathFolder, nameProject)
graphManager = GraphManager(project, demand)

Hs, tolls, gammas, times = graphManager.GradientDescent(np.ones(76)*3)
np.savetxt(join("TempData", "Hs3.csv"),     Hs,     delimiter=',')
np.savetxt(join("TempData", "tolls3.csv"),  tolls,  delimiter=',')
np.savetxt(join("TempData", "gammas3.csv"), gammas, delimiter=',')
np.savetxt(join("TempData", "times3.csv"),  times,  delimiter=',')
print("Total Time %.1fs" % np.sum(times))
project.close()

project, demand = InitProject(pathFolder, nameProject)
graphManager = GraphManager(project, demand)

Hs, tolls, gammas, times = graphManager.GradientDescent(np.ones(76)*4)
np.savetxt(join("TempData", "Hs4.csv"),     Hs,     delimiter=',')
np.savetxt(join("TempData", "tolls4.csv"),  tolls,  delimiter=',')
np.savetxt(join("TempData", "gammas4.csv"), gammas, delimiter=',')
np.savetxt(join("TempData", "times4.csv"),  times,  delimiter=',')
print("Total Time %.1fs" % np.sum(times))
project.close()

os.system('shutdown -t 1')
