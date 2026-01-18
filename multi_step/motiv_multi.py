import numpy as np
import matplotlib.pyplot as plt
import time

# Expensive function (simulating a complex physics simulation)
def expensive_f(t, y):
    # Simulate expensive computation with artificial delay
    time.sleep(0.01)  # 10ms per evaluation
    return -0.5 * y + np.sin(t)  # Some ODE

# Problem parameters
h = 0.1
t_end = 10.0  # Long integration
n_steps = int(t_end / h)

print("="*60)
print("REAL-WORLD MOTIVATION: COMPUTATIONAL COST")
print("="*60)
print(f"Integrating from t=0 to t={t_end} with h={h}")
print(f"Total steps needed: {n_steps}")
print()

# Count function evaluations
rk4_evals = 0
ab2_evals = 0

# Simulate RK4 evaluations
start_time = time.time()
for step in range(n_steps):
    # RK4 needs 4 evaluations per step
    rk4_evals += 4
    # Simulate the time for these evaluations
    for _ in range(4):
        expensive_f(0, 0)  # Just to trigger the sleep
rk4_time = time.time() - start_time

# Simulate AB2 evaluations (after startup)
start_time = time.time()
# Startup: 2 steps with Euler (2 evals)
ab2_evals = 2
expensive_f(0, 0)
expensive_f(0, 0)

# Then AB2: 1 eval per step
for step in range(2, n_steps):
    ab2_evals += 1
    expensive_f(0, 0)
ab2_time = time.time() - start_time

print("RESULTS:")
print(f"{'Method':<25} {'Evaluations':<15} {'Time (s)':<15} {'Speedup':<15}")
print("-"*70)
print(f"{'Runge-Kutta 4':<25} {rk4_evals:<15} {rk4_time:<15.2f} {'1×':<15}")
print(f"{'Adams-Bashforth 2':<25} {ab2_evals:<15} {ab2_time:<15.2f} {rk4_time/ab2_time:<15.1f}×")
print()

# Visual impact
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart: Evaluations
methods = ['RK4', 'AB2']
evaluations = [rk4_evals, ab2_evals]
times = [rk4_time, ab2_time]

bars1 = ax1.bar(methods, evaluations, color=['red', 'blue'])
ax1.set_ylabel('Function Evaluations', fontsize=12)
ax1.set_title('Total Evaluations Needed', fontsize=13, fontweight='bold')
ax1.set_ylim(0, max(evaluations)*1.1)

# Add labels on bars
for bar, val in zip(bars1, evaluations):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height + 5,
             f'{val}', ha='center', va='bottom', fontweight='bold')
    ax1.text(bar.get_x() + bar.get_width()/2, height/2,
             f'{4 if bar.get_facecolor() == "red" else 1} per step',
             ha='center', va='center', color='white', fontweight='bold')

ax1.grid(True, alpha=0.3, axis='y')

# Bar chart: Time
bars2 = ax2.bar(methods, times, color=['red', 'blue'])
ax2.set_ylabel('Computation Time (seconds)', fontsize=12)
ax2.set_title('Actual Computation Time', fontsize=13, fontweight='bold')
ax2.set_ylim(0, max(times)*1.1)

# Add labels on bars
for bar, val in zip(bars2, times):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height + 0.1,
             f'{val:.1f}s', ha='center', va='bottom', fontweight='bold')
    ax2.text(bar.get_x() + bar.get_width()/2, height/2,
             f'{rk4_time/ab2_time:.1f}× faster' if bar.get_facecolor() == "blue" else 'Baseline',
             ha='center', va='center', color='white', fontweight='bold')

ax2.grid(True, alpha=0.3, axis='y')

plt.suptitle('MOTIVATION: Multi-Step Methods are FASTER for Long Integrations', 
             fontsize=14, fontweight='bold')
plt.tight_layout()

# Now show the "memory" concept
fig2, ax3 = plt.subplots(figsize=(12, 6))

