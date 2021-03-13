import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
import winsound
from ComputeOptimalTolls import *
from ComputeFlow import *
from ComputeOptimalTollsApproximate import *


verbose = True

pathDataFolder = '..\\myRealData\\'
pathLogFolder = '.\\Log\\'

currentTime = datetime.now()
currentTime = currentTime.strftime("%Y%m%d%H%M%S")

pathLogFile = pathLogFolder + currentTime + "-Log.txt"
pathSolFile = pathLogFolder + currentTime + "-Sol.csv"

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
nameNet4 = 'SiouxFallsSmall'
nameNet5 = 'Friedrichshain'
nameNet6 = 'Massachusetts'

nameNet = nameNet3
numSmpl = 0

with open(pathLogFile, 'wt') as logFile:

    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    # G = ModifyODs(G, numODs=0, scaleFactor=0.853)
    G = ModifyODs(G, numODs=0, scaleFactor=1)

    sampleODs = G.dataOD
    # sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.05)

    # xNash, costNash, idxZeroFlowNash, idxNonZeroFlowNash, idxUsedNash, flowNash = ComputeFlow(G, G.dataOD, type='Nash', verbose=verbose)
    # print("Nash Flow Cost: %f" % costNash)

    # xOpt, costOpt, idxZeroFlowOpt, idxNonZeroFlowOpt, idxUsedOpt, flowOpt = ComputeFlow(G, G.dataOD, type='Optimal', verbose=verbose)
    # print("Optimal Flow Cost: %f" % costOpt)


    # tOpt1 = ComputeOptimalTollsApproximate(G, sampleODs, pathSolFile, idxZeroFlowNash, idxNonZeroFlowNash, idxUsedNash, verbose=verbose)
    # xToll1, costToll1, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt1, verbose=verbose)
    # print("costToll1: %f" % costToll1)
    # print("tOpt1: ", tOpt1)

    # tOpt2 = ComputeOptimalTollsApproximate(G, sampleODs, pathSolFile, idxZeroFlowOpt, idxNonZeroFlowOpt, idxUsedOpt, verbose=verbose)
    # xToll2, costToll2, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt2, verbose=verbose)
    # print("costToll2: %f" % costToll2)
    # print("tOpt2: ", tOpt2)

    tOpt = ComputeOptimalTolls(G, sampleODs, pathSolFile, verbose=verbose)
    # tOpt = [58.15028161777214, 119.73724317080284, 2.4469074450912167, 279.466367324196, 7.220138861314878, 102.91213662790821, 32.77964330756324, 8.881784197001252e-16, 109.14175777266402, 174.62201349285326, 5.6379190794511915, 136.47026602205844, 181.29348162919203, 2.8885806950841575, 123.14229108783333, 168.70047440141533, 111.06551720637219, 38.91726867018611, 25.879857031273694, 0.0, 140.90441771014582, 167.67508674626077, 0.5434550524572224, 116.2328937869941, 177.74955267590332, 11.40494395070234, 7.355393291368705, 38.17237014597133, 119.52275265011569, 35.68560507551036, 9.52235479346761, 293.0106342158531, 48.94534292820947, 33.774677865613576, 7.420233126927105, 291.6148064061655, 42.67497053780313, 14.716292031696632, 272.81524013415213, 116.95432455182683, 298.93143475497425, 183.13665287623223, 107.99439299230536, 1.7763568394002505e-15, 23.188798187466425, 169.47442328032136, 126.91551757826413, 269.7793161304718, 181.93718138600553, 1.791765351769254, 86.6222706467359, 78.7135712416619, 90.95835635764354, 12.193894976548105, 126.89347803249994, 2.089131528610225, 44.94667260502521, 135.50530028552393, 61.00904814939618, 21.484930716917997, 264.17952017484544, 218.79323310159555, 312.8189498359865, 51.65691715738239, 145.11545640129597, 77.3348473359211, 82.1622981059196, 0.0, 0.06490707401933049, 15.689618324091656, 67.36501264904322, 286.2110680461717, 61.25229600735986, 4.463926459059206, 182.69756662851572, 40.64584480139246]
    # xToll, costToll, _, _, _, _ = ComputeFlow(G, sampleODs, tOpt, verbose=verbose)
    # print("costToll: %f" % costToll)
    # print("tOpt: ", tOpt)

    logFile.close()

winsound.Beep(frequency=800, duration=1000)

pass
