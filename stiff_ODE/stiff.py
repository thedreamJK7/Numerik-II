import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')  # Suppress warnings for clarity

# ============================================
# 1. DEFINE A STIFF ODE SYSTEM
# ============================================

def stiff_system(t, y):
    """A classic stiff ODE: y' = A*y where A has eigenvalues -1000 and -1"""
    y1, y2 = y
    # Fast component: decays quickly (λ = -1000)
    # Slow component: decays slowly (λ = -1)
    dy1dt = -1000 * y1
    dy2dt = -1 * y2
    return [dy1dt, dy2dt]

# Initial conditions
y0 = [2.0, 1.0]
t_span = [0, 5]

# ============================================
# 2. NUMERICAL METHODS IMPLEMENTATION
# ============================================

def explicit_euler(f, y0, t_span, h):
    """Explicit Euler method"""
    t0, tf = t_span
    t = np.arange(t0, tf + h, h)
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    
    for i in range(len(t)-1):
        y[i+1] = y[i] + h * np.array(f(t[i], y[i]))
    
    return t, y

def implicit_euler(f, y0, t_span, h, tol=1e-8, max_iter=100):
    """Implicit Euler method (using fixed-point iteration)"""
    t0, tf = t_span
    t = np.arange(t0, tf + h, h)
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    
    for i in range(len(t)-1):
        # Initial guess
        y_guess = y[i]
        
        # Fixed-point iteration: y_{n+1} = y_n + h*f(t_{n+1}, y_{n+1})
        for _ in range(max_iter):
            f_new = np.array(f(t[i+1], y_guess))
            y_new = y[i] + h * f_new
            
            if np.linalg.norm(y_new - y_guess) < tol:
                break
            y_guess = y_new
        
        y[i+1] = y_new
    
    return t, y

# ============================================
# 3. ANALYTICAL SOLUTION (FOR COMPARISON)
# ============================================

def exact_solution(t):
    """Exact solution for our stiff system"""
    y1_exact = 2.0 * np.exp(-1000 * t)
    y2_exact = 1.0 * np.exp(-1 * t)
    return y1_exact, y2_exact

# ============================================
# 4. VISUALIZATION 1: COMPARE METHODS
# ============================================

# Time steps to test
step_sizes = [0.001, 0.002, 0.01]

plt.figure(figsize=(15, 10))

