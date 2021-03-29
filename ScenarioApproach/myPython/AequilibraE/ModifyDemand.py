import time
import numpy as np
from os.path import join
from aequilibrae.matrix import AequilibraeMatrix


pathFolder = '/home/onion/SiouxFalls'
nameProject = 'SiouxFalls.sqlite'

dmndFolder = join(pathFolder, '0_tntp_data')
projFolder = join(pathFolder, '1_project')
AssgFolder = join(pathFolder, '4_assignment_results')

demand = AequilibraeMatrix()
demand.load(join(dmndFolder, 'demand.omx'))
demand.computational_view(['matrix'])
baseDemand = demand.matrix_view

numSample = 3
randRange = 0.2

for s in range(numSample):
    randCoeff = np.random.randn(baseDemand.shape[0], baseDemand.shape[1]) * randRange + numSample
    randDemand = np.multiply(randCoeff, baseDemand)
    nameMatrix = 'Demand' + str(s+1)
    demand.matrix_view = randDemand
    demand.save([nameMatrix])

demand.close()
