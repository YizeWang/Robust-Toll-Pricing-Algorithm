from logging import error
import numpy as np
from scipy.stats import truncnorm


def GetBoundedPoisson(lb, ub, lam, numSmpl):
    X = np.random.poisson(lam, numSmpl)
    for ind, x in enumerate(X):
        while not (lb <= X[ind] <= ub):
            X[ind] = np.random.poisson(lam)
    return X

def GenerateSamples(ODs, numSmpl, type='uniform'):
    
    numDmnd = len(ODs)
    baseDemands = ODs[:, 2:]

    if type == 'uniform':
        uniRange = 0.2
        coeff = 2 * uniRange * np.random.rand(numDmnd, numSmpl) - uniRange + 1  # coeffs lie in [1-range, 1+range]
        sampleDmnd = np.multiply(coeff, baseDemands)                      # scale base demands with coefficients
    elif type == 'gaussian':
        sampleDmnd = np.zeros((numDmnd, numSmpl))
        for dmnd in range(numDmnd):
            mu = baseDemands[dmnd]
            sigma = 0.1 * mu
            lb = 0.8 * mu
            ub = 1.2 * mu
            X = truncnorm((lb-mu)/sigma, (ub-mu)/sigma, loc=mu, scale=sigma)
            sampleDmnd[dmnd, :] = X.rvs(numSmpl)
    elif type == 'poisson':
        sampleDmnd = np.zeros((numDmnd, numSmpl))
        for dmnd in range(numDmnd):
            lam = baseDemands[dmnd]
            lb = 0.8 * lam
            ub = 1.2 * lam
            sampleDmnd[dmnd, :] = GetBoundedPoisson(lb, ub, lam, numSmpl)
    else:
        error('Invalid name of distribution')

    sampleODs = np.hstack((ODs[:, :2], sampleDmnd))

    return sampleODs
