import numpy as np
import matplotlib.pyplot as plt

# Simple interpolation without scipy
def simple_interp1d(x_points, y_points, x_new, kind='linear'):
    """Simple interpolation without scipy dependency"""
    if kind == 'linear':
        return np.interp(x_new, x_points, y_points)
    else:  # cubic approximation
        result = np.zeros_like(x_new)
        for i, x in enumerate(x_new):
            # Find nearest points for cubic fit
            idx = np.searchsorted(x_points, x)
            idx = max(1, min(idx, len(x_points)-2))
            
            # Use 4 points for cubic if available
            if len(x_points) >= 4:
                start_idx = max(0, idx-2)
                end_idx = min(len(x_points), start_idx+4)
                x_sub = x_points[start_idx:end_idx]
                y_sub = y_points[start_idx:end_idx]
                
                if len(x_sub) >= 3:
                    coeffs = np.polyfit(x_sub, y_sub, min(3, len(x_sub)-1))
                    result[i] = np.polyval(coeffs, x)
                else:
                    result[i] = np.interp(x, x_points, y_points)
            else:
                result[i] = np.interp(x, x_points, y_points)
        return result

# ==============================================
# ODE: y' = cos(t) - y, y(0)=0
# Exact solution: y(t) = 0.5*(sin(t) - cos(t) + e^{-t})
# ==============================================
def f(t, y):
    return np.cos(t) - y

def exact_solution(t):
    return 0.5*(np.sin(t) - np.cos(t) + np.exp(-t))

# ==============================================
# CLASSICAL RK4 (Discrete)
# ==============================================
def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h/2, y + h*k1/2)
    k3 = f(t + h/2, y + h*k2/2)
    k4 = f(t + h, y + h*k3)
    return y + h*(k1 + 2*k2 + 2*k3 + k4)/6, [k1, k2, k3, k4]

# ==============================================
# CONTINUOUS RK4 (CRK4)
# ==============================================
def crk4_weights(theta):
    """Continuous extension weights for RK4 (Dormand-Prince)"""
    b1 = theta - 1.5*theta**2 + (2/3)*theta**3
    b2 = theta**2 - (2/3)*theta**3
    b3 = b2  # Same as b2
    b4 = -0.5*theta**2 + (2/3)*theta**3
    return [b1, b2, b3, b4]

def crk4_interpolate(Yk, h, K, theta):
    """Evaluate continuous solution at t = t_k + θh"""
    weights = crk4_weights(theta)
    return Yk + h * sum(w*k for w, k in zip(weights, K))

# ==============================================
# SIMULATION
# ==============================================
t0, t_end = 0, 3.0
h = 0.5
N = int((t_end - t0) / h)

# Store solutions
t_points = [t0]
Y_points = [0]
K_all = []  # Store k-values at each step

# Step 1: Solve with RK4 (compute discrete points)
y = 0
t = t0
for k in range(N):
    y_next, K = rk4_step(f, t, y, h)
    
    t_points.append(t + h)
    Y_points.append(y_next)
    K_all.append(K)  # Store k-values for this step
    
    y = y_next
    t = t + h

# Step 2: Compare interpolation methods
t_dense = np.linspace(t0, t_end, 500)
y_exact_dense = exact_solution(t_dense)

# Linear interpolation (naive)
y_linear_dense = simple_interp1d(t_points, Y_points, t_dense, kind='linear')

# Cubic spline (better but not optimal)
y_cubic_dense = simple_interp1d(t_points, Y_points, t_dense, kind='cubic')

