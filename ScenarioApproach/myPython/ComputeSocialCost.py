import numpy as np


def ComputeSocialCost(xLink, G):

    termLinear = np.multiply(G.T, xLink)                  # cost term linear in xLink
    TB = np.multiply(G.T, G.B)                            # free flow time * b
    base = np.divide(xLink, G.C)                          # xLink / capacity
    poly = np.power(base, G.P)                            # base * P
    termPoly = np.multiply(np.multiply(TB, poly), xLink)  # cost term polynomial in xLink

    return np.sum(termLinear + termPoly)
