import numpy as np
import matplotlib.pyplot as plt


numPieces = 20

x1 = np.linspace(0, 2, num=1000)
brp1 = 4 * (1 + 0.15 * np.power(x1, 4))

x2 = np.linspace(0, 2, num=numPieces+1)
brp2 = 4 * (1 + 0.15 * np.power(x2, 4))

pwl = np.interp(x1, x2, brp2)
indMaxDiff = np.argmax(np.divide(np.abs((pwl-brp1)), brp1))
maxDiff = np.max(np.divide(np.abs((pwl-brp1)), brp1))
plt.axvline(x1[indMaxDiff], color="red", linestyle="dashed", alpha=0.4)
plt.plot([x1[indMaxDiff], x1[indMaxDiff]], [brp1[indMaxDiff], pwl[indMaxDiff]], color="red")
plt.text(x1[indMaxDiff], brp1[indMaxDiff], '  {:.1f}%'.format(maxDiff*100), color='r')

plt.plot(x1, brp1, color='orange')
plt.plot(x2, brp2, color='b')
plt.scatter(x2, brp2, marker='x', color='b')
plt.xlim([0, 2])
plt.ylim([3, 14])
plt.xlabel('Scaled Flow')
plt.ylabel('Value of Latency Function')

plt.show()

numPieces = range(1, 50+1)
maxDiffs = []

for numPiece in numPieces:
    x = np.linspace(0, 2, num=numPiece+1)
    brp = 4 * (1 + 0.15 * np.power(x, 4))
    pwl = np.interp(x1, x, brp)
    indMaxDiff = np.argmax(np.divide(np.abs((pwl-brp1)), brp1))
    maxDiff = np.max(np.divide(np.abs((pwl-brp1)), brp1)) * 100
    maxDiffs.append(maxDiff)

plt.xlabel('Number of Pieces')
plt.ylabel('Maximal Relative Error (%)')
plt.xlim([0, 50])
plt.ylim([0, 10])
plt.plot(numPieces, maxDiffs)
plt.show()