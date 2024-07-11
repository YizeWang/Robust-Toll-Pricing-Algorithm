from ComputeOptimalFlowPoly import *
from ComputeNashFlowPoly import *


def ComputePoA(G, ODs):

    _, costNash = ComputeNashFlowPoly(G, ODs)
    _, costOpt = ComputeOptimalFlowPoly(G, ODs)

    PoA = costNash / costOpt
    
    print("PoA: %f" % (PoA))

    return PoA