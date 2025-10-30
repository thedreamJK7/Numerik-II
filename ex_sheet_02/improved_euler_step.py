import numpy as np

# Function representing the ODE dy/dt = f(t, y).
def func_f(t, y):
	return -200 * t * y**2

# Exact solution for error calculation
def exact_solution(t):
	return 1 / (1 + 100 * t**2)

# Explicit Euler method
def explicit_euler_method(a, b, y0, N, f, dtype=np.float64):
	"""Explicit Euler method for solving ODEs.

	Args:
		a (float): Start of the interval.
		b (float): End of the interval.
		y0 (float): Initial condition y(a).
		N (int): Number of steps.
		f (function): Function representing the ODE dy/dt = f(t, y).
		dtype (data-type): Desired data-type for the arrays.
	Returns:
		y N values at corresponding time values.
	"""
	h = dtype(b - a) / dtype(N)
	y = dtype(y0)
	t = dtype(a)

	for k in range(N):
		y = y + h * f(t, y)
		t = t + h
	return y

# Improved Euler (Heun's) method
def improved_euler_method(a, b, y0, N, f, dtype=np.float64):
	"""Improved Euler (Heun's) method for solving ODEs.

	Args:
		a (float): Start of the interval.
		b (float): End of the interval.
		y0 (float): Initial condition y(a).
		N (int): Number of steps.
		f (function): Function representing the ODE dy/dt = f(t, y).
		dtype (data-type): Desired data-type for the arrays.
	Returns:
		y N values at corresponding time values.
	"""
	h = dtype(b - a) / dtype(N)
	y = dtype(y0)
	t = dtype(a)

	for k in range(N):
		k1 = f(t, y)
		k2 = f(t + dtype(0.5) * h, y + dtype(0.5) * h * k1)
		y = y + h * k2
		t = t + h
	return y

if __name__ == "__main__":
	a = -1.0
	b = 0.0
	y0 = 1.0 / 101.0

	print("\nEuler method:")
	print("========================")
	N_values = [25, 50, 100, 200, 400, 800, 1600]
	for N in N_values:
		y_approx64 = explicit_euler_method(a, b, y0, N, func_f, dtype=np.float64)
		error64 = abs(y_approx64 - exact_solution(b))
		y_approx32 = explicit_euler_method(a, b, y0, N, func_f, dtype=np.float32)
		error32 = abs(y_approx32 - exact_solution(b))
		h = 1 / N
		print(f"N = {N}, h = {h:.6f}, YN (float64) = {y_approx64:.6f}, Error (float64) = {error64:.6f}, YN (float32) = {y_approx32:.6f}, Error (float32) = {error32:.6f}")

	print("\nImproved Euler method:")
	print("========================")
	for N in N_values:
		y_approx64 = improved_euler_method(a, b, y0, N, func_f, dtype=np.float64)
		error64 = abs(y_approx64 - exact_solution(b))
		y_approx32 = improved_euler_method(a, b, y0, N, func_f, dtype=np.float32)
		error32 = abs(y_approx32 - exact_solution(b))
		h = 1 / N
		print(f"N = {N}, h = {h:.6f}, YN (float64) = {y_approx64:.6f}, Error (float64) = {error64:.6f}, YN (float32) = {y_approx32:.6f}, Error (float32) = {error32:.6f}")
