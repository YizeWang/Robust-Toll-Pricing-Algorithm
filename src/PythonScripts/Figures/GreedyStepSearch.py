import matplotlib.pyplot as plt


def recta(x1, y1, x2, y2):
    a = (y1 - y2) / (x1 - x2)
    b = y1 - a * x1
    return (a, b)

def curva_b(xa, ya, xb, yb, xc, yc):
    (x1, y1, x2, y2) = (xa, ya, xb, yb)
    (a1, b1) = recta(xa, ya, xb, yb)
    (a2, b2) = recta(xb, yb, xc, yc)
    puntos = []

    for i in range(0, 1000):
        if x1 == x2:
            continue
        else:
            (a, b) = recta(x1, y1, x2, y2)
        x = i*(x2 - x1)/1000 + x1
        y = a*x + b
        if abs(x-0.125)<0.001:
            print(y)
        puntos.append((x,y))
        x1 += (xb - xa)/1000
        y1 = a1*x1 + b1
        x2 += (xc - xb)/1000
        y2 = a2*x2 + b2

    return puntos

lista1 = curva_b(0, 1, 0.1, -1, 0.125, 0.5)
lista2 = curva_b(0.125, 0.5, 0.325, 12.5, 0.45, 8)
lista3 = curva_b(0.45, 8, 0.575, 3.5, 0.8, -3)
lista4 = curva_b(0.8, -3, 0.99, 3, 1, 12)

fig, ax = plt.subplots()
ax.plot(*zip(*lista1), c='b')
ax.plot(*zip(*lista2), c='b')
ax.plot(*zip(*lista3), c='b')
ax.plot(*zip(*lista4), c='b')
ax.scatter(0.5, 6.22, color='r',zorder=10)
ax.scatter(0.25, 6.7, color='r',zorder=10)
ax.scatter(1, 12, color='r',zorder=10)
ax.scatter(0, 1, color='r',zorder=10)
ax.scatter(0.125, 0.6, color='r',zorder=10)
ax.annotate('(0,1)', [0.01, 1.3])
ax.annotate('(0.25, 6.7)', [0.27, 6.5])
ax.annotate('(0.125, 0.6)', [0.14, 0.2])
ax.annotate('(0.5, 6.22)', [0.52, 6.4])
ax.annotate('(1.0, 12.0)', [0.83, 11.8])
plt.xlim([0,1])
plt.ylim([-3.5,13])
plt.xlabel(r'$\tau$')
plt.ylabel(r'$O$')
plt.axhline(1, color="orange", linestyle="dashed", alpha=0.4)
plt.show()
