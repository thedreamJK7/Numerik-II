# Numerics II - Exam Preparation Roadmap

**Oral Exam Date:** February 16th, 2025  
**Study Period:** December 23, 2024 - February 15, 2025

## 📋 Quick Reference

### Core Topics Priority
1. **One-Step Methods** (Euler, RK methods) + Exercise Sheets 1-4
2. **Multi-Step Methods** (Adams, BDF) + Exercise Sheets 5-8  
3. **Stiff Problems & A-Stability** ⚠️ **CRITICAL** + Exercise Sheets 9-10
4. **Geometric Integration** (Hamiltonian systems) + Exercise Sheets 11-12

### Study Strategy: 60% Theory + 40% Exercise Sheets
**Why Exercise Sheets Matter:**
- Exercise sheets = Professor's exam blueprint
- Problems you solve = Questions you can answer  
- Solutions you explain = Oral exam preparation

### Must-Know Theorems
- Picard-Lindelöf (existence/uniqueness)
- Stability + Consistency ⇒ Convergence
- First & Second Dahlquist Barriers
- A-stability results for implicit methods

---

## 🎯 Exercise Sheet Collection Strategy

### MUST DO (High Exam Probability)
- ✅ **Sheet 3** (RK methods) - you have this
- **Sheet on Multi-step** (Adams, null stability)
- **Sheet on A-stability** (stability regions, BDF)
- **Sheet on Hamiltonian** systems

### SHOULD DO
- Sheet on step-size control
- Sheet on stiff problems applications  
- Sheet on convergence proofs

### Exercise Sheet Timeline
- **By Jan 5:** Complete Sheets 1-4 (one-step, RK, basic)
- **By Jan 12:** Complete Sheets 5-8 (multi-step, stability)
- **By Jan 19:** Complete Sheets 9-12 (stiff, geometric)
- **Jan 20-26:** Redo ALL marked problems
- **Final week:** Random spot checks + oral explanations

---

## 📅 6-Week Study Schedule

### Week 1 (Dec 23-29): One-Step Methods + Exercise Practice

#### Days 1-2: Core Theory (Ch 1.1-1.2.1)
**Focus Areas:**
- **Picard-Lindelöf Theorem** - uniqueness/existence conditions
- **Lipschitz continuity** - be able to verify for given functions
- **Gronwall Lemma** - understand proof technique
- **One-step structure:** `Y_{k+1} = Y_k + h_k Φ(...)`

**Key Definitions:**
- Consistency, Stability, Convergence

#### Days 3-4: Runge-Kutta Methods (Ch 1.2.2)
**Essential Methods (memorize):**
- **Explicit Euler** (order 1)
- **Improved Euler/Runge** (order 2)  
- **Classical RK4** (order 4) - **MEMORIZE BUTCHER TABLEAU**

**Theory:**
- Butcher tableau notation
- Stability function: `R(z) = 1 + zb^T(I - zA)^{-1}1`
- Order conditions (Theorem 1.42)
- **First Dahlquist Barrier:** explicit RK of s stages has max order s

#### Day 5: 🎯 **EXERCISE SESSION 1** - Sheet 3 Deep Dive (3 hours)

**Exercise 1: Consistency Condition ⭐**
```
Goal: Prove Σb_i = 1 for RK consistency
Key Steps:
1. Start: lim_{h→0} max_k ||f(t_k, y(t_k)) - Φ(t_k, y(t_k), h_k)|| = 0
2. Use: Φ(t,y,h) = Σ b_i K_i(t,y,h)  
3. Apply continuity: lim_{h→0} K_i(t,y,h) = f(t,y)
4. Conclude: Need Σb_i = 1

Exam Relevance: HIGH - Shows you understand consistency
```

**Exercise 2: RK4 Analysis ⭐⭐⭐**
```
Part a) RK4 Butcher Tableau (MEMORIZE):
0   |  0    0    0    0
1/2 | 1/2   0    0    0  
1/2 |  0   1/2   0    0
1   |  0    0    1    0
----+------------------
    | 1/6  1/3  1/3  1/6

Part b) Stability Function R(z) for RK4:
For y' = λy, compute K_1, K_2, K_3, K_4
Result: R(z) = 1 + z + z²/2 + z³/6 + z⁴/24
Compare to e^z Taylor series → Order 4 confirmed!

Exam Relevance: VERY HIGH - Classic oral exam question
```

**Programming Exercise Understanding:**
- Skip coding if time short
- BUT understand logistic equation behavior
- Know what happens with different step sizes h

