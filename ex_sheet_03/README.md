# Explicit Runge–Kutta (RK) Solver — Numerics II, Exercise Sheet 3

This project provides a general, explicit Runge–Kutta (RK) solver for autonomous ODEs of the form

  y'(t) = f(y(t)),  t ∈ (a, b],  y(a) = y0

implemented in `runge_kutta_ex.py`. The solver accepts an arbitrary explicit RK method via its Butcher tableau (A, b). A small test harness (in the `__main__` block) demonstrates the solver on the scalar logistic equation and reports the maximal error for several step sizes.

## Files
- `runge_kutta_ex.py` — The RK solver and a test harness for the logistic equation.

## Requirements
- Python 3.8+
- NumPy

Install NumPy if needed:

```bash
pip install numpy
```

## Usage
Run the script directly to execute the logistic test with a default RK4 tableau:

```bash
python3 runge_kutta_ex.py
```

It will print the maximum error over the time grid for h ∈ {0.5, 0.25, 0.125, 0.0625} and estimate the empirical order between successive step sizes.

Example output (RK4 on the logistic equation):

```
h       max_error
0.5     9.573491e-04
0.25    6.332652e-05
0.125   4.381826e-06
0.0625  2.883755e-07

Estimated orders (between successive h):
p(0.5->0.25) ≈ 3.918
p(0.25->0.125) ≈ 3.853
p(0.125->0.0625) ≈ 3.926
```

## API
### `runge_kutta_ex(f, y0, I, h, weights, A)`
General explicit RK stepper for autonomous ODEs.

- `f`: callable `f(y) -> array_like`, the autonomous right-hand side.
- `y0`: initial state (scalar or 1D array of length d).
- `I`: tuple `(t0, tf)`, integration interval.
- `h`: nominal step size (float). The solver chooses an integer number of steps N ≈ (tf−t0)/h and uses an effective step `h_eff = (tf−t0)/N` to land exactly on `tf`.
- `weights`: 1D array-like of length `s` — the RK weights `b`.
- `A`: 2D array-like `(s, s)` — the RK coefficient matrix for an explicit method (strictly lower triangular in practice).

Returns:
- `T`: array of shape `(N+1,)` — the time grid from `t0` to `tf`.
- `Y`: if `y0` is scalar, `Y` is 1D of shape `(N+1,)`; otherwise `Y` is 2D of shape `(N+1, d)`.

Update formulas used:
- Stage values: `k_j = f(y_n + h_eff * sum_{i<j} A[j,i] * k_i)` for `j = 0..s-1`.
- Solution update: `y_{n+1} = y_n + h_eff * sum_{j=0..s-1} b[j] * k_j`.

Input validation:
- Checks that `A` is square and `len(b) == A.shape[0]`.
- Ensures `f(y)` returns the same dimension as `y`.

## Changing the RK Method (Butcher tableau)
In the `__main__` section, a classical RK4 tableau is provided as an example:

```python
A_rk4 = np.array([
    [0.0, 0.0, 0.0, 0.0],
    [0.5, 0.0, 0.0, 0.0],
    [0.0, 0.5, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
])
b_rk4 = np.array([1.0/6, 1.0/3, 1.0/3, 1.0/6])
```

To use the method you derived in Exercise 2, simply replace `A_rk4` and `b_rk4` with your `(A, b)` values and re-run the script.

## The Logistic Test
The main script uses the logistic equation

```
y' = g y (1 − y/K),  y(0) = y0
```

with parameters `g = 2`, `K = 1`, `y0 = 0.1`, over `I = [0, 5]`. The exact solution is

```
y(t) = K / (1 + ((K − y0)/y0) * exp(−g t)).
```

For each step size `h` in `{0.5, 0.25, 0.125, 0.0625}`, the code computes

```
max_k | y_num(t_k) − y_exact(t_k) |
```

and prints the result. Using RK4, the errors decrease roughly like `O(h^4)`.

## Notes
- The solver is for autonomous right-hand sides `f(y)`; if your function depends on time, you can extend the stages to pass `t + c_j*h` as needed.
- If `(b − a)/h` is not (close to) an integer, the solver rounds the number of steps and adjusts `h_eff` so the last step hits `tf` exactly.
- Works for both scalar and vector-valued problems (y in R^d).

## License
This code is provided as-is for educational purposes in the context of Numerics II exercises.

## Author
Javokhir Kubaev

