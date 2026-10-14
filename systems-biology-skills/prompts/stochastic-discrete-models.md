# `stochastic-discrete-models` prompts

Model noise at low copy numbers, logical networks and discrete-time dynamics, and know when each is needed.

- **Give it:** species with molecule counts and reactions with stochastic constants, or Boolean rules with
  references, or an update rule for a difference equation
- **Skill file:** [`skills/stochastic-discrete-models/SKILL.md`](../skills/stochastic-discrete-models/SKILL.md)
- **Conversions and conventions:** [`noise-and-logic.md`](../skills/stochastic-discrete-models/references/noise-and-logic.md)

## 1. Simulate at low copy number

> Simulate this at low copy number with the Gillespie algorithm: production of A at 10 molecules per unit time, degradation at 0.5 per molecule per unit time, starting from zero. What are the mean and variance at t = 50, and how do they compare with the ODE?

A good answer: the ODE steady state is 10/0.5 = 20 molecules. A Gillespie simulation with a few hundred runs
gives a mean near 20 and a standard deviation near 4.5, because the variance equals the mean for this
birth–death (Poisson) process, giving a Fano factor of about 1. It reports the number of runs and the seed.

## 2. Boolean attractors

> Find the attractors of this Boolean network with synchronous updating: A = not C, B = A, C = B. Are they real?

A good answer: two attractors under synchronous updating, a cycle of length 6
(000 → 100 → 110 → 111 → 011 → 001) and a cycle of length 2 (010 ↔ 101). The 2-cycle is an artefact of
updating every node at once, and it should be checked with asynchronous updating before being interpreted.
The 6-cycle matches the oscillation expected of a three-node negative feedback ring.

## 3. Toggle switch

> What are the stable states of a two-gene toggle, A = A and not B, B = B and not A?

A good answer: three fixed points under synchronous updating: 00, 01 and 10. States 01 and 10 are the two
switch states. 11 goes to 00, and 00 is a fixed point with both genes off.

## 4. Logistic map

> For the logistic map x' = r x (1 - x), what happens at r = 2.8 and at r = 3.2?

A good answer: at r = 2.8 the orbit converges to the stable fixed point 1 − 1/r ≈ 0.643, and 0 is unstable.
At r = 3.2 that fixed point (0.6875) has become unstable and the orbit settles into a period-2 cycle
alternating about 0.513 and 0.799. It explains the stability condition |f′(x*)| < 1.

## 5. When is noise important

> When do I need a stochastic model instead of an ODE model for gene expression?

A good answer: when copy numbers are low (tens to hundreds), when expression is bursty, when single-cell data
show broad or bimodal distributions, or when variation between cells or rare events are the question. It
mentions intrinsic versus extrinsic noise, and that the ODE solution equals the stochastic mean only for
linear reactions.
