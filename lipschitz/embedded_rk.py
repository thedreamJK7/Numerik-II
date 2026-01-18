import numpy as np
import matplotlib.pyplot as plt

# ==============================================
# VISUALIZATION: EXTRAPOLATION vs EMBEDDED
# ==============================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# ------------------------------------------------------------
# Plot 1: EXTRAPOLATION METHOD (Inefficient)
# ------------------------------------------------------------
ax1 = axes[0]

# Draw function evaluations for extrapolation
stages_extrap = ['k₁', 'k₂', 'k₃', 'k₄', 'k₅', 'k₆']
times_extrap = [0, 0.25, 0.5, 0.5, 0.75, 1.0]
colors_extrap = ['blue', 'blue', 'blue', 'red', 'red', 'red']

# Half step method (blue)
ax1.plot([0, 0.5, 1.0], [1, 2, 3], 'b-', alpha=0.3, linewidth=2, label='Half-step path')
for i in range(3):
    ax1.plot(times_extrap[i], i+1, 'bo', markersize=10)
    ax1.text(times_extrap[i], i+1.1, stages_extrap[i], ha='center', fontsize=10, color='blue')

# Full step method (red)
ax1.plot([0, 1.0], [1, 3.5], 'r--', alpha=0.3, linewidth=2, label='Full-step path')
for i in range(3, 6):
    ax1.plot(times_extrap[i], 1 + 2.5*(i-3)/2, 'ro', markersize=10)
    ax1.text(times_extrap[i], 1 + 2.5*(i-3)/2 + 0.1, stages_extrap[i], ha='center', fontsize=10, color='red')

ax1.set_xlabel('Time')
ax1.set_ylabel('Stage')
ax1.set_title('EXTRAPOLATION METHOD\n(Inefficient: 6 evaluations)', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0.5, 4)

# Add annotations
ax1.text(0.5, 0.8, 'Half-step: 3 evals\nFull-step: 3 evals\nTOTAL: 6 evals', 
         ha='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

# ------------------------------------------------------------
# Plot 2: EMBEDDED METHOD (Efficient)
# ------------------------------------------------------------
ax2 = axes[1]

# Draw shared evaluations for embedded RK
stages_embedded = ['k₁', 'k₂', 'k₃', 'k₄', 'k₅', 'k₆']
times_embedded = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
colors_shared = ['green'] * 6

# All evaluations are shared
ax2.plot(times_embedded, [1, 1.5, 2, 2.5, 3, 3.5], 'g-', alpha=0.3, linewidth=2, label='Shared evaluations')
for i in range(6):
    ax2.plot(times_embedded[i], 1 + 0.5*i, 'go', markersize=10)
    ax2.text(times_embedded[i], 1 + 0.5*i + 0.1, stages_embedded[i], ha='center', fontsize=10, color='green')

# Show both methods using same points
ax2.plot([0, 1.0], [1, 3.5], 'b--', alpha=0.5, linewidth=1, label='Method 1 (order q)')
ax2.plot([0, 1.0], [1, 3.8], 'r:', alpha=0.5, linewidth=1, label='Method 2 (order q+1)')

ax2.set_xlabel('Time')
ax2.set_ylabel('Stage')
ax2.set_title('EMBEDDED RK METHOD\n(Efficient: 6 evaluations for BOTH)', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0.5, 4)

# Add annotations
ax2.text(0.5, 0.8, 'Shared: 6 evals\nBoth methods use these\nTOTAL: 6 evals', 
         ha='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))

plt.tight_layout()
plt.show()

# ==============================================
# EXAMPLE: DOPRI5(4) - The Famous Embedded RK
# ==============================================
print("\n" + "="*60)
print("DOPRI5(4) - Most Famous Embedded RK")
print("="*60)
print("Dormand-Prince 5(4):")
print("- Main method: order 5")
print("- Embedded method: order 4")
print("- 7 stages (function evaluations)")
print("- Uses same 7 k-values for BOTH methods!")
print()

# Show the shared computations
print("Shared computations (k₁ through k₇):")
print("k₁ = f(t₀, y₀)")
print("k₂ = f(t₀ + c₂h, y₀ + h(a₂₁k₁))")
print("k₃ = f(t₀ + c₃h, y₀ + h(a₃₁k₁ + a₃₂k₂))")
print("...")
print("k₇ = f(t₀ + c₇h, y₀ + h(a₇₁k₁ + ... + a₇₆k₆))")
print()

print("Then BOTH methods use these k's:")
print("y⁵ (order 5) = y₀ + h(b₁⁵k₁ + b₂⁵k₂ + ... + b₇⁵k₇)")
print("y⁴ (order 4) = y₀ + h(b₁⁴k₁ + b₂⁴k₂ + ... + b₇⁴k₇)")
print()

print("Error estimate = |y⁵ - y⁴| ≈ local truncation error")
print("Use this for adaptive step control!")

# ==============================================
# VISUALIZE ERROR ESTIMATION & STEP CONTROL
# ==============================================

fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))

# ------------------------------------------------------------
# Plot 1: Error estimation process
# ------------------------------------------------------------
ax1 = axes2[0, 0]

