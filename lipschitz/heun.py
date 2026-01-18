import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. DEFINE THE ODE AND EXACT SOLUTION (for comparison)
# ------------------------------------------------------------
def f(t, y):
    """The ODE: y' = -y + t + 1"""
    return -y + t + 1

def exact_solution(t):
    """Exact solution for y' = -y + t + 1, y(0) = 1"""
    return t + np.exp(-t)

# ------------------------------------------------------------
# 2. NUMERICAL METHODS
# ------------------------------------------------------------
def euler_step(f, t, y, h):
    """One step of Euler's method"""
    return y + h * f(t, y)

def heun_step(f, t, y, h):
    """One step of Heun's method (improved Euler)"""
    k1 = f(t, y)
    k2 = f(t + h, y + h * k1)
    return y + h * (k1 + k2) / 2

# ------------------------------------------------------------
# 3. SOLVE ODE WITH BOTH METHODS
# ------------------------------------------------------------
def solve_ode(method, f, t0, y0, t_end, h):
    """Solve ODE using specified method"""
    t_values = [t0]
    y_values = [y0]
    
    t = t0
    y = y0
    
    while t < t_end - 1e-10:  # Small tolerance for floating point
        y = method(f, t, y, h)
        t = t + h
        t_values.append(t)
        y_values.append(y)
    
    return np.array(t_values), np.array(y_values)

# ------------------------------------------------------------
# 4. PARAMETERS
# ------------------------------------------------------------
t0 = 0.0
t_end = 2.0
y0 = 1.0
h = 0.4  # Try changing this: 0.2, 0.1, 0.05

# ------------------------------------------------------------
# 5. COMPUTE SOLUTIONS
# ------------------------------------------------------------
# Exact solution for plotting
t_exact = np.linspace(t0, t_end, 200)
y_exact = exact_solution(t_exact)

# Numerical solutions
t_euler, y_euler = solve_ode(euler_step, f, t0, y0, t_end, h)
t_heun, y_heun = solve_ode(heun_step, f, t0, y0, t_end, h)

# ------------------------------------------------------------
# 6. VISUALIZE
# ------------------------------------------------------------
plt.figure(figsize=(12, 8))

# Plot 1: Solutions comparison
plt.subplot(2, 2, 1)
plt.plot(t_exact, y_exact, 'k-', linewidth=2, label='Exact Solution')
plt.plot(t_euler, y_euler, 'bo--', linewidth=1.5, markersize=6, label=f'Euler (h={h})')
plt.plot(t_heun, y_heun, 'rs--', linewidth=1.5, markersize=6, label=f'Heun (h={h})')
plt.xlabel('Time t')
plt.ylabel('y(t)')
plt.title('Euler vs Heun Methods')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Errors
plt.subplot(2, 2, 2)
# Compute errors at common time points
t_common = np.linspace(t0, t_end, 20)
y_exact_common = exact_solution(t_common)

# Interpolate numerical solutions to common times
y_euler_interp = np.interp(t_common, t_euler, y_euler)
y_heun_interp = np.interp(t_common, t_heun, y_heun)

error_euler = np.abs(y_exact_common - y_euler_interp)
error_heun = np.abs(y_exact_common - y_heun_interp)

plt.plot(t_common, error_euler, 'bo-', label=f'Euler Error (max={error_euler.max():.4f})')
plt.plot(t_common, error_heun, 'rs-', label=f'Heun Error (max={error_heun.max():.4f})')
plt.xlabel('Time t')
plt.ylabel('Absolute Error')
plt.title('Error Comparison')
plt.legend()
plt.grid(True, alpha=0.3)
plt.yscale('log')  # Log scale to better see differences

# ------------------------------------------------------------
# 7. VISUALIZE ONE STEP IN DETAIL
# ------------------------------------------------------------
# Let's zoom into first step
plt.subplot(2, 2, 3)

# Create detailed plot around first step
t_step = np.linspace(t0, t0 + h, 100)
y_exact_step = exact_solution(t_step)

# Euler step visualization
y_euler_step = y0 + f(t0, y0) * (t_step - t0)

