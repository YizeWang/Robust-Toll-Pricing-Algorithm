import os
import time
import numpy as np
from scipy import sparse
from datetime import datetime
from ParseTNTP import ModifyODs, ParseTNTP
from scipy.optimize import Bounds, minimize
from GetEqualityConstraints import GetEqualityConstraints
from scipy.optimize import LinearConstraint, NonlinearConstraint
from scipy.sparse import csc_matrix, eye, lil_matrix, dok_matrix, diags, hstack, vstack


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
nameNet7 = 'Pigou'

nameNet = nameNet3
numSmpl = 0

G = ParseTNTP(pathDataFolder, nameNet)
G = ModifyODs(G, numODs=0, scaleFactor=1)

M = G.numEdge
N = G.numNode
K = G.numDmnd

xDim = M
XDim = M + M * K
tDim = M
uDim = XDim
lDim = M + N * K

lb = np.concatenate((np.zeros(XDim), np.zeros(tDim), np.zeros(uDim), np.full(lDim, -np.inf)))
ub = np.concatenate((np.full(XDim, np.inf), np.full(tDim, np.inf), np.full(uDim, np.inf), np.full(lDim, np.inf)))
bounds = Bounds(lb, ub)

A, b = GetEqualityConstraints(G, G.dataOD)

# construct temp values
Q = np.divide(np.multiply(G.T, G.B), np.power(G.C, G.P))
ALPHA = np.multiply(Q, G.P+1)
BETA = np.multiply(ALPHA, G.P)

def Objective(v):
    termLinear = np.multiply(G.T, v[:xDim])
    termPoly = np.multiply(Q, np.power(v[:xDim], G.P+1))
    return np.sum(termLinear+termPoly)

def Jacobian(v):
    Jac = np.zeros_like(v)
    Jac[:M] = G.T + np.multiply(ALPHA, np.power(v[:xDim], G.P))
    return Jac

def Hessian(v):
    Hes = csc_matrix((XDim+tDim+uDim+lDim, XDim+tDim+uDim+lDim), dtype=np.float64)
    Hes[:xDim, :xDim] = diags(BETA*v[:xDim]**(G.P-1), format="csc")
    return Hes

# nonlinear constraint from stationarity
def fNonlinearConstraint1(v):
    tmp1 = np.zeros(XDim)
    tmp1[:xDim] = v[XDim:XDim+tDim] + G.T + np.multiply(np.multiply(G.T, G.B), np.power(np.divide(v[:xDim], G.C), G.P))
    tmp2 = v[XDim+tDim:XDim+tDim+uDim]
    tmp3 = A.transpose() @ v[XDim+tDim+uDim:]
    return tmp1 - tmp2 + tmp3

def JNonlinearConstraint1(v):
    tmp1 = np.divide(np.multiply(np.multiply(G.T, G.B), G.P), G.C)
    tmp2 = np.power(np.divide(v[:M], G.C), G.P-1)
    tmp3 = np.multiply(tmp1, tmp2)
    J1 = diags(tmp3)
    J1 = vstack((J1, csc_matrix((XDim-xDim, xDim))))
    J1 = hstack((J1, csc_matrix((XDim, XDim-xDim))))
    J2 = eye(tDim)
    J2 = vstack((J2, csc_matrix((XDim-xDim, tDim))))
    J3 = -eye(uDim)
    J4 = A.transpose()
    Jac = hstack((J1, J2, J3, J4))
    return Jac

def HNonlinearConstraint1(v, alpha):
    Hes = csc_matrix((XDim+tDim+uDim+lDim, XDim+tDim+uDim+lDim))
    tmp1 = np.multiply(np.multiply(np.multiply(G.P, G.T), G.B), G.P-1)
    tmp2 = np.power(G.C, 2)
    tmp3 = np.divide(tmp1, tmp2)
    tmp4 = np.divide(v[:xDim], G.C)
    tmp5 = np.power(tmp4, G.P-2)
    tmp6 = np.multiply(tmp3, tmp5)
    Hes[:xDim, :xDim] = diags(np.multiply(tmp6, alpha[:xDim]))
    return Hes

# nonlinear constraint from complementary slackness
def fNonlinearConstraint2(v):
    return sum(v[i]*v[i+XDim+tDim] for i in range(XDim))

def JNonlinearConstraint2(v):
    J1 = v[XDim+tDim:XDim+tDim+uDim]
    J2 = np.zeros(tDim)
    J3 = v[:XDim]
    J4 = np.zeros(lDim)
    Jac = np.hstack((J1, J2, J3, J4))
    return Jac

def HNonlinearConstraint2(v, alpha):
    Hes = lil_matrix((XDim+tDim+uDim+lDim, XDim+tDim+uDim+lDim))
    for i in range(XDim): Hes[i, i+XDim+tDim] = Hes[i+XDim+tDim, i] = alpha[0]
    return Hes

X = eye(XDim, format='csc')
X = hstack((X, csc_matrix((XDim, tDim+uDim+lDim))))  # x = X @ v

linearConstraint = LinearConstraint(A@X, np.ravel(b), np.ravel(b))
nonlinearConstraint1 = NonlinearConstraint(fNonlinearConstraint1, 0.0, 0.0, jac=JNonlinearConstraint1, hess=HNonlinearConstraint1)
nonlinearConstraint2 = NonlinearConstraint(fNonlinearConstraint2, 0.0, 0.0, jac=JNonlinearConstraint2, hess=HNonlinearConstraint2)

v0 = np.zeros(XDim+tDim+uDim+lDim)
result = minimize(Objective, v0, method='trust-constr', jac=Jacobian, hess=Hessian,
                  constraints=[linearConstraint, nonlinearConstraint1, nonlinearConstraint2],
                  options={'disp': True, 'sparse_jacobian': True, 'maxiter': 50000}, bounds=bounds)

print(result)
