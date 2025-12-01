import numpy as np

# Verify the exact solution satisfies the ODE: y' = -λy - e^(-t), y(0) = 1

def verify_lambda_1():
    print("Verifying λ = 1:")
    print("y(t) = (1 - t) * e^(-t)")
    print("y'(t) = -e^(-t) + (1-t)*(-e^(-t)) = -e^(-t) - (1-t)*e^(-t) = -(2-t)*e^(-t)")
    print("But wait, let me recalculate:")
    print("y'(t) = d/dt[(1-t)*e^(-t)] = -e^(-t) + (1-t)*(-e^(-t)) = -e^(-t) - e^(-t) + t*e^(-t)")
    print("     = -2e^(-t) + t*e^(-t) = (-2 + t)*e^(-t)")
    print()
    print("Check ODE: -λy - e^(-t) = -1*(1-t)*e^(-t) - e^(-t)")
    print("         = -(1-t)*e^(-t) - e^(-t) = -e^(-t) + t*e^(-t) - e^(-t)")
    print("         = -2e^(-t) + t*e^(-t) = (-2 + t)*e^(-t) ✓")
    print()
    print("Check y(0) = (1-0)*e^0 = 1 ✓")
    print()

def verify_lambda_general():
    print("Verifying λ ≠ 1:")
    print("y(t) = -1/(λ-1) * e^(-t) + λ/(λ-1) * e^(-λt)")
    print()
    print("y'(t) = -1/(λ-1) * (-e^(-t)) + λ/(λ-1) * (-λ*e^(-λt))")
    print("      = 1/(λ-1) * e^(-t) - λ²/(λ-1) * e^(-λt)")
    print()
    print("Check ODE: -λy - e^(-t)")
    print("         = -λ*[-1/(λ-1)*e^(-t) + λ/(λ-1)*e^(-λt)] - e^(-t)")
    print("         = λ/(λ-1)*e^(-t) - λ²/(λ-1)*e^(-λt) - e^(-t)")
    print("         = [λ/(λ-1) - 1]*e^(-t) - λ²/(λ-1)*e^(-λt)")
    print("         = [λ - (λ-1)]/(λ-1)*e^(-t) - λ²/(λ-1)*e^(-λt)")
    print("         = 1/(λ-1)*e^(-t) - λ²/(λ-1)*e^(-λt) ✓")
    print()
    print("Check y(0) = -1/(λ-1)*1 + λ/(λ-1)*1 = [-1 + λ]/(λ-1) = (λ-1)/(λ-1) = 1 ✓")
    print()

# Numerical verification
def numerical_check():
    print("Numerical verification:")
    t = 0.5
    
    # λ = 1
    lam = 1
    y = (1 - t) * np.exp(-t)
    y_prime_numerical = -2*np.exp(-t) + t*np.exp(-t)
    y_prime_ode = -lam * y - np.exp(-t)
    print(f"λ = {lam}, t = {t}:")
    print(f"  y'(analytical) = {y_prime_numerical:.10f}")
    print(f"  y'(from ODE)   = {y_prime_ode:.10f}")
    print(f"  Match: {np.isclose(y_prime_numerical, y_prime_ode)}")
    print()
    
    # λ = 1000
    lam = 1000
    y = -1/(lam-1) * np.exp(-t) + lam/(lam-1) * np.exp(-lam*t)
    y_prime_numerical = 1/(lam-1) * np.exp(-t) - lam**2/(lam-1) * np.exp(-lam*t)
    y_prime_ode = -lam * y - np.exp(-t)
    print(f"λ = {lam}, t = {t}:")
    print(f"  y'(analytical) = {y_prime_numerical:.10e}")
    print(f"  y'(from ODE)   = {y_prime_ode:.10e}")
    print(f"  Match: {np.isclose(y_prime_numerical, y_prime_ode)}")

verify_lambda_1()
verify_lambda_general()
numerical_check()
