# `linear-algebra-networks` prompts

Write networks and equation sets as matrices, solve them exactly, and explain what rank, determinant and
eigenvalues mean for the biology.

- **Give it:** the matrix or equations, what rows and columns stand for, and what you want (solve, classify,
  invert, decompose, eigenvalues)
- **Skill file:** [`skills/linear-algebra-networks/SKILL.md`](../skills/linear-algebra-networks/SKILL.md)
- **What the numbers mean:** [`geometric-meaning.md`](../skills/linear-algebra-networks/references/geometric-meaning.md)

## 1. Rank and solvability

> What is the rank of the matrix with rows (1, 2) and (2, 4), and does the system x + 2y = 3, 2x + 4y = 6 have a unique solution? Use the Rouche-Capelli theorem.

A good answer: rank 1, because the second row is twice the first. The augmented matrix also has rank 1, so
by Rouché–Capelli the system is consistent. The rank is below the two unknowns, so there are infinitely
many solutions with one free parameter (for example x = 3 − 2y).

## 2. Determinant and inverse

> Compute the determinant and inverse of the matrix with rows (2, 1) and (1, 3), and explain the determinant geometrically.

A good answer: determinant 5. The inverse has rows (3/5, −1/5) and (−1/5, 2/5). The determinant is the area
of the parallelogram spanned by the column vectors (2, 1) and (1, 3); because it is not zero, the
matrix is invertible.

## 3. Eigenvalues

> Find the eigenvalues of the matrix with rows (0, 1) and (-2, -3) from the characteristic polynomial, and say what they mean if this is the Jacobian of a two-species model.

A good answer: the characteristic polynomial is λ² + 3λ + 2 = 0, giving eigenvalues −2 and −1. Both are real
and negative, so the steady state is a stable node: perturbations decay without oscillation, the slowest
mode with rate 1.

## 4. Gauss-Jordan

> Bring the matrix with rows (1, 2, 3) and (4, 5, 6) to reduced row-echelon form, showing the row operations, and give the pivot columns and the rank.

A good answer: R2 − 4R1 gives (0, −3, −6). Dividing by −3 gives (0, 1, 2), and R1 − 2R2 gives (1, 0, −1).
The reduced form has rows (1, 0, −1) and (0, 1, 2), pivots in columns 1 and 2, and rank 2.

## 5. Null space of a chain

> For the chain of reactions A -> B -> C written as the matrix with rows (1, -1, 0) and (0, 1, -1), find the null space and explain what it means.

A good answer: the null space has dimension 1 (3 columns minus rank 2) and is spanned by (1, 1, 1). In a
stoichiometric reading, the only steady-state flux pattern is equal flux through every step.
