# Local vs Global Error Analysis

## 🎯 Purpose
This visualization demonstrates the crucial difference between **local errors** and **global errors** in numerical methods - a fundamental concept for understanding numerical stability and convergence.

## 📊 What the Code Shows

### **Key Concepts:**

#### **Local Error (τₖ)**
- Error made in **ONE step** assuming we start from the exact solution
- Formula: `τₖ = y(t_{k+1}) - [y(tₖ) + hΦ(tₖ, y(tₖ), h)]`
- Shows the **method's accuracy** per step

#### **Global Error (eₖ)**  
- **Accumulated error** after k steps of the actual computation
- Formula: `eₖ = y(tₖ) - Yₖ`
- Shows the **total deviation** from exact solution

### **Mathematical Relationship:**
```
e_{k+1} ≈ (1 + hL)eₖ + hτₖ
```
- Global error grows due to:
  1. **Propagation** of previous global error (amplified by stability factor)
  2. **Addition** of new local error

## 📈 Visualization Components

### **1. Overall Solution Plot**
- Shows exact solution vs Euler approximation
- Colored regions indicate error accumulation
- Arrows show error propagation between steps

### **2. Single Step Analysis**
- Zooms into one step to show local vs global error
- Blue region: local error (method accuracy)
- Red arrows: global error (accumulated deviation)

### **3. Error Propagation Diagram**
- Tracks how local errors contribute to global error growth
- Shows amplification factors between steps

### **4. Walking Analogy**
- Intuitive analogy: walking with imperfect steps
- Local error = step size error
- Global error = total position deviation

### **5. Mathematical Framework**
- Key formulas and relationships
- Gronwall lemma application
- Stability analysis concepts

## 🔑 Key Insights for Exam Preparation

### **Why This Matters:**
1. **Method Design:** Small local error doesn't guarantee small global error
2. **Stability:** Unstable methods amplify errors exponentially  
3. **Convergence:** Need both consistency (small local error) AND stability
4. **Step Size:** Smaller h reduces local error but may require more steps

### **Exam Questions You Can Answer:**
- "Explain the difference between local and global error"
- "How do local errors propagate to become global errors?"
- "Why can a method with small local error still fail?"
- "What role does stability play in error accumulation?"

## 🧮 Numerical Example Results

For ODE: `y' = y`, `y(0) = 1`, step size `h = 0.5`:

| Step | Local Error τₖ | Global Error eₖ | Amplification |
|------|---------------|----------------|---------------|
| 1    | 0.148721      | 0.148721       | 1.00×         |
| 2    | 0.245200      | 0.468282       | 1.58×         |
| 3    | 0.404266      | 1.106689       | 1.42×         |
| 4    | 0.666522      | 2.326556       | 1.48×         |

**Observation:** Even though local errors are "reasonable", global error grows significantly due to error propagation and amplification.

## 🎯 Connection to Numerics II Theory

This visualization directly illustrates:
- **Consistency:** `lim_{h→0} τₖ = 0`
- **Stability:** Bounded amplification of errors
- **Convergence:** Consistency + Stability ⇒ Convergence
- **Gronwall Lemma:** Error bound estimation

Perfect preparation for understanding why numerical methods succeed or fail! 🚀