import numpy as np

def runge_kutta_ex(f, y0, I, h, weights, A):
	"""
	General explicit Runge-Kutta method for solving ODEs.

	Parameters:
	f : function
		The autonomous ODE right-hand side f(y) mapping R^d -> R^d.
	y0 : array_like
		Initial condition.
	I : tuple
		Interval of integration (t0, tf).
	h : float
		Step size.
	weights : array_like
		Weights for the Runge-Kutta method.
	A : 2D array_like
		Coefficient matrix for the Runge-Kutta method.
	
	Returns:
		T : np.ndarray of shape (N+1,)
			Time grid from t0 to tf inclusive.
		Y : np.ndarray of shape (N+1, d)
			Solution values at each time step.
	"""
	# Normalize inputs
	A = np.asarray(A, dtype=float)
	b = np.asarray(weights, dtype=float)
	y = np.atleast_1d(np.asarray(y0, dtype=float)).copy()
	t0, tf = float(I[0]), float(I[1])

	# Basic checks
	if A.ndim != 2 or A.shape[0] != A.shape[1]:
		raise ValueError("A must be a square 2D array (s x s).")
	s = A.shape[0]
	if b.ndim != 1 or b.shape[0] != s:
		raise ValueError("weights b must be a 1D array of length s matching A.")

	# Determine steps to hit tf (use rounding to avoid floating errors)
	total = tf - t0
	if h <= 0:
		raise ValueError("Step size h must be positive.")
	num_steps = int(round(total / h))
	if num_steps <= 0:
		raise ValueError("Number of steps must be positive; check I and h.")
	h_eff = total / num_steps

	# Allocate outputs
	d = y.size
	T = np.empty(num_steps + 1, dtype=float)
	Y = np.empty((num_steps + 1, d), dtype=float)
	T[0] = t0
	Y[0] = y

	# Time stepping
	t = t0
	k = np.zeros((s, d), dtype=float)
	for n in range(num_steps):
		# Stages
		for j in range(s):
			if j == 0:
				y_stage = y
			else:
				# y_stage = y + h_eff * sum_{i<j} A[j,i] * k[i]
				y_stage = y + h_eff * np.sum((A[j, :j].reshape(-1, 1)) * k[:j], axis=0)
			# Evaluate f at stage; ensure 1D shape
			kj = np.atleast_1d(np.asarray(f(y_stage), dtype=float)).reshape(-1)
			if kj.size != d:
				raise ValueError("f(y) must return a vector of the same dimension as y.")
			k[j] = kj

		# Solution update
		y = y + h_eff * np.sum((b.reshape(-1, 1)) * k, axis=0)
		t = t + h_eff
		T[n + 1] = t
		Y[n + 1] = y

	# Return (T, Y) for vector problems; flatten to 1D for scalar
	return (T, Y) if d > 1 else (T, Y.reshape(-1))


if __name__ == "__main__":
	# Test harness: logistic equation y' = g*y*(1 - y/K)
	g = 2.0
	K = 1.0
	y0 = 0.1
	I = (0.0, 5.0)

	def f_logistic(y):
		# Accept vector y (shape (d,)); here d=1
		return g * y * (1.0 - y / K)

	def y_exact(t):
		# Exact solution for logistic equation
		# y(t) = K / (1 + ((K - y0)/y0) * exp(-g t))
		t = np.asarray(t, dtype=float)
		return K / (1.0 + ((K - y0) / y0) * np.exp(-g * t))

	# Example Butcher tableau: Classical RK4 (this butcher tableau is based on exercise 2)
	A_rk4 = np.array([
		[0.0, 0.0, 0.0, 0.0],
		[0.5, 0.0, 0.0, 0.0],
		[0.0, 0.5, 0.0, 0.0],
		[0.0, 0.0, 1.0, 0.0],
	])
	b_rk4 = np.array([1.0/6, 1.0/3, 1.0/3, 1.0/6])

	hs = [0.5, 0.25, 0.125, 0.0625]
	results = []
	for h in hs:
		T, Y = runge_kutta_ex(f_logistic, y0, I, h, b_rk4, A_rk4)
		Y_exact = y_exact(T)
		err = np.abs(Y - Y_exact)
		max_err = float(np.max(err))
		results.append((h, max_err))

	print("h\tmax_error")
	for h, e in results:
		print(f"{h}\t{e:.6e}")

	# Estimate empirical order between successive h values
	if len(results) >= 2:
		print("\nEstimated orders (between successive h):")
		for i in range(len(results)-1):
			h1, e1 = results[i]
			h2, e2 = results[i+1]
			if e2 > 0 and h1 != h2:
				p = np.log(e1/e2) / np.log(h1/h2)
				print(f"p({h1}->{h2}) ≈ {p:.3f}")
			else:
				print(f"p({h1}->{h2}) undefined (zero error or equal h)")