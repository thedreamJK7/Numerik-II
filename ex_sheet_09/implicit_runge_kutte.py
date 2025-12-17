import numpy as np
import matplotlib.pyplot as plt

def get_gauss_tableau():
    sqrt3 = np.sqrt(3)

    c = np.array([
		1/2 - sqrt3/6,
        1/2 + sqrt3/6
    ])
    A = np.array([
        [1/4,           1/4 - sqrt3/6],
        [1/4 + sqrt3/6, 1/4          ]
    ])
    b = np.array([1/2, 1/2])
    
    return c, A, b

def get_sdirk_tableau():
    sqrt3 = np.sqrt(3)
    a_plus = 1/2 + sqrt3/6
    c = np.array([
        a_plus,
        1 - a_plus
    ])
    A = np.array([
		[a_plus,        0      ],
		[1 - 2*a_plus,  a_plus ]
    ])
    
    b = np.array([1/2, 1/2])
    return c, A, b

def f(t, y, lam):
    return -lam * (y - np.exp(-t)) - np.exp(-t)

def df_dy(t, y, lam):
    return -lam

def exact_solution(t):
    return np.exp(-t)

def solve_implicit_rk(method_name, N, lam):
    if method_name.lower() == 'gauss':
        c, A, b = get_gauss_tableau()
    elif method_name.lower() == 'sdirk':
        c, A, b = get_sdirk_tableau()
    else:
        raise ValueError("method_name must be 'gauss' or 'sdirk'")
    t0, tf = 0.0, 1.0
    y0 = 1.0
    h = (tf - t0) / N
    t_vals = np.linspace(t0, tf, N + 1)
    y_vals = np.zeros(N + 1)
    y_vals[0] = y0
    
    s = len(c)
    for n in range(N):
        t_n = t_vals[n]
        y_n = y_vals[n]
        k = solve_stage_equations(t_n, y_n, h, c, A, lam, method_name)
        y_vals[n + 1] = y_n + h * np.dot(b, k)    
    return t_vals, y_vals

def solve_stage_equations(t_n, y_n, h, c, A, lam, method_name):
    s = len(c)
    I = np.eye(s)
    matrix = I + lam * h * A
    
    rhs = np.zeros(s)
    for i in range(s):
        t_stage = t_n + c[i] * h
        exp_neg_t = np.exp(-t_stage)
        rhs[i] = -lam * (y_n - exp_neg_t) - exp_neg_t
    
    k = np.linalg.solve(matrix, rhs)
    return k

if __name__ == "__main__":
    lambdas = [10, 100, 1000, 1e4, 1e5]
    N_values = [20, 40]
    methods = ['gauss', 'sdirk']
    
    print("=" * 80)
    print("IMPLICIT RUNGE-KUTTA METHODS FOR STIFF PROBLEMS")
    print("=" * 80)
    
    print("\nGAUSS METHOD TABLEAU:")
    c_g, A_g, b_g = get_gauss_tableau()
    print(f"c = {c_g}")
    print(f"A = \n{A_g}")
    print(f"b = {b_g}")
    
    print("\nSDIRK METHOD TABLEAU:")
    c_s, A_s, b_s = get_sdirk_tableau()
    print(f"c = {c_s}")
    print(f"A = \n{A_s}")
    print(f"b = {b_s}")
    
    y_exact_at_1 = exact_solution(1.0)
    print(f"\nExact solution at t=1: y(1) = e^(-1) = {y_exact_at_1:.10f}")
    
    print("\n" + "=" * 80)
    print("RESULTS TABLE")
    print("=" * 80)
    print(f"{'λ':<8} {'E_Gauss(20,λ)':<15} {'p_Gauss(λ)':<12} {'E_SDIRK(20,λ)':<15} {'p_SDIRK(λ)':<12}")
    print("-" * 80)
    
    for lam in lambdas:
        results = {}
        
        for method in methods:
            errors = {}
            for N in N_values:
                t_vals, y_vals = solve_implicit_rk(method, N, lam)
                
                y_numerical = y_vals[-1]
                error = abs(y_numerical - y_exact_at_1)
                errors[N] = error
            
            if errors[40] > 0:
                p = np.log2(errors[20] / errors[40])
            else:
                p = float('inf')
            
            results[method] = {
                'error_20': errors[20],
                'p': p
            }
        
        print(f"{lam:<8.0e} {results['gauss']['error_20']:<15.6e} "
              f"{results['gauss']['p']:<12.2f} {results['sdirk']['error_20']:<15.6e} "
              f"{results['sdirk']['p']:<12.2f}")