import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as patches

# Set up the figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

# ODE: y' = -0.5y, y(0) = 1
def f(t, y):
    return -0.5 * y

def exact_solution(t):
    return np.exp(-0.5 * t)

# Initialize
t0, tf = 0, 3
h = 0.5
steps = int((tf - t0) / h)
t_vals = np.linspace(t0, tf, steps + 1)
y_exact = exact_solution(t_vals)

# Storage for visualization
eval_points = []
method_colors = {'RK4': 'red', 'AB2': 'blue', 'Exact': 'green'}
method_markers = {'RK4': 'o', 'AB2': 's', 'Exact': 'x'}

# Adams-Bashforth 2-step
y_ab = np.zeros(steps + 1)
y_ab[0] = 1.0
# First step with Euler (simple startup)
y_ab[1] = y_ab[0] + h * f(t_vals[0], y_ab[0])

# RK4 solution
y_rk4 = np.zeros(steps + 1)
y_rk4[0] = 1.0

# Animation frames
frames = []

# Collect frame data
for step in range(1, steps + 1):
    frame_data = {'step': step, 'rk4_points': [], 'ab_points': []}
    
    # RK4 step (4 evaluations)
    t = t_vals[step-1]
    y = y_rk4[step-1]
    
    # Show RK4 evaluations
    k1 = f(t, y)
    frame_data['rk4_points'].append((t, y, 'k1'))
    
    k2 = f(t + h/2, y + h*k1/2)
    frame_data['rk4_points'].append((t + h/2, y + h*k1/2, 'k2'))
    
    k3 = f(t + h/2, y + h*k2/2)
    frame_data['rk4_points'].append((t + h/2, y + h*k2/2, 'k3'))
    
    k4 = f(t + h, y + h*k3)
    frame_data['rk4_points'].append((t + h, y + h*k3, 'k4'))
    
    y_rk4[step] = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    
    # Adams-Bashforth step
    if step > 1:
        y_ab[step] = y_ab[step-1] + h * (1.5 * f(t_vals[step-1], y_ab[step-1]) 
                                        - 0.5 * f(t_vals[step-2], y_ab[step-2]))
        # AB2 uses only current f evaluation (reuses previous)
        frame_data['ab_points'].append((t_vals[step-1], y_ab[step-1], 'f_current'))
    elif step == 1:
        frame_data['ab_points'].append((t_vals[step-1], y_ab[step-1], 'f_current'))
    
    frames.append(frame_data)

# Plot exact solution
ax1.plot(t_vals, y_exact, 'g-', linewidth=2, label='Exact Solution', alpha=0.7, zorder=1)
ax2.plot(t_vals, y_exact, 'g-', linewidth=2, label='Exact Solution', alpha=0.7, zorder=1)

# Initial setup
ax1.set_xlim(-0.1, tf + 0.1)
ax1.set_ylim(0, 1.1)
ax1.set_xlabel('Time (t)')
ax1.set_ylabel('y(t)')
ax1.set_title('Runge-Kutta 4 (One-Step Method)', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right')

ax2.set_xlim(-0.1, tf + 0.1)
ax2.set_ylim(0, 1.1)
ax2.set_xlabel('Time (t)')
ax2.set_ylabel('y(t)')
ax2.set_title('Adams-Bashforth 2 (Multi-Step Method)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right')

# Add explanation boxes
props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)

ax1.text(0.02, 0.98, '4 evaluations per step\nStart fresh each step', 
         transform=ax1.transAxes, fontsize=9, verticalalignment='top',
         bbox=props)

ax2.text(0.02, 0.98, '1 new evaluation per step\nReuses previous evaluations', 
         transform=ax2.transAxes, fontsize=9, verticalalignment='top',
         bbox=props)