for idx, h in enumerate(step_sizes):
    # Exact solution
    t_exact = np.linspace(0, 5, 1000)
    y1_exact, y2_exact = exact_solution(t_exact)
    
    # Numerical solutions
    t_exp, y_exp = explicit_euler(stiff_system, y0, t_span, h)
    t_imp, y_imp = implicit_euler(stiff_system, y0, t_span, h)
    
    # Plot fast component (y1)
    plt.subplot(3, 2, 2*idx + 1)
    plt.plot(t_exact, y1_exact, 'k-', label='Exact', linewidth=2)
    plt.plot(t_exp, y_exp[:, 0], 'r--o', markersize=4, label=f'Explicit Euler (h={h})')
    plt.plot(t_imp, y_imp[:, 0], 'b--s', markersize=4, label=f'Implicit Euler (h={h})')
    plt.xlabel('Time')
    plt.ylabel('y1 (Fast component)')
    plt.title(f'Step size h = {h}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot slow component (y2)
    plt.subplot(3, 2, 2*idx + 2)
    plt.plot(t_exact, y2_exact, 'k-', label='Exact', linewidth=2)
    plt.plot(t_exp, y_exp[:, 1], 'r--o', markersize=4, label=f'Explicit Euler (h={h})')
    plt.plot(t_imp, y_imp[:, 1], 'b--s', markersize=4, label=f'Implicit Euler (h={h})')
    plt.xlabel('Time')
    plt.ylabel('y2 (Slow component)')
    plt.title(f'Step size h = {h}')
    plt.legend()
    plt.grid(True, alpha=0.3)

plt.suptitle('Stiff ODE: Comparison of Explicit vs Implicit Euler', fontsize=16, y=1.02)
plt.tight_layout()
plt.show()

# ============================================
# 5. VISUALIZATION 2: STABILITY REGIONS
# ============================================

def plot_stability_regions():
    """Plot stability regions in complex plane"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Stability region for Explicit Euler: |1 + hλ| ≤ 1
    theta = np.linspace(0, 2*np.pi, 400)
    # Circle centered at -1 with radius 1
    circle_real = -1 + np.cos(theta)
    circle_imag = np.sin(theta)
    
    axes[0].fill(circle_real, circle_imag, 'lightblue', alpha=0.5)
    axes[0].plot(circle_real, circle_imag, 'b-', linewidth=2)
    axes[0].set_xlim(-4, 2)
    axes[0].set_ylim(-3, 3)
    axes[0].axhline(0, color='black', alpha=0.3)
    axes[0].axvline(0, color='black', alpha=0.3)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_title('Explicit Euler Stability Region')
    axes[0].set_xlabel('Re(hλ)')
    axes[0].set_ylabel('Im(hλ)')
    
    # Mark our stiff eigenvalue locations
    h = 0.01
    eigenvalues = [-1000, -1]
    for eig in eigenvalues:
        point = h * eig
        axes[0].plot(point, 0, 'ro', markersize=10, 
                    label=f'hλ={point:.1f} (λ={eig})' if eig == -1000 else None)
    axes[0].legend()
    
    # Stability region for Implicit Euler: |1 - hλ| ≥ 1
    # Actually it's the exterior of circle centered at 1 with radius 1
    axes[1].fill_between([-6, 2], [-3, -3], [3, 3], color='lightgreen', alpha=0.3)
    # Show the unstable region (right half of the circle)
    circle_real2 = 1 + np.cos(theta)
    circle_imag2 = np.sin(theta)
    axes[1].fill(circle_real2, circle_imag2, 'white')
    axes[1].plot(circle_real2, circle_imag2, 'g-', linewidth=2)
    
    axes[1].set_xlim(-6, 2)
    axes[1].set_ylim(-3, 3)
    axes[1].axhline(0, color='black', alpha=0.3)
    axes[1].axvline(0, color='black', alpha=0.3)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_title('Implicit Euler Stability Region (A-stable)')
    axes[1].set_xlabel('Re(hλ)')
    axes[1].set_ylabel('Im(hλ)')
    
    # Mark our stiff eigenvalue locations
    for eig in eigenvalues:
        point = h * eig
        axes[1].plot(point, 0, 'ro', markersize=10, 
                    label=f'hλ={point:.1f} (λ={eig})' if eig == -1000 else None)
    axes[1].legend()
    
    plt.suptitle('Stability Regions in Complex Plane', fontsize=14)
    plt.tight_layout()
    plt.show()

plot_stability_regions()

# ============================================
# 6. VISUALIZATION 3: ERROR VS STEP SIZE
# ============================================

# Test various step sizes
step_sizes_test = np.logspace(-4, -1, 20)  # From 0.0001 to 0.1
errors_exp = []
errors_imp = []

for h in step_sizes_test:
    # Numerical solutions
    t_exp, y_exp = explicit_euler(stiff_system, y0, t_span, h)
    t_imp, y_imp = implicit_euler(stiff_system, y0, t_span, h)
    
    # Exact solution at final time
    y1_exact, y2_exact = exact_solution(t_span[1])
    y_exact_final = np.array([y1_exact, y2_exact])
    
    # Compute error (L2 norm)
    error_exp = np.linalg.norm(y_exp[-1] - y_exact_final)
    error_imp = np.linalg.norm(y_imp[-1] - y_exact_final)
    
    errors_exp.append(error_exp)
    errors_imp.append(error_imp)

plt.figure(figsize=(10, 6))
plt.loglog(step_sizes_test, errors_exp, 'ro-', linewidth=2, markersize=8, label='Explicit Euler')
plt.loglog(step_sizes_test, errors_imp, 'bs-', linewidth=2, markersize=8, label='Implicit Euler')

# Add reference lines for slope 1 (first order)
ref_x = np.array([1e-4, 1e-3])
ref_y = ref_x * 1e-3  # Arbitrary scaling
plt.loglog(ref_x, ref_y, 'k--', label='Slope 1 (O(h))')

plt.xlabel('Step size (h)')
plt.ylabel('Error at t=5 (L2 norm)')
plt.title('Error vs Step Size for Stiff ODE')
plt.grid(True, alpha=0.3, which='both')
plt.legend()
plt.tight_layout()
plt.show()

# ============================================
# 7. VISUALIZATION 4: EXPLICIT METHOD INSTABILITY
# ============================================

# Show what happens when step size is too large for explicit method
h_dangerous = 0.0021  # Just above stability limit for fast component

t_exp, y_exp = explicit_euler(stiff_system, y0, [0, 0.1], h_dangerous)
t_imp, y_imp = implicit_euler(stiff_system, y0, [0, 0.1], h_dangerous)

t_exact = np.linspace(0, 0.1, 1000)
y1_exact, y2_exact = exact_solution(t_exact)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(t_exact, y1_exact, 'k-', linewidth=2, label='Exact')
plt.plot(t_exp, y_exp[:, 0], 'r--o', markersize=6, label=f'Explicit Euler (h={h_dangerous})')
plt.plot(t_imp, y_imp[:, 0], 'b--s', markersize=4, label=f'Implicit Euler (h={h_dangerous})')
plt.xlabel('Time')
plt.ylabel('y1 (Fast component)')
plt.title('Explicit Method Becomes Unstable!')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
# Zoom in on the oscillations
plt.plot(t_exp[:20], y_exp[:20, 0], 'ro-', linewidth=2, markersize=6, label='Explicit Euler')
plt.plot(t_imp[:20], y_imp[:20, 0], 'bs-', markersize=4, label='Implicit Euler')
plt.xlabel('Time')
plt.ylabel('y1 (Fast component)')
plt.title('Zoom: Explicit Method Oscillates and Grows')
plt.legend()
plt.grid(True, alpha=0.3)

plt.suptitle(f'Step size h={h_dangerous} > 2/|λ_max| = {2/1000:.6f} (Stability limit)', fontsize=14)
plt.tight_layout()
plt.show()

# ============================================
# 8. SUMMARY TABLE
# ============================================

print("="*60)
print("SUMMARY: STIFF ODE NUMERICAL SOLUTION")
print("="*60)
print("\nSystem: y1' = -1000*y1, y2' = -1*y2")
print("Eigenvalues: λ1 = -1000 (fast), λ2 = -1 (slow)")
print("\nStability condition for Explicit Euler: |1 + hλ| ≤ 1")
print(f"For λ = -1000: |1 - 1000h| ≤ 1 → h ≤ {2/1000:.6f}")
print("\nKey Observations:")
print("1. Explicit Euler requires h ≤ 0.002 for stability")
print("2. Implicit Euler remains stable for any h > 0")
print("3. For accuracy, both methods need small h initially")
print("4. Implicit can use larger h after fast component decays")
print("="*60)