### Week 2 (Dec 30 - Jan 5): Multi-Step Methods + Exercise Practice

#### Days 6-7: Simple Multi-Step (Ch 1.3.1)
- **Adams-Bashforth** (explicit, order m)
- **Adams-Moulton** (implicit, order m+1)
- **Predictor-Corrector** (PECE) schemes
- Stability (Theorem 1.63)

#### Days 8-9: General Linear Multi-Step (Ch 1.3.2-1.3.3)
**Critical Concepts:**
- Characteristic polynomial: `ρ(z) = Σa_j z^{m-j}`
- **Null stability:** roots satisfy `|z_i| ≤ 1`, simple on unit circle
- **Assumption (S)** and equivalence to null stability
- **KEY RESULT:** Consistency + Null stability ⇒ Convergence

#### Day 10: 🎯 **EXERCISE SESSION 2** - Multi-Step Practice (3 hours)

**Typical Exercise Types:**
```
Type 1: Adams Method Implementation
- Derive Adams-Bashforth for m=2,3
- Derive Adams-Moulton for m=2,3
- Compare stability regions

Type 2: Null Stability Check
Given coefficients [a_0, a_1, ..., a_m]:
1. Form ρ(z) = Σa_j z^{m-j}
2. Find roots of ρ(z) = 0
3. Check |z_i| ≤ 1 and simple on unit circle
4. Conclude null stability

Type 3: Order Verification
- Use Taylor expansion method
- Match coefficients with exact solution
- Determine highest order achieved

Exam Bridge: "Check null stability of this 3-step method"
```

### Week 3 (Jan 6-12): Stiff Problems + Critical Exercises ⚠️

#### Days 11-12: A-Stability (Ch 1.4.1)
**Essential Understanding:**
- **Stiff ODEs** - why explicit methods fail
- **Model problem:** `y' = λy` with `Re(λ) ≤ 0`
- **Stability region S:** `{z ∈ ℂ : |R(z)| ≤ 1}`
- **A-stability:** `ℂ^- ⊂ S`

**Key Results:**
- Theorem 1.95: No explicit RK is A-stable
- **Implicit Euler** - A-stable (know proof!)
- **Trapezoidal rule** - A-stable

#### Days 13-14: Important Implicit Methods
**Gaussian Methods:**
- Theorem 1.111: ALL are A-stable, order 2s

**BDF Methods:**
- Orders m=1,2: A-stable
- Orders m=3,4,5,6: A(α)-stable  
- m>6: NOT null-stable!

**L-stability:** `R(∞) = 0` (strong damping)

#### Day 15: 🎯 **EXERCISE SESSION 3** - Stiff Problems (3 hours)

**Type 1: Stability Region Analysis**
```
Classic θ-method Exercise:
Y_{k+1} = Y_k + h[(1-θ)f(t_k, Y_k) + θf(t_{k+1}, Y_{k+1})]

Tasks:
a) Find R(z) for test equation y' = λy
   Answer: R(z) = (1 + (1-θ)z)/(1 - θz)
   
b) For what θ is method A-stable?
   Answer: θ ≥ 1/2
   
c) Special cases:
   θ=0: Explicit Euler (not A-stable)
   θ=1/2: Trapezoidal rule (A-stable)  
   θ=1: Implicit Euler (A-stable, L-stable)

Exam Relevance: GUARANTEED oral exam topic
```

**Type 2: BDF Method Analysis**
```
Tasks:
- Derive BDF2: Y_{k+1} = (4Y_k - Y_{k-1})/3 + (2h/3)f_{k+1}
- Check null stability of characteristic polynomial
- Verify order 2
- Show A-stability using R(z)

Red Flag: "Derive and analyze BDF method of order m"
```

### Week 4 (Jan 13-19): Geometric Integration + Exercise Practice

#### Days 16-17: Hamiltonian Systems (Ch 2.1)
**Core Concepts:**
- **Hamiltonian:** `H(p,q)`, `p' = -H_q`, `q' = H_p`
- **Energy conservation:** H is first integral (Lemma 2.9)
- **Symplectic transformation:** `A^T J A = J`
- **Flow is symplectic** (Theorem 2.14 - Poincaré)

#### Day 18: 🎯 **EXERCISE SESSION 4** - Geometric Methods (2 hours)

