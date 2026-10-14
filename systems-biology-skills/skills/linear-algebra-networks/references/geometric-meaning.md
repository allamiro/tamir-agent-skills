# What the numbers mean

| Quantity | Geometric meaning | In a network model |
|---|---|---|
| Determinant | Signed area (2x2) or volume (3x3) of the parallelogram or box spanned by the columns; zero means the columns are flat (dependent) | A singular Jacobian means a steady state that is not isolated (a line of steady states, or a bifurcation) |
| Rank | Number of independent directions the columns span | Number of independent mass balances in a stoichiometric matrix |
| Null space | Directions that the matrix sends to zero | Steady-state flux directions (right null space); conserved moieties (left null space) |
| Inverse | The transformation that undoes the matrix | Exists only when no information is lost |
| Eigenvector | A direction the matrix only stretches | A mode of a linear system that evolves on its own |
| Eigenvalue | The stretch factor along that direction | Growth (positive real part) or decay (negative) rate of the mode; imaginary part gives oscillation frequency |
| Trace | Sum of the diagonal, equal to the sum of the eigenvalues | For a 2x2 Jacobian, trace < 0 and det > 0 means a stable steady state |

## The four kinds of knowledge, applied to the determinant

The workbook's checklist asks for four kinds of knowledge for each topic. For the determinant:

- Declarative: what it is (the signed area or volume above).
- Procedural: how to compute it (2x2 formula, Sarrus for 3x3, Laplace expansion in general, or elimination).
- Contextual: when to use it (to decide invertibility; only for square matrices).
- Conceptual: why it works (it measures how the transformation scales areas, so zero means a collapse).
