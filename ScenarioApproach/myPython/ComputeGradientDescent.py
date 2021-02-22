import numpy as np
from ComputeBigH import *

def ComputeGradientDescent(G, tolls, A, bMat, Q, q, deltaToll=0.01):

    M = q.shape[0]
    gradH = np.zeros(M, dtype=np.double)

    for m in range(M):

        minusTolls = tolls + 0
        plusTolls = tolls + 0
        minusTolls[m] = minusTolls[m] - deltaToll
        plusTolls[m] = plusTolls[m] + deltaToll

        minusH = ComputeBigH(A, bMat, minusTolls, Q, q)
        plusH  = ComputeBigH(A, bMat, plusTolls, Q, q)

        gradient = (plusH - minusH) / (2 * deltaToll)
        gradH[m] = gradient

    return gradH