# Simulate a step
t = np.linspace(0, 1, 100)
y_exact = np.exp(-t)  # Exact solution

# Simulate two approximations
y_high = np.exp(-t) + 0.1*np.exp(-5*t)  # Higher order approximation
y_low = np.exp(-t) + 0.2*np.exp(-5*t)   # Lower order approximation

ax1.plot(t, y_exact, 'k-', linewidth=3, label='Exact solution')
ax1.plot(t, y_high, 'b--', linewidth=2, label='Higher order (q+1)')
ax1.plot(t, y_low, 'r:', linewidth=2, label='Lower order (q)')

# Highlight error
ax1.fill_between(t, y_high, y_low, alpha=0.2, color='purple', label='Error estimate |y⁵ - y⁴|')

ax1.set_xlabel('Time t')
ax1.set_ylabel('y(t)')
ax1.set_title('Embedded RK: Two Approximations from Same k-values', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3)

# ------------------------------------------------------------
# Plot 2: Step size adaptation
# ------------------------------------------------------------
ax2 = axes2[0, 1]

# Simulate adaptive step sizes
times = [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.5, 3.0]
step_sizes = [0.5, 0.3, 0.2, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.4]
errors = [0.01, 0.008, 0.005, 0.002, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.003]

# Step sizes
ax2.plot(times, step_sizes, 'bo-', linewidth=2, markersize=8, label='Step size h')
ax2.set_xlabel('Time t')
ax2.set_ylabel('Step size h', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')
ax2.set_title('Adaptive Step Size Control', fontsize=12)
ax2.grid(True, alpha=0.3)

# Error on second y-axis
ax2b = ax2.twinx()
ax2b.plot(times, errors, 'rs--', linewidth=2, markersize=6, label='Error estimate')
ax2b.set_ylabel('Error estimate', color='red')
ax2b.tick_params(axis='y', labelcolor='red')

# Add threshold line
ax2b.axhline(y=0.002, color='g', linestyle='--', alpha=0.5, label='Tolerance')
ax2b.text(3.1, 0.002, 'Tolerance', va='center', color='green')

# Combine legends
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2b.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

# ------------------------------------------------------------
# Plot 3: Efficiency comparison
# ------------------------------------------------------------
ax3 = axes2[1, 0]

# Comparison of methods
methods = ['Fixed h\n(small)', 'Fixed h\n(large)', 'Extrapolation', 'Embedded RK']
evals_per_step = [4, 4, 12, 7]  # Function evaluations per step
total_steps = [100, 20, 30, 25]  # Rough estimates
total_cost = [400, 80, 360, 175]  # Total evaluations

x = np.arange(len(methods))
width = 0.25

bars1 = ax3.bar(x - width, evals_per_step, width, label='Evals/step', color='skyblue')
bars2 = ax3.bar(x, total_steps, width, label='Total steps', color='lightgreen')
bars3 = ax3.bar(x + width, total_cost, width, label='Total evals', color='salmon')

ax3.set_xlabel('Method')
ax3.set_ylabel('Count')
ax3.set_title('Efficiency Comparison', fontsize=12)
ax3.set_xticks(x)
ax3.set_xticklabels(methods)
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)

# ------------------------------------------------------------
# Plot 4: Butcher tableau for embedded RK
# ------------------------------------------------------------
ax4 = axes2[1, 1]
ax4.axis('off')

# Draw a schematic Butcher tableau
table_text = """
EMBEDDED RK BUTCHER TABLEAU:

Butcher Tableau Structure:
c | A
--+--------
  | b⁵  (5th order)
  | b⁴  (4th order)

KEY IDEA:
- Same aᵢⱼ, cᵢ for both methods
- Different bᵢ coefficients  
- 7 evaluations → TWO methods!
"""

ax4.text(0.1, 0.9, table_text, fontsize=10, va='top',
         bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9))

plt.tight_layout()
plt.show()

# ==============================================
# REAL EXAMPLE: MATLAB's ode45
# ==============================================
print("\n" + "="*60)
print("REAL-WORLD EXAMPLE: MATLAB's ode45")
print("="*60)
print("ode45 uses DOPRI5(4) - Dormand-Prince 5(4) embedded RK")
print()
print("How it works:")
print("1. Compute k₁...k₇ (7 function evaluations)")
print("2. Get TWO approximations:")
print("   - y⁵: 5th order accurate (main solution)")
print("   - y⁴: 4th order accurate (for error estimate)")
print("3. Error = |y⁵ - y⁴|")
print("4. Adjust step size based on error:")
print("   • If error > tolerance → decrease h, retry step")
print("   • If error << tolerance → increase h for next step")
print("   • If error ≈ tolerance → accept step, keep h")
print()
print("Benefits:")
print("• Automatic error control")
print("• Efficient (shared computations)")
print("• Robust (handles various problems)")
print("• User specifies tolerance, not step size")

if __name__ == "__main__":
    print("Embedded RK visualization complete!")
    print("This demonstrates the efficiency advantage of embedded methods.")