# Exercise Sheet 7 - Roadmap

## Exercise 2: Embedded RK Scheme for Stiff Problem

### Vazifa:
Exercise 5 dagi adaptive RK4(3) schemani Exercise 1 dagi stiff problem uchun moslashtirish.

---

## ROADMAP - Qadamma-qadam yo'riqnoma

### QADAM 1: Butcher Tableau ni yozish
```python
# Exercise 5 dan copy qiling:
A_rk4 = np.array([...])  # 4x4 matrix
b_rk4 = np.array([...])  # RK4 weights
b_rk3 = np.array([...])  # RK3 weights (embedded)

# YANGI: c vektorini qo'shing!
c_rk4 = np.array([0.0, 0.5, 0.5, 1.0])  # Time offsets
```

**Nima uchun c kerak?** Non-autonomous ODE da vaqt (t) ham o'zgaradi!

---

### QADAM 2: Stiff problem funksiyasini yozish
```python
def f(t, y, lam):
    """
    ODE: y'(t) = -λ(y(t) - e^(-t)) - e^(-t)
    """
    # TODO: Formulani yozing
    pass

def exact_solution(t):
    """
    Exact: y(t) = e^(-t)
    """
    # TODO: Yozing
    pass
```

---

### QADAM 3: Adaptive RK funksiyasini moslashtirish

**Exercise 5 dan farqi:**

| Exercise 5 | Exercise 7 |
|------------|------------|
| `f(y_stage)` | `f(t_stage, y_stage, lam)` |
| `y` - 2D vector | `y` - scalar (1D) |
| `c` yo'q | `c` kerak! |

**O'zgartirishlar:**

```python
def solve_adaptive_rk43_stiff(f, y0, I, h0, epsilon, q, lam):
    # 1. Initialization
    a, b = I
    t = a
    y = float(y0)  # Scalar!
    h = h0
    # ...
    
    while t < b:
        # 2. RK stages
        for j in range(4):
            # MUHIM: Stage time ni hisoblang!
            t_stage = t + c_rk4[j] * h
            
            # Stage value
            if j == 0:
                y_stage = y
            else:
                y_stage = y + h * np.sum(A_rk4[j, :j] * k[:j])
            
            # MUHIM: f(t, y, lam) formatida chaqiring!
            k[j] = f(t_stage, y_stage, lam)
        
        # 3. RK4 va RK3 yechimlar
        y_rk4 = y + h * np.sum(b_rk4 * k)
        y_rk3 = y + h * np.sum(b_rk3 * k)
        
        # 4. Error estimate
        err_estimate = np.abs(y_rk4 - y_rk3)
        
        # 5. Step size control
        # ... (Exercise 5 dagi kabi)
```

---

### QADAM 4: Test va vizualizatsiya

```python
if __name__ == "__main__":
    # Parametrlar
    y0 = 1.0
    I = (0.0, 1.0)
    h0 = 0.01
    epsilon = 1e-4
    q = 3
    
    lambdas = [1, 1000]
    
    # 2x2 subplot yaratish (har bir lambda uchun 2 ta grafik)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    for idx, lam in enumerate(lambdas):
        print(f"\nLambda = {lam}")
        print("="*50)
        
        # 1. Yechish
        t_vals, y_vals, fevals = solve_adaptive_rk43_stiff(
            f, y0, I, h0, epsilon, q, lam
        )
        
        # 2. Exact solution
        y_exact = exact_solution(t_vals)
        
        # 3. Error
        error = np.abs(y_vals - y_exact)
        max_error = np.max(error)
        
        # 4. Statistika chiqarish
        print(f"Steps: {len(t_vals) - 1}")
        print(f"Function evaluations: {fevals}")
        print(f"Max error: {max_error:.6e}")
        
        # 5. CHAP GRAFIK: Solution
        ax1 = axes[idx, 0]
        ax1.plot(t_vals, y_vals, 'b-o', markersize=3, 
                 label='Adaptive RK4(3)', alpha=0.7)
        ax1.plot(t_vals, y_exact, 'r--', linewidth=2, 
                 label='Exact solution')
        ax1.set_xlabel('t')
        ax1.set_ylabel('y(t)')
        ax1.set_title(f'Solution for λ = {lam}')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 6. ONG GRAFIK: Error (log scale)
        ax2 = axes[idx, 1]
        ax2.semilogy(t_vals, error, 'g-o', markersize=3)
        ax2.set_xlabel('t')
        ax2.set_ylabel('|Error|')
        ax2.set_title(f'Absolute Error for λ = {lam}')
        ax2.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig('ex_sheet_07/solution_comparison.png', dpi=150)
    plt.show()
```

**Grafik tushuntirish:**

1. **2x2 subplot** - 4 ta grafik:
   - Qator 1: λ = 1 (solution + error)
   - Qator 2: λ = 1000 (solution + error)

2. **Chap grafiklar** - Solution:
   - Ko'k chiziq + nuqtalar: Adaptive RK4(3)
   - Qizil chiziq: Exact solution
   - Ikkalasi bir-biriga yaqin bo'lishi kerak

