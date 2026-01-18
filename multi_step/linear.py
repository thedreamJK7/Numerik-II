import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Create a visualization
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('What "Linear" Means in Multi-Step Methods', fontsize=14, fontweight='bold')

# Example: Adams-Bashforth 2-step (Linear)
# Y_{k+1} - Y_k = h * [1.5*f(t_k, Y_k) - 0.5*f(t_{k-1}, Y_{k-1})]
# Here: a0=1, a1=-1, b0=1.5, b1=-0.5

# Example 1: Linear combination visualization
ax1 = axes[0, 0]
ax1.set_title('Linear Multi-Step Formula', fontsize=11)

# Draw the equation structure
equation_text = r'$\sum_{j=0}^{m} a_j Y_{k+1-j} = h \sum_{j=0}^{m} b_j f_{k+1-j}$'
ax1.text(0.5, 0.7, equation_text, ha='center', fontsize=14, 
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Add explanation
explanation = """Key Properties:
1. Linear in Y-values: a₀Y_{k+1} + a₁Y_k + ... 
2. Linear in f-values: b₀f_k + b₁f_{k-1} + ...
3. Weights (a_j, b_j) are constants
4. No nonlinear terms"""
ax1.text(0.5, 0.3, explanation, ha='center', fontsize=9, 
         transform=ax1.transAxes, 
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')

# Example 2: Linear vs Nonlinear comparison
ax2 = axes[0, 1]
ax2.set_title('Linear vs Nonlinear Operations', fontsize=11)

# Create comparison table
operations = [
    ('Linear (Allowed)', ['a·Y', 'b·f(Y)', 'Y₁ + Y₂', 'f₁ - f₂']),
    ('Nonlinear (NOT allowed)', ['Y²', 'sin(Y)', 'f₁·f₂', '√Y', 'Y·f(Y)'])
]

y_pos = 0.8
for op_type, examples in operations:
    color = 'lightgreen' if 'Linear' in op_type else 'lightcoral'
    ax2.text(0.1, y_pos, op_type, fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=color, alpha=0.8))
    y_pos -= 0.1
    for ex in examples:
        ax2.text(0.15, y_pos, f'• {ex}', fontsize=9)
        y_pos -= 0.07
    y_pos -= 0.05

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')

# Example 3: Concrete Adams-Bashforth example
ax3 = axes[1, 0]
ax3.set_title('Example: Adams-Bashforth 2-Step (Linear)', fontsize=11)

# Show the specific linear formula
ab2_formula = r'$Y_{k+1} - Y_k = h\left[\frac{3}{2}f_k - \frac{1}{2}f_{k-1}\right]$'
ax3.text(0.5, 0.6, ab2_formula, ha='center', fontsize=14,
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Show the weights
weights_text = """Weights are constants:
a₀ = 1, a₁ = -1, a₂ = 0
b₀ = 0, b₁ = 3/2, b₂ = -1/2

This is LINEAR because:
• Y terms: 1·Y_{k+1} + (-1)·Y_k
• f terms: (3/2)·f_k + (-1/2)·f_{k-1}
• All operations are linear combinations"""
ax3.text(0.5, 0.2, weights_text, ha='center', fontsize=9,
         transform=ax3.transAxes,
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')

# Example 4: What WOULDN'T be linear
ax4 = axes[1, 1]
ax4.set_title('Examples of NON-Linear Multi-Step', fontsize=11)

nonlinear_examples = [
    (r'$Y_{k+1} = Y_k + h\cdot f_k \cdot f_{k-1}$', 'Product of f-values'),
    (r'$Y_{k+1} = \sin(Y_k) + h f_k$', 'Nonlinear function of Y'),
    (r'$Y_{k+1} = Y_k^2 + h f_k$', 'Square of Y'),
    (r'$Y_{k+1} = Y_k + h\sqrt{f_k}$', 'Square root of f')
]

y_pos = 0.8
for formula, desc in nonlinear_examples:
    # Draw a "forbidden" symbol
    circle = plt.Circle((0.15, y_pos), 0.03, color='red', fill=False, linewidth=2)
    line1 = plt.Line2D([0.12, 0.18], [y_pos-0.03, y_pos+0.03], color='red', linewidth=2)
    line2 = plt.Line2D([0.12, 0.18], [y_pos+0.03, y_pos-0.03], color='red', linewidth=2)
    ax4.add_patch(circle)
    ax4.add_line(line1)
    ax4.add_line(line2)
    
    # Show the formula
    ax4.text(0.25, y_pos, formula, fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.6))
    ax4.text(0.25, y_pos-0.04, desc, fontsize=8, style='italic')
    y_pos -= 0.2

ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis('off')

plt.tight_layout()

# Now show a practical example
fig2, (ax5, ax6) = plt.subplots(1, 2, figsize=(12, 5))

# Left: Visualize the linear combination
ax5.set_title('Visualizing Linear Combination', fontsize=12)

# Create timeline
time_points = ['Y_{k+1}', 'Y_k', 'Y_{k-1}', 'Y_{k-2}']
x_pos = [0, 1, 2, 3]
a_weights = [1, -1, 0, 0]  # For AB2
b_weights = [0, 1.5, -0.5, 0]  # For AB2

# Plot Y terms
ax5.scatter(x_pos, [w+0.2 for w in a_weights], c='blue', s=200, marker='s', label='Y weights (a_j)')
for i, (x, w) in enumerate(zip(x_pos, a_weights)):
    if w != 0:
        ax5.text(x, w+0.25, f'a={w}', ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        ax5.text(x, -0.1, time_points[i], ha='center', fontsize=10)

# Plot f terms
ax5.scatter(x_pos, [w-0.2 for w in b_weights], c='red', s=200, marker='o', label='f weights (b_j)')
for i, (x, w) in enumerate(zip(x_pos, b_weights)):
    if w != 0:
        ax5.text(x, w-0.25, f'b={w}', ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

ax5.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax5.set_xlabel('Time index (j)')
ax5.set_ylabel('Weight value')
ax5.set_title('Weights for Adams-Bashforth 2-Step', fontsize=11)
ax5.legend()
ax5.grid(True, alpha=0.3)
ax5.set_ylim(-1, 2)

# Right: Show linearity property
ax6.set_title('Linearity Means Superposition Works', fontsize=12)

# Draw superposition concept
x = np.linspace(0, 1, 100)
y1 = 0.5 * x  # First solution component
y2 = 0.3 * np.sin(2*np.pi*x)  # Second solution component
y_total = y1 + y2  # Superposition

ax6.plot(x, y1, 'b-', label='Solution part 1: y₁(t)', alpha=0.7)
ax6.plot(x, y2, 'r-', label='Solution part 2: y₂(t)', alpha=0.7)
ax6.plot(x, y_total, 'k--', linewidth=2, label='Total: y₁(t) + y₂(t)')

ax6.text(0.7, 0.8, 'Linearity property:\nIf method solves for y₁ and y₂\nit also solves for y₁ + y₂',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

ax6.set_xlabel('t')
ax6.set_ylabel('y(t)')
ax6.legend()
ax6.grid(True, alpha=0.3)

fig2.suptitle('Linear Multi-Step Methods: Practical Understanding', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("SUMMARY: Why 'Linear' Matters in Multi-Step Methods")
print("="*60)
print("\nA multi-step method is LINEAR if:")
print("1. Y terms appear only as: a₀Y_{k+1} + a₁Y_k + a₂Y_{k-1} + ...")
print("2. f terms appear only as: b₀f_k + b₁f_{k-1} + b₂f_{k-2} + ...")
print("3. The coefficients a_j and b_j are constants (don't depend on Y)")
print("\nThis is IMPORTANT because:")
print("• Linear methods are easier to analyze")
print("• Linear methods have nice stability properties")
print("• Linear methods allow superposition: if method works for y₁ and y₂,")
print("  it also works for y₁ + y₂")
print("\nMost common multi-step methods (Adams, BDF) are LINEAR!")