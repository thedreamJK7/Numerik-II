import numpy as np

# Mashqda aytilgan: y(t) = e^(-t) aniq yechim
# y'(t) = -e^(-t)

# Mashqdagi formula: y'(t) = -λ*y(t) - e^(-t) - e^(-t)

# Tekshirish: y = e^(-t) ni qo'yamiz
t = 0.5
lam = 1
y = np.exp(-t)
y_prime_exact = -np.exp(-t)

# Mashqdagi formula bilan
y_prime_formula = -lam * y - np.exp(-t) - np.exp(-t)

print(f"t = {t}")
print(f"y = e^(-t) = {y}")
print(f"y' (aniq) = -e^(-t) = {y_prime_exact}")
print(f"y' (formula) = -λ*y - 2*e^(-t) = {y_prime_formula}")
print(f"Mos keladimi? {np.isclose(y_prime_exact, y_prime_formula)}")

print("\n" + "="*50)
print("Agar formula to'g'ri bo'lsa:")
print("-e^(-t) = -λ*e^(-t) - 2*e^(-t)")
print("-e^(-t) = -(λ+2)*e^(-t)")
print("Bu faqat λ = -1 da to'g'ri!")
print("="*50)

print("\nEhtimol mashqda typo bor. Keling, to'g'ri formulani topaylik:")
print("Agar y'(t) = -λ*(y - e^(-t)) - e^(-t) bo'lsa:")
y_prime_corrected = -lam * (y - np.exp(-t)) - np.exp(-t)
print(f"y' (corrected) = {y_prime_corrected}")
print(f"Mos keladimi? {np.isclose(y_prime_exact, y_prime_corrected)}")
