import numpy as np

# Function representing the ODE dy/dt = f(t, y).
def func_f(t, y):
	return ((1 / (t + 1)) - y) / (t + 1)

# Analytical solution for comparison.
def analytical_solution(t):
	return (np.log(t + 1) + 1) / (t + 1)

def explicit_euler(h, f):
	"""Explicit Euler method for solving ODEs.

	Args:
		h (float): Step size.
		f (function): Function representing the ODE dy/dt = f(t, y).
		Returns:
		t_values (np.ndarray): Array of time values.
		y_values (np.ndarray): Array of solution values at corresponding time values.
	"""
	t_values = np.arange(0, 1 + h, h)
	# np.arange is used to create an array of time values from 0 to 1 (inclusive) with a step size of h.
	y_values = np.zeros(len(t_values))
	# np.zeros initializes an array of zeros to store the solution values.
	# Initial condition
	y_values[0] = 1

	"""
	for loop to iterate over each time step and apply the Explicit Euler formula.
	range(1, len(t_values)) is used to start from the second time step since the first value is the initial condition.
	"""
	for i in range(1, len(t_values)):
		t = t_values[i - 1]
		y = y_values[i - 1]
		y_values[i] = y + h * f(t, y)

	return t_values, y_values
if __name__ == "__main__":
	print("\nSolution with h = 0.2:")
	print("======================")
	h = 0.2
	t_values, y_values = explicit_euler(h, func_f)
	"""
	explicit_euler function is called with step size h = 0.2 and the function func_f.
	The returned t_values and y_values are stored in respective variables.
	"""

	# loop to print the results
	# zip is used to iterate over both t_values and y_values simultaneously.
	for t, y in zip(t_values, y_values):
		print(f"t: {t:.2f}, y: {y:.6f}")

	# Error at t=1
	print("\nError at t=1:")
	print("=============")
	error_h1 = abs(y_values[-1] - analytical_solution(1))
	print(f"h = 0.2: Error = {error_h1:.6f}")

	print("\nSolution with h = 0.1:")
	print("======================")
	h = 0.1
	t_values1, y_values1 = explicit_euler(h, func_f)
	"""
	explicit_euler function is called with step size h = 0.1 and the function func_f.
	The returned t_values and y_values are stored in respective variables.
	"""

	# loop to print the results
	# zip is used to iterate over both t_values and y_values simultaneously.
	for t, y in zip(t_values1, y_values1):
		print(f"t: {t:.2f}, y: {y:.6f}")
	
	# Error at t=1
	print("\nError at t=1:")
	print("=============")
	error_h2 = abs(y_values1[-1] - analytical_solution(1))
	print(f"h = 0.1: Error = {error_h2:.6f}")