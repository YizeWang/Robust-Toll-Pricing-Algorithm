import numpy as np
import matplotlib.pyplot as plt


x1 = np.linspace(1, 20, num=10000, endpoint=True)
y1 = 500 / x1
x2 = np.linspace(20, 40, num=10000, endpoint=True)
y2 = 10000 / x2**2
y3 = 500 / x2

plt.plot(x1, y1, label=r'$\gamma=500/i$')
plt.plot(x2, y2, label=r'$\gamma=10000/i^2$')
plt.xlabel(r'Number of Iterations $i$')
plt.ylabel(r'Step Size $\gamma$')
plt.legend()
plt.xlim([0,40])
plt.ylim([0, 500])
plt.show()
