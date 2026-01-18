import numpy as np
import matplotlib.pyplot as plt

# The ODE: y' = t - y
def f(t, y):
    return t - y

# Exact solution for comparison: y(t) = t - 1 + 2*exp(-t)
def exact_solution(t):
    return t - 1 + 2*np.exp(-t)

# Parameters
h = 0.1  # step size
t_vals = [0, 0.1, 0.2, 0.3]  # time points
y_exact = exact_solution(np.array(t_vals))

# Store our computed values
y_computed = np.zeros(len(t_vals))

print("="*60)
print("SIMPLE MULTI-STEP METHOD EXAMPLE")
print("="*60)
print(f"ODE: y' = t - y,  y(0) = 1,  h = {h}")
print()

# Step 1: Initial value
y_computed[0] = 1.0
print(f"Step 0: t = {t_vals[0]}, y = {y_computed[0]:.6f} (given)")
print(f"  f(t0, y0) = f({t_vals[0]}, {y_computed[0]}) = {f(t_vals[0], y_computed[0]):.6f}")
print()

# Step 2: Compute y1 using Euler (to start the multi-step method)
y_computed[1] = y_computed[0] + h * f(t_vals[0], y_computed[0])
print(f"Step 1 (Euler): t = {t_vals[1]}")
print(f"  y1 = y0 + h*f(t0, y0)")
print(f"     = {y_computed[0]} + {h}*{f(t_vals[0], y_computed[0])}")
print(f"     = {y_computed[1]:.6f}")
print(f"  f(t1, y1) = f({t_vals[1]}, {y_computed[1]:.6f}) = {f(t_vals[1], y_computed[1]):.6f}")
print()

# Step 3: Now use Adams-Bashforth 2-step
print("Now using Adams-Bashforth 2-step method:")
print("Formula: y_{k+1} = y_k + h * [1.5*f_k - 0.5*f_{k-1}]")
print()

# Step 3a: Compute y2
print(f"Step 2: Compute y2 at t = {t_vals[2]}")
print(f"  We need: f1 = {f(t_vals[1], y_computed[1]):.6f}, f0 = {f(t_vals[0], y_computed[0]):.6f}")
y_computed[2] = y_computed[1] + h * (1.5*f(t_vals[1], y_computed[1]) - 0.5*f(t_vals[0], y_computed[0]))
print(f"  y2 = y1 + h*(1.5*f1 - 0.5*f0)")
print(f"     = {y_computed[1]:.6f} + {h}*(1.5*{f(t_vals[1], y_computed[1]):.6f} - 0.5*{f(t_vals[0], y_computed[0]):.6f})")
print(f"     = {y_computed[1]:.6f} + {h}*({1.5*f(t_vals[1], y_computed[1]):.6f} - {0.5*f(t_vals[0], y_computed[0]):.6f})")
print(f"     = {y_computed[1]:.6f} + {h}*({1.5*f(t_vals[1], y_computed[1]) - 0.5*f(t_vals[0], y_computed[0]):.6f})")
print(f"     = {y_computed[2]:.6f}")
print(f"  f(t2, y2) = f({t_vals[2]}, {y_computed[2]:.6f}) = {f(t_vals[2], y_computed[2]):.6f}")
print()

# Step 3b: Compute y3
print(f"Step 3: Compute y3 at t = {t_vals[3]}")
print(f"  We need: f2 = {f(t_vals[2], y_computed[2]):.6f}, f1 = {f(t_vals[1], y_computed[1]):.6f}")
y_computed[3] = y_computed[2] + h * (1.5*f(t_vals[2], y_computed[2]) - 0.5*f(t_vals[1], y_computed[1]))
print(f"  y3 = y2 + h*(1.5*f2 - 0.5*f1)")
print(f"     = {y_computed[2]:.6f} + {h}*(1.5*{f(t_vals[2], y_computed[2]):.6f} - 0.5*{f(t_vals[1], y_computed[1]):.6f})")
print(f"     = {y_computed[2]:.6f} + {h}*({1.5*f(t_vals[2], y_computed[2]):.6f} - {0.5*f(t_vals[1], y_computed[1]):.6f})")
print(f"     = {y_computed[2]:.6f} + {h}*({1.5*f(t_vals[2], y_computed[2]) - 0.5*f(t_vals[1], y_computed[1]):.6f})")
print(f"     = {y_computed[3]:.6f}")
print()

