# Stiff Problem - Roadmap va Tushuntirish

## Problem haqida qisqacha

Bizda oddiy differensial tenglama (ODE) bor:
```
y'(t) = -λ * y(t) - e^(-t) - e^(-t)
y(0) = 1
t ∈ [0, 1]
```

Aniq yechim: `y(t) = e^(-t)`

## Vazifa

4 xil raqamli usul bilan yechimni topish va taqqoslash:
- λ = 1 (oddiy holat)
- λ = 1000 (stiff problem - qattiq masala)

## Qadamlar (Roadmap)

### 1. Parametrlarni sozlash
- Step size: `h = 0.01`
- Grid points: `t_k = k * h`, k = 0, 1, ..., 100
- N = 100 (chunki 1/0.01 = 100)

### 2. To'rt usulni implement qilish

#### a) Explicit Euler (eng oddiy)
```
Y_{k+1} = Y_k + h * f(t_k, Y_k)
```
**Tushuntirish**: Har bir qadamda hozirggi qiymat va hosiladan foydalanib keyingi nuqtani topamiz.

#### b) Improved Euler (aniqroq)
```
Y_{k+1} = Y_k + h * f(t_k + h/2, Y_k + (h/2) * f(t_k, Y_k))
```
**Tushuntirish**: Avval yarim qadamda taxminiy qiymat topamiz, keyin uni ishlatib to'liq qadamni hisoblaymiz.

#### c) Runge-Kutta 4 (RK4) - eng aniq
```
K1 = f(t_k, Y_k)
K2 = f(t_k + h/2, Y_k + (h/2)*K1)
K3 = f(t_k + h/2, Y_k + (h/2)*K2)
K4 = f(t_k + h, Y_k + h*K3)
Y_{k+1} = Y_k + (h/6) * (K1 + 2*K2 + 2*K3 + K4)
```
**Tushuntirish**: 4 ta oraliq qiymat hisoblab, ularning o'rtachasidan foydalanadi. Juda aniq lekin ko'proq hisoblash talab qiladi.

#### d) Adams-Bashforth 2 (multi-step)
```
Y_{k+1} = Y_k + h * (3/2 * f(t_k, Y_k) - 1/2 * f(t_{k-1}, Y_{k-1}))
```
**Tushuntirish**: Oldingi ikki nuqtadan foydalanadi. Y_1 ni topish uchun Explicit Euler ishlatamiz.

### 3. Xatolikni hisoblash

Har bir nuqtada:
```
e_k = Y_k - y(t_k) = Y_k - e^(-t_k)
```

Maksimal xatolik:
```
E_max = max|e_k| (barcha k lar uchun)
```

### 4. Natijalarni taqqoslash

**Jadval yaratish**: 4 usul × 2 lambda qiymati = 8 ta E_max qiymati

| Method | λ = 1 | λ = 1000 |
|--------|-------|----------|
| Explicit Euler | ? | ? |
| Improved Euler | ? | ? |
| RK4 | ? | ? |
| Adams-Bashforth 2 | ? | ? |

### 5. Grafiklar chizish

Har bir λ uchun:
- Aniq yechim: `y(t) = e^(-t)` (qizil chiziq)
- 4 ta raqamli yechim (turli rangda)
- λ = 1000 da ba'zi usullar beqaror bo'lishi mumkin!

### 6. Tahlil qilish

Kutilayotgan natijalar:
- **λ = 1**: Barcha usullar yaxshi ishlaydi, RK4 eng aniq
- **λ = 1000** (stiff!): 
  - Explicit Euler: JUDA YOMON (beqaror)
  - Improved Euler: Yomon
  - RK4: Yaxshiroq lekin hali ham muammoli
  - Adams-Bashforth: Muammoli

**Stiff problem nima?** λ katta bo'lganda, yechim tez o'zgaradi va oddiy usullar beqaror bo'ladi.

## Kod strukturasi

```python
import numpy as np
import matplotlib.pyplot as plt

# 1. f(t, y) funksiyasini aniqlash
def f(t, y, lam):
    return -lam * y - np.exp(-t) - np.exp(-t)

# 2. Aniq yechim
def exact_solution(t):
    return np.exp(-t)

# 3. Har bir usulni implement qilish
def explicit_euler(f, y0, t_grid, lam):
    # ...
    
def improved_euler(f, y0, t_grid, lam):
    # ...
    
def rk4(f, y0, t_grid, lam):
    # ...
    
def adams_bashforth_2(f, y0, t_grid, lam):
    # ...

# 4. Xatolikni hisoblash
def compute_max_error(numerical, exact):
    return np.max(np.abs(numerical - exact))

# 5. Natijalarni chiqarish va grafik chizish
```

## Muhim eslatmalar

- `h = 0.01` juda kichik, shuning uchun λ = 1 da hammasi yaxshi ishlaydi
- λ = 1000 da explicit usullar beqaror bo'ladi (grafiklarda ko'rasiz)
- Stiff problemlar uchun implicit usullar kerak (masalan, Backward Euler)

Omad! 🚀
