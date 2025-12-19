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

### Week 3 (Jan 6-12): Stiff Problems ⚠️ **EXAM CRITICAL**

#### Days 10-11: A-Stability (Ch 1.4.1)
**Essential Understanding:**
- **Stiff ODEs** - why explicit methods fail
- **Model problem:** `y' = λy` with `Re(λ) ≤ 0`
- **Stability region S:** `{z ∈ ℂ : |R(z)| ≤ 1}`
- **A-stability:** `ℂ^- ⊂ S`

**Key Results:**
- Theorem 1.95: No explicit RK is A-stable
- **Implicit Euler** - A-stable (know proof!)
- **Trapezoidal rule** - A-stable

#### Days 12-13: Important Implicit Methods
**Gaussian Methods:**
- Theorem 1.111: ALL are A-stable, order 2s

**BDF Methods:**
- Orders m=1,2: A-stable
- Orders m=3,4,5,6: A(α)-stable
- m>6: NOT null-stable!

**L-stability:** `R(∞) = 0` (strong damping)

#### Day 14: Computational Aspects (Ch 1.4.2)
- DIRK/SDIRK schemes
- Newton iteration for implicit methods
- Why implicit methods needed for stiff problems

### Week 4 (Jan 13-19): Geometric Integration

#### Days 15-16: Hamiltonian Systems (Ch 2.1)
**Core Concepts:**
- **Hamiltonian:** `H(p,q)`, `p' = -H_q`, `q' = H_p`
- **Energy conservation:** H is first integral (Lemma 2.9)
- **Symplectic transformation:** `A^T J A = J`
- **Flow is symplectic** (Theorem 2.14 - Poincaré)

#### Day 17: Symplectic Methods (Ch 2.2)
**Methods:**
- Symplectic Euler I & II
- **Störmer-Verlet/Leapfrog** (order 2, symplectic)
- Why symplectic methods preserve energy better

### Week 5 (Jan 20-26): Review & Practice

#### Days 18-19: Essential Theorems
**Must Know Proofs:**
1. Picard-Lindelöf (existence/uniqueness)
2. Stability + Consistency ⇒ Convergence
3. Null stability ⇔ Assumption (S)
4. First Dahlquist barrier
5. Second Dahlquist barrier (A-stable multi-step order ≤ 2)
6. Gaussian methods are A-stable
7. Flow of Hamiltonian is symplectic

#### Days 20-21: Proof Techniques Practice
**Standard Proofs:**
- Gronwall Lemma applications
- Stability estimates (Theorems 1.24, 1.27)
- A-stability of implicit Euler using R(z)
- Symplectic Euler is symplectic (Theorem 2.23)

### Week 6 (Jan 27 - Feb 2): Problem Solving

**Work Through Key Examples:**
- Example 1.17: Euler vs Improved Euler convergence
- Example 1.31: perturbation effects
- Example 1.73: non null-stable method diverges
- Example 2.28: Hamiltonian system energy preservation

---

## 🎯 Absolute Must-Knows for Oral Exam

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