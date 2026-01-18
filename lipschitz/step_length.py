import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# ADAPTIVE STEP SIZE CONTROL IMPLEMENTATION
# ------------------------------------------------------------

def f(t, y):
    """Test ODE: y' = -20y + 20cos(t) - sin(t), exact solution: y(t) = cos(t)"""
    return -20*y + 20*np.cos(t) - np.sin(t)

def exact_solution(t):
    """Exact solution for verification"""
    return np.cos(t)

def euler_step(t, y, h):
    """Single Euler step"""
    return y + h * f(t, y)

def rk2_step(t, y, h):
    """Single RK2 (Heun) step"""
    k1 = f(t, y)
    k2 = f(t + h, y + h * k1)
    return y + h * (k1 + k2) / 2

def rk4_step(t, y, h):
    """Single RK4 step"""
    k1 = f(t, y)
    k2 = f(t + h/2, y + h*k1/2)
    k3 = f(t + h/2, y + h*k2/2)
    k4 = f(t + h, y + h*k3)
    return y + h * (k1 + 2*k2 + 2*k3 + k4) / 6

def embedded_rk_step(t, y, h):
    """
    Embedded RK2/RK3 pair for error estimation
    Returns: (y_low_order, y_high_order)
    """
    # RK2 (Heun method)
    k1 = f(t, y)
    k2 = f(t + h, y + h * k1)
    y2 = y + h * (k1 + k2) / 2
    
    # RK3 (using same function evaluations + one more)
    k3 = f(t + h/2, y + h*k1/2)
    y3 = y + h * (k1 + 4*k3 + k2) / 6
    
    return y2, y3

def adaptive_step_control(t0, y0, t_end, h_init, tol, method='embedded_rk'):
    """
    Adaptive step size control using embedded methods
    
    Parameters:
    - t0, y0: Initial conditions
    - t_end: Final time
    - h_init: Initial step size
    - tol: Error tolerance
    - method: 'embedded_rk', 'richardson', or 'fixed'
    
    Returns:
    - t_vals, y_vals: Solution arrays
    - h_vals: Step sizes used
    - error_estimates: Local error estimates
    """
    
    t_vals = [t0]
    y_vals = [y0]
    h_vals = []
    error_estimates = []
    
    t = t0
    y = y0
    h = h_init
    
    safety_factor = 0.9
    min_h = 1e-8
    max_h = 0.5
    
    step_count = 0
    max_steps = 10000
    
    while t < t_end and step_count < max_steps:
        # Don't overshoot the end
        if t + h > t_end:
            h = t_end - t
        
        if method == 'embedded_rk':
            # Use embedded RK pair
            y_low, y_high = embedded_rk_step(t, y, h)
            error_est = abs(y_high - y_low)
            
        elif method == 'richardson':
            # Richardson extrapolation: compare h and h/2 steps
            y_h = rk2_step(t, y, h)
            
            # Two steps of size h/2
            y_half = rk2_step(t, y, h/2)
            y_h2 = rk2_step(t + h/2, y_half, h/2)
            
            # Error estimate (assuming order p=2)
            error_est = abs(y_h2 - y_h) / (2**2 - 1)
            y_high = y_h2  # Use more accurate result
            
        else:  # fixed step
            y_high = rk2_step(t, y, h)
            error_est = 0.0
        
        # Step size control
        if method != 'fixed' and error_est > 0:
            # Compute optimal step size
            if error_est > tol:
                # Step rejected - reduce step size
                h_new = safety_factor * h * (tol / error_est)**(1/3)
                h = max(h_new, min_h)
                continue  # Retry with smaller step
            else:
                # Step accepted - possibly increase step size for next step
                h_new = safety_factor * h * (tol / error_est)**(1/4)
                h_next = min(max(h_new, h/2), max_h)  # Don't change too drastically
        else:
            h_next = h
        
        # Accept the step
        t += h
        y = y_high
        
        t_vals.append(t)
        y_vals.append(y)
        h_vals.append(h)
        error_estimates.append(error_est)
        
        h = h_next
        step_count += 1
    
    return np.array(t_vals), np.array(y_vals), np.array(h_vals), np.array(error_estimates)

