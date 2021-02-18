import numpy as np


def GenerateSamples(ODs, numSmpl, range=0.5):
    
    numDmnd = len(ODs)
    baseDemands = ODs[:, 2:2+1]

    coeff = 2 * range * np.random.rand(numDmnd, numSmpl) - range + 1 # coeffs lie in [1-range, 1+range]
    sampleDmnd = np.multiply(coeff, baseDemands)

    sampleODs = np.concatenate((ODs[:, 0:2], sampleDmnd), axis=1)

    return sampleODs