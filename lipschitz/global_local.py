import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# ODE: y' = y, y(0) = 1 (Exact solution: y(t) = e^t)
# ------------------------------------------------------------
def f(t, y):
    return y

def exact_solution(t):
    return np.exp(t)

def euler_step(t, y, h):
    """One Euler step"""
    return y + h * f(t, y)

# ------------------------------------------------------------
# SIMULATION PARAMETERS
# ------------------------------------------------------------
t0 = 0.0
t_end = 2.0
y0 = 1.0
h = 0.5  # Large step to see errors clearly
N = int((t_end - t0) / h)  # Number of steps

# Exact solution for plotting
t_exact = np.linspace(t0, t_end, 200)
y_exact = exact_solution(t_exact)

# ------------------------------------------------------------
# RUN EULER METHOD
# ------------------------------------------------------------
t_euler = [t0]
y_euler = [y0]
local_errors = []  # Store local errors at each step
global_errors = []  # Store global errors at each step

for k in range(N):
    t_k = t_euler[-1]
    y_k = y_euler[-1]
    
    # Take Euler step
    y_kplus1 = euler_step(t_k, y_k, h)
    
    # Compute LOCAL error (error made in THIS step assuming perfect start)
    y_exact_at_tk = exact_solution(t_k)
    y_exact_at_tkplus1 = exact_solution(t_k + h)
    
    # What Euler would give if starting from exact solution at t_k
    y_euler_from_exact = y_exact_at_tk + h * f(t_k, y_exact_at_tk)
    local_error = abs(y_exact_at_tkplus1 - y_euler_from_exact)
    
    # Compute GLOBAL error (actual accumulated error)
    global_error = abs(y_exact_at_tkplus1 - y_kplus1)
    
    # Store
    t_euler.append(t_k + h)
    y_euler.append(y_kplus1)
    local_errors.append(local_error)
    global_errors.append(global_error)

# Convert to arrays for plotting
t_euler = np.array(t_euler)
y_euler = np.array(y_euler)
local_errors = np.array(local_errors)
global_errors = np.array(global_errors)

# ------------------------------------------------------------
# CREATE VISUALIZATION
# ------------------------------------------------------------
fig = plt.figure(figsize=(16, 10))

# ------------------------------------------------------------
# SUBPLOT 1: OVERALL SOLUTION WITH ERRORS
# ------------------------------------------------------------
ax1 = plt.subplot(2, 3, (1, 2))

# Exact solution
ax1.plot(t_exact, y_exact, 'k-', linewidth=3, label='Exact solution: $y(t)=e^t$')

# Euler approximation
ax1.plot(t_euler, y_euler, 'ro--', linewidth=2, markersize=8, label=f'Euler method (h={h})')

# Fill between to show error accumulation
for i in range(len(t_euler)-1):
    t_segment = np.linspace(t_euler[i], t_euler[i+1], 50)
    y_exact_segment = exact_solution(t_segment)
    y_euler_segment = y_euler[i] + (t_segment - t_euler[i]) * f(t_euler[i], y_euler[i])
    
    # Color based on whether error is increasing/decreasing
    error_color = 'red' if global_errors[i] > (local_errors[i] if i>0 else 0) else 'orange'
    ax1.fill_between(t_segment, y_exact_segment, y_euler_segment, 
                      alpha=0.2, color=error_color)

# Mark step points
for i, (t, y) in enumerate(zip(t_euler, y_euler)):
    ax1.plot(t, y, 'ro', markersize=8)
    ax1.text(t, y-0.3, f'$y_{i}$', ha='center', fontsize=10, color='red')

# Arrows showing error propagation
for i in range(len(t_euler)-1):
    t_mid = (t_euler[i] + t_euler[i+1]) / 2
    y_mid_euler = (y_euler[i] + y_euler[i+1]) / 2
    y_mid_exact = exact_solution(t_mid)
    
    ax1.annotate('', xy=(t_mid, y_mid_exact), xytext=(t_mid, y_mid_euler),
                arrowprops=dict(arrowstyle='<->', color='red', lw=1.5, alpha=0.7))
    ax1.text(t_mid, (y_mid_euler + y_mid_exact)/2, f'$e_{i+1}$', 
             ha='center', va='center', backgroundcolor='white', fontsize=9)

