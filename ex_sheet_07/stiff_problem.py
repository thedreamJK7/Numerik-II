import numpy as np
import matplotlib.pyplot as plt

# 1. f(t, y) funksiyasini aniqlash
# ODE (from problem statement): y'(t) = -λ(y(t) - e^(-t)) - e^(-t), y(0) = 1
def f(t, y, lam):
    return -lam * (y - np.exp(-t)) - np.exp(-t)

# 2. Aniq yechim
# From problem statement: y(t) = e^(-t) for all λ ∈ ℝ
def exact_solution(t):
    return np.exp(-t)

# 3. Har bir usulni implement qilish
def explicit_euler(f, y0, t_grid, lam):
	y_values = np.zeros(len(t_grid))
	y_values[0] = y0
	h = t_grid[1] - t_grid[0]
	for i in range(1, len(t_grid)):
		t = t_grid[i - 1]
		y = y_values[i - 1]
		y_values[i] = y + h * f(t, y, lam)
	return y_values
    
def improved_euler(f, y0, t_grid, lam):
	y_values = np.zeros(len(t_grid))
	y_values[0] = y0
	h = t_grid[1] - t_grid[0]
	for i in range(1, len(t_grid)):
		t = t_grid[i - 1]
		y = y_values[i - 1]
		# Midpoint method: Y_{k+1} = Y_k + h*f(t_k + h/2, Y_k + (h/2)*f(t_k, Y_k))
		k = f(t, y, lam)
		y_values[i] = y + h * f(t + h/2, y + (h/2)*k, lam)
	return y_values
    
def rk4(f, y0, t_grid, lam):
	y_values = np.zeros(len(t_grid))
	y_values[0] = y0
	h = t_grid[1] - t_grid[0]
	for i in range(1, len(t_grid)):
		t = t_grid[i - 1]
		y = y_values[i - 1]
		k1 = f(t, y, lam)
		k2 = f(t + h / 2, y + (h / 2) * k1, lam)
		k3 = f(t + h / 2, y + (h / 2) * k2, lam)
		k4 = f(t + h, y + h * k3, lam)
		y_values[i] = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
	return y_values
    
def adams_bashforth_2(f, y0, t_grid, lam):
	y_values = np.zeros(len(t_grid))
	y_values[0] = y0
	h = t_grid[1] - t_grid[0]
	# First step using Explicit Euler
	y_values[1] = y_values[0] + h * f(t_grid[0], y_values[0], lam)
	for i in range(2, len(t_grid)):
		t_n1 = t_grid[i - 1]
		t_n2 = t_grid[i - 2]
		y_n1 = y_values[i - 1]
		y_n2 = y_values[i - 2]
		y_values[i] = y_n1 + (h / 2) * (3 * f(t_n1, y_n1, lam) - f(t_n2, y_n2, lam))
	return y_values

# 4. Xatolikni hisoblash
def compute_max_error(numerical, exact):
    return np.max(np.abs(numerical - exact))