# Function evaluation counters
counter_text1 = ax1.text(0.02, 0.1, 'Current step: 0\nEvaluations: 0', 
                         transform=ax1.transAxes, fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

counter_text2 = ax2.text(0.02, 0.1, 'Current step: 0\nEvaluations: 0', 
                         transform=ax2.transAxes, fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Keep track of plotted elements
rk4_scatter = ax1.scatter([], [], c='red', s=100, marker='o', label='RK4 Evaluations', zorder=5)
rk4_lines = []
ab_scatter = ax2.scatter([], [], c='blue', s=100, marker='s', label='AB2 Evaluations', zorder=5)
ab_previous_scatter = ax2.scatter([], [], c='lightblue', s=80, marker='s', 
                                 label='Reused Evaluation', alpha=0.6, zorder=4)
solution_line1, = ax1.plot([], [], 'r-', linewidth=2, label='RK4 Solution')
solution_line2, = ax2.plot([], [], 'b-', linewidth=2, label='AB2 Solution')

def init():
    rk4_scatter.set_offsets(np.empty((0, 2)))
    ab_scatter.set_offsets(np.empty((0, 2)))
    ab_previous_scatter.set_offsets(np.empty((0, 2)))
    solution_line1.set_data([], [])
    solution_line2.set_data([], [])
    return rk4_scatter, ab_scatter, ab_previous_scatter, solution_line1, solution_line2

# Animation function
def animate(frame_idx):
    frame = frames[frame_idx]
    step = frame['step']
    
    # Initialize highlight patches if not exists
    if not hasattr(animate, 'highlight_patches'):
        animate.highlight_patches = []
    
    # Clear previous lines (for RK4 evaluation lines)
    for line in rk4_lines:
        line.remove()
    rk4_lines.clear()
    
    # RK4 plot
    rk4_points = frame['rk4_points']
    if rk4_points:
        points_array = np.array([[p[0], p[1]] for p in rk4_points])
        rk4_scatter.set_offsets(points_array)
        
        # Draw lines connecting RK4 evaluation points
        y_current = y_rk4[step-1] if step > 0 else 1.0
        for i, point in enumerate(rk4_points):
            if i == 0:
                # Line from previous solution to k1
                line = ax1.plot([t_vals[step-1], point[0]], 
                               [y_current, point[1]], 
                               'r--', alpha=0.5, linewidth=1)[0]
                rk4_lines.append(line)
            else:
                # Lines between RK4 points
                prev_point = rk4_points[i-1]
                line = ax1.plot([prev_point[0], point[0]], 
                               [prev_point[1], point[1]], 
                               'r--', alpha=0.5, linewidth=1)[0]
                rk4_lines.append(line)
    
    # Update RK4 solution line
    solution_line1.set_data(t_vals[:step+1], y_rk4[:step+1])
    
    # AB2 plot
    ab_points = frame['ab_points']
    if ab_points:
        # Current evaluation
        points_array = np.array([[p[0], p[1]] for p in ab_points])
        ab_scatter.set_offsets(points_array)
        
        # Previous evaluations (reused)
        if step > 1:
            prev_points = [(t_vals[step-2], y_ab[step-2])]
            prev_array = np.array(prev_points)
            ab_previous_scatter.set_offsets(prev_array)
        else:
            ab_previous_scatter.set_offsets(np.empty((0, 2)))
        
        # Draw line from previous to current solution point (only once per step)
        if step > 0 and not hasattr(animate, f'ab_line_{step}'):
            line = ax2.plot(t_vals[step-1:step+1], y_ab[step-1:step+1], 
                           'b-', linewidth=2, zorder=3)[0]
            setattr(animate, f'ab_line_{step}', line)
    
    # Update AB2 solution line
    solution_line2.set_data(t_vals[:step+1], y_ab[:step+1])
    
    # Update counters
    counter_text1.set_text(f'Step: {step}\nEvaluations this step: {len(rk4_points)}\nTotal: {4*step}')
    counter_text2.set_text(f'Step: {step}\nEvaluations this step: {len(ab_points)}\nTotal: {step}')
    
    # Highlight current step - use axvspan instead of patches
    # Clear previous highlights by redrawing the background
    if hasattr(animate, 'highlight_patches'):
        for patch in animate.highlight_patches:
            try:
                patch.remove()
            except:
                pass
    
    # Create new highlights
    highlight1 = ax1.axvspan(t_vals[step]-h/2, t_vals[step]+h/2, 
                            alpha=0.2, color='yellow', zorder=0)
    highlight2 = ax2.axvspan(t_vals[step]-h/2, t_vals[step]+h/2, 
                            alpha=0.2, color='yellow', zorder=0)
    
    # Store references for next frame cleanup
    animate.highlight_patches = [highlight1, highlight2]
    
    return (rk4_scatter, ab_scatter, ab_previous_scatter, 
            solution_line1, solution_line2, counter_text1, counter_text2)

# Create animation
ani = FuncAnimation(fig, animate, frames=len(frames),
                    init_func=init, blit=False, interval=1000, repeat=False)

# Add overall title
fig.suptitle('Visual Comparison: Multi-Step vs. One-Step Methods', 
             fontsize=14, fontweight='bold', y=1.02)

# Add a legend explaining the visualization
fig.text(0.5, 0.01, 
         '● RK4: Needs 4 evaluations per step, each step independent\n'
         '■ AB2: Uses 1 new evaluation + reuses previous one → More efficient',
         ha='center', fontsize=10, style='italic',
         bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))

plt.show()

# Also create a summary bar chart
fig2, ax3 = plt.subplots(figsize=(10, 5))

# Data for bar chart
methods = ['RK4 (Step 1)', 'RK4 (Step 2)', 'RK4 (Step 3)', 
           'AB2 (Step 1)', 'AB2 (Step 2)', 'AB2 (Step 3)']
evaluations = [4, 4, 4, 1, 1, 1]  # New evaluations per step
colors = ['red', 'red', 'red', 'blue', 'blue', 'blue']
patterns = ['', '', '', '//', '//', '//']  # Pattern for reused evaluations

bars = ax3.bar(methods, evaluations, color=colors, edgecolor='black')

# Add pattern to AB2 bars to indicate reuse
for i, bar in enumerate(bars):
    if i >= 3:  # AB2 bars
        bar.set_hatch('//')

# Add labels and title
ax3.set_ylabel('Function Evaluations per Step', fontsize=12)
ax3.set_title('Computational Cost: New Evaluations per Step', fontsize=13, fontweight='bold')
ax3.set_ylim(0, 5)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold')

# Add annotations
ax3.text(1, 4.5, 'Each step independent', ha='center', fontsize=10, color='red')
ax3.text(4.5, 4.5, 'Reuses past evaluations', ha='center', fontsize=10, color='blue')

# Add total evaluation count
total_rk4 = 4 * 3
total_ab2 = 1 * 3
ax3.text(0.5, -0.15, f'Total: {total_rk4} evals', transform=ax3.transAxes, 
         ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='red', alpha=0.2))
ax3.text(0.9, -0.15, f'Total: {total_ab2} evals', transform=ax3.transAxes, 
         ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='blue', alpha=0.2))

plt.tight_layout()
plt.show()

print("Animation created! The visualization shows:")
print("1. LEFT: RK4 makes 4 new evaluations per step (red circles)")
print("2. RIGHT: AB2 makes 1 new evaluation (blue square), reuses previous (light blue)")
print("3. The highlighted yellow region shows the current time step")
print("4. Bottom chart summarizes computational efficiency")