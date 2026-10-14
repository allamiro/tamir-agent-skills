# `ode-dynamics` prompts

Simulate dynamic models, find their steady states, classify stability and rank the parameters that matter.

- **Give it:** the states with units and initial values, the rate laws and parameters, the time span, and the
  question (time course, steady state, stability, sensitivity)
- **Skill file:** [`skills/ode-dynamics/SKILL.md`](../skills/ode-dynamics/SKILL.md)
- **Stability from eigenvalues:** [`stability-classes.md`](../skills/ode-dynamics/references/stability-classes.md)

## 1. Steady state, stability and sensitivity

> Find the steady state of dS/dt = v0 - Vmax*S/(Km+S) with v0 = 1, Vmax = 2, Km = 0.5, classify its stability, and say which parameters the steady state is most sensitive to.

A good answer: steady state S = 0.5, from v0 = Vmax S/(Km + S), so S = Km v0/(Vmax − v0). The Jacobian is
−Vmax Km/(Km + S)² = −1, a single negative eigenvalue, so the steady state is a stable node. Normalised
sensitivities are 2 for v0, −2 for Vmax and 1 for Km, so the steady state is most sensitive to v0 and Vmax.
These are local values at the nominal point.

## 2. Damped oscillation

> Classify the steady state of dx/dt = y, dy/dt = -x - 0.2*y and describe the phase portrait.

A good answer: the steady state is (0, 0). The Jacobian has rows (0, 1) and (−1, −0.2), with eigenvalues
−0.1 ± 0.995i, so it is a stable focus. Trajectories spiral inwards in a damped oscillation with a period
of about 2π, and the damping ratio is about 0.1.

## 3. Solve by hand and check

> Solve dx/dt = -k x with x(0) = 10 and k = 0.5 by separation of variables, and check the value at t = 2 numerically.

A good answer: x(t) = 10 e^(−0.5 t), so x(2) = 10 e^(−1) ≈ 3.679. A fixed-step RK4 simulation with step 0.01
gives the same value to four or more digits. It suggests halving the step to confirm.

## 4. My simulation blows up

> My Euler simulation of a model with one fast reaction (rate constant 1000 per second) and one slow one (0.01 per second) oscillates and goes negative. Why, and what should I do?

A good answer: the system is stiff (stiffness ratio about 1e5), and explicit Euler with a step larger than
about 2/1000 s is unstable, so the oscillation is numerical. Use an implicit adaptive solver (BDF or LSODA,
or COPASI), or a quasi-steady-state reduction of the fast reaction, and confirm the result does not change
with tighter tolerances.

## 5. Bistability and hysteresis

> How do I check whether my gene circuit with positive feedback is bistable and shows hysteresis?

A good answer: find all steady states for a range of the input parameter (from several starting points),
classify each by eigenvalues, and look for a range with two stable states separated by an unstable one.
Sweep the input up and then down, starting each run from the previous steady state. If the switch happens
at different input values in each direction, the system shows hysteresis.
