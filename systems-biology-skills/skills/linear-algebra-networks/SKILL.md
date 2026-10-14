---
name: linear-algebra-networks
description: Writes biochemical networks and linear equation systems in matrix form and solves them exactly, covering matrix indices and operations, transpose, trace, determinants (2x2, Sarrus, Laplace, Cramer's rule), inverses, Gauss and Gauss-Jordan elimination, reduced row-echelon form, rank, the Rouche-Capelli theorem, LU decomposition, null spaces, and eigenvalues and eigenvectors with their geometric meaning. Use for "put these equations in matrix form", "what is the rank of this matrix", "does this system have a unique solution", "compute the eigenvalues", "invert this matrix", "explain the determinant geometrically", "check my Gauss elimination". Use stoichiometric-networks for flux and conservation analysis of a reaction network, ode-dynamics for stability of a nonlinear model, and network-analysis for graph measures.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Linear algebra for networks

## Purpose and activation

Every network analysis in this collection reduces to linear algebra: a stoichiometric matrix's null
space gives steady-state fluxes, a Jacobian's eigenvalues give stability, and a design matrix's rank says
which parameters can be estimated. Hand calculation is where signs get lost, so this skill computes
exactly (with fractions) and explains each result in terms of the biology. Activate when the user writes
or checks a matrix, solves a linear system, or needs the meaning of rank, determinant or an eigenvalue.

## Required inputs

The matrix or the equation set; what the rows and columns stand for (species, reactions, nodes,
equations, unknowns); and the question (solve, classify, invert, decompose, find eigenvalues).

## Workflow

1. **Write the matrix with labelled rows and columns.** For a linear equation set, the coefficient matrix A,
   the unknown vector x and the right side b; the augmented matrix [A | b] for elimination.
2. **Reduce** with `python3 scripts/linalg.py rref "A"`, which gives the pivot columns and the rank, exactly.
3. **Classify the system** with `python3 scripts/linalg.py solve "A" --b "b"`. By Rouché–Capelli, A x = b has a solution
   if and only if rank(A) = rank([A | b]); the solution is unique if that rank equals the number of unknowns,
   otherwise there is a family with (unknowns - rank) free parameters.
4. **For square matrices,** compute the determinant (`det`), the inverse (`inv`) or an LU factorisation (`lu`).
   A zero determinant means no inverse and dependent rows.
5. **Find the null space** (`null`): the directions x with A x = 0. In a stoichiometric matrix these are the
   steady-state flux directions (`stoichiometric-networks`).
6. **Find eigenvalues** (`eig`) from the characteristic polynomial det(A - λI) = 0. Their real parts decide
   stability of a linear(ised) system; complex pairs mean oscillation.
7. **Interpret** each number in terms of the network, with the meanings in `references/geometric-meaning.md`.
8. **Show the steps** when the user is learning: write the row operations, then confirm with the script.

## Decision framework

| Question | Tool | Note |
|---|---|---|
| Unique solution of a square system | det ≠ 0, then solve | Cramer's rule only for 2 or 3 unknowns by hand |
| Any system | rref, Rouché–Capelli | Works for non-square and singular matrices |
| Many right-hand sides | LU once, then substitute | Cheaper than repeated elimination |
| Dependencies among rows or columns | rank, null space | Left null space (of the transpose) for rows |
| Stability, modes, growth | eigenvalues | For nonlinear models, of the Jacobian at a steady state |
| Main directions of variation in data | eigenvectors of a covariance matrix | That is PCA (`multivariate-omics`) |

## Failure and edge cases

- **Floating-point rank:** a numerically tiny pivot treated as non-zero. Exact fractions avoid this; with
  measured data, use a tolerance and report it.
- **Sign errors in elimination** by hand, especially subtracting a negative row.
- **Sarrus's rule applied to a 4x4 matrix.** It works only for 3x3.
- **Inverting to solve a system** when elimination is cheaper and more stable.
- **Eigenvalues of a non-square matrix** requested; they do not exist.
- **Row and column labels swapped,** so the null space is computed for the wrong matrix.

## Validation

- `python3 scripts/linalg.py --selftest` passes; it was also cross-checked against NumPy on 962 random cases with no mismatch.
- A solution x satisfies A x = b when substituted back.
- rank + nullity = number of columns.
- The product of the eigenvalues equals the determinant, and their sum equals the trace.
- Falsifier: a claimed unique solution for a system whose rank is below the number of unknowns.

## Expected output

The labelled matrix; the reduced form with pivots and rank; the classification of the system and its
solution or solution family; any determinant, inverse, factorisation, null space or eigenvalues requested;
and the meaning of each result for the network.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 1 (supplied text): matrix form of
  linear equation sets, indices, augmented coefficient matrix, Cramer's rule, Gauss and Gauss–Jordan form,
  reduced row-echelon form, LU decomposition, rank, identity and zero matrices, trace, matrix operations,
  transpose, determinants (2x2, Sarrus, Cramer, Laplace), inverses, eigenvalues and eigenvectors are listed
  topics; the book's example that a 2x2 determinant is the area spanned by two vectors is in the supplied
  introduction. Chapter text not seen
- Linear algebra results: standard, author knowledge; the script was checked against NumPy (see Validation)