**Classic Pendulum Exercise:**
```
Hamiltonian: H(p,q) = p²/2 + (1 - cos q)

Tasks:
a) Write Hamilton's equations:
   p' = -H_q = -sin q
   q' = H_p = p

b) Apply Symplectic Euler:
   Method I:  p_{k+1} = p_k - h·sin(q_k)
              q_{k+1} = q_k + h·p_{k+1}
   
   Method II: q_{k+1} = q_k + h·p_k  
              p_{k+1} = p_k - h·sin(q_{k+1})

c) Show energy oscillates (bounded) vs. drifts (non-symplectic)

Exam Relevance: If Hamiltonian covered, often asked
```

**Symplecticity Verification:**
```
Task: Show method is symplectic (A^T J A = J)

Example: Symplectic Euler I
Jacobian: A = [1    0  ]
              [-h   1  ]

Check: A^T J A = [1  -h] [0   1] [1    0 ]
                  [0   1] [-1  0] [-h   1]
               = [0   1] = J ✓
                 [-1  0]

Red Flag: "Verify this method preserves symplecticity"
```

#### Day 19: Symplectic Methods Theory (Ch 2.2)
- Symplectic Euler I & II
- **Störmer-Verlet/Leapfrog** (order 2, symplectic)
- Why symplectic methods preserve energy better

---

## 📝 Exercise Sheet Mastery Strategy

### 3-Pass Method for Maximum Efficiency

#### Pass 1: Initial Attempt (60 min per sheet)
- Try each problem for 10-15 minutes
- Mark results: ✅ (solved), ❓ (struggled), ❌ (stuck)
- **Don't look at solutions yet!**
- Focus on understanding what's being asked

#### Pass 2: Theory-Informed Retry (45 min per sheet)  
- Review ❓ and ❌ problems with notes/script
- Apply theoretical knowledge to stuck problems
- Now check solutions or ask TA for help
- Understand the solution approach completely

#### Pass 3: Mastery Check (30 min per sheet)
- Redo all ❌ problems from memory
- Ensure ✅ problems can be solved quickly
- Create summary of key techniques used
- Practice explaining solutions out loud

### Exercise → Exam Question Bridge

**How Sheet Problems Become Oral Questions:**

| Exercise Sheet Topic | Becomes Exam Question |
|---------------------|----------------------|
| "Show Y_{k+1} = [1 + hλ + ...]Y_k for RK4" | "Derive stability function for RK4" |
| "Check null stability of coefficients" | "Is this 3-step method stable?" |
| "Verify method is A-stable" | "Show implicit Euler is A-stable" |
| "Show method is symplectic" | "Verify symplecticity of this scheme" |

### Red Flag Exercises (High Exam Probability)
- **Butcher tableau derivation** → Guaranteed exam topic
- **Null stability verification** → Very common  
- **A-stability proof** → Classic oral question
- **Symplecticity verification** → If covered, often asked
- **Method comparison** → Oral exam favorite

---

## 🎯 Mock Exam Sessions

### Week Before Exam (Feb 9-10): 40-Minute Simulations

**Sample Mock Exam Structure:**
```
Time: 40 minutes total
Format: Explain solutions OUT LOUD

Problem Set:
• 10 min: Derive RK2 Butcher tableau + verify order
• 10 min: Check null stability of Adams 3-step method  
• 12 min: Prove implicit Euler is A-stable using R(z)
• 8 min: Show symplectic Euler preserves symplecticity

Practice Phrases:
- "The key idea here is..."
- "This connects to Theorem X because..."
- "The intuition behind this is..."
```

### Exercise Sheet Collection Priority

**MUST HAVE (Get These First):**
1. ✅ Sheet 3 (RK methods) - you have this
2. Multi-step methods sheet (Adams, BDF, null stability)
3. A-stability sheet (stability regions, stiff problems)  
4. Hamiltonian systems sheet (if covered in course)

**SHOULD HAVE:**
5. Step-size control and adaptivity
6. Convergence theory and proofs
7. Stiff problem applications

**Sources to Check:**
- Ask TA/classmates for complete collection
- Course website/learning management system
- Previous year students (if available)
- Study group sharing

---

## 🔄 Week 5 (Jan 20-26): Intensive Review + Problem Mastery

### Days 20-21: Essential Theorems Review
**Must Know Proofs:**
1. **Picard-Lindelöf** (existence/uniqueness)
2. **Stability + Consistency ⇒ Convergence** (fundamental result)
3. **Null stability ⇔ Assumption (S)** (multi-step methods)
4. **First Dahlquist barrier** (explicit RK order limit)
5. **Second Dahlquist barrier** (A-stable multi-step order ≤ 2)
6. **Gaussian methods are A-stable** (all orders)
7. **Flow of Hamiltonian is symplectic** (Poincaré theorem)