3. **Ong grafiklar** - Error (log scale):
   - Yashil chiziq: Absolute error
   - Log scale ishlatiladi (kichik xatoliklarni ko'rish uchun)
   - `semilogy` - y o'qi logarifmik

4. **Marker options:**
   - `'b-o'` - ko'k chiziq + doira marker
   - `'r--'` - qizil chiziqli chiziq
   - `markersize=3` - kichik nuqtalar
   - `alpha=0.7` - shaffoflik

---

### QADAM 5: Observation yozish

**Quyidagilarni tahlil qiling:**

1. **λ = 1 (Non-stiff):**
   - Nechta step?
   - Function evaluations?
   - Max error?
   - Step size range?

2. **λ = 1000 (Stiff):**
   - Nechta step? (1 ga nisbatan)
   - Function evaluations? (Ko'proqmi?)
   - Step size qanday o'zgaradi?
   - Adaptive RK samaralimi?

3. **Xulosa:**
   - Explicit RK stiff problemda yaxshimi?
   - Nima uchun ko'p step kerak?
   - Qanday usul yaxshiroq bo'lardi?

---

## BONUS: Grafik chizish variantlari

### Variant 1: Oddiy grafik (bitta lambda uchun)
```python
# Lambda = 1 uchun
t_vals, y_vals, fevals = solve_adaptive_rk43_stiff(f, y0, I, h0, epsilon, q, lam=1)
y_exact = exact_solution(t_vals)

plt.figure(figsize=(12, 5))

# Chap: Solution
plt.subplot(1, 2, 1)
plt.plot(t_vals, y_vals, 'b-o', markersize=4, label='Adaptive RK4(3)')
plt.plot(t_vals, y_exact, 'r--', linewidth=2, label='Exact')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.title('Solution')
plt.legend()
plt.grid(True)

# Ong: Error
plt.subplot(1, 2, 2)
error = np.abs(y_vals - y_exact)
plt.semilogy(t_vals, error, 'g-o', markersize=4)
plt.xlabel('t')
plt.ylabel('|Error|')
plt.title('Absolute Error')
plt.grid(True)

plt.tight_layout()
plt.show()
```

### Variant 2: Ikkalasini bir grafigda
```python
plt.figure(figsize=(10, 6))

for lam in [1, 1000]:
    t_vals, y_vals, _ = solve_adaptive_rk43_stiff(f, y0, I, h0, epsilon, q, lam)
    plt.plot(t_vals, y_vals, '-o', markersize=3, label=f'λ = {lam}')

# Exact solution
t_exact = np.linspace(0, 1, 100)
y_exact = exact_solution(t_exact)
plt.plot(t_exact, y_exact, 'k--', linewidth=2, label='Exact')

plt.xlabel('t')
plt.ylabel('y(t)')
plt.title('Adaptive RK4(3) for Different λ')
plt.legend()
plt.grid(True)
plt.show()
```

### Variant 3: Step size ni ko'rsatish
```python
# solve_adaptive_rk43_stiff dan h_values ni ham qaytaring!

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Yuqori: Solution
ax1.plot(t_vals, y_vals, 'b-o', markersize=3, label='Adaptive RK4(3)')
ax1.plot(t_vals, y_exact, 'r--', linewidth=2, label='Exact')
ax1.set_ylabel('y(t)')
ax1.set_title(f'Solution for λ = {lam}')
ax1.legend()
ax1.grid(True)

# Pastki: Step size
ax2.plot(t_vals[:-1], h_values, 'g-o', markersize=3)
ax2.set_xlabel('t')
ax2.set_ylabel('Step size h')
ax2.set_title('Adaptive Step Size')
ax2.grid(True)

plt.tight_layout()
plt.show()
```

### Matplotlib cheat sheet:

**Line styles:**
- `'-'` - solid line
- `'--'` - dashed line
- `'-.'` - dash-dot line
- `':'` - dotted line

**Markers:**
- `'o'` - circle
- `'s'` - square
- `'^'` - triangle up
- `'*'` - star
- `'.'` - point

**Colors:**
- `'b'` - blue
- `'r'` - red
- `'g'` - green
- `'k'` - black
- `'m'` - magenta
- `'c'` - cyan

**Kombinatsiya:**
- `'b-o'` - blue line with circles
- `'r--'` - red dashed line
- `'g-*'` - green line with stars

---

## Asosiy farqlar (Exercise 5 vs 7)

### Exercise 5 (Van der Pol):
- `f(y)` - autonomous
- `y` - 2D vector
- `c` vektori kerak emas
- Exact solution yo'q

### Exercise 7 (Stiff):
- `f(t, y, λ)` - non-autonomous
- `y` - scalar
- `c` vektori KERAK!
- Exact solution: `e^(-t)`

---

## Foydali formulalar

**ODE:**
```
y'(t) = -λ(y(t) - e^(-t)) - e^(-t)
y(0) = 1
```

**Exact:**
```
y(t) = e^(-t)
```

**RK4 Butcher tableau:**
```
0   |
1/2 | 1/2
1/2 | 0   1/2
1   | 0   0   1
----|-------------
    | 1/6 1/3 1/3 1/6  <- b_rk4
    | 1/6 2/3 0   1/6  <- b_rk3
```

---

## Epsilon qiymati

Agar mashqda berilmagan bo'lsa:
```python
epsilon = 1e-4  # Standart tanlov
```

Boshqa variantlar: `1e-3`, `1e-5`, `1e-6`

---

## Muvaffaqiyat mezonlari

✅ Kod ishlaydi (xatoliksiz)
✅ λ = 1 va λ = 1000 uchun natija bor
✅ Grafik chizilgan (solution + error)
✅ Observation yozilgan
✅ Exact solution bilan taqqoslangan

---

Omad! 🚀
