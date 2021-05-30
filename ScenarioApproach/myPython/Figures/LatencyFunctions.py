import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 100, num=1000)

a = 0.10
b = 1.0
yAffine = a * x + b

t0 = 1.0
C = 25
P = 4
B = 0.15
yBRP = t0 * (1 + B * (x / C) ** P)

derAffine = a * np.ones_like(x)
derBRP = t0 * B / C ** P * x ** (P - 1)

plt.figure("Latency Function Values")
plt.plot(x, yAffine, label="Affine Latency Function")
plt.plot(x, yBRP, label="BRP Latency Function")
plt.xlabel("Flow (vehicles/minute)")
plt.ylabel("Travel Time (minutes)")
plt.legend()
plt.xlim([0, 100])
plt.ylim([0, 40])

plt.figure("Latency Function Derivatives")
plt.plot(x, derAffine, label="Affine Latency Function")
plt.plot(x, derBRP, label="BRP Latency Function")
plt.xlabel("Flow (vehicles/minute)")
plt.ylabel("Derivative of Travel Time")
plt.legend()
plt.xlim([0, 100])
plt.ylim([0, 0.4])
plt.show()