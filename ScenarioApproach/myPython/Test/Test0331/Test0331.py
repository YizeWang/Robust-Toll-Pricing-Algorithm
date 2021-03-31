import os
import sys
from typing import Tuple
import numpy as np
from os.path import join
import matplotlib.pyplot as plt


costNash = 7472359.874570
costOpt = 7194810.972165

currPath = os.path.abspath(os.path.dirname(sys.argv[0]))

hLists200 = np.genfromtxt(join(currPath, "hLists200.csv"),            delimiter=',')
hListsSV  = np.genfromtxt(join(currPath, "hListsSmallVariation.csv"), delimiter=',')

it200 = range(len(hLists200))
itSV  = range(len(hListsSV))

## figure 1 ##
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
lineObjects1 = ax1.plot(it200, hLists200)
ax1.set_xlabel("Number of Iteration")
ax1.set_ylabel("Social Cost")
ax1.set_title("Gradient Descent (5.0% Demand Variation)")
costNashObject1 = ax1.hlines(costNash, 0, it200[-1], color='y', linestyle='dashed', label='Nash Cost')
costOptObject1 = ax1.hlines(costOpt, 0, it200[-1], color='k', linestyle='dashed', label='Optimal Cost')
obj1 = iter(lineObjects1 + [costNashObject1, costOptObject1])
leg1 = tuple('Sample ' + str(i) for i in range(hLists200.shape[1])) + ('Nomial Nash Cost', 'Nomail Opt Cost')
ax1.legend(obj1, leg1, fontsize=8)

## figure 2 ##
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
lineObjects2 = ax2.plot(itSV, hListsSV, label=['1','2','3','4','5'])
ax2.set_xlabel("Number of Iteration")
ax2.set_ylabel("Social Cost")
ax2.set_title("Gradient Descent (0.1% Demand Variation)")
costNashObject2 = ax2.hlines(costNash, 0, itSV[-1], color='y', linestyle='dashed', label='Nash Cost')
costOptObject2 = ax2.hlines(costOpt, 0, itSV[-1], color='k', linestyle='dashed', label='Optimal Cost')
obj2 = iter(lineObjects2 + [costNashObject2, costOptObject2])
leg2 = tuple('Sample ' + str(i) for i in range(hListsSV.shape[1])) + ('Nomial Nash Cost', 'Nomail Opt Cost')
ax2.legend(obj2, leg2)

## figure 3 Decimal Comparison ##
Hs0 = np.genfromtxt(join(currPath, "HsNoRound.csv"), delimiter=',')
Hs1 = np.genfromtxt(join(currPath, "HsRound1.csv"),  delimiter=',')
Hs2 = np.genfromtxt(join(currPath, "HsRound2.csv"),  delimiter=',')

fig3 = plt.figure(3)
ax3 = fig3.add_subplot(111)
ax3.plot(range(len(Hs0)), Hs0, label='No Rounding')
ax3.plot(range(len(Hs1)), Hs1, label='Rounding to 0.1')
ax3.plot(range(len(Hs2)), Hs2, label='Rounding to 0.01')
ax3.set_xlabel("Number of Iteration")
ax3.set_ylabel("Social Cost")
ax3.set_title("Rounding Impact on Convergence")
ax3.legend()

# figure 4 number of traffic assignments #
numScenario = 10
x = np.array(range(0, numScenario)) + 1
y1 = 2 * numScenario
y2 = 0.5* (np.power(x, 2) + x)

fig4 = plt.figure(4)
ax4 = fig4.add_subplot(111)
ax4.hlines(y1, min(x), max(x), label='Normal given {} Scenarios'.format(numScenario), color='r')
ax4.plot(x, y2, label='Greedy Method', color='b')
ax4.set_xlabel("# Support Constraints")
ax4.set_ylabel("# Traffic Assignments")
ax4.set_title("Normal and Greedy Gradient Comparison")
ax4.legend()

plt.show()
