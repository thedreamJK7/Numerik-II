import numpy as np
import matplotlib.pyplot as plt


def symplectic_euler(m, g, r0, p0, q0, I, tau):
    t0, T = I
    N = int((T - t0) / tau)
    
    # Initialize arrays
    t = np.linspace(t0, T, N + 1)
    p = np.zeros(N + 1)
    q = np.zeros(N + 1)
    
    p[0] = p0
    q[0] = q0
    
    for k in range(N):
        p[k + 1] = p[k] - tau * (m * g / r0) * np.cos(q[k])    
        q[k + 1] = q[k] + tau * (1 / m) * p[k + 1]
    
    return p, q, t


def symplectic_euler_II(m, g, r0, p0, q0, I, tau):
    t0, T = I
    N = int((T - t0) / tau)
    
    t = np.linspace(t0, T, N + 1)
    p = np.zeros(N + 1)
    q = np.zeros(N + 1)
    
    p[0] = p0
    q[0] = q0
    
    for k in range(N):
        q[k + 1] = q[k] + tau * (1 / m) * p[k]
        p[k + 1] = p[k] - tau * (m * g / r0) * np.cos(q[k + 1])
    return p, q, t


def hamiltonian(p, q, m, g, r0):
    kinetic = p**2 / (2 * m)
    potential = (m * g / r0) * (1 - np.cos(q))
    return kinetic + potential


def explicit_euler(m, g, r0, p0, q0, I, tau):
    t0, T = I
    N = int((T - t0) / tau)
    
    t = np.linspace(t0, T, N + 1)
    p = np.zeros(N + 1)
    q = np.zeros(N + 1)
    
    p[0] = p0
    q[0] = q0
    
    for k in range(N):
        p[k + 1] = p[k] - tau * (m * g / r0) * np.cos(q[k])
        q[k + 1] = q[k] + tau * (1 / m) * p[k]
    
    return p, q, t