def compare_methods():
    """Compare fixed vs adaptive step size methods"""
    
    # Problem setup
    t0, y0 = 0.0, 1.0
    t_end = 2.0
    h_fixed = 0.05
    tol = 1e-4
    
    print("Adaptive Step Size Control Comparison")
    print("="*50)
    print(f"ODE: y' = -20y + 20cos(t) - sin(t)")
    print(f"Exact solution: y(t) = cos(t)")
    print(f"Time interval: [{t0}, {t_end}]")
    print(f"Tolerance: {tol}")
    print()
    
    # Solve with different methods
    methods = {
        'Fixed Step (RK2)': 'fixed',
        'Embedded RK2/3': 'embedded_rk', 
        'Richardson Extrapolation': 'richardson'
    }
    
    results = {}
    
    for name, method in methods.items():
        if method == 'fixed':
            # Fixed step size
            N = int((t_end - t0) / h_fixed)
            t_vals = np.linspace(t0, t_end, N+1)
            y_vals = np.zeros(N+1)
            y_vals[0] = y0
            
            for i in range(N):
                y_vals[i+1] = rk2_step(t_vals[i], y_vals[i], h_fixed)
            
            h_vals = np.full(N, h_fixed)
            error_estimates = np.zeros(N)
        else:
            # Adaptive methods
            t_vals, y_vals, h_vals, error_estimates = adaptive_step_control(
                t0, y0, t_end, h_fixed, tol, method)
        
        # Compute actual errors
        y_exact = exact_solution(t_vals)
        actual_errors = np.abs(y_vals - y_exact)
        
        results[name] = {
            't': t_vals,
            'y': y_vals,
            'h': h_vals,
            'error_est': error_estimates,
            'actual_error': actual_errors,
            'final_error': actual_errors[-1],
            'num_steps': len(h_vals),
            'total_evals': len(h_vals) * (3 if 'Embedded' in name else 2)
        }
        
        print(f"{name}:")
        print(f"  Steps taken: {len(h_vals)}")
        print(f"  Final error: {actual_errors[-1]:.2e}")
        print(f"  Function evaluations: {results[name]['total_evals']}")
        print(f"  Avg step size: {np.mean(h_vals):.4f}")
        print(f"  Min step size: {np.min(h_vals):.4f}")
        print(f"  Max step size: {np.max(h_vals):.4f}")
        print()
    
    return results

