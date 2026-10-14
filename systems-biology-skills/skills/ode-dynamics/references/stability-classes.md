# Stability from eigenvalues

For a steady state x\* of dx/dt = f(x), linearise: d(δx)/dt = J δx, with J the Jacobian of f at x\*.

| Eigenvalues of J | Class (2D name) | Behaviour near x* |
|---|---|---|
| All real, all negative | Stable node | Monotone approach |
| Complex pair, negative real part | Stable focus (spiral) | Damped oscillation |
| All real, all positive | Unstable node | Monotone departure |
| Complex pair, positive real part | Unstable focus | Growing oscillation |
| Real, opposite signs | Saddle | Approach along one direction, departure along another |
| Purely imaginary pair | Centre (linear); undecided for nonlinear | Linearisation cannot decide |
| A zero eigenvalue | Non-isolated or bifurcation point | Check conservation relations, then higher-order terms |

For a 2x2 Jacobian: stable if trace < 0 and determinant > 0; a focus if trace^2 < 4 det.

Damping ratio of a complex pair λ = -σ ± iω: ζ = σ / sqrt(σ^2 + ω^2); ζ near 0 means slowly damped oscillation.

Stiffness ratio: the largest |Re λ| divided by the smallest non-zero |Re λ|. Ratios in the thousands or more
call for an implicit solver.

Source: standard dynamical systems theory, author knowledge, VERIFY against a dynamical systems text.
