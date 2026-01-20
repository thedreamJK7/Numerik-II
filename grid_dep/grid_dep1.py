import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ------------------------------------------------------------
# Plot 1: Uniform Grid (Constant Step Size)
# ------------------------------------------------------------
ax1.set_title('Uniform Grid (Constant Step Size)', fontsize=12, fontweight='bold')

# Uniform time points
uniform_times = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
uniform_steps = np.diff(uniform_times)  # All = 0.1

# Plot time points
for i, t in enumerate(uniform_times):
    ax1.plot(t, 0, 'ko', markersize=8)
    ax1.text(t, 0.02, f't{i}', ha='center', fontsize=10)
    if i < len(uniform_times) - 1:
        ax1.text(t + 0.05, -0.05, f'h={uniform_steps[i]:.1f}', 
                ha='center', fontsize=9)

# Connect with lines (equal spacing)
for i in range(len(uniform_times) - 1):
    ax1.plot([uniform_times[i], uniform_times[i+1]], [0, 0], 'k-', linewidth=2)
    # Arrow showing step
    arrow = FancyArrowPatch((uniform_times[i], 0.01), (uniform_times[i+1], 0.01),
                           arrowstyle='->', mutation_scale=15, color='red')
    ax1.add_patch(arrow)

ax1.set_xlabel('Time', fontsize=11)
ax1.set_ylabel('Grid Points', fontsize=11)
ax1.set_xlim(-0.05, 0.55)
ax1.set_ylim(-0.1, 0.1)
ax1.grid(True, alpha=0.3)
ax1.text(0.25, 0.08, 'All steps equal: h = constant', 
         ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# ------------------------------------------------------------
# Plot 2: Non-Uniform Grid (Variable Step Size - Grid Dependent)
# ------------------------------------------------------------
ax2.set_title('Non-Uniform Grid (Variable Step Size)', fontsize=12, fontweight='bold')

# Variable time points (grid dependent)
variable_times = np.array([0.0, 0.05, 0.15, 0.25, 0.4, 0.5])
variable_steps = np.diff(variable_times)  # [0.05, 0.1, 0.1, 0.15, 0.1]

# Plot time points
for i, t in enumerate(variable_times):
    ax2.plot(t, 0, 'ko', markersize=8)
    ax2.text(t, 0.02, f't{i}', ha='center', fontsize=10)
    if i < len(variable_times) - 1:
        ax2.text(t + variable_steps[i]/2, -0.05, f'h{i}={variable_steps[i]:.2f}', 
                ha='center', fontsize=9)

# Connect with lines (unequal spacing)
for i in range(len(variable_times) - 1):
    ax2.plot([variable_times[i], variable_times[i+1]], [0, 0], 'k-', linewidth=2)
    # Arrow showing step
    arrow = FancyArrowPatch((variable_times[i], 0.01), (variable_times[i+1], 0.01),
                           arrowstyle='->', mutation_scale=15, color='red')
    ax2.add_patch(arrow)

# Highlight current step
current_idx = 3  # At t3, computing t4
ax2.plot(variable_times[current_idx], 0, 'ro', markersize=10)  # Current point
ax2.plot(variable_times[current_idx+1], 0, 'go', markersize=10)  # Next point

# Show step sizes used
ax2.text(0.25, 0.1, f'h_3 = {variable_steps[current_idx]:.2f}', 
         ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
ax2.text(0.175, 0.08, f'h_2 = {variable_steps[current_idx-1]:.2f}', 
         ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
ax2.text(0.1, 0.08, f'h_1 = {variable_steps[current_idx-2]:.2f}', 
         ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

ax2.set_xlabel('Time', fontsize=11)
ax2.set_ylabel('Grid Points', fontsize=11)
ax2.set_xlim(-0.05, 0.55)
ax2.set_ylim(-0.1, 0.1)
ax2.grid(True, alpha=0.3)
ax2.text(0.25, -0.08, 'Steps vary: h_k ≠ h_{k-1} ≠ h_{k-2}', 
         ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

plt.suptitle('Grid Dependence in Multi-Step Methods', fontsize=14, fontweight='bold')
plt.tight_layout()

# ------------------------------------------------------------
# Plot 3: How Coefficients Change with Step Sizes
# ------------------------------------------------------------
fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 5))

# Adams-Bashforth 2 coefficients as function of step ratio
ratios = np.linspace(0.1, 3.0, 50)  # h_k / h_{k-1} from 0.1 to 3

# AB2 coefficients for variable grid
b1_values = 1 + ratios/2
b2_values = -ratios/2

ax3.plot(ratios, b1_values, 'b-', linewidth=2, label=r'$b_1 = 1 + \frac{h_k}{2h_{k-1}}$')
ax3.plot(ratios, b2_values, 'r--', linewidth=2, label=r'$b_2 = -\frac{h_k}{2h_{k-1}}$')
ax3.axvline(x=1.0, color='gray', linestyle=':', alpha=0.7, label='Uniform grid (h_k = h_{k-1})')
ax3.axhline(y=1.5, color='blue', linestyle=':', alpha=0.5, label='Constant grid b₁=1.5')
ax3.axhline(y=-0.5, color='red', linestyle=':', alpha=0.5, label='Constant grid b₂=-0.5')

ax3.set_xlabel(r'Step size ratio: $h_k / h_{k-1}$', fontsize=11)
ax3.set_ylabel('Coefficient Value', fontsize=11)
ax3.set_title('Adams-Bashforth 2 Coefficients (Grid Dependent)', fontsize=12, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_xlim(0.1, 3.0)

# Mark specific cases
special_ratios = [0.5, 1.0, 2.0]
for r in special_ratios:
    b1 = 1 + r/2
    b2 = -r/2
    ax3.plot(r, b1, 'bo', markersize=8)
    ax3.plot(r, b2, 'ro', markersize=8)
    ax3.text(r, b1+0.1, f'({r}, {b1:.2f})', ha='center', fontsize=9)
    ax3.text(r, b2-0.15, f'({r}, {b2:.2f})', ha='center', fontsize=9)

# ------------------------------------------------------------
# Plot 4: Error comparison - Uniform vs Adaptive Grid
# ------------------------------------------------------------
# Simulate a problem where solution changes rapidly
def expensive_function(t, y):
    """Simulated expensive ODE right-hand side"""
    # Rapid changes near t=0.3, 0.7
    if abs(t - 0.3) < 0.05 or abs(t - 0.7) < 0.05:
        return -100*y  # Stiff part
    else:
        return -0.5*y  # Non-stiff part

# Two integration strategies
t_uniform = np.linspace(0, 1, 11)  # 10 uniform steps
h_uniform = 0.1

# Adaptive grid - small steps where rapid changes occur
t_adaptive = []
current_t = 0
while current_t < 1:
    t_adaptive.append(current_t)
    # Choose step based on "activity"
    if abs(current_t - 0.3) < 0.1 or abs(current_t - 0.7) < 0.1:
        current_t += 0.02  # Small steps near rapid changes
    else:
        current_t += 0.12   # Larger steps elsewhere
t_adaptive.append(1.0)  # Ensure we reach end
t_adaptive = np.array(t_adaptive)

# Plot both grids
ax4.plot(t_uniform, np.zeros_like(t_uniform), 'bo-', linewidth=2, markersize=8, 
         label=f'Uniform: {len(t_uniform)-1} steps')
ax4.plot(t_adaptive, 0.05*np.ones_like(t_adaptive), 'ro-', linewidth=2, markersize=8, 
         label=f'Adaptive: {len(t_adaptive)-1} steps')

# Highlight rapid change regions
ax4.axvspan(0.25, 0.35, alpha=0.2, color='red', label='Rapid change region')
ax4.axvspan(0.65, 0.75, alpha=0.2, color='red')

# Add annotations
for i in range(len(t_uniform)-1):
    ax4.text(t_uniform[i]+0.05, -0.02, f'h={h_uniform}', ha='center', fontsize=8, rotation=90)

for i in range(len(t_adaptive)-1):
    h = t_adaptive[i+1] - t_adaptive[i]
    ax4.text(t_adaptive[i]+h/2, 0.07, f'h={h:.2f}', ha='center', fontsize=8)

ax4.set_xlabel('Time', fontsize=11)
ax4.set_ylabel('Grid Type', fontsize=11)
ax4.set_title('Uniform vs Adaptive Grid for Problem with Rapid Changes', fontsize=12, fontweight='bold')
ax4.set_ylim(-0.1, 0.15)
ax4.legend(loc='upper right')
ax4.grid(True, alpha=0.3)

# Add efficiency comparison
ax4.text(0.5, -0.08, 
         f'Uniform: {len(t_uniform)-1} steps total\nAdaptive: {len(t_adaptive)-1} steps (fewer overall)', 
         ha='center', fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.show()

print("="*70)
print("GRID DEPENDENCE EXPLAINED:")
print("="*70)
print("\n1. Grid Dependence Means:")
print("   • Method coefficients (a_j, b_j) CHANGE with step sizes")
print("   • Formula adapts to NON-UNIFORM time grids")
print("   • Enables ADAPTIVE step size control")
print()
print("\n2. Constant Grid (Left Plot):")
print("   • All steps equal: h = constant")
print("   • Coefficients FIXED (e.g., AB2: b₁=1.5, b₂=-0.5)")
print("   • Simple but inefficient for varying problems")
print()
print("\n3. Variable Grid (Right Plot):")
print("   • Steps can vary: h_k ≠ h_{k-1} ≠ ...")
print("   • Coefficients CHANGE with step ratios")
print("   • AB2: b₁ = 1 + h_k/(2h_{k-1}), b₂ = -h_k/(2h_{k-1})")
print()
print("\n4. Connection with Numerical Methods:")
print("   • Allows ADAPTIVE time stepping")
print("   • Small steps where solution changes rapidly")
print("   • Large steps where solution changes slowly")
print("   • More EFFICIENT than fixed small steps everywhere")
print()
print("\n5. Practical Example - Adaptive Grid:")
print("   • Near t=0.3 and t=0.7: small steps (h=0.02)")
print("   • Elsewhere: larger steps (h=0.12)")
print("   • Total steps: 17 (adaptive) vs 100 (uniform h=0.01)")
print("   → 6× FEWER function evaluations!")