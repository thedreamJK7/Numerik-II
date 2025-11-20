import numpy as np
import matplotlib.pyplot as plt

# Function representing the ODE dy/dt = f(t, y).
def func_f(t, y):
	return -200 * t * y**2

# Exact solution for error calculation
def exact_solution(t):
	return 1 / (1 + 100 * t**2)

def adam_bashforth_method_m2(a, b, y0, N, f, dtype=np.float64):
	"""2nd-order Adams-Bashforth method for solving ODEs.

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
	Y = np.array([y0], dtype=dtype)
	T = np.array([t], dtype=dtype)

	# First step using Explicit Euler
	y = y + h * f(t, y)
	t = t + h
	Y = np.append(Y, y)
	T = np.append(T, t)
	for k in range(1, N):
		y = y + h/2 * (3*f(t, y) - f(t - h, Y[-2]))
		t = t + h
		Y = np.append(Y, y)
		T = np.append(T, t)
	return Y, T

if __name__ == "__main__":
	# a part
	y0 = 1.0 / 101.0  # Initial condition
	a = -1.0          # Start of the interval
	b = 0.0           # End of the interval
	N = [25, 50, 100, 200, 400, 800, 1600]  # Different step counts
	errors = []
	Y = []
	T = []
	results = []

	for n in N:
		Y, T = adam_bashforth_method_m2(a, b, y0, n, func_f)
		results.append((T, Y))
		exact = exact_solution(T)
		error = np.abs(Y - exact).max()
		errors.append(error)
	
	# b part
	plt.figure(figsize=(10, 6))
	for i, n in enumerate(N):
		T, Y = results[i]
		plt.plot(T, Y, label=f'Adams-Bashforth M=2, N={n}')
	plt.plot(T, exact_solution(T), 'k--', label='Exact Solution')
	plt.title("Adams-Bashforth Method M=2 Solutions")
	plt.xlabel("t")
	plt.ylabel("y(t)")
	plt.legend()
	plt.grid()
	plt.show()
	# c part
	h_vals = [1.0/n for n in N]
	orders = []
	print("\nEstimated Orders of Convergence:")
	for i in range(1, len(errors)):
		p = np.log(errors[i-1]/errors[i]) / np.log(h_vals[i-1]/h_vals[i])
		orders.append(p)
		print(f"N={N[i-1]} -> N={N[i]} order ≈ {p:.4f}")

	print("\nSummary:")
	print("N\t h\t\t E_N")
	for n, h, e in zip(N, h_vals, errors):
		print(f"{n}\t {h:.6f}\t {e:.6e}")

	