# Continuous RK4 interpolation
y_crk4_dense = np.zeros_like(t_dense)
for i, t_val in enumerate(t_dense):
    # Find which step contains t_val
    step_idx = int((t_val - t0) // h)
    step_idx = min(step_idx, N-1)  # Clamp to last step
    
    t_k = t0 + step_idx * h
    theta = (t_val - t_k) / h
    theta = max(0, min(1, theta))  # Clamp to [0, 1]
    
    y_crk4_dense[i] = crk4_interpolate(Y_points[step_idx], h, K_all[step_idx], theta)

# ==============================================
# VISUALIZATION
# ==============================================
fig = plt.figure(figsize=(16, 12))

# ------------------------------------------------------------
# Plot 1: OVERVIEW - All interpolation methods
# ------------------------------------------------------------
ax1 = plt.subplot(3, 3, (1, 2))

ax1.plot(t_dense, y_exact_dense, 'k-', linewidth=3, alpha=0.8, label='Exact solution')
ax1.plot(t_dense, y_linear_dense, 'r--', linewidth=2, label='Linear interpolation')
ax1.plot(t_dense, y_cubic_dense, 'g:', linewidth=2, label='Cubic spline')
ax1.plot(t_dense, y_crk4_dense, 'b-', linewidth=2, label='Continuous RK4')
ax1.plot(t_points, Y_points, 'ko', markersize=8, label='RK4 nodes')

# Highlight one step for detailed view
highlight_step = 2  # Third step
t_highlight_start = t0 + highlight_step * h
t_highlight_end = t_highlight_start + h
ax1.axvspan(t_highlight_start, t_highlight_end, alpha=0.1, color='orange', label='Step for detailed view')

ax1.set_xlabel('Time t', fontsize=12)
ax1.set_ylabel('y(t)', fontsize=12)
ax1.set_title('Interpolation Methods Comparison', fontsize=14, fontweight='bold')
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, alpha=0.3)

# ------------------------------------------------------------
# Plot 2: ERROR COMPARISON
# ------------------------------------------------------------
ax2 = plt.subplot(3, 3, 3)

errors = {
    'Linear': np.abs(y_linear_dense - y_exact_dense),
    'Cubic': np.abs(y_cubic_dense - y_exact_dense),
    'CRK4': np.abs(y_crk4_dense - y_exact_dense)
}

# Box plot of errors
positions = [1, 2, 3]
methods = ['Linear', 'Cubic', 'CRK4']
box_data = [errors['Linear'], errors['Cubic'], errors['CRK4']]

bp = ax2.boxplot(box_data, positions=positions, widths=0.6, patch_artist=True)