def demonstrate_energy_conservation():
    m = 1.0      # mass
    g = 9.81     # gravity
    r0 = 1.0     # length
    
    p0 = 0.0     # initial momentum
    q0 = np.pi/6 # initial angle (30 degrees - smaller for better conservation)
    
    I = (0, 20)  # longer time to see energy behavior
    tau = 0.05   # smaller step size for better accuracy
    
    p_symp1, q_symp1, t = symplectic_euler(m, g, r0, p0, q0, I, tau)
    p_symp2, q_symp2, _ = symplectic_euler_II(m, g, r0, p0, q0, I, tau)
    p_euler, q_euler, _ = explicit_euler(m, g, r0, p0, q0, I, tau)
    
    H_symp1 = hamiltonian(p_symp1, q_symp1, m, g, r0)
    H_symp2 = hamiltonian(p_symp2, q_symp2, m, g, r0)
    H_euler = hamiltonian(p_euler, q_euler, m, g, r0)
    
    H0 = hamiltonian(p0, q0, m, g, r0)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    ax1.plot(q_symp1, p_symp1, 'b-', label='Symplectic Euler I', linewidth=2)
    ax1.plot(q_symp2, p_symp2, 'g--', label='Symplectic Euler II', linewidth=2)
    ax1.plot(q_euler, p_euler, 'r:', label='Explicit Euler', linewidth=2)
    ax1.set_xlabel('q (angle)')
    ax1.set_ylabel('p (momentum)')
    ax1.set_title('Phase Portrait')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(t, q_symp1, 'b-', label='Symplectic Euler I')
    ax2.plot(t, q_symp2, 'g--', label='Symplectic Euler II')
    ax2.plot(t, q_euler, 'r:', label='Explicit Euler')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('q (angle)')
    ax2.set_title('Angle vs Time')
    ax2.legend()
    ax2.grid(True)
    
    ax3.plot(t, H_symp1, 'b-', label=f'Symplectic I (drift: {H_symp1[-1]-H0:.6f})')
    ax3.plot(t, H_symp2, 'g--', label=f'Symplectic II (drift: {H_symp2[-1]-H0:.6f})')
    ax3.plot(t, H_euler, 'r:', label=f'Explicit Euler (drift: {H_euler[-1]-H0:.6f})')
    ax3.axhline(y=H0, color='k', linestyle='-', alpha=0.5, label=f'True energy: {H0:.6f}')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Energy H(p,q)')
    ax3.set_title('Energy Conservation')
    ax3.legend()
    ax3.grid(True)
    
    ax4.semilogy(t, np.abs(H_symp1 - H0), 'b-', label='Symplectic Euler I')
    ax4.semilogy(t, np.abs(H_symp2 - H0), 'g--', label='Symplectic Euler II')
    ax4.semilogy(t, np.abs(H_euler - H0), 'r:', label='Explicit Euler')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('|H(t) - H(0)|')
    ax4.set_title('Energy Error (log scale)')
    ax4.legend()
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig('ex_sheet_10/pendulum_energy_conservation.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Print summary
    print("Energy Conservation Analysis:")
    print(f"Initial energy H(0) = {H0:.6f}")
    print(f"Symplectic Euler I:  Final energy = {H_symp1[-1]:.6f}, drift = {H_symp1[-1]-H0:.6f}")
    print(f"Symplectic Euler II: Final energy = {H_symp2[-1]:.6f}, drift = {H_symp2[-1]-H0:.6f}")
    print(f"Explicit Euler:      Final energy = {H_euler[-1]:.6f}, drift = {H_euler[-1]-H0:.6f}")
    print()
    print("KEY OBSERVATION:")
    print("- Symplectic methods: Energy oscillates but stays bounded")
    print("- Explicit Euler: Energy grows without bound (secular drift)")
    print("- This is why symplectic integrators are essential for long-time simulations")


def verify_symplecticity():
    print("Symplecticity Verification for Symplectic Euler:")
    print("=" * 50)
    
    print("Key Insight: Symplectic Euler is EXACTLY symplectic for separable Hamiltonians!")
    print("H(p,q) = T(p) + V(q) where T(p) = p²/(2m) and V(q) = (mg/r0)(1-cos q)")
    print()
    
    print("For separable Hamiltonian systems:")
    print("p' = -∂H/∂q = -V'(q)")
    print("q' = ∂H/∂p = T'(p)")
    print()
    
    print("Symplectic Euler I method:")
    print("p_{k+1} = p_k - τ * V'(q_k)")
    print("q_{k+1} = q_k + τ * T'(p_{k+1})")
    print()
    
    print("This can be written as composition of two exact symplectic maps:")
    print("Map 1: (p,q) → (p - τV'(q), q)     [momentum update]")
    print("Map 2: (p,q) → (p, q + τT'(p))     [position update]")
    print()
    
    print("Each map has Jacobian:")
    print("A₁ = [1    -τV''(q)]    A₂ = [1     0   ]")
    print("     [0       1    ]         [τT''(p) 1   ]")
    print()
    
    print("Example: Linear Harmonic Oscillator")
    print("H = p²/2 + ω²q²/2, so p' = -ω²q, q' = p")
    print()
    
    tau = 0.1
    omega = 1.0
    
    A1 = np.array([[1, -tau * omega**2],
                   [0, 1]])
    A2 = np.array([[1, 0],
                   [tau, 1]])
    A_total = A2 @ A1  # Composition: first A1, then A2
    
    J = np.array([[0, 1],
                  [-1, 0]])
    
    result = A_total.T @ J @ A_total
    
    print(f"For harmonic oscillator (ω = {omega}, τ = {tau}):")
    print(f"A₁ = {A1}")
    print(f"A₂ = {A2}")
    print(f"A_total = A₂ A₁ = {A_total}")
    print()
    print(f"Symplecticity check: A^T J A = {result}")
    print(f"Should equal J = {J}")
    print(f"Difference: {np.max(np.abs(result - J)):.2e}")
    
    if np.allclose(result, J, atol=1e-14):
        print("✓ Method is EXACTLY symplectic for separable Hamiltonians!")
    else:
        print("✗ Numerical error in calculation")
    

def test_moon_parameters():
    print("Part b) Testing with Moon Parameters")
    print("=" * 40)
    
    r0 = 0.10  # m
    m = 0.10   # kg  
    g = 1.62   # m/s² (Moon gravity)
    
    p0 = 0.0   # initial momentum
    q0 = 0.0   # initial angle
    
    I = (0, 20)  # seconds
    
    step_sizes = [0.1, 0.05, 0.01]
    
    print(f"Parameters: r0 = {r0} m, m = {m} kg, g = {g} m/s²")
    print(f"Initial conditions: p0 = {p0}, q0 = {q0}")
    print(f"Time interval: {I}")
    print()
    
    results = {}
    for tau in step_sizes:
        print(f"Testing with step size τ = {tau}")
        p, q, t = symplectic_euler(m, g, r0, p0, q0, I, tau)
        
        results[tau] = {'p': p, 'q': q, 't': t}
        
        print(f"  Final time: {t[-1]:.2f} s")
        print(f"  Final angle: {q[-1]:.6f} rad")
        print(f"  Final momentum: {p[-1]:.6f} kg⋅m²/s")
        print()
    
    return results, (r0, m, g, p0, q0, I)


def plot_phase_and_trajectories(results, params):
    print("Part c) Plotting Results")
    print("=" * 40)
    
    r0, m, g, p0, q0, I = params
    
    fig = plt.figure(figsize=(15, 12))
    
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    colors = ['blue', 'red', 'green']
    step_sizes = list(results.keys())
    
    for i, (tau, color) in enumerate(zip(step_sizes, colors)):
        p, q, t = results[tau]['p'], results[tau]['q'], results[tau]['t']
        
        x = r0 * np.cos(q)
        y = r0 * np.sin(q)
        
        H = hamiltonian(p, q, m, g, r0)
        
        ax1 = fig.add_subplot(gs[0, i])
        ax1.plot(q, p, color=color, linewidth=2)
        ax1.set_xlabel('q (angle)')
        ax1.set_ylabel('p (momentum)')
        ax1.set_title(f'Phase Space (τ = {tau})')
        ax1.grid(True)
        
        ax2 = fig.add_subplot(gs[1, i])
        ax2.plot(x, y, color=color, linewidth=2)
        ax2.set_xlabel('x(t) = r₀cos(q)')
        ax2.set_ylabel('y(t) = r₀sin(q)')
        ax2.set_title(f'Euclidean Trajectory (τ = {tau})')
        ax2.set_aspect('equal')
        ax2.grid(True)
        
        circle = plt.Circle((0, 0), r0, fill=False, color='black', linestyle='--', alpha=0.5)
        ax2.add_patch(circle)
        
        ax3 = fig.add_subplot(gs[2, i])
        ax3.plot(t, H, color=color, linewidth=2)
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('H(p,q)')
        ax3.set_title(f'Hamiltonian (τ = {tau})')
        ax3.grid(True)
        
        radius = np.sqrt(x**2 + y**2)
        print(f"τ = {tau}: Radius variation = {np.max(radius) - np.min(radius):.2e}")
    
    plt.suptitle('Symplectic Euler Method - Moon Pendulum Analysis', fontsize=16)
    plt.savefig('ex_sheet_10/moon_pendulum_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()


def prove_radius_preservation():
    print("Part d) Radius Preservation Proof")
    print("=" * 40)
    
    print("Mathematical Proof:")
    print("Given: x(t) = r₀cos(q(t)), y(t) = r₀sin(q(t))")
    print()
    print("The radius is:")
    print("r(t) = √(x(t)² + y(t)²)")
    print("     = √((r₀cos(q))² + (r₀sin(q))²)")
    print("     = √(r₀²cos²(q) + r₀²sin²(q))")
    print("     = √(r₀²(cos²(q) + sin²(q)))")
    print("     = √(r₀² × 1)")
    print("     = r₀")
    print()
    print("Therefore: r(t) = r₀ = constant for all t ≥ 0")
    print()
    print("This holds because cos²(q) + sin²(q) = 1 (trigonometric identity)")
    print("The radius is preserved regardless of the numerical method used!")


def compare_methods_detailed():
    print("Part f) Detailed Method Comparison")
    print("=" * 40)
    
    r0, m, g = 0.10, 0.10, 1.62
    p0, q0 = 0.0, 0.1  # Small initial angle for better comparison
    I = (0, 20)
    tau = 0.05
    p_symp, q_symp, t = symplectic_euler(m, g, r0, p0, q0, I, tau)
    p_expl, q_expl, _ = explicit_euler(m, g, r0, p0, q0, I, tau)
    
    H_symp = hamiltonian(p_symp, q_symp, m, g, r0)
    H_expl = hamiltonian(p_expl, q_expl, m, g, r0)
    H0 = hamiltonian(p0, q0, m, g, r0)
    x_symp, y_symp = r0 * np.cos(q_symp), r0 * np.sin(q_symp)
    x_expl, y_expl = r0 * np.cos(q_expl), r0 * np.sin(q_expl)
    
    r_symp = np.sqrt(x_symp**2 + y_symp**2)
    r_expl = np.sqrt(x_expl**2 + y_expl**2)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    ax1.plot(q_symp, p_symp, 'b-', label='Symplectic Euler', linewidth=2)
    ax1.plot(q_expl, p_expl, 'r--', label='Explicit Euler', linewidth=2)
    ax1.set_xlabel('q (angle)')
    ax1.set_ylabel('p (momentum)')
    ax1.set_title('Phase Space Comparison')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(x_symp, y_symp, 'b-', label='Symplectic Euler', linewidth=2)
    ax2.plot(x_expl, y_expl, 'r--', label='Explicit Euler', linewidth=2)
    circle = plt.Circle((0, 0), r0, fill=False, color='black', linestyle=':', alpha=0.7)
    ax2.add_patch(circle)
    ax2.set_xlabel('x(t)')
    ax2.set_ylabel('y(t)')
    ax2.set_title('Euclidean Trajectory Comparison')
    ax2.set_aspect('equal')
    ax2.legend()
    ax2.grid(True)
    
    # Energy comparison
    ax3.plot(t, H_symp, 'b-', label=f'Symplectic (drift: {H_symp[-1]-H0:.4f})', linewidth=2)
    ax3.plot(t, H_expl, 'r--', label=f'Explicit (drift: {H_expl[-1]-H0:.4f})', linewidth=2)
    ax3.axhline(y=H0, color='k', linestyle=':', alpha=0.7, label=f'True energy: {H0:.4f}')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Energy H(p,q)')
    ax3.set_title('Energy Conservation')
    ax3.legend()
    ax3.grid(True)
    
    # Radius preservation
    ax4.plot(t, r_symp, 'b-', label=f'Symplectic (var: {np.max(r_symp)-np.min(r_symp):.2e})', linewidth=2)
    ax4.plot(t, r_expl, 'r--', label=f'Explicit (var: {np.max(r_expl)-np.min(r_expl):.2e})', linewidth=2)
    ax4.axhline(y=r0, color='k', linestyle=':', alpha=0.7, label=f'True radius: {r0}')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Radius r(t)')
    ax4.set_title('Radius Preservation')
    ax4.legend()
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig('ex_sheet_10/method_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Print numerical comparison
    print(f"Energy drift comparison:")
    print(f"  Symplectic Euler: {H_symp[-1]-H0:.6f}")
    print(f"  Explicit Euler:   {H_expl[-1]-H0:.6f}")
    print()
    print(f"Radius preservation:")
    print(f"  Symplectic Euler variation: {np.max(r_symp)-np.min(r_symp):.2e}")
    print(f"  Explicit Euler variation:   {np.max(r_expl)-np.min(r_expl):.2e}")
    print(f"  Theoretical radius: {r0}")


if __name__ == "__main__":
    print("Exercise Sheet 10: Symplectic Euler Method for Pendulum")
    print("=" * 60)
    
    results, params = test_moon_parameters()
    print()
    plot_phase_and_trajectories(results, params)
    
    print()
    prove_radius_preservation()
    
    print()
    compare_methods_detailed()