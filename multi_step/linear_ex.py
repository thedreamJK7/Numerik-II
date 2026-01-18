import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Example 1: Linear combination
ax1 = axes[0]
ax1.text(0.5, 0.6, r'$1.5 \cdot f_k - 0.5 \cdot f_{k-1}$', 
         ha='center', fontsize=14,
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
ax1.text(0.5, 0.4, "Constants × functions", ha='center', fontsize=10)
ax1.text(0.5, 0.2, "✅ LINEAR", ha='center', fontsize=12, fontweight='bold', color='green')
ax1.set_title('Linear: Multiplication by Constants')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')

# Example 2: Non-linear because of function composition
ax2 = axes[1]
ax2.text(0.5, 0.6, r'$f_k \cdot f_{k-1}$', 
         ha='center', fontsize=14,
         bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
ax2.text(0.5, 0.4, "Function × function", ha='center', fontsize=10)
ax2.text(0.5, 0.2, "❌ NOT LINEAR", ha='center', fontsize=12, fontweight='bold', color='red')
ax2.set_title('Non-linear: Product of Functions')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')

# Example 3: Constants are okay, non-linear functions are not
ax3 = axes[2]
ax3.text(0.5, 0.7, r'$3 \cdot \sin(f_k)$', 
         ha='center', fontsize=14,
         bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
ax3.text(0.5, 0.5, "Constant × non-linear function", ha='center', fontsize=10)
ax3.text(0.5, 0.3, "❌ NOT LINEAR", ha='center', fontsize=12, fontweight='bold', color='red')
ax3.set_title('Still Non-linear: sin() is non-linear')
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')

plt.suptitle('Linear vs. Non-linear in Multi-Step Methods', fontsize=14, fontweight='bold')
plt.tight_layout()

# Another visualization
fig2, ax = plt.subplots(figsize=(10, 6))

# Show what "linear in the data" means
x = np.array([1, 2, 3, 4])  # Some data points
coefficients = np.array([0.5, -1.5, 2.0, -0.5])  # Constants

# Linear combination: L(x) = 0.5*x1 - 1.5*x2 + 2.0*x3 - 0.5*x4
linear_result = np.dot(coefficients, x)

# Visualize the linear operation
positions = np.arange(len(x))
ax.bar(positions - 0.2, x, width=0.4, label='Data: x', alpha=0.7)
ax.bar(positions + 0.2, coefficients, width=0.4, label='Constants: a', alpha=0.7, color='orange')

# Draw multiplication and addition
for i, (xi, ci) in enumerate(zip(x, coefficients)):
    ax.text(i, max(xi, ci) + 0.2, f'{ci}×{xi} = {ci*xi:.1f}', 
            ha='center', fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.axhline(y=linear_result, color='red', linestyle='--', linewidth=2, alpha=0.7)
ax.text(len(x)-0.5, linear_result+0.2, f'Sum = {linear_result}', 
        color='red', fontsize=12, fontweight='bold')

ax.set_xlabel('Index j')
ax.set_ylabel('Value')
ax.set_title('Linear Combination: L(x) = a₁x₁ + a₂x₂ + a₃x₃ + a₄x₄', fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xticks(positions)
ax.set_xticklabels([f'x_{i+1}' for i in range(len(x))])

plt.tight_layout()
plt.show()

print("\n" + "="*70)
print("WHY CONSTANT MULTIPLICATION IS LINEAR")
print("="*70)
print("\nFormal definition: A function L is linear if:")
print("1. L(x + y) = L(x) + L(y)  (additivity)")
print("2. L(α·x) = α·L(x)  (homogeneity, where α is constant)")
print()
print("Example: L(f) = 1.5·f_k - 0.5·f_{k-1}")
print("Check additivity: L(f+g) = 1.5·(f+g)_k - 0.5·(f+g)_{k-1}")
print("                 = (1.5·f_k - 0.5·f_{k-1}) + (1.5·g_k - 0.5·g_{k-1})")
print("                 = L(f) + L(g) ✓")
print()
print("Check homogeneity: L(α·f) = 1.5·(α·f)_k - 0.5·(α·f)_{k-1}")
print("                  = α·(1.5·f_k - 0.5·f_{k-1})")
print("                  = α·L(f) ✓")
print()
print("So yes: Multiplying by constants and adding is LINEAR!")