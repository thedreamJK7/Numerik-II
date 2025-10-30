import numpy as np
import matplotlib.pyplot as plt

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
	half_h = dtype(0.5) * h

	for k in range(N):
		k1 = f(t, y)
		k2 = f(t + half_h, y + half_h * k1)
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
	# Collect arrays for NPZ storage (Explicit Euler)
	Ns_e = []
	hs_e = []
	y32_e = []
	e32_e = []
	y64_e = []
	e64_e = []
	for N in N_values:
		y_approx64 = explicit_euler_method(a, b, y0, N, func_f, dtype=np.float64)
		error64 = abs(y_approx64 - exact_solution(b))
		y_approx32 = explicit_euler_method(a, b, y0, N, func_f, dtype=np.float32)
		error32 = abs(y_approx32 - exact_solution(b))
		h = 1 / N
		print(f"N = {N}, h = {h:.6f}, YN (float64) = {y_approx64:.6f}, Error (float64) = {error64:.6f}, YN (float32) = {y_approx32:.6f}, Error (float32) = {error32:.6f}")

		# store
		Ns_e.append(N)
		hs_e.append(h)
		y32_e.append(float(y_approx32))
		e32_e.append(float(error32))
		y64_e.append(float(y_approx64))
		e64_e.append(float(error64))

	# Save arrays for explicit Euler
	Ns_e = np.array(Ns_e, dtype=np.int32)
	hs_e = np.array(hs_e, dtype=np.float64)
	y32_e = np.array(y32_e, dtype=np.float32)
	e32_e = np.array(e32_e, dtype=np.float32)
	y64_e = np.array(y64_e, dtype=np.float64)
	e64_e = np.array(e64_e, dtype=np.float64)
	log10_h_e = np.log10(hs_e)
	log10_e32_e = np.log10(e32_e)
	log10_e64_e = np.log10(e64_e)
	np.savez("explicit_euler_results.npz",
			 Ns=Ns_e, hs=hs_e,
			 y32=y32_e, e32=e32_e,
			 y64=y64_e, e64=e64_e,
			 log10_h=log10_h_e,
			 log10_e32=log10_e32_e,
			 log10_e64=log10_e64_e)

	print("\nImproved Euler method:")
	print("========================")
	# Collect arrays for NPZ storage (Improved Euler)
	Ns_i = []
	hs_i = []
	y32_i = []
	e32_i = []
	y64_i = []
	e64_i = []
	for N in N_values:
		y_approx64 = improved_euler_method(a, b, y0, N, func_f, dtype=np.float64)
		error64 = abs(y_approx64 - exact_solution(b))
		y_approx32 = improved_euler_method(a, b, y0, N, func_f, dtype=np.float32)
		error32 = abs(y_approx32 - exact_solution(b))
		h = 1 / N
		print(f"N = {N}, h = {h:.6f}, YN (float64) = {y_approx64:.6f}, Error (float64) = {error64:.6f}, YN (float32) = {y_approx32:.6f}, Error (float32) = {error32:.6f}")

		# store
		Ns_i.append(N)
		hs_i.append(h)
		y32_i.append(float(y_approx32))
		e32_i.append(float(error32))
		y64_i.append(float(y_approx64))
		e64_i.append(float(error64))

	# Save arrays for improved Euler
	Ns_i = np.array(Ns_i, dtype=np.int32)
	hs_i = np.array(hs_i, dtype=np.float64)
	y32_i = np.array(y32_i, dtype=np.float32)
	e32_i = np.array(e32_i, dtype=np.float32)
	y64_i = np.array(y64_i, dtype=np.float64)
	e64_i = np.array(e64_i, dtype=np.float64)
	log10_h_i = np.log10(hs_i)
	log10_e32_i = np.log10(e32_i)
	log10_e64_i = np.log10(e64_i)
	np.savez("improved_euler_results.npz",
			 Ns=Ns_i, hs=hs_i,
			 y32=y32_i, e32=e32_i,
			 y64=y64_i, e64=e64_i,
			 log10_h=log10_h_i,
			 log10_e32=log10_e32_i,
			 log10_e64=log10_e64_i)
	
	data = np.load("explicit_euler_results.npz")
	hs   = data["hs"]
	e32  = data["e32"]
	e64  = data["e64"]

	plt.figure(figsize=(6,4))
	plt.loglog(hs, e32, "o-", label="float32")
	plt.loglog(hs, e64, "s-", label="float64")
	plt.gca().invert_xaxis()               # optional: smaller h to the right
	plt.xlabel("h = 1/N")
	plt.ylabel("absolute error |Y_N - 1|")
	plt.title("Error vs h (Explicit Euler)")
	plt.grid(True, which="both", ls=":", alpha=0.6)
	plt.legend()
	plt.tight_layout()
	plt.savefig("explicit_euler_errors.png", dpi=150)

	data = np.load("improved_euler_results.npz")
	hs   = data["hs"]
	e32  = data["e32"]
	e64  = data["e64"]

	plt.figure(figsize=(6,4))
	plt.loglog(hs, e32, "o-", label="float32")
	plt.loglog(hs, e64, "s-", label="float64")
	plt.gca().invert_xaxis()
	plt.xlabel("h = 1/N")
	plt.ylabel("absolute error |Y_N - 1|")
	plt.title("Error vs h (Improved Euler)")
	plt.grid(True, which="both", ls=":", alpha=0.6)
	plt.legend()
	plt.tight_layout()
	plt.savefig("improved_euler_errors.png", dpi=150)
