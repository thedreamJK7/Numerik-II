# Exercise Sheet 5 – Adams–Bashforth (Order 2) and Adaptive RK4(3)

This sheet contains two independent numerical ODE exercises implemented in Python:
1. A constant step-size explicit two-step Adams–Bashforth method of order 2 applied to a scalar nonlinear IVP with known exact solution (file `adam_bashforth.py`).
2. An adaptive embedded Runge–Kutta 4(3) procedure with automatic step-size control applied to the Van der Pol oscillator (file `solve_adaptive_rk43_procedure.py`).

Both scripts use only `numpy` and `matplotlib`.

---
## 1. Adams–Bashforth Method of Order 2 (`adam_bashforth.py`)
### Problem Definition
Initial value problem (IVP):
\[ y'(t) = -200\, t\, y(t)^2, \quad t \in [-1,0], \qquad y(-1) = \frac{1}{101}. \]
Exact solution:
\[ y(t) = \frac{1}{100 t^2 + 1}. \]
The right–hand side function is:
\[ f(t,y) = -200\, t\, y^2. \]

### Numerical Method
The two-step Adams–Bashforth (AB2) scheme for uniform step size \( h = (b-a)/N = 1/N \) and nodes \( t_k = a + k h \) is:
\[ Y_{k+1} = Y_k + \frac{h}{2} \big( 3 f(t_k,Y_k) - f(t_{k-1},Y_{k-1}) \big), \quad k \ge 1. \]
Because AB2 is a two-step method, a single starting value beyond the initial condition is required. We obtain \( Y_1 \) using the explicit Euler method:
\[ Y_1 = Y_0 + h f(t_0, Y_0). \]
After this, the AB2 recurrence advances the solution.

### Implementation Notes
- The function `adam_bashforth_method_m2(a, b, y0, N, f)` returns arrays `(Y, T)` with the numerical solution and time grid.
- The script loops over \( N \in \{25, 50, 100, 200, 400, 800, 1600\} \) and stores maximum errors:
  \[ E_N = \max_{0\le k \le N} |Y_k - y(t_k)|. \]
- The empirical convergence order between successive refinements is computed by:
  \[ p \approx \frac{ \log(E_{N_{i-1}}/E_{N_i}) }{ \log(h_{i-1}/h_i) }. \]
Since AB2 has global order 2, the printed orders should be close to 2.

### Output
The script prints a summary table of `N`, step size `h = 1/N`, maximum error `E_N`, and pairwise estimated orders. It also plots the numerical solution curves versus the exact solution.

### How to Run
```bash
python adam_bashforth.py
```
Expected behavior:
- A plot window with curves for each `N` and the exact solution (dashed).
- Console output listing estimated orders ≈ 2.

---
## 2. Adaptive Embedded Runge–Kutta 4(3) (`solve_adaptive_rk43_procedure.py`)
### Problem Definition
We solve the (moderately stiff for larger \(\mu\)) Van der Pol system:
\[
\begin{cases}
 y_1' = y_2, \\
 y_2' = \mu (1 - y_1^2) y_2 - y_1,
\end{cases}
\]
with parameters:
- \( \mu = 10 \) (in code: `mu=10.0`),
- Initial condition: \( y(0) = (0, 1) \),
- Interval: \( t \in [0, 20] \).

### Embedded Pair and Error Estimate
The code implements a classical 4-stage RK4 tableau for the primary 4th-order solution and an embedded 3rd-order estimate using alternative weights:
- 4th order weights: \( b = (1/6, 1/3, 1/3, 1/6) \)
- 3rd order embedded weights: \( b^* = (1/6, 2/3, 0, 1/6) \)
After computing all stage derivatives \( k_j \), two solutions are formed: \( y_{\text{RK4}} \) and \( y_{\text{RK3}} \). The infinity-norm local error estimate:
\[ \| y_{\text{RK4}} - y_{\text{RK3}} \|_{\infty} \]
serves to adapt the step size.

### Step-Size Adaptation Strategy
Let \( h \) be the current step, \( \varepsilon \) the tolerance, and \( q \) the order of the lower method (here \( q=3 \)). The scaling factor:
\[ s = \left( \frac{h \varepsilon}{\text{err}} \right)^{1/q} \]
(if `err` extremely small, a cap like `s=2.0` is used). Decisions:
- If \( s \ge 1 \): accept the step, advance \( t \leftarrow t + h \), enlarge next step: \( h_{\text{new}} = \min(2, s) h \).
- Else: reject the step and shrink \( h_{\text{new}} = \max(0.5, s) h \); recompute at same \( t \).
The integration stops exactly at \( b \) by truncating the last step when `t + h > b`.

### Additional Components
- `rk4_fixed`: Uniform step classic RK4 for comparison.
- High-fidelity reference solution via RK4 with a very small step (`2**-14`) is computed for post-run error assessment.
- `interp_ref`: Linear interpolation of the reference solution at adaptive and fixed time grids for fair error comparison.
- Reported metrics: number of function evaluations (`fevals`) and maximum deviations from the reference for adaptive vs fixed methods.

### Output
Running the script produces:
- Two stacked plots comparing adaptive RK4(3) and fixed-step RK4 trajectories for `y1` and `y2`.
- Printed statistics: total function evaluations and reference-based maximum errors for each method.
Adaptive integration should typically achieve comparable accuracy with fewer function evaluations than a coarse fixed step, or higher accuracy for similar cost when the tolerance is tightened.

### How to Run
```bash
python solve_adaptive_rk43_procedure.py
```
Adjustable parameters (near bottom of the file):
- `h0`: initial step size (e.g. `1e-4`).
- `epsilon`: error tolerance (e.g. `1e-4`).
- `q`: lower order (keep `q=3` for RK4(3)).
You can experiment by decreasing `epsilon` to test robustness and observe smaller adaptive steps in stiff regions.

### Notes on Efficiency
- Storing results in Python lists then converting to NumPy arrays at the end avoids repeated reallocation overhead of `np.append`.
- A safety factor (e.g. multiply `s` by 0.9) is sometimes used in production codes to avoid step rejection oscillations; here a simple clamp is applied.

---
## 3. Dependencies
Install required libraries if missing:
```bash
pip install numpy matplotlib
```
Python version: Any modern 3.x version should work.

---
## 4. Interpreting Convergence (AB2)
For the Adams–Bashforth test, a log–log plot of `E_N` vs `h` should display a slope ≈ 2. The empirical order calculation in the script confirms second-order global accuracy.

---
## 5. Possible Extensions
- Replace the Euler starter with a higher-order one-step method (e.g. RK2) to reduce starting error.
- Add a safety factor and minimum/maximum step constraints in the adaptive RK routine.
- Implement a more advanced interpolation (Hermite) for the reference projection.
- Generalize the adaptive procedure to arbitrary embedded Runge–Kutta pairs.

---
## 6. References
- Hairer, Nørsett, Wanner: *Solving Ordinary Differential Equations I*.
- Butcher: *Numerical Methods for Ordinary Differential Equations*.
- Standard RK4 and Adams–Bashforth method derivations (any introductory numerical analysis text).

---
## 7. License / Usage
Educational code for exercise purposes. Use and modify freely for learning.

---
## 8. Quick Summary
| File | Purpose | Method | Adaptivity |
|------|---------|--------|------------|
| `adam_bashforth.py` | Fixed-step solution of scalar nonlinear IVP | AB2 + Euler start | No |
| `solve_adaptive_rk43_procedure.py` | Van der Pol oscillator | Embedded RK4(3) | Yes |

Happy experimenting!
