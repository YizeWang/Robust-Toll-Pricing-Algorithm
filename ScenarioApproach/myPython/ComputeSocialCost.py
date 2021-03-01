import numpy as np


def ComputeSocialCost(xLink, G):

    termLinear = np.multiply(G.T, xLink)
    TB = np.multiply(G.T, G.B)
    base = np.divide(xLink, G.C)
    poly = np.power(base, G.P)
    termPoly = np.multiply(TB, poly)
    termPoly = np.multiply(termPoly, xLink)

    return np.sum(termLinear + termPoly)