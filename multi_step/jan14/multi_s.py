import matplotlib.pyplot as plt
import numpy as np

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Visualization 1: Time steps and indices
ax1.set_title('Understanding the Indices: k, j, m', fontsize=12, fontweight='bold')

# Create timeline
time_points = [0, 1, 2, 3, 4, 5]  # t₀, t₁, t₂, t₃, t₄, t₅
labels = ['t₀', 't₁', 't₂', 't₃', 't₄', 't₅']

# Plot timeline
for i, (t, label) in enumerate(zip(range(len(time_points)), labels)):
    ax1.plot(t, 0, 'ko', markersize=10)  # Time point
    ax1.text(t, 0.05, label, ha='center', fontsize=12, fontweight='bold')
    
    # Index numbers below
    ax1.text(t, -0.05, f'k={i}', ha='center', fontsize=10, color='blue')

# Current step highlight
current_k = 3  # We're at step k=3 (t₃)
ax1.plot(current_k, 0, 'ro', markersize=12)  # Red for current
ax1.text(current_k, 0.1, f'Current: k={current_k}\n(t₃)', 
         ha='center', fontsize=10, fontweight='bold', color='red',
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

# Show m (memory length) = 2
m = 2
for j in range(m+1):  # j = 0, 1, 2
    idx = current_k - j  # This gives us k, k-1, k-2 when j=0,1,2
    ax1.plot(idx, 0.1 + 0.05*j, 'bs', markersize=8)  # Blue squares for used points
    ax1.text(idx, 0.15 + 0.05*j, f'j={j}\nY_{{{current_k+1-j}}}', 
             ha='center', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

ax1.set_xlabel('Time Step Index (k)', fontsize=11)
ax1.set_ylim(-0.2, 0.3)
ax1.axis('off')
ax1.text(0.1, -0.15, 'Time increases →', fontsize=10, color='gray', style='italic')

# Visualization 2: The summation formula
ax2.set_title('The Summation: $\sum_{j=0}^m a_j Y_{k+1-j}$', fontsize=12, fontweight='bold')
ax2.axis('off')

# Draw the formula with explanation
formula_parts = [
    (r'$\sum_{j=0}^m$', 'Sum over j from 0 to m'),
    (r'$a_j$', 'Coefficient (weight) for each term'),
    (r'$Y_{k+1-j}$', 'Solution value at time step k+1-j')
]

y_pos = 0.8
for symbol, meaning in formula_parts:
    ax2.text(0.1, y_pos, symbol, fontsize=14, 
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    ax2.text(0.4, y_pos, meaning, fontsize=10, va='center')
    y_pos -= 0.2

# Show concrete example
example_text = r"""
Concrete Example (m=2, k=3):

$\sum_{j=0}^{2} a_j Y_{4-j} =$

$a_0 Y_{4} + a_1 Y_{3} + a_2 Y_{2}$

What this means:
• j=0: $a_0 Y_{k+1} = a_0 Y_{4}$ (future/current unknown)
• j=1: $a_1 Y_{k} = a_1 Y_{3}$ (current known)
• j=2: $a_2 Y_{k-1} = a_2 Y_{2}$ (past known)
"""

ax2.text(0.1, 0.3, example_text, fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.suptitle('Multi-Step Method Notation Explained', fontsize=14, fontweight='bold')
plt.tight_layout()

# Now show what m means in practice
fig2, axes = plt.subplots(1, 3, figsize=(15, 4))

methods = [
    ('1-step (Euler)', 0, r'$Y_{k+1} - Y_k = h f_k$'),
    ('2-step (Adams-Bashforth)', 1, r'$Y_{k+1} - Y_k = h(\frac{3}{2}f_k - \frac{1}{2}f_{k-1})$'),
    ('3-step', 2, r'$Y_{k+1} - Y_k = h(\frac{23}{12}f_k - \frac{16}{12}f_{k-1} + \frac{5}{12}f_{k-2})$')
]

for idx, (name, m_val, formula) in enumerate(methods):
    ax = axes[idx]
    ax.set_title(f'{name}\n(m = {m_val})', fontsize=11)
    ax.axis('off')
    
    # Show m value
    ax.text(0.5, 0.8, f'm = {m_val}', fontsize=14, fontweight='bold',
            ha='center', bbox=dict(boxstyle='circle', facecolor='lightblue', alpha=0.8))
    
    # Show formula
    ax.text(0.5, 0.5, formula, fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    
    # Show what it uses
    uses = f'Uses {m_val+1} past values:'
    for j in range(m_val+1):
        uses += f'\n  • Y_{{k-{j}}}'
    ax.text(0.5, 0.2, uses, fontsize=9, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))

fig2.suptitle('What "m" Controls: How Many Past Steps We Use', 
              fontsize=14, fontweight='bold', y=1.05)

plt.show()

print("\n" + "="*70)
print("QUICK REFERENCE GUIDE")
print("="*70)
print()
print("k = CURRENT step index (we're at time t_k, solution Y_k)")
print("j = SUMMATION index (runs from 0 to m)")
print("m = MEMORY length (how many past steps we use)")
print()
print("Y_{k+1-j} means:")
print("  • When j=0: Y_{k+1}   (the FUTURE value we want to find)")
print("  • When j=1: Y_{k}     (the CURRENT known value)")
print("  • When j=2: Y_{k-1}   (the PAST known value)")
print("  • ... and so on until j=m: Y_{k+1-m}")
print()
print("In your specific formula:")
print(r"  ∑_{j=0}^m a_j Y_{k+1-j} = Y_{k+1} - Y_k")
print("This means: A weighted sum of past+future Y's equals the simple difference")