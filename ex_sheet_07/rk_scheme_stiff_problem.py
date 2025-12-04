import numpy as np
import matplotlib.pyplot as plt

A_rk4 = np.array([
	[0.0, 0.0, 0.0, 0.0],
	[0.5, 0.0, 0.0, 0.0],
	[0.0, 0.5, 0.0, 0.0],
	[0.0, 0.0, 1.0, 0.0],
])

c_rk4 = np.array([0.0, 0.5, 0.5, 1.0])  # Time offsets
b_rk4 = np.array([1.0/6, 1.0/3, 1.0/3, 1.0/6])
b_rk3 = np.array([1.0/6, 2.0/3, 0.0, 1.0/6])

def f(t, y, lam):
    return -lam * (y - np.exp(-t)) - np.exp(-t)

def exact_solution(t):
    return np.exp(-t)

def solve_adaptive_rk43_stiff(f, y0, I, h0, epsilon, q, lam):
	a, b = I
	t = a
	y = np.atleast_1d(np.asarray(y0, dtype=float)).copy()
	h = h0
	t_values = [t]
	y_values = [y.copy()]
	fevals = 0
	while t < b:
		if t + h > b:
			h = b - t 
		s = A_rk4.shape[0]
		d = y.size
		k = np.zeros((s, d), dtype=float)
		for j in range(s):
			if j == 0:
				y_stage = y
			else:
				y_stage = y + h * np.sum((A_rk4[j, :j].reshape(-1, 1)) * k[:j], axis=0)
			kj = np.atleast_1d(np.asarray(f(t + c_rk4[j] * h, y_stage, lam), dtype=float)).reshape(-1)
			k[j] = kj
			fevals += 1

		y_rk4 = y + h * np.sum((b_rk4.reshape(-1, 1)) * k, axis=0)
		y_rk3 = y + h * np.sum((b_rk3.reshape(-1, 1)) * k, axis=0)

		err_estimate = np.linalg.norm(y_rk4 - y_rk3, ord=np.inf)

		if err_estimate < 1e-16:
			s = 2.0
		else:
			s = (h * epsilon / err_estimate) ** (1.0 / q)

		if s >= 1.0:
			t += h
			y = y_rk4
			t_values.append(t)
			y_values.append(y.copy())
			h = min(2.0, s) * h
		else:
			h = max(0.5, s) * h
			continue
	return np.array(t_values), np.array(y_values), fevals

if __name__ == "__main__":
	lambdas = [1, 1000]
	y0 = 1.0
	I = (0.0, 1.0)
	h0 = 0.01
	epsilon = 1e-4
	q = 3.0

	fig, axes = plt.subplots(2, 2, figsize=(14, 10))
	for lam in lambdas:
		print(f"\n{'='*50}")
		print(f"Lambda = {lam}")
		print(f"{'='*50}")
		
		t_values, y_values, fevals = solve_adaptive_rk43_stiff(f, y0, I, h0, epsilon, q, lam)
		exact_values = exact_solution(t_values)
		error = np.abs(y_values - exact_values)
		max_error = np.max(error)

		print(f"Steps: {len(t_values) - 1}")
		print(f"Function evaluations: {fevals}")
		print(f"Max error: {max_error:.6e}")

		ax1 = axes[lambdas.index(lam), 0]
		ax1.plot(t_values, y_values, 'b-o', markersize=3, 
                 label='Adaptive RK4(3)', alpha=0.7)
		ax1.plot(t_values, exact_values, 'r--', linewidth=2, 
                 label='Exact solution')
		ax1.set_xlabel('t')
		ax1.set_ylabel('y(t)')
		ax1.set_title(f'Solution for λ = {lam}')
		ax1.legend()
		ax1.grid(True, alpha=0.3)

		ax2 = axes[lambdas.index(lam), 1]
		ax2.semilogy(t_values, error, 'g-o', markersize=3)
		ax2.set_xlabel('t')
		ax2.set_ylabel('|Error|')
		ax2.set_title(f'Absolute Error for λ = {lam}')
		ax2.grid(True, alpha=0.3, which='both')
		
	plt.tight_layout()
	plt.savefig('ex_sheet_07/solution_comparison.png', dpi=150)
	plt.show()
		

		
