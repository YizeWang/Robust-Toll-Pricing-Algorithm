from InitProject import *
from ImposeToll import *
from AssignTraffic import *
from InitGraph import *
import numpy as np
import time


pathFolder = '/home/onion/SiouxFalls'
nameProject = 'SiouxFalls.sqlite'

t = np.zeros(76)

project, demand = InitProject(pathFolder, nameProject)
graph = InitGraph(project)
ImposeToll(graph, t)

maxIter=1000


for gap in [0.01, 0.001, 0.0001, 0.00001]:
    times = []

    start = time.time()
    nashFlowmsa, rgapmsa = AssignTraffic(graph, demand, 'msa', maxIter, gap)
    np.savetxt(f"TempData/{gap}/rgapmsa.csv", rgapmsa, delimiter=",")
    np.savetxt(f"TempData/{gap}/nashFlowmsacsv", nashFlowmsa, delimiter=",")
    times.append(time.time()-start)

    start = time.time()
    nashFlowbfw, rgapbfw = AssignTraffic(graph, demand, 'bfw', maxIter, gap)
    np.savetxt(f"TempData/{gap}/rgapbfw.csv", rgapbfw, delimiter=",")
    np.savetxt(f"TempData/{gap}/nashFlowbfw.csv", nashFlowbfw, delimiter=",")
    times.append(time.time()-start)

    start = time.time()
    nashFlowfrankwolfe, rgapfrankwolfe = AssignTraffic(graph, demand, 'frank-wolfe', maxIter, gap)
    np.savetxt(f"TempData/{gap}/rgapfrankwolfe.csv", rgapfrankwolfe, delimiter=",")
    np.savetxt(f"TempData/{gap}/nashFlowfrankwolfe.csv", nashFlowfrankwolfe, delimiter=",")
    times.append(time.time()-start)

    start = time.time()
    nashFlowfw, rgapfw = AssignTraffic(graph, demand, 'fw', maxIter, gap)
    np.savetxt(f"TempData/{gap}/rgapfw.csv", rgapfw, delimiter=",")
    np.savetxt(f"TempData/{gap}/nashFlowfw.csv", nashFlowfw, delimiter=",")
    times.append(time.time()-start)

    start = time.time()
    nashFlowcfw, rgapcfw = AssignTraffic(graph, demand, 'cfw', maxIter, gap)
    np.savetxt(f"TempData/{gap}/rgapcfw.csv", rgapcfw, delimiter=",")
    np.savetxt(f"TempData/{gap}/nashFlowcfw.csv", nashFlowcfw, delimiter=",")
    times.append(time.time()-start)

    np.savetxt(f"TempData/{gap}/time.csv", times, delimiter=",")

pass
