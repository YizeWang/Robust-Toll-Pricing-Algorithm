import numpy as np
from os.path import join
from aequilibrae.project import Project
from aequilibrae.matrix import AequilibraeMatrix


def InitProject(pathFolder, nameProject):
    
    dmndFolder = join(pathFolder, '0_tntp_data')
    projFolder = join(pathFolder, '1_project')
    AssgFolder = join(pathFolder, '4_assignment_results')

    project = Project()
    project.load(projFolder)

    demand = AequilibraeMatrix()
    demand.load(join(dmndFolder, 'demand.omx'))
    demand.computational_view(['matrix'])

    return project, demand