def visualize_results(results):
    """Create comprehensive visualization"""
    
    fig = plt.figure(figsize=(16, 12))
    
    # Create exact solution for reference
    t_fine = np.linspace(0, 2, 1000)
    y_fine = exact_solution(t_fine)
    
    # Colors for different methods
    colors = {'Fixed Step (RK2)': 'blue', 
              'Embedded RK2/3': 'red', 
              'Richardson Extrapolation': 'green'}
    
    # Plot 1: Solutions comparison
    ax1 = plt.subplot(2, 3, 1)
    ax1.plot(t_fine, y_fine, 'k-', linewidth=3, label='Exact solution')
    
    for name, data in results.items():
        ax1.plot(data['t'], data['y'], 'o--', color=colors[name], 
                markersize=4, linewidth=1.5, label=name)
    
    ax1.set_xlabel('Time t')
    ax1.set_ylabel('y(t)')
    ax1.set_title('Solution Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Step sizes
    ax2 = plt.subplot(2, 3, 2)
    
    for name, data in results.items():
        if len(data['h']) > 0:
            t_steps = data['t'][:-1]  # Step sizes correspond to intervals
            ax2.semilogy(t_steps, data['h'], 'o-', color=colors[name], 
                        markersize=4, linewidth=1.5, label=name)
    
    ax2.set_xlabel('Time t')
    ax2.set_ylabel('Step size h')
    ax2.set_title('Step Size Evolution')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Error estimates vs actual errors
    ax3 = plt.subplot(2, 3, 3)
    
    for name, data in results.items():
        if len(data['error_est']) > 0 and np.any(data['error_est'] > 0):
            t_steps = data['t'][:-1]
            ax3.semilogy(t_steps, data['error_est'], 's--', color=colors[name], 
                        markersize=4, alpha=0.7, label=f'{name} (estimated)')
        
        ax3.semilogy(data['t'], data['actual_error'], 'o-', color=colors[name], 
                    markersize=4, linewidth=1.5, label=f'{name} (actual)')
    
    ax3.axhline(y=1e-4, color='gray', linestyle=':', alpha=0.7, label='Tolerance')
    ax3.set_xlabel('Time t')
    ax3.set_ylabel('Error')
    ax3.set_title('Error Estimates vs Actual Errors')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Efficiency comparison
    ax4 = plt.subplot(2, 3, 4)
    
    methods = list(results.keys())
    final_errors = [results[name]['final_error'] for name in methods]
    num_evals = [results[name]['total_evals'] for name in methods]
    
    scatter = ax4.scatter(num_evals, final_errors, 
                         c=[colors[name] for name in methods], s=100)
    
    for i, name in enumerate(methods):
        ax4.annotate(name, (num_evals[i], final_errors[i]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    ax4.set_xlabel('Function Evaluations')
    ax4.set_ylabel('Final Error')
    ax4.set_title('Efficiency: Error vs Cost')
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.3)
    
    # Plot 5: Step size distribution
    ax5 = plt.subplot(2, 3, 5)
    
    for name, data in results.items():
        if len(data['h']) > 0:
            ax5.hist(data['h'], bins=20, alpha=0.6, color=colors[name], 
                    label=name, density=True)
    
    ax5.set_xlabel('Step size h')
    ax5.set_ylabel('Density')
    ax5.set_title('Step Size Distribution')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Adaptive control illustration
    ax6 = plt.subplot(2, 3, 6)
    
    # Show step size control for embedded method
    if 'Embedded RK2/3' in results:
        data = results['Embedded RK2/3']
        t_steps = data['t'][:-1]
        
        # Color code by whether step was likely accepted/rejected
        colors_adaptive = ['green' if err < 1e-4 else 'orange' if err < 5e-4 else 'red' 
                          for err in data['error_est']]
        
        for i in range(len(t_steps)):
            ax6.bar(t_steps[i], data['h'][i], width=data['h'][i]*0.8, 
                   color=colors_adaptive[i], alpha=0.7, 
                   edgecolor='black', linewidth=0.5)
    
    ax6.set_xlabel('Time t')
    ax6.set_ylabel('Step size h')
    ax6.set_title('Adaptive Step Control\n(Green: accepted, Orange/Red: challenging)')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def demonstrate_step_control_theory():
    """Demonstrate the theory behind step size control"""
    
    print("\nStep Size Control Theory")
    print("="*40)
    print("1. Error Estimation:")
    print("   - Embedded methods: Use two methods of different orders")
    print("   - Richardson extrapolation: Compare h and h/2 steps")
    print("   - Error estimate: E ≈ |y_high - y_low|")
    print()
    print("2. Step Size Selection:")
    print("   - If E > tol: reject step, reduce h")
    print("   - If E ≤ tol: accept step, possibly increase h")
    print("   - Formula: h_new = safety_factor × h × (tol/E)^(1/(p+1))")
    print("   - where p is the order of the lower-order method")
    print()
    print("3. Benefits:")
    print("   - Automatic accuracy control")
    print("   - Efficiency: large steps where possible, small where needed")
    print("   - Reliability: prevents catastrophic errors")
    print()

if __name__ == "__main__":
    # Run the comparison
    results = compare_methods()
    
    # Create visualizations
    visualize_results(results)
    
    # Show theory
    demonstrate_step_control_theory()
    
    print("Step size control demonstration complete!")
    print("Key insight: Adaptive methods automatically balance accuracy and efficiency.")