# Color boxes
colors = ['lightcoral', 'lightgreen', 'lightblue']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax2.set_xticks(positions)
ax2.set_xticklabels(methods)
ax2.set_ylabel('Absolute Error', fontsize=12)
ax2.set_title('Error Distribution', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_yscale('log')

# Add mean error values
for i, method in enumerate(methods):
    mean_err = np.mean(errors[method])
    ax2.text(i+1, mean_err*1.5, f'mean={mean_err:.2e}', 
             ha='center', fontsize=9, bbox=dict(boxstyle="round,pad=0.2", facecolor="white"))

# ------------------------------------------------------------
# Plot 3: ZOOM ON ONE STEP - Continuous RK4 Construction
# ------------------------------------------------------------
ax3 = plt.subplot(3, 3, 4)

# Focus on highlighted step
step_idx = highlight_step
t_k = t0 + step_idx * h
Y_k = Y_points[step_idx]
K = K_all[step_idx]

# Generate continuous solution for this step
theta_vals = np.linspace(0, 1, 100)
t_step = t_k + theta_vals * h
y_crk4_step = np.array([crk4_interpolate(Y_k, h, K, theta) for theta in theta_vals])
y_exact_step = exact_solution(t_step)

# Plot exact and CRK4 for this step
ax3.plot(t_step, y_exact_step, 'k-', linewidth=3, label='Exact')
ax3.plot(t_step, y_crk4_step, 'b-', linewidth=2, label='Continuous RK4')

# Show the RK4 nodes
ax3.plot([t_k, t_k + h], [Y_k, Y_points[step_idx+1]], 'ko', markersize=8, label='RK4 nodes')

# Visualize the weighted combination
for i, k_val in enumerate(K):
    if i == 0:  # Only show first component to avoid clutter
        weights_i = np.array([crk4_weights(theta)[i] for theta in theta_vals])
        weight_curve = Y_k + h * weights_i * k_val
        ax3.plot(t_step, weight_curve, '--', alpha=0.5, linewidth=1, 
                 label=f'h·b_{i+1}(θ)·k_{i+1}')

ax3.set_xlabel(f'Time t (step {step_idx})', fontsize=12)
ax3.set_ylabel('y(t)', fontsize=12)
ax3.set_title('Continuous RK4: Weighted Sum of k-values', fontsize=14, fontweight='bold')
ax3.legend(loc='upper right', fontsize=8)
ax3.grid(True, alpha=0.3)

# ------------------------------------------------------------
# Plot 4: WEIGHT FUNCTIONS b_i(θ)
# ------------------------------------------------------------
ax4 = plt.subplot(3, 3, 5)

theta = np.linspace(0, 1, 100)
# Compute all weight functions for all theta values
all_weights = np.array([crk4_weights(t) for t in theta])

for i in range(4):
    if i == 2:
        continue  # Skip b3 (same as b2)
    
    b_i = all_weights[:, i]
    label = f'b_{i+1}(θ)'
    ax4.plot(theta, b_i, linewidth=2, label=label)

ax4.set_xlabel('θ (fraction of step)', fontsize=12)
ax4.set_ylabel('Weight b_i(θ)', fontsize=12)
ax4.set_title('Continuous RK4 Weight Functions', fontsize=14, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.axhline(y=0, color='k', linestyle='-', alpha=0.3, linewidth=0.5)

# ------------------------------------------------------------
# Plot 5: HOW k-VALUES ARE REUSED
# ------------------------------------------------------------
ax5 = plt.subplot(3, 3, 6)

# Draw a computational graph
nodes = ['t_k', 'k₁', 'k₂', 'k₃', 'k₄', 'Y_{k+1}', 'CRK(θ)']
node_pos = [(0, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 2), (2.5, 1)]

for (x, y), label in zip(node_pos, nodes):
    ax5.plot(x, y, 'o', markersize=12 if label == 'CRK(θ)' else 8, 
             color='red' if 'k' in label else 'blue')
    ax5.text(x, y + 0.15, label, ha='center', fontsize=10, fontweight='bold')

# Draw connections
connections = [
    (0, 1), (0, 1),  # t_k → k₁
    (0, 2), (1, 2),  # t_k, k₁ → k₂
    (0, 3), (2, 3),  # t_k, k₂ → k₃  
    (0, 4), (3, 4),  # t_k, k₃ → k₄
    (0, 5), (1, 5), (2, 5), (3, 5), (4, 5),  # All → Y_{k+1}
    (1, 6), (2, 6), (3, 6), (4, 6)  # All k's → CRK(θ)
]

for i, j in connections:
    xi, yi = node_pos[i]
    xj, yj = node_pos[j]
    ax5.plot([xi, xj], [yi, yj], 'k-', alpha=0.3, linewidth=1)

ax5.text(2.5, 0.5, 'CRK(θ) = Y_k + hΣb_i(θ)k_i\nSame k-values, different weights!', 
         ha='center', fontsize=9,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))

ax5.set_xlim(-0.5, 5.5)
ax5.set_ylim(0, 4)
ax5.set_title('Computational Graph: Reusing k-values', fontsize=14, fontweight='bold')
ax5.axis('off')

# ------------------------------------------------------------
# Plot 6: ERROR VS θ FOR ONE STEP
# ------------------------------------------------------------
ax6 = plt.subplot(3, 3, 7)

theta_test = np.linspace(0, 1, 50)
errors_crk4 = []
errors_linear = []

for theta in theta_test:
    t_val = t_k + theta * h
    # CRK4
    y_crk4 = crk4_interpolate(Y_k, h, K, theta)
    errors_crk4.append(abs(y_crk4 - exact_solution(t_val)))
    
    # Linear interpolation between nodes
    y_linear = Y_k + theta * (Y_points[step_idx+1] - Y_k)
    errors_linear.append(abs(y_linear - exact_solution(t_val)))

ax6.plot(theta_test, errors_crk4, 'b-', linewidth=2, label='Continuous RK4')
ax6.plot(theta_test, errors_linear, 'r--', linewidth=2, label='Linear interpolation')

ax6.set_xlabel('θ (position in step)', fontsize=12)
ax6.set_ylabel('Local Error', fontsize=12)
ax6.set_title(f'Error vs Position in Step', fontsize=14, fontweight='bold')
ax6.legend()
ax6.grid(True, alpha=0.3)
ax6.set_yscale('log')

# ------------------------------------------------------------
# Plot 7: ORDER OF ACCURACY CONFIRMATION
# ------------------------------------------------------------
ax7 = plt.subplot(3, 3, 8)

# Test different step sizes
hs = [0.5, 0.25, 0.125, 0.0625]
max_errors_crk4 = []
max_errors_linear = []
max_errors_cubic = []

for h_test in hs:
    # Quick simulation
    t_pts = [t0]
    y_pts = [0]
    k_all_test = []
    
    y = 0
    t = t0
    while t < t_end - 1e-10:
        y_next, K_test = rk4_step(f, t, y, h_test)
        t_pts.append(t + h_test)
        y_pts.append(y_next)
        k_all_test.append(K_test)
        y = y_next
        t = t + h_test
    
    # Sample at midpoints of each step
    errors_step_crk4 = []
    errors_step_linear = []
    
    for i in range(len(k_all_test)):
        t_k_test = t0 + i * h_test
        theta = 0.5  # Midpoint
        
        # CRK4
        y_crk4_test = crk4_interpolate(y_pts[i], h_test, k_all_test[i], theta)
        errors_step_crk4.append(abs(y_crk4_test - exact_solution(t_k_test + theta*h_test)))
        
        # Linear
        y_linear_test = y_pts[i] + theta * (y_pts[i+1] - y_pts[i])
        errors_step_linear.append(abs(y_linear_test - exact_solution(t_k_test + theta*h_test)))
    
    max_errors_crk4.append(np.max(errors_step_crk4))
    max_errors_linear.append(np.max(errors_step_linear))

# Plot convergence
ax7.loglog(hs, max_errors_crk4, 'bo-', linewidth=2, markersize=8, label='CRK4')
ax7.loglog(hs, max_errors_linear, 'rs--', linewidth=2, markersize=8, label='Linear')

# Reference slopes
x_ref = [0.1, 0.5]
ax7.loglog(x_ref, [0.01, 0.01*5], 'k:', alpha=0.5, label='Slope 1 (O(h))')
ax7.loglog(x_ref, [0.0001, 0.0001*16], 'k--', alpha=0.5, label='Slope 4 (O(h⁴))')

ax7.set_xlabel('Step size h', fontsize=12)
ax7.set_ylabel('Maximum Error at θ=0.5', fontsize=12)
ax7.set_title('Convergence Rate', fontsize=14, fontweight='bold')
ax7.legend()
ax7.grid(True, alpha=0.3, which='both')

# ------------------------------------------------------------
# Plot 8: SUMMARY - WHY CRK MATTERS
# ------------------------------------------------------------
ax8 = plt.subplot(3, 3, 9)
ax8.axis('off')

summary_text = """
CONTINUOUS RUNGE-KUTTA KEY IDEAS:

1. Same k-values for entire step
   - Compute k₁, k₂, k₃, k₄ once
   - Reuse for all θ ∈ [0,1]

2. Weight functions bᵢ(θ)
   - Polynomials in θ
   - Cheap to evaluate
   - Designed for high order

3. Continuous formula:
   y(tₖ + θh) ≈ Yₖ + h∑bᵢ(θ)kᵢ

4. Benefits:
   • Same accuracy as RK4 everywhere
   • No extra f-evaluations
   • Smooth solution between nodes
   • Accurate event detection

Cost: Same as RK4!
Accuracy: O(h⁴) uniformly!
"""

ax8.text(0.1, 0.95, summary_text, fontsize=10, va='top',
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9))

plt.suptitle('Continuous Runge-Kutta: High-Order Accurate Continuous Solution from Discrete Computation', 
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()