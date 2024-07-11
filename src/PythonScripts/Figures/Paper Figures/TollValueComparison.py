import os
from os.path import join

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import numpy as np

pathCurrFolder = os.path.abspath(os.getcwd())
pathDataFolder = join(pathCurrFolder, os.pardir, "DataTollValueComparison")

pathDataT0 = os.path.join(pathDataFolder, 'MarginCostToll.csv')
pathDataT1 = os.path.join(pathDataFolder, 'Toll1.csv')
pathDataT2 = os.path.join(pathDataFolder, 'Toll2.csv')

indEdge = np.arange(1, 76 + 1)
T0 = np.genfromtxt(pathDataT0, delimiter=',')
T1 = np.genfromtxt(pathDataT1, delimiter=',')
T2 = np.genfromtxt(pathDataT2, delimiter=',')
print(np.max(T1))
print(np.max(T2))

plt.figure("Toll Value", figsize=(13, 10), dpi=80)
plt.plot(indEdge, T0, label='MCT', color='tab:green', linewidth=3)
plt.plot(indEdge, T1, label='Toll1', color='magenta', linewidth=3)
plt.plot(indEdge, T2, label='Toll2', color='orange', linewidth=3)
plt.xlim([1, 76])
plt.xticks(np.hstack((np.hstack(([1], np.arange(10, 76, 10))), 76)), fontsize=32)
plt.ylim([0, 60])
plt.yticks(np.arange(0, 60 + 1, 10), fontsize=32)
plt.xlabel(r"Edge Index $e$", fontsize=36)
plt.ylabel(r"Toll Value $\tau$", fontsize=36)
legend_font = font_manager.FontProperties(size=32)
plt.legend(prop=legend_font, loc='upper right', framealpha=1)
plt.show()
