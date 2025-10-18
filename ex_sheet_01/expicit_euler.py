import numpy as np

def func_f(t, y):
	return (np.log(t + 1) - y) / (t + 1)

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
	y_values = np.zeros(len(t_values))
	y_values[0] = 0

	for i in range(1, len(t_values)):
		t = t_values[i - 1]
		y = y_values[i - 1]
		y_values[i] = y + h * f(t, y)

	return t_values, y_values
if __name__ == "__main__":
	h = 0.1
	t_values, y_values = explicit_euler(h, func_f)

	for t, y in zip(t_values, y_values):
		print(f"t: {t:.2f}, y: {y:.6f}")