# Heun step visualization
k1 = f(t0, y0)
k2 = f(t0 + h, y0 + h * k1)
slope_avg = (k1 + k2) / 2
y_heun_step = y0 + slope_avg * (t_step - t0)

plt.plot(t_step, y_exact_step, 'k-', linewidth=2, label='Exact')
plt.plot(t_step, y_euler_step, 'b--', linewidth=2, label='Euler (slope at start)')
plt.plot(t_step, y_heun_step, 'r--', linewidth=2, label='Heun (avg slope)')

# Mark points
plt.plot(t0, y0, 'ko', markersize=8, label='Start (t₀, y₀)')
plt.plot(t0 + h, y_euler[1], 'bo', markersize=8, label='Euler endpoint')
plt.plot(t0 + h, y_heun[1], 'ro', markersize=8, label='Heun endpoint')
plt.plot(t0 + h, exact_solution(t0 + h), 'k*', markersize=10, label='Exact endpoint')

plt.xlabel('Time t')
plt.ylabel('y(t)')
plt.title(f'First Step Detail (h={h})')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)

# ------------------------------------------------------------
# 8. SLOPE FIELD VISUALIZATION
# ------------------------------------------------------------
plt.subplot(2, 2, 4)

# Create slope field
t_grid, y_grid = np.meshgrid(np.linspace(t0, t_end, 15), 
                             np.linspace(0.5, 2.5, 15))

# Calculate slopes
slopes = f(t_grid, y_grid)

# Normalize arrow lengths for visualization
norm = np.sqrt(1 + slopes**2)
dt_arrow = 0.1 / norm
dy_arrow = slopes * dt_arrow

plt.quiver(t_grid, y_grid, dt_arrow, dy_arrow, angles='xy', 
           scale_units='xy', scale=2, alpha=0.6, color='gray')

# Overlay solutions
plt.plot(t_exact, y_exact, 'k-', linewidth=2, label='Exact')
plt.plot(t_euler, y_euler, 'bo--', linewidth=1, markersize=4, label='Euler')
plt.plot(t_heun, y_heun, 'rs--', linewidth=1, markersize=4, label='Heun')

plt.xlabel('Time t')
plt.ylabel('y(t)')
plt.title('Slope Field with Solutions')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 9. PRINT NUMERICAL RESULTS
# ------------------------------------------------------------
print("="*60)
print("NUMERICAL RESULTS COMPARISON")
print("="*60)
print(f"Step size: h = {h}")
print(f"Time interval: [{t0}, {t_end}]")
print(f"Initial condition: y({t0}) = {y0}")
print()

# Final values
y_exact_final = exact_solution(t_end)
print(f"Exact solution at t={t_end}:  y = {y_exact_final:.6f}")
print(f"Euler method at t={t_end}:    y = {y_euler[-1]:.6f} (error = {abs(y_exact_final - y_euler[-1]):.6f})")
print(f"Heun method at t={t_end}:     y = {y_heun[-1]:.6f} (error = {abs(y_exact_final - y_heun[-1]):.6f})")
print()

# Convergence rates (test with different h)
print("="*60)
print("CONVERGENCE STUDY")
print("="*60)
hs = [0.4, 0.2, 0.1, 0.05]
errors_euler = []
errors_heun = []

for h_test in hs:
    # Euler
    t_e, y_e = solve_ode(euler_step, f, t0, y0, t_end, h_test)
    error_e = abs(exact_solution(t_end) - y_e[-1])
    errors_euler.append(error_e)
    
    # Heun
    t_h, y_h = solve_ode(heun_step, f, t0, y0, t_end, h_test)
    error_h = abs(exact_solution(t_end) - y_h[-1])
    errors_heun.append(error_h)
    
    print(f"h={h_test:.3f}: Euler error={error_e:.6f}, Heun error={error_h:.6f}")

# Compute convergence rates
print()
print("Convergence rates (error ~ h^p):")
for i in range(len(hs)-1):
    rate_euler = np.log(errors_euler[i]/errors_euler[i+1]) / np.log(2)
    rate_heun = np.log(errors_heun[i]/errors_heun[i+1]) / np.log(2)
    print(f"h {hs[i]}→{hs[i+1]}: Euler p≈{rate_euler:.2f}, Heun p≈{rate_heun:.2f}")