import numpy as np
import matplotlib.pyplot as plt

# Exact solution: y' = cos(t), y(0)=0
def exact_solution(t):
    return np.sin(t)

# RK4 with interpolation
def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h/2, y + h*k1/2)
    k3 = f(t + h/2, y + h*k2/2)
    k4 = f(t + h, y + h*k3)
    return y + h*(k1 + 2*k2 + 2*k3 + k4)/6

# Solve and compare interpolation methods
f = lambda t, y: np.cos(t)  # y' = cos(t)
t0, t_end = 0, 2*np.pi
h = 0.5
N = int((t_end - t0) / h)

# Compute RK4 points
t_points = [t0]
y_points = [0]
y = 0
t = t0

for k in range(N):
    y = rk4_step(f, t, y, h)
    t = t + h
    t_points.append(t)
    y_points.append(y)

# Linear interpolation
def linear_interp(t_query, t_pts, y_pts):
    idx = np.searchsorted(t_pts, t_query) - 1
    idx = max(0, min(idx, len(t_pts)-2))
    t0, t1 = t_pts[idx], t_pts[idx+1]
    y0, y1 = y_pts[idx], y_pts[idx+1]
    return y0 + (t_query - t0) * (y1 - y0) / (t1 - t0)

# Dense interpolation (for comparison - what we WANT)
t_dense = np.linspace(t0, t_end, 500)
y_exact_dense = exact_solution(t_dense)
y_linear_dense = np.array([linear_interp(t, t_points, y_points) for t in t_dense])

# Error comparison
error_linear = np.abs(y_linear_dense - y_exact_dense)
error_at_nodes = np.abs(np.array(y_points) - exact_solution(np.array(t_points)))

# Plot
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Plot 1: Solutions
ax1 = axes[0, 0]
ax1.plot(t_dense, y_exact_dense, 'k-', linewidth=3, label='Exact: sin(t)')
ax1.plot(t_points, y_points, 'ro', markersize=8, label='RK4 points (order 4)')
ax1.plot(t_dense, y_linear_dense, 'b--', linewidth=2, label='Linear interpolation')

# Fill error region
ax1.fill_between(t_dense, y_exact_dense, y_linear_dense, alpha=0.2, color='red', label='Interpolation error')

