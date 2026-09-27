import numpy as np
from scipy.integrate import solve_ivp

# System parameters
a, b, c, p = 49.0, 8.0, 180.0, 6.0

def lorenz_5d(t, state):
    x1, x2, x3, x4, x5 = state
    dx1 = a * (x2 - x1) + x2 * x3 + x3 + x4 + x5
    dx2 = c * x2 - x1 * x3 + x4 + x5
    dx3 = x1 * x2 - b * x3
    dx4 = -p * (x1 + x2)
    dx5 = -x1
    return [dx1, dx2, dx3, dx4, dx5]

def jacobian(state):
    x1, x2, x3, x4, x5 = state
    # J_ij = d(f_i) / d(x_j)
    J = np.array([
        [-a, a + x3, x2 + 1, 1.0, 1.0],
        [-x3, c, -x1, 1.0, 1.0],
        [x2, x1, -b, 0.0, 0.0],
        [-p, -p, 0.0, 0.0, 0.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0]
    ])
    return J

def compute_lyapunov_spectrum(t_max=200.0, dt=0.01):
    n = 5
    state = np.array([0.2, 0.1, 0.2, 0.1, 0.2])
    Q = np.eye(n) # Orthonormal tangent vectors
    lyap_sum = np.zeros(n)
    
    t = 0.0
    steps = int(t_max / dt)
    
    for _ in range(steps):
        # 1. Evolve base state and tangent space (Variational equations: dQ/dt = J * Q)
        # Flatten state (5) + Q matrix (25) = 30 variables
        y0 = np.concatenate([state, Q.ravel()])
        
        sol = solve_ivp(
            lambda _, y: np.concatenate([
                lorenz_5d(_, y[:n]),
                (jacobian(y[:n]) @ y[n:].reshape(n, n)).ravel()
            ]),
            [t, t + dt], y0, method='RK45'
        )
        
        y_final = sol.y[:, -1]
        state = y_final[:n]
        Q_matrix = y_final[n:].reshape(n, n)
        
        # 2. QR Decomposition for orthogonalization and scaling tracking
        Q, R = np.linalg.qr(Q_matrix)
        
        # Accumulate logarithms of diagonal elements of R
        lyap_sum += np.log(np.abs(np.diagonal(R)))
        t += dt
        
    # Average over total time to get Lyapunov Exponents
    return lyap_sum / t_max

exponents = compute_lyapunov_spectrum()
print("Lyapunov Exponents:", exponents)