# Summary table
print("="*60)
print("RESULTS SUMMARY")
print("="*60)
print(f"{'t':>6} {'Multi-Step':>12} {'Exact':>12} {'Error':>12}")
print("-"*45)
for i in range(len(t_vals)):
    error = abs(y_computed[i] - y_exact[i])
    print(f"{t_vals[i]:6.2f} {y_computed[i]:12.6f} {y_exact[i]:12.6f} {error:12.6f}")

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Solution trajectory
t_fine = np.linspace(0, 0.3, 100)
ax1.plot(t_fine, exact_solution(t_fine), 'k-', label='Exact Solution', alpha=0.7, linewidth=2)
ax1.plot(t_vals, y_computed, 'ro-', linewidth=2, markersize=8, label='Multi-Step (AB2)')
ax1.set_xlabel('t')
ax1.set_ylabel('y(t)')
ax1.set_title('Multi-Step Method Solution')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Annotate each point
for i, (t, y) in enumerate(zip(t_vals, y_computed)):
    ax1.annotate(f'y{i}', xy=(t, y), xytext=(5, 5), 
                textcoords='offset points', fontweight='bold')

# Plot 2: Step-by-step diagram
ax2.axis('off')
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)

# Draw step diagram
y_pos = 8
step_info = [
    ("Step 0: y₀ = 1.0 (given)", "f₀ = 0 - 1 = -1"),
    ("Step 1: Euler: y₁ = 1 + 0.1×(-1) = 0.9", "f₁ = 0.1 - 0.9 = -0.8"),
    ("Step 2: AB2: y₂ = 0.9 + 0.1×(1.5×(-0.8) - 0.5×(-1))", "= 0.9 + 0.1×(-0.7) = 0.83"),
    ("Step 3: AB2: y₃ = 0.83 + 0.1×(1.5×(-0.63) - 0.5×(-0.8))", "= 0.83 + 0.1×(-0.545) = 0.7755")
]

for i, (main_text, detail_text) in enumerate(step_info):
    # Draw a box for each step
    box = plt.Rectangle((1, y_pos-0.5), 8, 1, fill=True, 
                       facecolor='lightblue', edgecolor='black', alpha=0.7)
    ax2.add_patch(box)
    
    # Add step number
    ax2.text(0.5, y_pos, f'Step {i}', ha='right', va='center', 
            fontweight='bold', fontsize=10)
    
    # Add main text
    ax2.text(1.1, y_pos+0.2, main_text, ha='left', va='center', fontsize=9)
    
    # Add detail text
    ax2.text(1.1, y_pos-0.2, detail_text, ha='left', va='center', 
            fontsize=9, style='italic')
    
    # Draw arrow to next step
    if i < len(step_info) - 1:
        ax2.arrow(5, y_pos-0.8, 0, -1.2, head_width=0.2, 
                 head_length=0.2, fc='black', ec='black')
    
    y_pos -= 2

ax2.set_title('Computation Steps', fontsize=12, fontweight='bold', y=0.95)

plt.suptitle('Simple Multi-Step Method Example: Adams-Bashforth 2-Step', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("WHAT WE DID:")
print("="*60)
print("1. Used Euler method for 1 step (to get started)")
print("2. Used Adams-Bashforth 2-step for remaining steps")
print("3. Each multi-step needs only ONE new f evaluation")
print("4. Reuses previous f value from memory")
print("\nKey benefit: After startup, only 1 function evaluation per step!")