ax1.set_xlabel('Time t')
ax1.set_ylabel('y(t)')
ax1.set_title('ORDER LOSS: RK4 + Linear Interpolation\n(4th order → 2nd order between nodes)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Error
ax2 = axes[0, 1]
ax2.semilogy(t_dense, error_linear, 'r-', linewidth=2, label='Interpolation error (between nodes)')
ax2.semilogy(t_points, error_at_nodes, 'bo', markersize=8, label='RK4 error (at nodes)')
ax2.set_xlabel('Time t')
ax2.set_ylabel('Absolute Error (log scale)')
ax2.set_title('Error: At Nodes vs Between Nodes')
ax2.legend()
ax2.grid(True, alpha=0.3, which='both')

# Plot 3: Zoom on one interval
ax3 = axes[1, 0]
zoom_start, zoom_end = 1.0, 1.5
zoom_mask = (t_dense >= zoom_start) & (t_dense <= zoom_end)

# Dense exact in zoom region
t_zoom = np.linspace(zoom_start, zoom_end, 200)
y_exact_zoom = exact_solution(t_zoom)

# Cubic interpolation for comparison (what we should use)
def simple_cubic_interp(t_query, t_pts, y_pts):
    """Simple cubic interpolation without scipy"""
    # Use numpy's polynomial interpolation
    if len(t_pts) >= 4:
        # Use 4 nearest points for cubic
        idx = np.searchsorted(t_pts, t_query) - 1
        idx = max(1, min(idx, len(t_pts)-3))
        t_sub = t_pts[idx-1:idx+3]
        y_sub = y_pts[idx-1:idx+3]
        coeffs = np.polyfit(t_sub, y_sub, 3)
        return np.polyval(coeffs, t_query)
    else:
        return linear_interp(t_query, t_pts, y_pts)

y_cubic_zoom = np.array([simple_cubic_interp(t, t_points, y_points) for t in t_zoom])

# Linear interpolation in zoom
y_linear_zoom = np.array([linear_interp(t, t_points, y_points) for t in t_zoom])

ax3.plot(t_zoom, y_exact_zoom, 'k-', linewidth=3, label='Exact')
ax3.plot(t_zoom, y_linear_zoom, 'r--', linewidth=2, label='Linear interp')
ax3.plot(t_zoom, y_cubic_zoom, 'g:', linewidth=2, label='Cubic spline')
ax3.plot([zoom_start, zoom_end], 
         [linear_interp(zoom_start, t_points, y_points), 
          linear_interp(zoom_end, t_points, y_points)], 
         'ro', markersize=8, label='RK4 points')

ax3.set_xlabel('Time t')
ax3.set_ylabel('y(t)')
ax3.set_title(f'Zoom: [{zoom_start:.1f}, {zoom_end:.1f}]')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Error comparison + Dense output demonstration
ax4 = axes[1, 1]
error_cubic = np.abs(y_cubic_zoom - y_exact_zoom)

# Add dense output (Hermite interpolation simulation)
# For RK4, we can construct 4th order dense output using derivatives
def rk4_dense_output_demo(t_query, t_pts, y_pts, f):
    """Simulate 4th order dense output for RK4"""
    idx = np.searchsorted(t_pts, t_query) - 1
    idx = max(0, min(idx, len(t_pts)-2))
    
    t0, t1 = t_pts[idx], t_pts[idx+1]
    y0, y1 = y_pts[idx], y_pts[idx+1]
    h = t1 - t0
    theta = (t_query - t0) / h
    
    # Use derivative information (f(t,y)) for Hermite interpolation
    f0 = f(t0, y0)
    f1 = f(t1, y1)
    
    # 4th order Hermite interpolation (simplified)
    # This maintains RK4's 4th order accuracy
    return y0 + h * theta * (f0 + theta * (3*(y1-y0)/h - 2*f0 - f1) + 
                            theta**2 * (2*(y1-y0)/h - f0 - f1))

y_dense_zoom = np.array([rk4_dense_output_demo(t, t_points, y_points, f) for t in t_zoom])
error_dense = np.abs(y_dense_zoom - y_exact_zoom)

ax4.semilogy(t_zoom, np.abs(y_linear_zoom - y_exact_zoom), 'r-', linewidth=2, 
             label='Linear interp (O(h²) - ORDER LOSS!)')
ax4.semilogy(t_zoom, error_cubic, 'g--', linewidth=2, label='Cubic spline (O(h⁴))')
ax4.semilogy(t_zoom, error_dense, 'b:', linewidth=2, 
             label='Dense output (O(h⁴) - NO ORDER LOSS!)')

# Add theoretical lines
h_theory = np.array([0.1, 0.5])
ax4.semilogy(t_zoom[[0, -1]], [h**2, h**2], 'r:', alpha=0.5, label='O(h²) theory')
ax4.semilogy(t_zoom[[0, -1]], [h**4*1000, h**4*1000], 'b:', alpha=0.5, label='O(h⁴) theory')

ax4.set_xlabel('Time t')
ax4.set_ylabel('Error (log scale)')
ax4.set_title('Order Loss: Linear vs Dense Output')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.show()

# Print statistics
print("="*60)
print("ORDER LOSS IN INTERPOLATION")
print("="*60)
print(f"Step size h = {h}")
print(f"RK4 order = 4 (error at nodes ~ h⁴ = {h**4:.6f})")
print()
print("KEY CONCEPT: ORDER LOSS")
print("- RK4 gives 4th order accuracy AT GRID POINTS")
print("- Linear interpolation gives only 2nd order BETWEEN grid points")
print("- This is called 'ORDER LOSS' - you lose 2 orders of accuracy!")
print()
print("Maximum errors:")
print(f"  At RK4 nodes:        {np.max(error_at_nodes):.6f} (O(h⁴) = O({h**4:.6f}))")
print(f"  Linear interpolation: {np.max(error_linear):.6f} (O(h²) = O({h**2:.6f}))")
print(f"  Order loss factor: {np.max(error_linear)/np.max(error_at_nodes):.1f}x worse!")
print()
print("THEORETICAL ANALYSIS:")
print("- RK4 local error: C₁h⁵ (4th order method)")
print("- Linear interpolation error: C₂h³ (2nd order interpolation)")
print("- Between nodes: error dominated by interpolation = O(h²)")
print("- At nodes: error from RK4 = O(h⁴)")
print()
print("SOLUTION: Use dense output (continuous extension)")
print("- Hermite interpolation using derivative info")
print("- Maintains 4th order accuracy between grid points")
print("- No order loss!")
print()
print("For smaller h = 0.1:")
print(f"  RK4 nodes: error ~ {0.1**4:.8f}")
print(f"  Linear interp: error ~ {0.1**2:.6f}")
print(f"  Linear is {(0.1**2)/(0.1**4):.0f}x less accurate between nodes!")
print()
print("EXAM KEY POINT:")
print("Order loss occurs when interpolation order < method order")
print("Always use dense output for high-order methods!")