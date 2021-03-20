import os
import sys
import numpy as np
from ParseTNTP import *
from GenerateSamples import *
from datetime import datetime
from ComputeOptimalTolls import *
from ComputeFlow import *
from ComputeOptimalTollsApproximate import *


verbose = True

pathCurrFolder = os.path.abspath(os.getcwd())
pathParFolder = os.path.abspath(os.path.join(pathCurrFolder, '..'))
pathDataFolder = os.path.join(pathParFolder, 'myRealData')
pathLogFolder = os.path.join(pathCurrFolder, 'Log')

currentTime = datetime.now()
currentTime = currentTime.strftime("%Y%m%d%H%M%S")

pathLogFile = os.path.join(pathLogFolder, (currentTime + "-Log.txt"))
pathSolFile = os.path.join(pathLogFolder, (currentTime + "-Sol.csv"))

nameNet1 = 'SimpleGeneralNetwork'
nameNet2 = 'SiouxFalls'
nameNet3 = 'Brasse'
nameNet4 = 'SiouxFallsSmall'
nameNet5 = 'Friedrichshain'
nameNet6 = 'Massachusetts'

nameNet = nameNet2
numSmpl = 0

with open(pathLogFile, 'wt') as logFile:

    sys.stdout = logFile

    G = ParseTNTP(pathDataFolder, nameNet)
    # G = ModifyODs(G, numODs=0, scaleFactor=0.853)
    G = ModifyODs(G, numODs=0, scaleFactor=1)

    sampleODs = G.dataOD
    # sampleODs = GenerateSamples(G.dataOD, numSmpl, range=0.05)
    
    xNash, costNash, idxZeroFlowNash, idxNonZeroFlowNash, idxUsedNash, flowNash = ComputeFlow(G, G.dataOD, type='Nash', verbose=verbose)
    print("Nash Flow Cost: %f" % costNash)

    xOpt, costOpt, idxZeroFlowOpt, idxNonZeroFlowOpt, idxUsedOpt, flowOpt = ComputeFlow(G, G.dataOD, type='Optimal', verbose=False)
    print("Optimal Flow Cost: %f" % costOpt)

    # tOpt = [1.310199458065761657e-01,5.431666257508416251e-01,3.296720051291811338e+00,3.118463631881682740e+00,1.703363369004611272e-01,4.275722695478436641e-01,0.000000000000000000e+00,2.068878496502238040e-01,2.662514102009613914e+00,1.358845261990536457e+00,9.864788756567602901e-01,4.320749828485540789e+00,2.143875993600181218e+00,6.129409410508826817e+00,1.270088650845236700e+01,6.081270271861221488e+00,3.000141563010249035e-01,1.038183801520250693e+00,5.612620208557480339e+00,2.331337625483780873e-01,6.120767296627678711e+00,3.342678357110728360e+00,4.751794011035584298e+00,5.909845817206184071e-01,9.074018780794009809e-01,2.221959247051395359e+00,6.103099220959083304e+00,2.152426350167462754e+00,6.480775167991540187e+00,6.958387285285017931e+00,1.163681309233458805e+01,3.566998590316758477e+00,7.371626646970411478e+00,4.160853535660032243e+00,3.674920670269736234e-01,8.721716911803181205e+00,1.170111089526316261e+00,2.203559976209889804e-01,4.883757083950032829e+00,2.199457899264807281e+00,3.625063100654291048e+00,5.647037516175601901e+00,4.108042008994403638e-01,6.434544787612008321e+00,3.618777263483152318e+00,1.061873995789724034e+01,3.298903313589814257e+00,8.128069709728611869e+00,1.394835205933982181e+01,9.885387972182932415e-02,1.004526735262884785e+01,2.065075680286148962e+00,4.581864078761466175e+00,9.737319990608148679e-01,5.240026295113920513e-02,2.299497980303313760e+00,1.006642619395461541e-01,7.588001951671192735e+00,1.263240864674252562e+00,2.627946281898291936e+00,1.095775014974196537e+01,6.814575375276089808e+00,8.264609756776895466e+00,1.895582925140353092e+00,5.651559394770559130e+00,8.006971774771837858e+00,5.451482450770241961e+00,5.584005737412562453e+00,1.387058635406634433e-01,3.626917305043872553e+00,8.998457744252455370e+00,8.000528641986829115e+00,3.933728156990983216e+00,3.729132966716866004e+00,4.088446173053599253e+00,1.713905175718325680e+00]
    # tOpt = ComputeOptimalTolls(G, sampleODs, pathSolFile, verbose=True)
    # xToll, costToll, _, _, _, flowNash = ComputeFlow(G, sampleODs, tOpt, verbose=True)
    # print("costToll: %f" % costToll)
    # print("tOpt: ", tOpt)

    logFile.close()

pass
