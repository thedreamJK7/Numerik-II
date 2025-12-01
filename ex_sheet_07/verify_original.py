import numpy as np

# From the photo: y'(t) = -λ(y(t) - e^(-t)) - e^(-t)
# Claimed exact solution: y(t) = e^(-t) for all λ

print("Verifying the exact solution from the problem statement:")
print("ODE: y'(t) = -λ(y(t) - e^(-t)) - e^(-t)")
print("Claimed: y(t) = e^(-t) for all λ")
print()

# If y(t) = e^(-t), then y'(t) = -e^(-t)
print("If y(t) = e^(-t):")
print("  y'(t) = -e^(-t)")
print()

# Check if it satisfies the ODE
print("Substitute into ODE:")
print("  RHS = -λ(e^(-t) - e^(-t)) - e^(-t)")
print("      = -λ(0) - e^(-t)")
print("      = -e^(-t)")
print()
print("  LHS = y'(t) = -e^(-t)")
print()
print("  LHS = RHS ✓")
print()

# Check initial condition
print("Check y(0) = e^0 = 1 ✓")
print()

# Numerical verification
print("Numerical verification:")
for lam in [1, 1000]:
    t = 0.5
    y = np.exp(-t)
    y_prime_exact = -np.exp(-t)
    y_prime_ode = -lam * (y - np.exp(-t)) - np.exp(-t)
    print(f"λ = {lam}, t = {t}:")
    print(f"  y'(exact)    = {y_prime_exact:.10f}")
    print(f"  y'(from ODE) = {y_prime_ode:.10f}")
    print(f"  Match: {np.isclose(y_prime_exact, y_prime_ode)}")
    print()

print("="*60)
print("CONCLUSION: The original problem statement is CORRECT!")
print("y(t) = e^(-t) IS the exact solution for all λ")
print("="*60)