ax1.set_xlabel('Time $t$', fontsize=12)
ax1.set_ylabel('$y(t)$', fontsize=12)
ax1.set_title('Euler Method: Solution with Global Errors $e_k$', fontsize=14, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_xlim([t0, t_end])
ax1.set_ylim([0.8, 8])

# ------------------------------------------------------------
# SUBPLOT 2: ZOOM ON ONE STEP - LOCAL ERROR
# ------------------------------------------------------------
ax2 = plt.subplot(2, 3, 3)

# Focus on step from t=0 to t=h
step_to_show = 0  # First step
t_start = t_euler[step_to_show]
t_end_step = t_euler[step_to_show + 1]

# Create detailed view
t_detail = np.linspace(t_start, t_end_step, 100)
y_exact_detail = exact_solution(t_detail)

# Euler line for this step
y_euler_line = y_euler[step_to_show] + (t_detail - t_start) * f(t_start, y_euler[step_to_show])

# What if we started from EXACT solution at t_start?
y_exact_at_start = exact_solution(t_start)
y_euler_from_exact = y_exact_at_start + (t_detail - t_start) * f(t_start, y_exact_at_start)

# Plot
ax2.plot(t_detail, y_exact_detail, 'k-', linewidth=3, label='Exact solution')
ax2.plot(t_detail, y_euler_line, 'r--', linewidth=2, label='Actual Euler step')
ax2.plot(t_detail, y_euler_from_exact, 'b--', linewidth=2, label='Euler from exact start')

# Points
ax2.plot(t_start, y_euler[step_to_show], 'ro', markersize=8, label='Start: $(t_k, y_k)$')
ax2.plot(t_start, y_exact_at_start, 'ko', markersize=8, label='Exact start: $(t_k, y(t_k))$')
ax2.plot(t_end_step, y_euler[step_to_show+1], 'rs', markersize=10, label='Euler result')
ax2.plot(t_end_step, exact_solution(t_end_step), 'k*', markersize=12, label='Exact at $t_{k+1}$')

# Highlight LOCAL error (difference between blue dashed and black at t_end)
ax2.fill_between(t_detail, y_exact_detail, y_euler_from_exact, 
                 alpha=0.3, color='blue', label='Local error region')
ax2.annotate('', xy=(t_end_step, exact_solution(t_end_step)), 
             xytext=(t_end_step, y_euler_from_exact[-1]),
             arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
ax2.text(t_end_step+0.02, (exact_solution(t_end_step) + y_euler_from_exact[-1])/2,
         'Local error\n$\\tau_k$', ha='left', va='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))

# Highlight GLOBAL error (difference between red dashed and black at t_end)
ax2.annotate('', xy=(t_end_step, exact_solution(t_end_step)), 
             xytext=(t_end_step, y_euler_line[-1]),
             arrowprops=dict(arrowstyle='<->', color='red', lw=2))
ax2.text(t_end_step-0.02, (exact_solution(t_end_step) + y_euler_line[-1])/2,
         'Global error\n$e_{k+1}$', ha='right', va='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="pink"))

ax2.set_xlabel('Time $t$', fontsize=12)
ax2.set_ylabel('$y(t)$', fontsize=12)
ax2.set_title(f'Step {step_to_show+1}: Local vs Global Error', fontsize=14, fontweight='bold')
ax2.legend(loc='upper left', fontsize=9)
ax2.grid(True, alpha=0.3)

# ------------------------------------------------------------
# SUBPLOT 3: ERROR PROPAGATION DIAGRAM
# ------------------------------------------------------------
ax3 = plt.subplot(2, 3, 4)

# Create schematic of error propagation
step_positions = np.arange(N+1)
global_error_vals = [0] + list(global_errors)
local_error_vals = [0] + list(local_errors)

# Plot error propagation
ax3.plot(step_positions, global_error_vals, 'ro-', linewidth=2, markersize=8, 
         label='Global error $e_k$')
ax3.plot(step_positions[1:], local_error_vals[1:], 'bs--', linewidth=2, markersize=8,
         label='Local error $\\tau_k$')

# Add arrows showing how local errors contribute to global
for k in range(N):
    ax3.annotate('', xy=(k+1, global_error_vals[k+1]), 
                 xytext=(k, global_error_vals[k]),
                 arrowprops=dict(arrowstyle='->', color='green', lw=1.5, alpha=0.7))
    
    # Label with amplification factor
    if k > 0 and (global_error_vals[k] + local_error_vals[k+1]) > 0:
        amplification = global_error_vals[k+1] / (global_error_vals[k] + local_error_vals[k+1])
        ax3.text(k+0.5, (global_error_vals[k] + global_error_vals[k+1])/2,
                f'×{amplification:.2f}', ha='center', va='bottom',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="yellow", alpha=0.7))

ax3.set_xlabel('Step number $k$', fontsize=12)
ax3.set_ylabel('Error magnitude', fontsize=12)
ax3.set_title('Error Propagation: How Local Errors Become Global', fontsize=14, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

# ------------------------------------------------------------
# SUBPLOT 4: ANALOGY - WALKING WITH IMPERFECT STEPS
# ------------------------------------------------------------
ax4 = plt.subplot(2, 3, 5)

# Create walking analogy
target_position = 10  # Want to walk 10 meters
step_sizes = [1.0, 0.9, 1.1, 0.95, 1.05]  # Imperfect steps
N_steps = len(step_sizes)

positions = [0]
for step in step_sizes:
    positions.append(positions[-1] + step)

# Plot
step_x = np.arange(N_steps + 1)
ax4.bar(step_x, positions, alpha=0.3, color='skyblue', edgecolor='blue')
ax4.plot(step_x, positions, 'bo-', linewidth=2, markersize=8, label='Actual path')

# Target line
ax4.axhline(y=target_position, color='k', linestyle='--', linewidth=2, label='Target position')

# Perfect steps (1.0 each)
perfect_positions = np.arange(N_steps + 1) * (target_position / N_steps)
ax4.plot(step_x, perfect_positions, 'r--', linewidth=2, label='Perfect steps')

# Annotations
for i in range(N_steps):
    # Local error: difference from perfect step IF starting perfectly
    local_err = abs(step_sizes[i] - (target_position / N_steps))
    
    # Global error: actual accumulated difference
    global_err = abs(positions[i+1] - perfect_positions[i+1])
    
    ax4.text(i+0.5, positions[i+1]+0.2, f'L={local_err:.2f}\nG={global_err:.2f}', 
             ha='center', fontsize=8,
             bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))

ax4.set_xlabel('Step number', fontsize=12)
ax4.set_ylabel('Position (meters)', fontsize=12)
ax4.set_title('Walking Analogy:\nLocal vs Global Position Error', fontsize=14, fontweight='bold')
ax4.legend(loc='upper left')
ax4.grid(True, alpha=0.3)

# ------------------------------------------------------------
# SUBPLOT 5: MATHEMATICAL RELATIONSHIP
# ------------------------------------------------------------
ax5 = plt.subplot(2, 3, 6)

# Show the recurrence relation
text_content = r"""
Local Error τₖ:
τₖ = y(t_{k+1}) - [y(tₖ) + hΦ(tₖ, y(tₖ), h)]

Global Error eₖ:
eₖ = y(tₖ) - Yₖ

Recurrence Relation:
e_{k+1} = eₖ + h[L eₖ] + hτₖ

Simplified:
e_{k+1} ≈ (1 + hL)eₖ + hτₖ

Solution (Gronwall):
eₖ ≤ e^{LT} Σⱼ₌₀^{k-1} hτⱼ

Key Insight:
• Local error = error in ONE step
• Global error = accumulated errors  
• Small local error + Stability ⇒ Small global error
"""

ax5.text(0.1, 0.95, text_content, fontsize=10, va='top',
         bbox=dict(boxstyle="round,pad=1.0", facecolor="lightyellow", edgecolor="orange"))
ax5.set_xticks([])
ax5.set_yticks([])
ax5.set_title('Mathematical Relationship', fontsize=14, fontweight='bold')
ax5.axis('off')

# ------------------------------------------------------------
# ADD SUMMARY TEXT
# ------------------------------------------------------------
plt.figtext(0.02, 0.02, 
            'Summary: Local error τₖ = error made in step k assuming perfect start. '
            'Global error eₖ = accumulated error after k steps. '
            'Even with small local errors, global error can grow exponentially if method is unstable.',
            fontsize=10, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))

plt.tight_layout(rect=[0, 0.05, 1, 0.98])
plt.show()

# ------------------------------------------------------------
# PRINT NUMERICAL VALUES
# ------------------------------------------------------------
print("="*70)
print("LOCAL vs GLOBAL ERROR - NUMERICAL EXAMPLE")
print("="*70)
print(f"ODE: y' = y, y(0) = 1, Step size h = {h}")
print(f"Exact solution: y(t) = e^t")
print()

for k in range(N):
    print(f"Step {k+1}: t = {t_euler[k]:.1f} → {t_euler[k+1]:.1f}")
    print(f"  Exact at t_k: y({t_euler[k]:.1f}) = {exact_solution(t_euler[k]):.6f}")
    print(f"  Euler at t_k: Y_{k} = {y_euler[k]:.6f}")
    print(f"  Global error e_{k} = {abs(exact_solution(t_euler[k]) - y_euler[k]):.6f}")
    
    # What Euler would give starting from exact solution
    y_euler_from_exact_k = exact_solution(t_euler[k]) + h * f(t_euler[k], exact_solution(t_euler[k]))
    print(f"  Euler from exact start would give: {y_euler_from_exact_k:.6f}")
    print(f"  Exact at t_{k+1}: y({t_euler[k+1]:.1f}) = {exact_solution(t_euler[k+1]):.6f}")
    print(f"  Local error τ_{k} = {local_errors[k]:.6f}")
    print(f"  Actual Euler gives: Y_{k+1} = {y_euler[k+1]:.6f}")
    print(f"  New global error e_{k+1} = {global_errors[k]:.6f}")
    print()

if __name__ == "__main__":
    print("Running Local vs Global Error Analysis...")
    print("This visualization shows the difference between local and global errors in numerical methods.")