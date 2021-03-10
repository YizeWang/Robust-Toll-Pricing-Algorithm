import numpy as np


def GenerateSamples(ODs, numSmpl, range=0.2):
    
    numDmnd = len(ODs)
    baseDemands = ODs[:, 2:]

    coeff = 2 * range * np.random.rand(numDmnd, numSmpl) - range + 1  # coeffs lie in [1-range, 1+range]
    sampleDmnd = np.multiply(coeff, baseDemands)                      # scale base demands with coefficients

    sampleODs = np.hstack((ODs[:, :2], sampleDmnd))

    return sampleODs
