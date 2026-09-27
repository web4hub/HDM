import numpy as np
from scipy.integrate import solve_ivp
import openpyxl

def run_lyapunov_sweep(a_vals, c_vals, t_max=100.0, dt=0.01):
    results = []
    n = 5
    b, p = 8.0, 6.0

    for a in a_vals:
        for c in c_vals:
            # Local definitions of system and Jacobian for current parameters
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
                return np.array([
                    [-a, a + x3, x2 + 1, 1.0, 1.0],
                    [-x3, c, -x1, 1.0, 1.0],
                    [x2, x1, -b, 0.0, 0.0],
                    [-p, -p, 0.0, 0.0, 0.0],
                    [-1.0, 0.0, 0.0, 0.0, 0.0]
                ])

            # Initialize state and tangent space matrix
            state = np.array([0.2, 0.1, 0.2, 0.1, 0.2])
            Q = np.eye(n)
            lyap_sum = np.zeros(n)
            t = 0.0
            steps = int(t_max / dt)

            # Integration loop with periodic QR decomposition
            for _ in range(steps):
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
                
                Q, R = np.linalg.qr(Q_matrix)
                lyap_sum += np.log(np.abs(np.diagonal(R)))
                t += dt

            exponents = lyap_sum / t_max
            # Count positive Lyapunov exponents to classify behavior
            pos_count = np.sum(exponents > 1e-4)
            classification = "Hyperchaotic" if pos_count >= 2 else ("Chaotic" if pos_count == 1 else "Stable/Periodic")

            results.append({
                "a": a,
                "c": c,
                "LE1": exponents[0],
                "LE2": exponents[1],
                "LE3": exponents[2],
                "LE4": exponents[3],
                "LE5": exponents[4],
                "Sum": np.sum(exponents),
                "PositiveExponents": pos_count,
                "Classification": classification
            })
            print(f"Completed -> a: {a}, c: {c} | Status: {classification}")

    return results

def export_to_spreadsheet(sweep_data, filename="hyperchaos_sweep_output.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Parameter Sweep"

    # Header Row
    headers = ["Parameter a", "Parameter c", "LE 1", "LE 2", "LE 3", "LE 4", "LE 5", "Sum (Kaplan-Yorke)", "Pos Count", "Classification"]
    ws.append(headers)

    # Data Rows
    for row in sweep_data:
        ws.append([
            row["a"], row["c"], 
            row["LE1"], row["LE2"], row["LE3"], row["LE4"], row["LE5"],
            row["Sum"], row["PositiveExponents"], row["Classification"]
        ])

    wb.save(filename)
    print(f"Sweep results successfully exported to {filename}")

# Define parameter ranges for the sweep
a_range = [45, 49, 53]
c_range = [170, 180, 190]

# Execute sweep and save
if __name__ == "__main__":
    data = run_lyapunov_sweep(a_range, c_range, t_max=50.0)
    export_to_spreadsheet(data)
