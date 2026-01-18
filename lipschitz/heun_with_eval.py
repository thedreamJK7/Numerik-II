import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# ODE: y' = f(t, y) = -y + 2 (simple example)
# ------------------------------------------------------------
def f(t, y):
    return -y + 2

def exact_solution(t, t0=0, y0=1):
    """Exact solution: y' = -y + 2, y(0)=1"""
    return 2 - np.exp(-t)

# ------------------------------------------------------------
# PARAMETERS FOR ONE STEP
# ------------------------------------------------------------
t0 = 0.0          # Start time
y0 = 1.0          # Initial value
h = 1.0           # Step size (large to see clearly)
t1 = t0 + h       # End time

# ------------------------------------------------------------
# HEUN'S METHOD STEP BY STEP
# ------------------------------------------------------------
print("="*60)
print("HEUN'S METHOD - STEP BY STEP")
print("="*60)

# Step 1: Compute k₁ (slope at beginning)
k1 = f(t0, y0)
print(f"Step 1: k₁ = f(t₀, y₀) = f({t0}, {y0}) = {k1:.4f}")
print(f"       This is the slope at the START point")

# Step 2: Euler predictor
y_euler = y0 + h * k1
print(f"\nStep 2: Euler predictor")
print(f"       y_pred = y₀ + h·k₁ = {y0} + {h}·{k1:.4f} = {y_euler:.4f}")
print(f"       This gives predicted point at (t₁, y_pred) = ({t1}, {y_euler:.4f})")

# Step 3: Compute k₂ (slope at predicted point)
k2 = f(t1, y_euler)
print(f"\nStep 3: k₂ = f(t₁, y_pred) = f({t1}, {y_euler:.4f}) = {k2:.4f}")
print(f"       This is the slope at the PREDICTED point")

# Step 4: Average slopes
slope_avg = (k1 + k2) / 2
print(f"\nStep 4: Average slope")
print(f"       (k₁ + k₂)/2 = ({k1:.4f} + {k2:.4f})/2 = {slope_avg:.4f}")

# Step 5: Heun update
y_heun = y0 + h * slope_avg
print(f"\nStep 5: Heun update")
print(f"       y_heun = y₀ + h·(k₁+k₂)/2 = {y0} + {h}·{slope_avg:.4f} = {y_heun:.4f}")

# Exact solution for comparison
y_exact = exact_solution(t1)
error_euler = abs(y_exact - y_euler)
error_heun = abs(y_exact - y_heun)

print(f"\nExact solution at t={t1}: y = {y_exact:.4f}")
print(f"Euler error: {error_euler:.4f}")
print(f"Heun error:  {error_heun:.4f}")

# ------------------------------------------------------------
# VISUALIZATION
# ------------------------------------------------------------
plt.figure(figsize=(14, 10))

# Create time points for plotting exact solution
t_plot = np.linspace(t0, t1, 100)
y_exact_plot = exact_solution(t_plot)

# ------------------------------------------------------------
# SUBPLOT 1: COMPLETE VIEW
# ------------------------------------------------------------
plt.subplot(2, 2, 1)

# Exact solution
plt.plot(t_plot, y_exact_plot, 'k-', linewidth=3, label='Exact Solution')

# Points
plt.plot(t0, y0, 'ko', markersize=10, label=f'Start: (t₀, y₀) = ({t0}, {y0})')
plt.plot(t1, y_euler, 'bo', markersize=10, label=f'Euler: ({t1}, {y_euler:.3f})')
plt.plot(t1, y_heun, 'ro', markersize=10, label=f'Heun: ({t1}, {y_heun:.3f})')
plt.plot(t1, y_exact, 'k*', markersize=15, label=f'Exact: ({t1}, {y_exact:.3f})')

# Euler line (using k₁)
t_euler = [t0, t1]
y_euler_line = [y0, y_euler]
plt.plot(t_euler, y_euler_line, 'b--', linewidth=2, label=f'Euler: slope k₁ = {k1:.3f}')

# Heun line (using average slope)
y_heun_line = [y0, y_heun]
plt.plot(t_euler, y_heun_line, 'r-', linewidth=3, label=f'Heun: avg slope = {slope_avg:.3f}')

# Slope at predicted point (k₂)
# Draw short line segment at predicted point to show k₂ slope
t_k2 = [t1 - 0.2, t1 + 0.2]
y_k2 = [y_euler - 0.2*k2, y_euler + 0.2*k2]
plt.plot(t_k2, y_k2, 'g:', linewidth=2, label=f'Slope k₂ = {k2:.3f}')

plt.xlabel('Time t')
plt.ylabel('y(t)')
plt.title(f'Heun Method - Complete View (h={h})')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)

# ------------------------------------------------------------
# SUBPLOT 2: SLOPE VISUALIZATION
# ------------------------------------------------------------
plt.subplot(2, 2, 2)

# Create slope field
t_slope = np.linspace(t0 - 0.2, t1 + 0.2, 20)
y_slope = np.linspace(0.8, 2.2, 20)
T, Y = np.meshgrid(t_slope, y_slope)
slopes = f(T, Y)

# Normalize arrows for better visualization
norm = np.sqrt(1 + slopes**2)
dt_arr = 0.15 / norm
dy_arr = slopes * dt_arr

plt.quiver(T, Y, dt_arr, dy_arr, angles='xy', scale_units='xy', 
           scale=3, alpha=0.3, color='gray')

# Plot the key elements
plt.plot(t_plot, y_exact_plot, 'k-', linewidth=2, label='Exact')
plt.plot([t0, t1], [y0, y_euler], 'b--', linewidth=2, label=f'Euler: slope k₁')
plt.plot([t0, t1], [y0, y_heun], 'r-', linewidth=3, label=f'Heun: avg slope')