### Days 22-23: Proof Techniques Practice
**Standard Proof Patterns:**
- **Gronwall Lemma applications** (stability estimates)
- **Stability estimates** (Theorems 1.24, 1.27)
- **A-stability using R(z)** (complex analysis approach)
- **Symplectic verification** (matrix algebra, Theorem 2.23)

### Days 24-26: 🔁 **REDO ALL MARKED PROBLEMS**
**Systematic Review:**
- Revisit every ❓ and ❌ from all exercise sheets
- Can you solve them without notes now?
- Practice explaining each solution out loud
- Create one-page summaries of solution techniques

**Daily Goal:** Master 4-5 previously difficult problems per day

---

## 📚 Week 6 (Jan 27 - Feb 2): Problem Solving + Script Examples

### Key Script Examples to Master
- **Example 1.17:** Euler vs Improved Euler convergence rates
- **Example 1.31:** Perturbation effects on stability
- **Example 1.73:** Non null-stable method diverges (crucial example!)
- **Example 2.28:** Hamiltonian system energy preservation

### Daily Practice Routine
- **Morning (2h):** Review one major topic from script
- **Afternoon (2h):** Work through 3-4 exercise problems
- **Evening (1h):** Practice explaining concepts aloud

### Random Exercise Spot Checks
**Daily Challenge:**
- Pick 2 random problems from any completed sheet
- Solve from scratch in 20 minutes total
- Explain solution as if in oral exam
- Identify which theorem/concept is being tested

**Success Metric:** Can solve 80% of random problems confidently

---

### Concepts You Must Explain
- **Lipschitz continuity** → uniqueness
- **Consistency, Stability, Convergence** triangle
- **Null stability** for multi-step methods
- **A-stability** for stiff problems
- **Symplecticity** for Hamiltonian systems

### Methods (Structure + Order)
| Method | Order | Type | Key Property |
|--------|-------|------|--------------|
| Explicit Euler | 1 | One-step | Simple, not A-stable |
| Improved Euler | 2 | One-step | Better accuracy |
| RK4 | 4 | One-step | High accuracy |
| Adams-Bashforth | m | Multi-step | Explicit |
| Adams-Moulton | m+1 | Multi-step | Implicit |
| BDF (m=1,2) | m | Multi-step | A-stable |
| Symplectic Euler | 1 | Geometric | Energy preserving |
| Störmer-Verlet | 2 | Geometric | Symplectic |

### Exam Skills - Be Ready To:
1. **Derive** consistency order for simple methods
2. **Check** if method is A-stable using R(z)
3. **Explain** why explicit methods fail for stiff problems
4. **Show** a method is symplectic (like Theorem 2.23)
5. **Apply** Gronwall Lemma to stability analysis

---

## 📚 Final Week (Feb 3-15): Intensive Review

### Create Summary Sheets
1. **Method Comparison Table** (order, stability, computational cost)
2. **Decision Tree:** When to use what method
3. **Key Definitions** (one-page reference)
4. **Main Theorems** with conditions

### Daily Practice (Feb 3-15)
- **Morning:** Review one major topic
- **Afternoon:** Work through examples
- **Evening:** Practice explaining concepts aloud

---

## 💡 Study Tips for Oral Exam Success

### Understanding Over Memorization
- Focus on **why** theorems are true, not just what they say
- Practice explaining theorems out loud
- Draw stability regions for different methods
- Understand the motivation behind each concept

### Practice Techniques
- Work through at least one example per major topic
- Explain concepts to an imaginary student
- Draw diagrams and visualizations
- Connect different topics (e.g., stiffness → A-stability → implicit methods)

### Red Flags to Avoid
- Don't just memorize formulas without understanding
- Don't skip the "why" behind theoretical results
- Don't ignore computational aspects
- Don't forget to practice verbal explanations

---

## 🚨 Last-Minute Checklist (Feb 14-15)

### Day Before Exam
- [ ] Review all must-know theorems
- [ ] Practice explaining A-stability concept
- [ ] Review method comparison table
- [ ] Go through Hamiltonian system basics
- [ ] Practice one proof technique

### Morning of Exam
- [ ] Quick review of key definitions
- [ ] Glance at method orders and properties
- [ ] Review stability regions sketch
- [ ] Stay calm and confident!

---

**Remember:** This is an oral exam - focus on understanding and clear explanation rather than perfect mathematical notation. Good luck! 🍀