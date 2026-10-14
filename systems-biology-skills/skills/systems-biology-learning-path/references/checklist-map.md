# Map of the workbook's learning checklist

Topics and priorities (1 = first) as listed in the Sauter and Albrecht checklist (supplied text), with the
skill in this collection that covers each. Topic names are the workbook's; grouping and skill mapping are ours.

## Part 0: Introduction and learning (all priority 2)

Systems medicine, network medicine, self-efficacy, regulation of effort, performance gain with practice,
self-directed learning, critical thinking, knowledge organisation, elaboration, skill level, elements of
mastery, competence levels. Skill: `systems-biology-learning-path`, `network-analysis`.

## Part 1: Biochemical network in matrix form

| Priority | Topics | Skill |
|---|---|---|
| 1 | Define systems biology; PCA, PLSR, VIP; linear equations in matrix form; matrix indices; augmented matrix; Gauss and Gauss–Jordan; rank; identity and zero matrix; trace; matrix multiplication, sum, scalar multiplication, transpose; 2x2 determinant and inverse; eigenvalues | `linear-algebra-networks`, `multivariate-omics` |
| 2 | Incidence matrix; adjacency matrix and list; hypergraph; Cramer's rule; 3x3 determinant (Sarrus); 3x3 inverse; eigenvectors | `network-analysis`, `linear-algebra-networks` |
| 3 | Graph notation; reduced row-echelon form; LU decomposition; Laplace expansion; fast eigenvalue formula | `linear-algebra-networks` |

## Part 2: Metabolic modelling

| Priority | Topics | Skill |
|---|---|---|
| 1 | Classify metabolic models; stoichiometric matrix; steady state; Rouché–Capelli; classify MFA (dynamic, isotope tracer); pros and cons of FBA | `stoichiometric-networks`, `flux-balance-analysis` |
| 2 | Elementary flux modes; conservation relations; MFA; FBA; constrained optimisation cone | same |
| 3 | Left and right null space | `stoichiometric-networks` |

## Part 3: Dynamics, control and systems theory

| Priority | Topics | Skill |
|---|---|---|
| 1 | Black box; block diagram; ODE; general system properties; feed-forward and feedback loops; state space; classify systems; steady state; stability; damping; characteristic polynomial; eigenvalue stability classification; p-q and a-b-c formulas; complex numbers; differentiation rules; separation of variables; integration factor | `control-systems-feedback`, `ode-dynamics` |
| 2 | Hysteresis; synthetic vs systems biology; ODE vs PDE; systems of ODEs; nonlinear dynamics; open vs closed loop; SISO vs MIMO; time vs frequency domain; controllability; observability; transfer function; phase portrait; trajectory; slope field; isoclines; discrete systems; difference equations; linearisation | `control-systems-feedback`, `ode-dynamics`, `stochastic-discrete-models` |
| 3 | Laplace transform; Fourier transform | `control-systems-feedback` |

## Part 4: Physical modelling and enzyme kinetics

| Priority | Topics | Skill |
|---|---|---|
| 1 | Reality and model; modelling cycle; assumptions; model building; variable, parameter, coefficient; sensitivity analysis; model classification; extensive and intensive quantities; quantity calculus; balancing; mass and amount balances; mass action; reaction rate; Michaelis–Menten; Hill; analysis without equations | `model-building-design`, `quantities-units-balances`, `enzyme-kinetics`, `ode-dynamics` |
| 2 | Akaike information criterion; first and second laws of thermodynamics; SI units; reversible MM; MM with inhibition; substrate inhibition; cooperative enzymes | `parameter-estimation-model-selection`, `quantities-units-balances`, `enzyme-kinetics` |
| 3 | Dimension analysis; poorly posed problems; noise; volume balance; Lineweaver–Burk plot | `model-building-design`, `parameter-estimation-model-selection`, `enzyme-kinetics` |

The checklist marks "distinguish variable, parameter, coefficient" with an unclear priority ("f1" in the
supplied text); it is treated here as priority 1.
