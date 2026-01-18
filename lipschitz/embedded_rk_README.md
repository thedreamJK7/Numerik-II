# Embedded Runge-Kutta Methods

## 🎯 Purpose
This implementation demonstrates **embedded Runge-Kutta methods** - the foundation of modern adaptive ODE solvers like MATLAB's `ode45` and Python's `scipy.integrate.solve_ivp`.

## 🔑 Core Concept

### **The Embedded RK Idea:**
Instead of using two separate methods for error estimation (expensive), embedded methods use **shared k-values** to compute two approximations of different orders simultaneously.

```
Traditional approach:  Method 1 + Method 2 = 2× cost
Embedded approach:     Method 1 + Method 2 = ~1× cost (shared k-values)
```

### **How It Works:**
1. **Compute shared k-values:** k₁, k₂, ..., k₇ (for DOPRI5(4))
2. **Two approximations:** 
   - Higher order: y⁵ = y₀ + h(b₁⁵k₁ + ... + b₇⁵k₇)
   - Lower order: y⁴ = y₀ + h(b₁⁴k₁ + ... + b₇⁴k₇)
3. **Error estimate:** |y⁵ - y⁴| ≈ local truncation error
4. **Step control:** Accept/reject step based on error vs tolerance

## 🚀 Implemented Methods

### **1. DOPRI5(4) - Dormand-Prince**
- **7 stages** (k₁ through k₇)
- **5th order main method** (used as solution)
- **4th order embedded method** (for error estimation)
- **Industry standard** (used in MATLAB's ode45)
- **Optimal for non-stiff problems**

### **2. RK2(3) - Bogacki-Shampine**
- **4 stages** (k₁ through k₄)
- **3rd order main method**
- **2nd order embedded method**
- **Simpler alternative** for less demanding problems

## 📊 Performance Results

From the test run with tolerance 1e-6:

| Method | Steps | Rejected | Final Error | Function Evals | Efficiency |
|--------|-------|----------|-------------|----------------|------------|
| DOPRI5(4) | 73 | 7 | 2.68e-07 | 560 | **Excellent** |
| RK2(3) | 317 | 8 | 6.41e-06 | 1300 | Good |

### **Key Observations:**
1. **DOPRI5(4)** achieves better accuracy with fewer function evaluations
2. **Higher order methods** are more efficient for tight tolerances
3. **Automatic step control** handles problem difficulty seamlessly

## 🎯 Comprehensive Visualization (6 Plots)

### **1. Solution Comparison**
- Shows both methods vs exact solution
- Demonstrates accuracy differences

### **2. Adaptive Step Size Evolution**
- Shows how step sizes adapt to problem difficulty
- Larger steps in smooth regions, smaller in challenging areas

### **3. Error Analysis**
- Compares estimated vs actual errors
- Shows tolerance adherence

### **4. Efficiency Scatter Plot**
- Error vs computational cost
- Identifies most efficient method

### **5. Shared Computations Illustration**
- Visualizes how both methods use same k-values
- Shows efficiency of embedded approach

### **6. Butcher Tableau Structure**
- Mathematical framework explanation
- Key advantages summary

## 🔬 Mathematical Foundation

### **Butcher Tableau for Embedded Methods:**
```
┌─────┬─────────────────┐
│  c  │        A        │  ← Shared coefficients
├─────┼─────────────────┤
│     │      b⁵         │  ← 5th order weights
│     │      b⁴         │  ← 4th order weights
└─────┴─────────────────┘
```

### **Error Estimation Theory:**
For embedded pair of orders p and p+1:
```
Local error ≈ |y_{p+1} - y_p|
```
This estimates the local truncation error of the p-th order method.

### **Step Size Control Formula:**
```
h_new = safety_factor × h × (tolerance / error_estimate)^(1/(p+1))
```
where p is the order of the lower-order method.

## 🎯 Key Advantages

### **1. Efficiency**
- **Shared computations:** Same k-values for both methods
- **Optimal cost:** ~7 evaluations for two methods (DOPRI5(4))
- **Smart stepping:** Large steps where possible, small where needed

### **2. Reliability**
- **Automatic error control:** User specifies tolerance, not step size
- **Robust error estimation:** Based on order difference
- **Adaptive behavior:** Handles varying problem difficulty

### **3. Practical Benefits**
- **User-friendly:** Specify tolerance instead of step size
- **Versatile:** Works for wide range of problems
- **Industry standard:** Proven in real applications

## 🔑 Exam-Critical Understanding

### **Core Concepts You Must Know:**

1. **Embedded Pair Concept:**
   - Two methods sharing k-values
   - Different b-coefficients, same A and c

2. **Error Estimation:**
   - |y_high - y_low| estimates local error
   - More reliable than Richardson extrapolation

3. **Step Size Control:**
   - Accept/reject based on error vs tolerance
   - Optimal formula for step adjustment

4. **Efficiency Analysis:**
   - Cost ≈ single method, benefit = two methods
   - Higher order methods more efficient for tight tolerances

### **Typical Exam Questions:**

1. **"Explain how embedded RK methods work"**
   - ✅ Shared k-values, different b-coefficients, error estimation

2. **"Why are embedded methods more efficient than Richardson extrapolation?"**
   - ✅ Shared computations vs separate evaluations

3. **"How does DOPRI5(4) achieve automatic step size control?"**
   - ✅ Error estimate from order difference, step adjustment formula

4. **"What are the advantages of embedded methods?"**
   - ✅ Efficiency, reliability, user-friendliness

## 💡 Real-World Applications

### **MATLAB's ode45:**
- Uses DOPRI5(4) embedded method
- Default choice for non-stiff ODEs
- Automatic tolerance control

### **Python's scipy.integrate:**
- `solve_ivp` with `method='RK45'` uses DOPRI5(4)
- `method='RK23'` uses Bogacki-Shampine
- Industry-standard implementations

### **When to Use:**
- **Non-stiff ODEs:** DOPRI5(4) is optimal
- **Moderate accuracy:** RK2(3) sufficient
- **High accuracy:** Consider higher-order embedded pairs
- **Stiff problems:** Use implicit methods instead

This implementation provides the complete foundation for understanding embedded RK methods - the backbone of modern adaptive ODE solvers! 🚀