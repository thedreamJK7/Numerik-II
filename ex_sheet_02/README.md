# Numerik-II — How to Run

This repository contains Python scripts for numerical ODE experiments (Explicit Euler and Improved Euler). The main runner is `ex_sheet_02/improved_euler_step.py`.

## Requirements
- macOS with Python 3
- Packages:
  - numpy (required)
  - matplotlib (optional, for plotting)

### Option A: Use system/user Python
```
python3 --version
python3 -m pip install --user --upgrade pip
python3 -m pip install --user numpy matplotlib
```

### Option B: Use a virtual environment (recommended)
```
cd /Users/javokhir/Desktop/numerik_2
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install numpy matplotlib
```
Note: When the venv is active, the prompt shows `(.venv)`. Run all commands in the same terminal session.

## Run the experiments
The script runs both methods (Explicit Euler and Improved Euler) in float32 and float64 for N ∈ {25, 50, 100, 200, 400, 800, 1600}, prints tables, and saves results as NPZ arrays.

```
cd /Users/javokhir/Desktop/numerik_2/ex_sheet_02
python3 improved_euler_step.py
```

Outputs created in `ex_sheet_02/`:
- `explicit_euler_results.npz`
- `improved_euler_results.npz`

Each NPZ contains: `Ns`, `hs`, `y32`, `e32`, `y64`, `e64`, `log10_h`, `log10_e32`, `log10_e64`.

## Make log–log error plots (optional)
If `matplotlib` is installed, you can produce error-vs-h plots from the NPZ files.

```
python3 - <<'PY'
import numpy as np
import matplotlib.pyplot as plt

# Explicit Euler
E = np.load('explicit_euler_results.npz')
plt.figure(figsize=(6,4))
plt.loglog(E['hs'], E['e32'], 'o-', label='float32')
plt.loglog(E['hs'], E['e64'], 's-', label='float64')
plt.gca().invert_xaxis()
plt.xlabel('h = 1/N')
plt.ylabel('absolute error |Y_N - 1|')
plt.title('Error vs h (Explicit Euler)')
plt.grid(True, which='both', ls=':', alpha=0.6)
plt.legend(); plt.tight_layout(); plt.savefig('explicit_euler_errors.png', dpi=150)

# Improved Euler
I = np.load('improved_euler_results.npz')
plt.figure(figsize=(6,4))
plt.loglog(I['hs'], I['e32'], 'o-', label='float32')
plt.loglog(I['hs'], I['e64'], 's-', label='float64')
plt.gca().invert_xaxis()
plt.xlabel('h = 1/N')
plt.ylabel('absolute error |Y_N - 1|')
plt.title('Error vs h (Improved Euler)')
plt.grid(True, which='both', ls=':', alpha=0.6)
plt.legend(); plt.tight_layout(); plt.savefig('improved_euler_errors.png', dpi=150)
PY
```

This creates `explicit_euler_errors.png` and `improved_euler_errors.png` next to the NPZ files.

## VS Code tips
- Open the folder `/Users/javokhir/Desktop/numerik_2` in VS Code.
- Set the Python interpreter to the one where you installed packages (Command Palette → “Python: Select Interpreter”).
- Prefer running via `python3` (or your venv’s `python`).

## Troubleshooting
- NumPy missing: install into the exact interpreter you use to run the script.
```
python3 -c "import sys; print(sys.executable)"
python3 -c "import numpy as np; print(np.__version__)"
```
- Plots not generated: install matplotlib and re-run the plotting step.
- Path issues: use the absolute paths above, or `cd` into the folder first.

## Expected behavior
- Explicit Euler: error ~ O(h) (slope ≈ 1 on log–log).
- Improved Euler: error ~ O(h^2) (slope ≈ 2 on log–log).
- float32 flattens earlier than float64 at small h due to rounding.
