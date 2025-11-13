import numpy as np
import matplotlib.pyplot as plt

def f(y, mu=10.0):
    y1, y2 = y
    return np.array([y2, mu * (1.0 - y1**2) * y2 - y1], dtype=float)

def runge_kutta_ex(f, y0, I, h, weights, A):
	A = np.asarray(A, dtype=float)
	b = np.asarray(weights, dtype=float)
	y = np.atleast_1d(np.asarray(y0, dtype=float)).copy()
	t0, tf = float(I[0]), float(I[1])

	s = A.shape[0]
	total = tf - t0
	num_steps = int(round(total / h))
	h_eff = total / num_steps

	d = y.size
	T = np.empty(num_steps + 1, dtype=float)
	Y = np.empty((num_steps + 1, d), dtype=float)
	T[0] = t0
	Y[0] = y

	t = t0
	k = np.zeros((s, d), dtype=float)
	for n in range(num_steps):
		for j in range(s):
			if j == 0:
				y_stage = y
			else:
				y_stage = y + h_eff * np.sum((A[j, :j].reshape(-1, 1)) * k[:j], axis=0)
			kj = np.atleast_1d(np.asarray(f(y_stage), dtype=float)).reshape(-1)
			k[j] = kj
		y = y + h_eff * np.sum((b.reshape(-1, 1)) * k, axis=0)
		t = t + h_eff
		T[n + 1] = t
		Y[n + 1] = y

	return (T, Y)

if __name__ == "__main__":
	y0_vec = np.array([0.0, 1.0])
	I = (0.0, 20.0)
	hs = [0.5, 0.25, 0.125, 0.0625]
	href = 2.0**-14

	A_rk4 = np.array([
		[0.0, 0.0, 0.0, 0.0],
		[0.5, 0.0, 0.0, 0.0],
		[0.0, 0.5, 0.0, 0.0],
		[0.0, 0.0, 1.0, 0.0],
	])
	b_rk4 = np.array([1.0/6, 1.0/3, 1.0/3, 1.0/6])
	results = []
	for h in hs:
		T, Y = runge_kutta_ex(f, y0_vec, I, h, b_rk4, A_rk4)
		results.append((T, Y))

	fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
	for i, (T, Y) in enumerate(results):
		ax1.plot(T, Y[:, 0], label=f'h={hs[i]}')
		ax2.plot(T, Y[:, 1], label=f'h={hs[i]}')

	ax1.set_title("Van der Pol Oscillator (RK4)")
	ax1.set_ylabel("y1(t)")
	ax1.grid(True)
	ax1.legend()

	ax2.set_xlabel("Time t")
	ax2.set_ylabel("y2(t)")
	ax2.grid(True)
	ax2.legend()

	plt.tight_layout()
	plt.show()