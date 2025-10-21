# Explicit Euler Method for ODE Numerical Solution

This Python code implements the **Explicit Euler method** to solve the initial value problem:

\[ (1 + t)y'(t) + y(t) = \frac{1}{1 + t}, \quad y(0) = 1 \]

## 📋 Problem Description

The code computes numerical approximations of the ODE solution in the interval [0,1] using two different step sizes:
- **h₁ = 0.2** (coarse approximation)
- **h₂ = 0.1** (finer approximation)

## 🧮 Mathematical Formulation

### ODE Rearrangement:
\[ y'(t) = \frac{\frac{1}{1+t} - y}{1 + t} \]

### Analytical Solution:
\[ y(t) = \frac{\ln(t + 1) + 1}{1 + t} \]

### Explicit Euler Method:
\[ y_{n+1} = y_n + h \cdot f(t_n, y_n) \]

## 📊 Results Summary

### Step Size h = 0.2:
- **Final value at t=1:** y = 0.858686
- **Error at t=1:** 0.012112

### Step Size h = 0.1:
- **Final value at t=1:** y = 0.851985  
- **Error at t=1:** 0.005411

## 🔍 Error Analysis

The results demonstrate that **smaller step sizes reduce the error**:
- **Error reduction:** 0.012112 → 0.005411 (≈55% decrease)
- **Theoretical expectation:** Halving the step size should approximately halve the error for a first-order method
- **Actual observation:** Error decreased by factor of 2.24, showing good convergence behavior

## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- NumPy library

### Installation
```bash
pip install numpy
```

### Running the Code
```bash
python3 explicit_euler.py
```

## � Project Structure
```
ex_sheet_01/
├── explicit_euler.py
└── README.md
```

## 💻 Code Features

- **`func_f(t, y)`**: Defines the ODE right-hand side
- **`analytical_solution(t)`**: Computes exact solution for comparison
- **`explicit_euler(h, f)`**: Implements the Explicit Euler method
- **Error computation**: Calculates absolute error at t=1

## 📈 Key Observations

1. **Convergence**: The method shows first-order convergence as expected
2. **Accuracy**: Smaller step sizes provide more accurate solutions
3. **Efficiency**: Trade-off between computational cost (more steps) and accuracy
4. The script prints the error ratio E(h=0.2)/E(h=0.1) and an estimated order p, which should be close to 1 for Euler's method.

## 👤 Author
Javokhir Kubaev

## 📄 License
Educational Use