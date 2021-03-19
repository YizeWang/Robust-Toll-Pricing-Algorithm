from GraphManager import *
from InitProject import *
import numpy as np
from os.path import join


pathFolder = '/home/onion/SiouxFalls'
nameProject = 'SiouxFalls.sqlite'

project, demand = InitProject(pathFolder, nameProject)
graphManager = GraphManager(project, demand)

Hs, tolls, gammas = graphManager.GradientDescent()

np.savetxt(join("TempData","Hs.csv"), Hs, delimiter=',')
np.savetxt(join("TempData","tolls.csv"), tolls, delimiter=',')
np.savetxt(join("TempData","gammas.csv"), gammas, delimiter=',')