# Mark the slopes as vectors
plt.arrow(t0, y0, 0.8, 0.8*k1, head_width=0.03, head_length=0.05, 
          fc='blue', ec='blue', alpha=0.7, label='k₁ vector')
plt.arrow(t1, y_euler, 0.8, 0.8*k2, head_width=0.03, head_length=0.05, 
          fc='green', ec='green', alpha=0.7, label='k₂ vector')

plt.plot(t0, y0, 'ko', markersize=10)
plt.plot(t1, y_euler, 'bo', markersize=10)
plt.plot(t1, y_heun, 'ro', markersize=10)
plt.plot(t1, y_exact, 'k*', markersize=12)

plt.xlabel('Time t')
plt.ylabel('y(t)')
plt.title('Slope Field with k₁ and k₂ Vectors')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)

# ------------------------------------------------------------
# SUBPLOT 3: STEP-BY-STEP DIAGRAM
# ------------------------------------------------------------
plt.subplot(2, 2, 3)

# Draw numbered steps
plt.plot([t0, t0], [0, y0], 'k:', alpha=0.5)
plt.plot([t1, t1], [0, y0], 'k:', alpha=0.5)

# Step 1: k₁
plt.text(t0, -0.15, 'Step 1: k₁ = f(t₀,y₀)', ha='center', fontsize=10, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
plt.arrow(t0, -0.1, 0, y0+0.1, head_width=0.03, head_length=0.05, 
          fc='blue', ec='blue', alpha=0.5)

# Step 2: Euler predictor
plt.text((t0+t1)/2, y0-0.2, 'Step 2: Predict\nusing k₁', ha='center', fontsize=9,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
plt.plot([t0, t1], [y0, y_euler], 'g--', linewidth=2)

# Step 3: k₂
plt.text(t1, y_euler+0.1, 'Step 3: k₂ = f(t₁,y_pred)', ha='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="orange"))
plt.arrow(t1, y_euler-0.1, 0, 0.2, head_width=0.03, head_length=0.05,
          fc='orange', ec='orange', alpha=0.5)

# Step 4: Average
plt.text((t0+t1)/2, (y0+y_heun)/2+0.1, 'Step 4: Average\nslopes', ha='center', fontsize=9,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

# Step 5: Update
plt.text(t1, y_heun-0.15, 'Step 5: Update\nusing average', ha='center', fontsize=9,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="pink"))

# Final lines
plt.plot([t0, t1], [y0, y_heun], 'r-', linewidth=3)
plt.plot([t0, t1], [y0, y_euler], 'b--', linewidth=2)

# Points
plt.plot(t0, y0, 'ko', markersize=10)
plt.plot(t1, y_euler, 'bo', markersize=10)
plt.plot(t1, y_heun, 'ro', markersize=10)
plt.plot(t1, y_exact, 'k*', markersize=12)

plt.xlabel('Time t')
plt.ylabel('y(t)')
plt.title('Step-by-Step Visualization')
plt.grid(True, alpha=0.3)
plt.ylim(-0.2, 2.2)

# ------------------------------------------------------------
# SUBPLOT 4: ERROR COMPARISON FOR DIFFERENT h
# ------------------------------------------------------------
plt.subplot(2, 2, 4)

hs = [2.0, 1.0, 0.5, 0.25, 0.125]
errors_euler = []
errors_heun = []

for h_test in hs:
    # Euler
    y_e = y0 + h_test * f(t0, y0)
    errors_euler.append(abs(exact_solution(h_test) - y_e))
    
    # Heun
    k1_test = f(t0, y0)
    k2_test = f(t0 + h_test, y0 + h_test * k1_test)
    y_h = y0 + h_test * (k1_test + k2_test) / 2
    errors_heun.append(abs(exact_solution(h_test) - y_h))

plt.loglog(hs, errors_euler, 'bo-', linewidth=2, markersize=8, label='Euler Error')
plt.loglog(hs, errors_heun, 'rs-', linewidth=2, markersize=8, label='Heun Error')

# Add reference slopes
x_ref = [0.125, 0.5]
plt.loglog(x_ref, [0.3, 0.3*4], 'b:', alpha=0.5, label='Slope 1 (Euler)')
plt.loglog(x_ref, [0.01, 0.01*4], 'r:', alpha=0.5, label='Slope 2 (Heun)')

plt.xlabel('Step size h (log scale)')
plt.ylabel('Error at t=h (log scale)')
plt.title('Error vs Step Size (log-log)')
plt.legend()
plt.grid(True, alpha=0.3, which='both')

# Add text about convergence rates
plt.text(0.15, 0.3, 'Euler: error ~ h¹\nHeun: error ~ h²', 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# ADDITIONAL EXPLANATION
# ------------------------------------------------------------
print("\n" + "="*60)
print("KEY INSIGHTS FROM THE GRAPH:")
print("="*60)
print("1. k₁ = slope at STARTING point (t₀, y₀)")
print("2. Use k₁ to PREDICT where we'll be: y_pred = y₀ + h·k₁")
print("3. k₂ = slope at PREDICTED point (t₁, y_pred)")
print("4. AVERAGE the slopes: (k₁ + k₂)/2")
print("5. Use AVERAGE slope for the final update")
print()
print("WHY THIS IS BETTER THAN EULER:")
print("- Euler uses ONLY the starting slope (k₁)")
print("- Heun CORRECTS by checking slope at predicted point (k₂)")
print("- Average gives better estimate of slope over the WHOLE interval")
print()
print("CONVERGENCE:")
print("- Euler: error decreases like h¹ (halve h → halve error)")
print("- Heun: error decreases like h² (halve h → quarter error)")