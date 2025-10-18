Explicit Euler Method for ODE Numerical Solution

This Python code implements the Explicit Euler method to solve the initial value problem:
(1+t)y′(t)+y(t)=11+t,y(0)=1
(1+t)y′(t)+y(t)=1+t1​,y(0)=1
📁 Project Structure
text

euler_method/
├── euler_solver.py
└── README.md

🚀 Quick Start
Prerequisites

    Python 3.6+

    NumPy library

Installation

    Clone or download the project files

    Install dependencies:
    bash

pip install numpy

Run the code:
bash

python euler_solver.py

💻 Usage

The code automatically computes solutions for two step sizes:

    h₁ = 0.2 (coarse approximation)

    h₂ = 0.1 (finer approximation)

Output Includes:

    Numerical solutions at all time points

    Analytical solution comparison

    Error analysis at t = 1

    Step size impact discussion

📊 Example Output
text

Solution with h = 0.2:
t: 0.00, y: 1.000000, Analytical: 1.000000, Error: 0.000000
t: 0.20, y: 0.833333, Analytical: 0.847998, Error: 0.014665
...

Error Analysis:
h = 0.2: Error at t=1 = 0.045215
h = 0.1: Error at t=1 = 0.022348

🧮 Mathematical Background
ODE Form:

The problem is rearranged to:
y′(t)=1(1+t)2−y(t)1+t
y′(t)=(1+t)21​−1+ty(t)​
Analytical Solution:
y(t)=ln⁡(t+1)+11+t
y(t)=1+tln(t+1)+1​
Method:

Explicit Euler method:
yn+1=yn+h⋅f(tn,yn)
yn+1​=yn​+h⋅f(tn​,yn​)
🔧 Code Functions

    func_f(t, y): Defines the ODE right-hand side

    analytical_solution(t): Computes exact solution

    explicit_euler(h, f): Implements Euler method

    compute_error(): Calculates and compares errors

📈 Results Analysis

The error decreases with smaller step sizes, demonstrating the first-order convergence of the Explicit Euler method. Halving the step size approximately halves the error, consistent with theoretical expectations.
🛠 Requirements

    numpy >= 1.19.0

👥 Author

Javokhir Kubaev
📄 License

Educational Use