import os
import sys
import numpy as np
from os.path import join
import matplotlib.pyplot as plt

costNash = 7472359.874570
costOpt = 7194810.972165
costRestrictedOptToll = 7200479.683378
         
currPath = os.path.abspath(os.path.dirname(sys.argv[0]))

H0 = np.genfromtxt(join(currPath, "Hs0.csv"))
H1 = np.genfromtxt(join(currPath, "Hs1.csv"))
H2 = np.genfromtxt(join(currPath, "Hs2.csv"))
H3 = np.genfromtxt(join(currPath, "Hs3.csv"))
H4 = np.genfromtxt(join(currPath, "Hs4.csv"))

it0 = range(len(H0))
it1 = range(len(H1))
it2 = range(len(H2))
it3 = range(len(H3))
it4 = range(len(H4))
maxIteration = max([len(H0), len(H1), len(H2), len(H3), len(H4)])

## figure 1 ##
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.plot(it0, H0, color='b', label='Init Toll: All 0')
ax1.plot(it1, H1, color='g', label='Init Toll: All 1')
ax1.plot(it2, H2, color='r', label='Init Toll: All 2')
ax1.plot(it3, H3, color='c', label='Init Toll: All 3')
ax1.plot(it4, H4, color='m', label='Init Toll: All 4')
ax1.hlines(costNash, 0, maxIteration, color='y', linestyle='dashed', label='Nash Cost')
ax1.hlines(costOpt, 0, maxIteration, color='k', linestyle='dashed', label='Optimal Cost')
ax1.hlines(costRestrictedOptToll, 0, maxIteration, color='lime', linestyle='dashed', label='Gurobi Optimal Cost (Toll < 10)')
ax1.set_xlabel("Number of Iteration")
ax1.set_ylabel("Social Cost")
ax1.set_title("Gradient Descent")
ax1.legend()

## figure 2 ##
itGamma = range(1, maxIteration+1)
Gamma = 0.001 / np.array(itGamma)

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.plot(itGamma, Gamma, label="Gamma = 0.001 / Iteration")
ax2.set_xlabel("Number of Iteration")
ax2.set_ylabel("Step Size")
ax2.set_title("Step Size")
ax2.legend()

## figure 3 ##
T0 = np.genfromtxt(join(currPath, "times0.csv"))
T1 = np.genfromtxt(join(currPath, "times1.csv"))
T2 = np.genfromtxt(join(currPath, "times2.csv"))
T3 = np.genfromtxt(join(currPath, "times3.csv"))
T4 = np.genfromtxt(join(currPath, "times4.csv"))
fig3 = plt.figure(3)
ax3 = fig3.add_subplot(111)
ax3.plot(range(len(T0)), T0, color='b', label='Init Toll: All 0')
ax3.plot(range(len(T1)), T1, color='g', label='Init Toll: All 1')
ax3.plot(range(len(T2)), T2, color='r', label='Init Toll: All 2')
ax3.plot(range(len(T3)), T3, color='c', label='Init Toll: All 3')
ax3.plot(range(len(T4)), T4, color='m', label='Init Toll: All 4')
ax3.set_xlabel("Number of Iteration")
ax3.set_ylabel("Time")
ax3.set_title("Time of Each Iteration")
ax3.legend()

# figure 4 ##
Toll0 = np.genfromtxt(join(currPath, "tolls0.csv"), delimiter=',')
Toll1 = np.genfromtxt(join(currPath, "tolls1.csv"), delimiter=',')
Toll2 = np.genfromtxt(join(currPath, "tolls2.csv"), delimiter=',')
Toll3 = np.genfromtxt(join(currPath, "tolls3.csv"), delimiter=',')
Toll4 = np.genfromtxt(join(currPath, "tolls4.csv"), delimiter=',')
TollGurobi = np.genfromtxt(join(currPath, "tollOptGurobi.csv"), delimiter=',')
fig4 = plt.figure(4)
ax41 = fig4.add_subplot(221)
ax42 = fig4.add_subplot(222)
ax43 = fig4.add_subplot(223)
ax44 = fig4.add_subplot(224)
ax41.plot(range(len(Toll0)), Toll0, linewidth=0.5)
ax42.plot(range(len(Toll1)), Toll1, linewidth=0.5)
ax43.plot(range(len(Toll2)), Toll2, linewidth=0.5)
ax44.plot(range(len(Toll3)), Toll3, linewidth=0.5)
ax41.set_xlabel("Number of Iteration")
ax41.set_ylabel("Tolls")
ax41.set_title("Toll Evolution - Init: All 0")
ax42.set_xlabel("Number of Iteration")
ax42.set_ylabel("Tolls")
ax42.set_title("Toll Evolution - Init: All 1")
ax43.set_xlabel("Number of Iteration")
ax43.set_ylabel("Tolls")
ax43.set_title("Toll Evolution - Init: All 2")
ax44.set_xlabel("Number of Iteration")
ax44.set_ylabel("Tolls")
ax44.set_title("Toll Evolution - Init: All 3")
print("Toll0 Range: [%.3f, %.3f]" % (np.min(Toll0[-1, :]), np.max(Toll0[-1, :])))
print("Toll1 Range: [%.3f, %.3f]" % (np.min(Toll1[-1, :]), np.max(Toll1[-1, :])))
print("Toll2 Range: [%.3f, %.3f]" % (np.min(Toll2[-1, :]), np.max(Toll2[-1, :])))
print("Toll3 Range: [%.3f, %.3f]" % (np.min(Toll3[-1, :]), np.max(Toll3[-1, :])))
print("Toll4 Range: [%.3f, %.3f]" % (np.min(Toll4[-1, :]), np.max(Toll4[-1, :])))

plt.show()
