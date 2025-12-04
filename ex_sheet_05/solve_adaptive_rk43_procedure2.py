import numpy as np
import matplotlib.pyplot as plt

A_rk4 = np.array([
	[0.0, 0.0, 0.0, 0.0],
	[0.5, 0.0, 0.0, 0.0],
	[0.0, 0.5, 0.0, 0.0],
	[0.0, 0.0, 1.0, 0.0],
])
b_rk4 = np.array([1.0/6, 1.0/3, 1.0/3, 1.0/6])
b_rk3 = np.array([1.0/6, 2.0/3, 0.0, 1.0/6])

def solve_adaptive_rk43_procedure(f, y0, I, h0, epsilon, q):
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
			kj = np.atleast_1d(np.asarray(f(y_stage), dtype=float)).reshape(-1)
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


def	vdp(y, mu=10.0):
	y1, y2 = y
	return np.array([y2, mu * (1.0 - y1**2) * y2 - y1], dtype=float)

def rk4_fixed(f, y0, I, h):
	a, b = I
	t, y = a, np.array(y0, dtype=float)
	T, Y = [t], [y.copy()]
	while t < b:
		if t + h > b:
			h = b - t  
		k1 = f(y)
		k2 = f(y + 0.5 * h * k1)
		k3 = f(y + 0.5 * h * k2)
		k4 = f(y + h * k3)

		y += (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
		t += h
		T.append(t)
		Y.append(y.copy())
	return np.array(T), np.array(Y)

def interp_ref(Tref, Yref, Tq):
	idx = np.searchsorted(Tref, Tq, side='right')
	idx[idx==0]=1; idx[idx==len(Tref)]=len(Tref)-1
	t0,t1 = Tref[idx-1], Tref[idx]
	w = (Tq - t0)/(t1 - t0)
	return Yref[idx-1]*(1-w)[:,None] + Yref[idx]*w[:,None]

if __name__ == "__main__":
	y0_vec = np.array([0.0, 1.0])
	I = (0.0, 20.0)
	h0 = 1e-4
	epsilon = 1e-4
	q = 3 
	T, Y, fevals = solve_adaptive_rk43_procedure(vdp, y0_vec, I, h0, epsilon, q)

	T_fixed, Y_fixed = rk4_fixed(vdp, y0_vec, I, 0.0625)
	fe_fx = (len(T_fixed) - 1) * 4  # Each RK4 step uses 4 function evaluations
	fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
	ax1.plot(T, Y[:, 0], label='Adaptive RK4(3)', color='blue')
	ax1.plot(T_fixed, Y_fixed[:, 0], label='Fixed RK4', color='orange', linestyle='--')
	ax1.set_ylabel('y1')
	ax1.set_title('Van der Pol Oscillator: Adaptive RK4(3) vs Fixed RK4')
	ax1.legend()
	ax2.plot(T, Y[:, 1], label='Adaptive RK4(3)', color='blue')
	ax2.plot(T_fixed, Y_fixed[:, 1], label='Fixed RK4', color='orange', linestyle='--')
	ax2.set_ylabel('y2')
	ax2.set_xlabel('Time t')
	ax2.legend()
	plt.grid(True)
	plt.show()
	T_ref, Y_ref = rk4_fixed(vdp, y0_vec, I, 2**-14)
	Y_ref_ad = interp_ref(T_ref, Y_ref, T)
	Y_ref_fx = interp_ref(T_ref, Y_ref, T_fixed)
	err_ad = np.max(np.max(np.abs(Y - Y_ref_ad), axis=1))
	err_fx = np.max(np.max(np.abs(Y_fixed - Y_ref_fx), axis=1))
	print(f"fevals(adaptive)={fevals}, err_ad={err_ad:.4e}")
	print(f"fevals(fixed)={fe_fx}, err_fx={err_fx:.4e}")