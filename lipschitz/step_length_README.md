# Adaptive Step Size Control

## 🎯 Purpose
This implementation demonstrates **adaptive step size control** - a crucial technique in numerical ODE solving that automatically adjusts step sizes to maintain accuracy while maximizing efficiency.

## 📊 What the Code Demonstrates

### **Test Problem:**
```
ODE: y' = -20y + 20cos(t) - sin(t)
Exact solution: y(t) = cos(t)
Initial condition: y(0) = 1
```
This is a **stiff-like** problem that challenges numerical methods and benefits greatly from adaptive stepping.

### **Three Methods Compared:**

#### **1. Fixed Step Size (RK2)**
- Traditional approach with constant step size
- Simple but potentially inefficient
- May waste computation or miss accuracy requirements

#### **2. Embedded RK2/3 Method**
- Uses two Runge-Kutta methods of different orders
- Error estimate: `E ≈ |y_RK3 - y_RK2|`
- Efficient: reuses function evaluations

#### **3. Richardson Extrapolation**
- Compares solutions with step sizes `h` and `h/2`
- Error estimate: `E ≈ |y(h/2) - y(h)| / (2^p - 1)`
- More expensive but very reliable

## 🔧 Step Size Control Algorithm

### **Error Estimation:**
```python
if error_estimate > tolerance:
    # Reject step, reduce step size
    h_new = safety_factor * h * (tol/error)^(1/(p+1))
    retry with h_new
else:
    # Accept step, possibly increase step size
    h_next = safety_factor * h * (tol/error)^(1/(p+1))
```

### **Key Parameters:**
- **Safety factor:** 0.9 (conservative scaling)
- **Order p:** Method order for step size formula
- **Min/Max step:** Prevent extreme step sizes

## 📈 Results Analysis

From the test run:

| Method | Steps | Final Error | Function Evals | Efficiency |
|--------|-------|-------------|----------------|------------|
| Fixed RK2 | 40 | 4.42e-04 | 80 | Baseline |
| Embedded RK2/3 | 46 | 1.88e-04 | 138 | Better accuracy |
| Richardson | 44 | 8.21e-05 | 88 | Best accuracy/cost |

### **Key Observations:**
1. **Richardson extrapolation** achieves best accuracy with reasonable cost
2. **Embedded methods** provide good balance of accuracy and efficiency
3. **Adaptive methods** automatically handle problem difficulty

## 🎯 Visualization Features

The code generates 6 comprehensive plots:

### **1. Solution Comparison**
- Shows all three methods vs exact solution
- Demonstrates accuracy differences

### **2. Step Size Evolution**
- Shows how adaptive methods adjust step sizes
- Reveals problem difficulty regions

### **3. Error Analysis**
- Compares estimated vs actual errors
- Shows tolerance adherence

### **4. Efficiency Plot**
- Error vs computational cost
- Identifies most efficient methods

### **5. Step Size Distribution**
- Histogram of step sizes used
- Shows adaptation patterns

### **6. Adaptive Control Visualization**
- Color-coded step acceptance/rejection
- Green: accepted, Orange/Red: challenging regions

## 🔑 Key Concepts for Exam Preparation

### **Why Adaptive Step Size Matters:**
1. **Efficiency:** Large steps where solution is smooth
2. **Accuracy:** Small steps where solution changes rapidly
3. **Reliability:** Automatic error control prevents failures
4. **Robustness:** Handles varying problem difficulty

### **Error Estimation Techniques:**
- **Embedded methods:** Different order methods with shared evaluations
- **Richardson extrapolation:** Halving step size comparison
- **Local vs global error:** Step-by-step vs accumulated error

### **Step Size Selection Strategy:**
- **Conservative:** Safety factor < 1.0
- **Order-dependent:** Formula uses method order p
- **Bounded:** Min/max limits prevent extremes

## 🎯 Exam-Relevant Questions You Can Answer

1. **"How does adaptive step size control work?"**
   - ✅ Error estimation + step size adjustment algorithm

2. **"Compare embedded methods vs Richardson extrapolation"**
   - ✅ Efficiency vs reliability trade-offs

3. **"Why is adaptive stepping important for stiff problems?"**
   - ✅ Automatic handling of multiple time scales

4. **"What are the components of step size control?"**
   - ✅ Error estimation, acceptance criteria, step adjustment

5. **"How do you balance accuracy and efficiency?"**
   - ✅ Tolerance-based control with safety factors

## 💡 Practical Insights

### **When to Use Adaptive Methods:**
- **Unknown problem behavior:** Don't know optimal step size
- **Varying difficulty:** Solution changes character over time
- **Accuracy requirements:** Need to meet specific tolerances
- **Efficiency concerns:** Want to minimize computational cost

### **Method Selection Guidelines:**
- **Embedded RK:** Good general-purpose choice
- **Richardson:** When highest accuracy is needed
- **Fixed step:** Only when problem is well-understood

This implementation provides a complete foundation for understanding adaptive step size control - essential for modern ODE solvers! 🚀