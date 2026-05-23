import numpy as np
import pandas as pd

def solve_dual_simplex(c, A, b):
    m, n = A.shape
    tableau = np.zeros((m + 1, n + m + 1))
    tableau[:m, :n] = A
    tableau[:m, n:n+m] = np.eye(m)
    tableau[:m, -1] = b
    tableau[-1, :n] = -np.array(c)

    steps = []
    basis = [n + i for i in range(m)]
    iteration = 0
    max_iterations = 20

    while iteration < max_iterations:
        idx_labels = [f"x{b_idx+1}" if b_idx < n else f"s{b_idx-n+1}" for b_idx in basis] + ["Z"]
        cols = [f"x{i+1}" for i in range(n)] + [f"s{i+1}" for i in range(m)] + ["b"]
        
        df = pd.DataFrame(np.round(tableau, 3), columns=cols, index=idx_labels)

        if np.all(tableau[:-1, -1] >= -1e-7):
            steps.append((iteration, df, "Оптимальний план знайдено."))
            break

        leave_row = np.argmin(tableau[:-1, -1])

        if np.all(tableau[leave_row, :-1] >= -1e-7):
            steps.append((iteration, df, "Задача не має допустимих розв'язків."))
            break

        row_vals = tableau[leave_row, :-1]
        z_vals = tableau[-1, :-1]

        ratios = np.full_like(row_vals, np.inf, dtype=float)
        for j in range(n + m):
            if row_vals[j] < -1e-7:
                ratios[j] = abs(z_vals[j] / row_vals[j])

        enter_col = np.argmin(ratios)

        if ratios[enter_col] == np.inf:
            steps.append((iteration, df, "Помилка вибору стовпця."))
            break

        out_var = idx_labels[leave_row]
        in_var = cols[enter_col]
        steps.append((iteration, df.copy(), f"Ітерація {iteration}. Виходить: {out_var}, Входить: {in_var}"))

        pivot_element = tableau[leave_row, enter_col]
        tableau[leave_row, :] = tableau[leave_row, :] / pivot_element

        for i in range(m + 1):
            if i != leave_row:
                tableau[i, :] -= tableau[i, enter_col] * tableau[leave_row, :]

        basis[leave_row] = enter_col
        iteration += 1

    if iteration == max_iterations:
        steps.append((iteration, df, "Перевищено ліміт ітерацій."))

    return steps