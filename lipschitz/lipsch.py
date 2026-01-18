import numpy as np
import matplotlib.pyplot as plt

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# ------------------------------------------------------------
# Plot 1: Lipschitz function f(x) = |x|
# ------------------------------------------------------------
x1 = np.linspace(-1, 1, 400)
y1 = np.abs(x1)

ax1.plot(x1, y1, 'b-', linewidth=3, label='$f(x) = |x|$')
ax1.set_title('LIPSCHITZ FUNCTION\n$L=1$ exists', fontsize=12, fontweight='bold', color='green')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Show secant lines with bounded slope
for x_start in [-0.8, -0.4, 0, 0.4]:
    x_end = x_start + 0.4
    ax1.plot([x_start, x_end], [np.abs(x_start), np.abs(x_end)], 
             'r--', alpha=0.6, linewidth=1)
    slope = (np.abs(x_end) - np.abs(x_start)) / (x_end - x_start)
    ax1.text((x_start+x_end)/2, (np.abs(x_start)+np.abs(x_end))/2 + 0.05,
             f'slope={slope:.1f}', fontsize=8, color='red')

# Add Lipschitz bound
ax1.text(0.6, 0.3, 'All slopes ≤ 1\n$L=1$ works!', 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.8),
         fontsize=10)

# ------------------------------------------------------------
# Plot 2: Non-Lipschitz function f(x) = √|x|
# ------------------------------------------------------------
x2 = np.linspace(0, 1, 400)
y2 = np.sqrt(x2)

ax2.plot(x2, y2, 'b-', linewidth=3, label='$f(x) = \sqrt{x}$')
ax2.set_title('NON-LIPSCHITZ FUNCTION\nNo finite $L$ exists', fontsize=12, fontweight='bold', color='red')
ax2.set_xlabel('x')
ax2.set_ylabel('f(x)')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Show secant lines with unbounded slope near 0
x_points = [0.001, 0.01, 0.05, 0.1, 0.3]
colors = ['red', 'orange', 'purple', 'brown', 'green']

for i, x_end in enumerate(x_points):
    x_start = 0
    slope = (np.sqrt(x_end) - 0) / (x_end - 0)
    ax2.plot([x_start, x_end], [0, np.sqrt(x_end)], 
             color=colors[i], linestyle='--', alpha=0.7, linewidth=1)
    ax2.text(x_end/2, np.sqrt(x_end)/2 - 0.03,
             f'slope={slope:.1f}', fontsize=8, color=colors[i])

# Highlight the problem at x=0
ax2.axvline(x=0, color='k', linestyle=':', alpha=0.3)
ax2.fill_between(x2[:50], 0, y2[:50], color='red', alpha=0.2, 
                 label='Slope → ∞ as x→0')

ax2.text(0.15, 0.8, 'Slope = $\\frac{1}{\\sqrt{x}}$ → ∞\nas x → 0', 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8),
         fontsize=10)

plt.tight_layout()
plt.show()