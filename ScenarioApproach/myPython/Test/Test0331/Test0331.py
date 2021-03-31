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

plt.show()
