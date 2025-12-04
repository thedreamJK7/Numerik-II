import numpy as np
import matplotlib.pyplot as plt

# Gronwall lemmasi bilan baholash
def gronwall_estimate(t, u0, alpha, beta):
    """u'(t) ≤ βu(t) + α tengsizlik uchun Gronwall bahosi"""
    return u0 * np.exp(beta * t) + (alpha/beta) * (np.exp(beta * t) - 1)

# Haqiqiy funksiya va uning Gronwall bahosi
t = np.linspace(0, 2, 100)

# Misol: u'(t) = 2u(t) + 1, u(0) = 0
u0 = 0
alpha = 1
beta = 2

# Gronwall bahosi
u_gronwall = gronwall_estimate(t, u0, alpha, beta)

# Haqiqiy yechim (tenglik holati)
u_exact = 0.5 * (np.exp(2*t) - 1)

plt.figure(figsize=(10, 6))
plt.plot(t, u_exact, 'b-', linewidth=2, label='Haqiqiy yechim: u(t) = 0.5(e^{2t} - 1)')
plt.plot(t, u_gronwall, 'r--', linewidth=2, label='Gronwall bahosi')
plt.fill_between(t, u_exact, u_gronwall, alpha=0.2, color='red')
plt.title('Gronwall Lemmasi: Tengsizlikni Baholash')
plt.xlabel('t')
plt.ylabel('u(t)')
plt.legend()
plt.grid(True)
plt.show()

print("Gronwall lemmasi har doim haqiqiy yechimdan KATTA yoki TENG baho beradi")