# 5. Natijalarni chiqarish va grafik chizish
if __name__ == "__main__":
	# Parametrlar (mashq bo'yicha)
	y0 = 1.0
	t0, tf = 0.0, 1.0
	h = 0.01  # Mashqda berilgan
	N = int((tf - t0) / h)
	t_grid = np.linspace(t0, tf, N + 1)
	
	lambdas = [1, 1000]  # Ikki holat
	methods = {"Explicit Euler": explicit_euler,
			   "Improved Euler": improved_euler,
			   "RK4": rk4,
			   "Adams-Bashforth 2": adams_bashforth_2}
	
	# a) Jadval uchun xatoliklarni hisoblash
	print("=" * 60)
	print("PART A: Maximum Nodal Error (E_max) Table")
	print("=" * 60)
	print(f"{'Method':<25} {'λ = 1':<15} {'λ = 1000':<15}")
	print("-" * 60)
	
	results = {}
	# Exact solution is the same for all λ: y(t) = e^(-t)
	exact_vals = exact_solution(t_grid)  # lam doesn't matter
	
	for name, method in methods.items():
		errors_for_method = []
		for lam in lambdas:
			numerical_vals = method(f, y0, t_grid, lam)
			error = compute_max_error(numerical_vals, exact_vals)
			errors_for_method.append(error)
			results[(name, lam)] = numerical_vals
		print(f"{name:<25} {errors_for_method[0]:<15.6e} {errors_for_method[1]:<15.6e}")
	
	# b) Grafiklar chizish
	for lam in lambdas:
		fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
		
		# Aniq yechim (same for all λ)
		exact_vals = exact_solution(t_grid)
		
		# LEFT PLOT: Normal scale
		ax1.plot(t_grid, exact_vals, 'k-', linewidth=2, label='Exact Solution', zorder=10)
		
		# Raqamli yechimlar
		colors = ['b', 'g', 'r', 'm']
		markers = ['o', 's', '^', 'd']
		for (name, method), color, marker in zip(methods.items(), colors, markers):
			numerical_vals = results[(name, lam)]
			# Faqat finite qiymatlarni plot qilish
			mask = np.isfinite(numerical_vals)
			if np.any(mask):
				ax1.plot(t_grid[mask], numerical_vals[mask], color=color, marker=marker, 
						 markevery=max(1, np.sum(mask)//10), markersize=4, 
						 label=f"{name} ({'unstable' if not np.all(mask) else 'stable'})", alpha=0.7)
			else:
				ax1.plot([], [], color=color, label=f"{name} (completely unstable)")
		
		ax1.set_xlabel('t', fontsize=12)
		ax1.set_ylabel('y(t)', fontsize=12)
		ax1.set_title(f'Solutions for λ = {lam} (Linear Scale)', fontsize=14)
		ax1.legend(loc='best', fontsize=9)
		ax1.grid(True, alpha=0.3)
		
		# Y-axis ni cheklash
		if lam == 1:
			ax1.set_ylim([0, 1.2])
		else:
			ax1.set_ylim([-2, 2])
		
		# RIGHT PLOT: Error plot (log scale)
		for (name, method), color, marker in zip(methods.items(), colors, markers):
			numerical_vals = results[(name, lam)]
			errors = np.abs(numerical_vals - exact_vals)
			# NaN va Inf larni handle qilish
			errors = np.where(np.isfinite(errors), errors, 1e100)
			# 0 bo'lgan errorlarni 1e-16 bilan almashtirish (log uchun)
			errors = np.where(errors == 0, 1e-16, errors)
			ax2.semilogy(t_grid, errors, color=color, marker=marker,
						 markevery=10, markersize=4, label=name, alpha=0.7)
		
		ax2.set_xlabel('t', fontsize=12)
		ax2.set_ylabel('|Error|', fontsize=12)
		ax2.set_title(f'Absolute Error for λ = {lam} (Log Scale)', fontsize=14)
		ax2.legend(loc='best')
		ax2.grid(True, alpha=0.3, which='both')
		
	plt.show()
	
	# c) Tahlil
	print("\n" + "=" * 60)
	print("PART C: Performance Analysis")
	print("=" * 60)
	print("\nλ = 1 (Non-stiff case):")
	print("  - Barcha usullar yaxshi ishlaydi")
	print("  - RK4 eng yuqori aniqlikka ega")
	print("  - Explicit Euler ham qoniqarli natija beradi")
	print("\nλ = 1000 (Stiff case):")
	print("  - Explicit Euler beqaror (juda katta xatolik)")
	print("  - Improved Euler ham yetarlicha yaxshi emas")
	print("  - RK4 nisbatan yaxshiroq, lekin hali ham muammoli")
	print("  - Adams-Bashforth ham stiff problemda qiynaladi")
	print("\nXulosa: Stiff problemlar uchun implicit usullar kerak!")
	print("=" * 60)