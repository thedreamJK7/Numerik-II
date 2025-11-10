import numpy as np
import matplotlib.pyplot as plt

# y' = y² differensial tenglamaning yechimi
def exact_solution(t, C):
    return 1 / (C - t)

# Grafik chizish
t1 = np.linspace(0, 0.9, 100)  # t=1 dan oldin
t2 = np.linspace(1.1, 2, 100)  # t=1 dan keyin

y1 = exact_solution(t1, 1)  # y(0)=1 => C=1
y2 = exact_solution(t2, 1)

plt.figure(figsize=(10, 6))
plt.plot(t1, y1, 'b-', linewidth=2, label='t=1 gacha')
plt.plot(t2, y2, 'r-', linewidth=2, label='t=1 dan keyin')
plt.axvline(x=1, color='red', linestyle='--', alpha=0.7, label='t=1 (cheksizlik)')
plt.title('y\' = y², y(0) = 1\nYechim t=1 da "portlaydi" (blow-up)')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.ylim(-10, 10)
plt.show()

print("t=0.9 da: y =", exact_solution(0.9, 1))
print("t=0.99 da: y =", exact_solution(0.99, 1))
print("t=1.01 da: y =", exact_solution(1.01, 1))
