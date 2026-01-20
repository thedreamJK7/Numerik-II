import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# ------------------------------------------------------------
# Plot 1: What is a GRID? (Time discretization)
# ------------------------------------------------------------
ax1 = axes[0, 0]
ax1.set_title('What is a "GRID"?', fontsize=12, fontweight='bold')

# Create time grid from t=0 to t=1
t_grid = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

# Draw the grid lines (vertical lines)
for t in t_grid:
    ax1.axvline(x=t, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax1.plot(t, 0, 'ko', markersize=10, zorder=5)  # Grid point
    ax1.text(t, -0.15, f't={t}', ha='center', fontsize=10)

# Label the grid
ax1.text(0.5, 0.9, 'TIME GRID = Collection of time points', 
         ha='center', fontsize=11,
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Show step sizes (horizontal arrows)
for i in range(len(t_grid)-1):
    mid_t = (t_grid[i] + t_grid[i+1]) / 2
    ax1.annotate('', xy=(t_grid[i+1], 0.05), xytext=(t_grid[i], 0.05),
                arrowprops=dict(arrowstyle='<->', color='red', linewidth=2))
    ax1.text(mid_t, 0.1, f'h{i+1}={t_grid[i+1]-t_grid[i]:.1f}', 
             ha='center', fontsize=10)

ax1.set_xlabel('Time (t)', fontsize=11)
ax1.set_ylabel('Grid Points', fontsize=11)
ax1.set_xlim(-0.1, 1.1)
ax1.set_ylim(-0.2, 1.2)
ax1.grid(False)
ax1.set_yticks([])

# ------------------------------------------------------------
# Plot 2: What is a NODE? (Solution points on grid)
# ------------------------------------------------------------
ax2 = axes[0, 1]
ax2.set_title('What are "NODES"?', fontsize=12, fontweight='bold')

# Same time grid
t_grid = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

# Sample solution y(t) = e^{-t} (just for visualization)
y_true = np.exp(-t_grid)

# Draw the grid lines
for t in t_grid:
    ax2.axvline(x=t, color='gray', linestyle='--', alpha=0.5, linewidth=1)

# Plot true solution (continuous)
t_fine = np.linspace(0, 1, 100)
y_fine = np.exp(-t_fine)
ax2.plot(t_fine, y_fine, 'b-', linewidth=2, alpha=0.5, label='True solution y(t)')

# Plot NODES (numerical solution points)
for i, (t, y) in enumerate(zip(t_grid, y_true)):
    ax2.plot(t, y, 'ro', markersize=12, zorder=5)  # NODE = (t_k, Y_k)
    ax2.text(t, y-0.15, f'Node {i}: (t{i}, Y{i})', 
             ha='center', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    # Show coordinates
    ax2.text(t, y+0.05, f'({t:.1f}, {y:.2f})', 
             ha='center', fontsize=9)

ax2.set_xlabel('Time (t)', fontsize=11)
ax2.set_ylabel('Solution y(t)', fontsize=11)
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.text(0.5, -0.2, 'NODES = Numerical solution values at grid points: (t_k, Y_k)', 
         ha='center', fontsize=11,
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# ------------------------------------------------------------
# Plot 3: What is a SLOPE? (Derivative f(t,y) at nodes)
# ------------------------------------------------------------
ax3 = axes[1, 0]
ax3.set_title('What is "SLOPE"? (Derivative f(t,y))', fontsize=12, fontweight='bold')

# Define a simple ODE: y' = -0.5y (slope depends on y)
def f(t, y):
    return -0.5 * y

# Time grid and true solution
t_grid = np.array([0.0, 0.3, 0.6, 0.9])
y_true = np.exp(-0.5 * t_grid)  # Exact solution: y = e^{-0.5t}

# Plot true solution
t_fine = np.linspace(0, 1, 100)
y_fine = np.exp(-0.5 * t_fine)
ax3.plot(t_fine, y_fine, 'b-', linewidth=2, alpha=0.5, label='True solution y(t)')

# Plot nodes
for i, (t, y) in enumerate(zip(t_grid, y_true)):
    ax3.plot(t, y, 'ro', markersize=10, zorder=5)
    ax3.text(t, y+0.05, f'Y{i}', ha='center', fontsize=10)

# Draw SLOPES (tangent lines) at each node
for i, (t, y) in enumerate(zip(t_grid, y_true)):
    slope = f(t, y)  # Compute derivative at this point
    
    # Draw tangent line (small segment)
    t_start = t - 0.1
    t_end = t + 0.1
    y_start = y + slope * (-0.1)
    y_end = y + slope * 0.1
    
    ax3.plot([t_start, t_end], [y_start, y_end], 
             'r-', linewidth=2, label=f'Slope at t{i}' if i==0 else "")
    
    # Add slope value
    ax3.text(t, y-0.1, f"f(t{i},Y{i}) = {slope:.2f}", 
             ha='center', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    
    # Arrow showing slope direction
    arrow = FancyArrowPatch((t, y), (t+0.08, y+slope*0.08),
                           arrowstyle='->', mutation_scale=15, 
                           color='red', linewidth=2)
    ax3.add_patch(arrow)

ax3.set_xlabel('Time (t)', fontsize=11)
ax3.set_ylabel('Solution y(t)', fontsize=11)
ax3.legend(loc='upper right')
ax3.grid(True, alpha=0.3)
ax3.text(0.5, -0.1, 'SLOPE = Derivative y\'(t) = f(t,y) evaluated at nodes', 
         ha='center', fontsize=11,
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# ------------------------------------------------------------
# Plot 4: Putting it ALL together - Multi-Step Method
# ------------------------------------------------------------
ax4 = axes[1, 1]
ax4.set_title('Multi-Step Method: Grid + Nodes + Slopes', fontsize=12, fontweight='bold')

# Time grid (non-uniform to show grid dependence)
t_grid = np.array([0.0, 0.15, 0.35, 0.6, 1.0])
steps = np.diff(t_grid)

# Some made-up solution values (for visualization)
Y = np.array([1.0, 0.85, 0.65, 0.45, 0.25])

# Plot grid lines
for t in t_grid:
    ax4.axvline(x=t, color='gray', linestyle='--', alpha=0.5, linewidth=1)

# Plot nodes
for i, (t, y) in enumerate(zip(t_grid, Y)):
    ax4.plot(t, y, 'ro', markersize=12, zorder=5)
    ax4.text(t, y-0.05, f'Y{i}', ha='center', fontsize=10, fontweight='bold')
    ax4.text(t, -0.1, f't{i}', ha='center', fontsize=10)

# Show current step (computing Y4 from Y3, Y2, Y1)
current_k = 3  # Computing Y4 at t=1.0 from previous values

# Highlight nodes used in multi-step method
used_nodes = [current_k-2, current_k-1, current_k]  # Using Y1, Y2, Y3 to get Y4
for idx in used_nodes:
    ax4.plot(t_grid[idx], Y[idx], 'go', markersize=14, zorder=4)

# Draw slopes at used nodes
for idx in used_nodes:
    # Simple slope visualization (not actual computation)
    slope = -0.5 * Y[idx]  # Just for visualization
    
    # Draw small tangent
    t = t_grid[idx]
    y = Y[idx]
    t_start = t - 0.08
    t_end = t + 0.08
    y_start = y + slope * (-0.08)
    y_end = y + slope * 0.08
    
    ax4.plot([t_start, t_end], [y_start, y_end], 
             'g-', linewidth=2)
    
    # Label the slope
    ax4.text(t, y+0.05, f'f{i}', ha='center', fontsize=9)

# Show multi-step formula
formula_text = r'$Y_4 = Y_3 + h_3 \times [b_1 f_3 + b_2 f_2 + b_3 f_1]$'
ax4.text(0.5, 0.9, formula_text, ha='center', fontsize=11,
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

# Show step sizes
for i in range(len(t_grid)-1):
    mid_t = (t_grid[i] + t_grid[i+1]) / 2
    ax4.text(mid_t, 0.05, f'h{i+1}', ha='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

# Draw arrow for current step
arrow = FancyArrowPatch((t_grid[current_k], Y[current_k]), 
                       (t_grid[current_k+1], Y[current_k+1]),
                       arrowstyle='->', mutation_scale=20, 
                       color='red', linewidth=3, zorder=3)
ax4.add_patch(arrow)
ax4.text(0.8, 0.35, 'Current step\ncomputing Y4', 
         ha='center', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))

ax4.set_xlabel('Time (t)', fontsize=11)
ax4.set_ylabel('Solution Y', fontsize=11)
ax4.set_xlim(-0.1, 1.1)
ax4.set_ylim(-0.2, 1.2)
ax4.grid(True, alpha=0.3)

plt.suptitle('GRID, NODES, and SLOPE in Numerical ODE Solving', 
             fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout()

# ------------------------------------------------------------
# Simple summary diagram
# ------------------------------------------------------------
fig2, ax5 = plt.subplots(figsize=(10, 6))
ax5.axis('off')

# Create a flowchart-like explanation
concepts = [
    ("GRID", "Time points: t₀, t₁, t₂, ...", (0.1, 0.9)),
    ("↓", "Discretization of time axis", (0.1, 0.8)),
    ("NODES", "Solution values: Y₀, Y₁, Y₂, ... at grid points", (0.1, 0.7)),
    ("↓", "We want to compute these numerically", (0.1, 0.6)),
    ("SLOPES", "Derivatives: f₀, f₁, f₂, ... = f(tₖ, Yₖ)", (0.1, 0.5)),
    ("↓", "From the ODE: y' = f(t,y)", (0.1, 0.4)),
    ("MULTI-STEP", "Use past slopes to predict next node", (0.1, 0.3)),
    ("↓", "Formula: ∑aⱼY_{k+1-j} = h∑bⱼf_{k+1-j}", (0.1, 0.2)),
    ("SOLUTION", "Sequence of nodes approximating y(t)", (0.1, 0.1))
]

# Draw boxes and arrows
for i, (title, desc, pos) in enumerate(concepts):
    # Draw box
    box = plt.Rectangle((pos[0]-0.08, pos[1]-0.04), 0.85, 0.08,
                       fill=True, facecolor='lightblue', 
                       edgecolor='black', alpha=0.7)
    ax5.add_patch(box)
    
    # Add text
    ax5.text(pos[0], pos[1], title, fontsize=12, fontweight='bold', 
             ha='left', va='center')
    ax5.text(pos[0]+0.3, pos[1], desc, fontsize=10, 
             ha='left', va='center')
    
    # Draw arrow (except for last one)
    if i < len(concepts)-1:
        next_pos = concepts[i+1][2]
        ax5.arrow(pos[0]+0.4, pos[1]-0.04, 0, -0.08,
                 head_width=0.02, head_length=0.02, 
                 fc='black', ec='black')

ax5.set_xlim(0, 1)
ax5.set_ylim(0, 1)
ax5.set_title('The Complete Picture: How Everything Fits Together', 
              fontsize=13, fontweight='bold', y=0.95)

plt.tight_layout()
plt.show()

print("\n" + "="*80)
print("SUMMARY DEFINITIONS:")
print("="*80)
print("\n1. GRID: Set of time points where we compute solution")
print("   • Example: t₀=0.0, t₁=0.2, t₂=0.4, t₃=0.6, ...")
print("   • Step sizes: h₁ = t₁ - t₀, h₂ = t₂ - t₁, ...")
print("   • Can be UNIFORM (all h equal) or NON-UNIFORM (h vary)")
print()
print("\n2. NODES: Numerical solution values at grid points")  
print("   • Example: Y₀ at t₀, Y₁ at t₁, Y₂ at t₂, ...")
print("   • We DON'T know these initially (except Y₀)")
print("   • Goal: Compute Y₁, Y₂, Y₃, ... accurately")
print()
print("\n3. SLOPES: Derivatives f(tₖ, Yₖ) = y'(t) evaluated at nodes")
print("   • From ODE: y' = f(t,y)")
print("   • Example: f₀ = f(t₀,Y₀), f₁ = f(t₁,Y₁), ...")
print("   • Multi-step methods: Store past slopes to predict future")
print()
print("\n4. MULTI-STEP FORMULA connects them all:")
print("   • Uses: PAST nodes (Y values) + PAST slopes (f values)")
print("   • Computes: NEXT node (Y_{k+1})")
print("   • Coefficients depend on GRID spacing (grid dependence)")
print()
print("\n" + "="*80)
print("ANALOGY: Building a staircase:")
print("="*80)
print("• GRID = Where you place steps (1m, 2m, 3m marks on wall)")
print("• NODES = Height of each step (Y values)")
print("• SLOPES = Steepness at each step (derivatives)")
print("• METHOD = Rules for deciding next step height based on previous steps")