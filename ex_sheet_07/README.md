# Exercise Sheet 7 - Stiff Problems

## Vazifalar (Tasks)

### Exercise 1: Stiff Problem Analysis ✅
**Fayl:** `stiff_problem.py`

**Maqsad:** Quyidagi stiff ODE ni turli usullar bilan yechish:
- ODE: `y'(t) = -λ(y(t) - e^(-t)) - e^(-t)`, `y(0) = 1`
- Aniq yechim: `y(t) = e^(-t)`
- λ = 1 va λ = 1000 uchun test qilish

**Usullar:**
- Explicit Euler
- Improved Euler (Midpoint)
- RK4
- Adams-Bashforth 2

**Natija:** Stiff problemlarda (λ = 1000) explicit usullar beqaror bo'ladi.

---

### Exercise 2: Embedded RK Scheme for Stiff Problem 🔄
**Fayl:** `rk_scheme_stiff_problem.py`

**Maqsad:** Exercise 5 dagi adaptive RK4(3) schemani Exercise 1 dagi stiff problem uchun moslashtirish.

#### Roadmap:

**1. Kod strukturasini moslashtirish**
   - [ ] Exercise 5 dagi `solve_adaptive_rk43_procedure` funksiyasini copy qilish
   - [ ] `f(y)` formatini `f(t, y, lam)` formatiga o'zgartirish
   - [ ] Butcher tableau (A_rk4, b_rk4, b_rk3) ni saqlash

**2. Stiff problem uchun f(t, y, λ) funksiyasini yozish**
   - [ ] `f(t, y, lam)` funksiyasini implement qilish
   - [ ] Exercise 1 dagi formulani ishlatish: `-lam * (y - exp(-t)) - exp(-t)`

**3. Adaptive RK schemani test qilish**
   - [ ] λ = 1 uchun test (non-stiff case)
   - [ ] λ = 1000 uchun test (stiff case)
   - [ ] Turli h0, epsilon parametrlarini sinab ko'rish

**4. Natijalarni vizualizatsiya qilish**
   - [ ] Approximate solution (adaptive RK) ni plot qilish
   - [ ] Exact solution `y(t) = e^(-t)` ni plot qilish
   - [ ] Ikkalasini bir grafigda ko'rsatish
   - [ ] Xatolikni (error) alohida plot qilish

**5. Tahlil va observation**
   - [ ] λ = 1 da adaptive RK qanday ishlaydi?
   - [ ] λ = 1000 da adaptive RK qanday ishlaydi?
   - [ ] Step size (h) qanday o'zgaradi?
   - [ ] Function evaluations soni qancha?
   - [ ] Explicit RK scheme stiff problemda yaxshi ishlayaptimi?

---

## Kutilayotgan natijalar (Expected Observations)

### λ = 1 (Non-stiff):
- Adaptive RK yaxshi ishlashi kerak
- Kichik xatolik
- Step size barqaror

### λ = 1000 (Stiff):
- Adaptive RK qiyinchilik ko'rishi mumkin
- Step size juda kichik bo'lishi kerak (barqarorlik uchun)
- Ko'p function evaluations kerak bo'ladi
- Explicit scheme stiff problem uchun samarasiz
- **Observation:** Stiff problemlar uchun implicit schemes yaxshiroq!

---

## Ishga tushirish (How to Run)

```bash
# Exercise 1
python ex_sheet_07/stiff_problem.py

# Exercise 2
python ex_sheet_07/rk_scheme_stiff_problem.py
```

---

## Asosiy farqlar (Key Differences)

| Aspect | Exercise 5 (Van der Pol) | Exercise 7 (Stiff Problem) |
|--------|-------------------------|---------------------------|
| ODE format | `f(y)` - autonomous | `f(t, y, λ)` - non-autonomous |
| Problem type | Non-linear oscillator | Linear stiff problem |
| Dimension | 2D system | 1D scalar |
| Exact solution | Yo'q | `y(t) = e^(-t)` |
| Challenge | Non-linearity | Stiffness |

---

## Foydali formulalar

**Stiff ODE:**
```
y'(t) = -λ(y(t) - e^(-t)) - e^(-t)
y(0) = 1
```

**Exact solution:**
```
y(t) = e^(-t)
```

**Stability region:** Explicit RK4 ning stability region cheklangan, shuning uchun stiff problemlarda (katta λ) juda kichik step size kerak.
