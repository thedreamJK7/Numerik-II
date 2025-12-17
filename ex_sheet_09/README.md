# Exercise Sheet 9 - Implicit Runge-Kutta Methods for Stiff Problems

## Overview

This exercise implements and compares two implicit Runge-Kutta methods for solving stiff differential equations. Building on Exercise 7, where we saw that explicit methods struggle with stiff problems, we now use implicit methods that can handle large stiffness parameters efficiently.

---

## Problem Statement

**Stiff ODE (same as Exercise 7):**
```
y'(t) = -λ(y(t) - e^(-t)) - e^(-t),    t ∈ [0,1],    y(0) = 1
```

**Exact Solution:**
```
y(t) = e^(-t)    for all λ > 0
```

**Stiffness Parameters:**
```
λ ∈ {10, 100, 1000, 10⁴, 10⁵}
```

---

## Methods Implemented

### Method 1: Gauss Method (2-stage implicit RK)

**Butcher Tableau:**
```
1/2 - √3/6  |  1/4      1/4 - √3/6
1/2 + √3/6  |  1/4 + √3/6    1/4
------------|------------------
            |  1/2      1/2
```

**Numerical Values:**
```
c = [0.2113248654, 0.7886751346]
A = [[ 0.25,       -0.03867513],
     [ 0.53867513,  0.25      ]]
b = [0.5, 0.5]
```

### Method 2: SDIRK Method (Singly Diagonally Implicit RK)

**Parameters:**
```
a+ = 1/2 + √3/6 ≈ 0.7886751346
```

**Butcher Tableau:**
```
a+     |  a+      0
1-a+   |  1-2a+   a+
-------|-------------
       |  1/2     1/2
```

**Numerical Values:**
```
c = [0.7886751346, 0.2113248654]
A = [[ 0.78867513,  0.        ],
     [-0.57735027,  0.78867513]]
b = [0.5, 0.5]
```

---

## Implementation Details

### Key Features:
- **Fixed step size:** N = 20 and N = 40 steps
- **Linear system solver:** Uses `numpy.linalg.solve` for implicit equations
- **Efficient handling:** Exploits linearity of the stiff problem
- **Convergence analysis:** Computes observed convergence orders

### Implicit System Solution:
For our stiff problem, the implicit stage equations become:
```
(I + λh*A) * k = rhs
```
where `rhs` contains the explicit terms. This linear system is solved directly.

---

## Results

### Comparison Table

| λ | E_Gauss(20,λ) | p_Gauss(λ) | E_SDIRK(20,λ) | p_SDIRK(λ) |
|---|---------------|------------|---------------|------------|
| 10¹ | 5.6e-08 | 4.00 | 3.0e-05 | 2.72 |
| 10² | 5.5e-07 | 4.02 | 6.5e-05 | 2.21 |
| 10³ | 6.6e-06 | 4.23 | 7.5e-05 | 2.03 |
| 10⁴ | 3.4e-05 | 3.00 | 7.6e-05 | 2.00 |
| 10⁵ | 4.3e-05 | 2.12 | 7.6e-05 | 1.99 |

**Legend:**
- `E(N,λ)` = Global error: `|y_N - e^(-1)|`
- `p(λ)` = Convergence order: `log₂(E(20,λ)/E(40,λ))`

---

## Key Observations

### 1. **Efficiency Comparison with Exercise 7:**
- **Exercise 7 (Explicit RK4/3):** λ=1000 required 833 steps (3556 function evaluations)
- **Exercise 9 (Implicit RK):** λ=10⁵ requires only 20 steps!
- **Conclusion:** Implicit methods are vastly more efficient for stiff problems

### 2. **Method Comparison:**
- **Gauss Method:** 
  - Higher accuracy (smaller errors)
  - Shows super-convergence (order ≈ 4)
  - More complex implementation
- **SDIRK Method:**
  - More stable convergence (order ≈ 2 as expected)
  - Simpler structure (singly diagonally implicit)
  - Consistent performance across all λ values

### 3. **Stiffness Handling:**
- Both methods maintain accuracy even for λ = 10⁵
- No step size restrictions due to stability
- Convergence orders remain reasonable for all stiffness levels

---

## Usage

### Run the complete analysis:
```bash
python3 ex_sheet_09/implicit_runge_kutte.py
```

### Expected Output:
1. Butcher tableaux for both methods
2. Complete results table
3. Convergence analysis
4. Performance observations

---

## File Structure

```
ex_sheet_09/
├── README.md                    # This file
├── implicit_runge_kutte.py      # Main implementation
└── [generated plots/data]       # Optional output files
```

---

## Mathematical Background

### Implicit RK Methods:
Unlike explicit methods, implicit RK methods can have `A[i,j] ≠ 0` for `j ≥ i`, requiring the solution of nonlinear (or linear) systems at each time step.

### Stability:
Implicit methods have much larger stability regions, making them ideal for stiff problems where explicit methods would require impractically small step sizes.

### A-Stability:
Both implemented methods are A-stable, meaning they can handle arbitrarily stiff problems without step size restrictions.

---

## Comparison with Previous Exercises

| Aspect | Exercise 7 (Explicit) | Exercise 9 (Implicit) |
|--------|----------------------|----------------------|
| **Method Type** | Adaptive RK4(3) | Fixed step Gauss/SDIRK |
| **Stiffness Handling** | Poor (many tiny steps) | Excellent (fixed steps) |
| **λ = 1000 Steps** | 833 steps needed | 20 steps sufficient |
| **λ = 10⁵ Feasibility** | Impractical | Easy |
| **Computational Cost** | High (many evaluations) | Low (few large steps) |
| **Accuracy** | Good (when converges) | Excellent |

---

## Theoretical Notes

### Gauss Methods:
- Based on Gaussian quadrature
- Achieve order 2s for s stages
- Show super-convergence for smooth problems

### SDIRK Methods:
- Singly Diagonally Implicit structure
- Easier to implement than fully implicit methods
- Good balance of efficiency and stability

---

## Extensions

Possible extensions for further study:
1. **Adaptive step size control** for implicit methods
2. **Higher-order implicit methods** (3-stage, 4-stage)
3. **Rosenbrock methods** (linearly implicit)
4. **Performance benchmarking** against commercial solvers
5. **Nonlinear stiff problems** requiring Newton iteration

---

## References

- Hairer, E., & Wanner, G. (1996). *Solving Ordinary Differential Equations II: Stiff and Differential-Algebraic Problems*
- Butcher, J. C. (2016). *Numerical Methods for Ordinary Differential Equations*
- Exercise sheets from Numerical Analysis II course