# Timeline visualization
time_points = np.arange(n_steps)
rk4_memory = [4] * n_steps  # Always 4
ab2_memory = [2] + [1] * (n_steps-1)  # 2 for startup, then 1

# Plot with stacked effect
ax3.fill_between(time_points[:10], 0, rk4_memory[:10], 
                 alpha=0.3, color='red', label='RK4: 4 evals/step')
ax3.fill_between(time_points[:10], 0, ab2_memory[:10], 
                 alpha=0.3, color='blue', label='AB2: 1 eval/step after startup')

# Add annotations
ax3.annotate('STARTUP\n(extra cost)', xy=(0.5, 2), xytext=(2, 4),
             arrowprops=dict(arrowstyle='->', color='blue'),
             fontsize=10, ha='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax3.annotate('Long-term savings!\nReuses past information', xy=(7, 1), xytext=(4, 6),
             arrowprops=dict(arrowstyle='->', color='blue'),
             fontsize=10, ha='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Show what happens at a specific step
step_to_examine = 5
ax3.axvline(x=step_to_examine, color='green', linestyle='--', alpha=0.7)
ax3.text(step_to_examine, 4.5, f'Step {step_to_examine}:', 
         ha='center', fontweight='bold', fontsize=10)

# Draw what each method does
rk4_box = plt.Rectangle((step_to_examine-0.3, 0), 0.6, 4, 
                       fill=True, facecolor='red', alpha=0.5, edgecolor='black')
ab2_box = plt.Rectangle((step_to_examine-0.3, 0), 0.6, 1, 
                       fill=True, facecolor='blue', alpha=0.5, edgecolor='black')
ax3.add_patch(rk4_box)
ax3.add_patch(ab2_box)

ax3.text(step_to_examine, 2, 'RK4: Compute\n4 new points', 
         ha='center', va='center', fontsize=9, color='white', fontweight='bold')
ax3.text(step_to_examine, 0.5, 'AB2: Compute\n1 new point,\nreuse 1 old', 
         ha='center', va='center', fontsize=9, color='white', fontweight='bold')

ax3.set_xlabel('Time Step Number', fontsize=12)
ax3.set_ylabel('Function Evaluations per Step', fontsize=12)
ax3.set_title('The Memory Advantage: Multi-Step Methods Remember Past Computations', 
              fontsize=13, fontweight='bold')
ax3.set_ylim(0, 5)
ax3.set_xlim(-0.5, 9.5)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Add a cost equation
equation_text = r'$\text{Total Cost} = (\text{Evaluations per step}) \times (\text{Number of steps})$'
ax3.text(0.5, -0.15, equation_text, transform=ax3.transAxes, 
         ha='center', fontsize=11, 
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

plt.tight_layout()

# REAL-WORLD EXAMPLE
print("\n" + "="*60)
print("REAL-WORLD SCENARIO:")
print("="*60)
print("You're simulating:")
print("- Weather prediction for 10 days ahead")
print("- Rocket trajectory for Mars mission")
print("- Protein folding over microseconds")
print()
print("Function f(t,y) might involve:")
print("- Solving Navier-Stokes equations (fluid dynamics)")
print("- Computing gravitational forces between N bodies")
print("- Quantum mechanical calculations")
print()
print(f"EACH evaluation takes ~10ms (in our example)")
print(f"For {n_steps} steps:")
print(f"  RK4: {rk4_time:.1f} seconds to complete")
print(f"  AB2: {ab2_time:.1f} seconds to complete")
print(f"  DIFFERENCE: {rk4_time - ab2_time:.1f} seconds saved!")
print()
print("Now scale this up:")
print("What if each evaluation takes 1 second?")
print(f"  RK4: {rk4_evals} seconds = {rk4_evals/3600:.1f} hours")
print(f"  AB2: {ab2_evals} seconds = {ab2_evals/3600:.1f} hours")
print(f"  You save: {(rk4_evals - ab2_evals)/3600:.1f} hours!")

plt.show()