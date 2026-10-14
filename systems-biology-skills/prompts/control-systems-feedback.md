# `control-systems-feedback` prompts

Use systems and control theory: block diagrams, state space, transfer functions, controllability,
observability and what feedback does.

- **Give it:** the system as equations or a diagram, its inputs, outputs and states, whether it is linear or
  linearised, and the question
- **Skill file:** [`skills/control-systems-feedback/SKILL.md`](../skills/control-systems-feedback/SKILL.md)
- **Feedback examples in biology:** [`loop-examples.md`](../skills/control-systems-feedback/references/loop-examples.md)

## 1. Controllable, observable, stable

> My linearised two-state model has A with rows (0, 1) and (-2, -3), input matrix B = (0, 1) and output C = (1, 0). Is the system controllable and observable? Give the transfer function, poles and steady-state gain.

A good answer: the controllability matrix [B, AB] has rank 2, so the system is controllable, and the
observability matrix has rank 2, so it is observable. The transfer function is G(s) = 1/(s² + 3s + 2),
with poles −2 and −1 (stable) and steady-state gain 0.5.

## 2. Routh-Hurwitz

> Is the characteristic polynomial s^3 + s^2 + 2s + 8 stable? Use the Routh-Hurwitz criterion.

A good answer: the first column of the Routh array is 1, 1, −6, 8. It has two sign changes, so two roots have
positive real part and the system is unstable.

## 3. Closing the loop

> A process has transfer function 4/(10 s + 1). What do gain and time constant become when I close a unity negative feedback loop around it, and what is the biological analogue?

A good answer: closed-loop gain K/(1 + K) = 0.8, time constant τ/(1 + K) = 2 instead of 10, and a
steady-state error of 0.2 of the set point. Negative feedback speeds the response and reduces sensitivity
to parameter changes, as in end-product inhibition or autorepression.

## 4. Second-order response

> A system has natural frequency 2 rad per unit time and damping ratio 0.3. What overshoot and settling time should I expect?

A good answer: overshoot about 37 percent (exp(−πζ/√(1−ζ²))), peak time about 1.65, and a 2 percent
settling time of about 6.7 (4/(ζ ωn), a rule of thumb). It notes that these formulas assume an
underdamped second-order system without zeros.

## 5. Feed-forward loops

> What is the difference between a coherent and an incoherent feed-forward loop, and what does each do in gene regulation?

A good answer: in a coherent loop, the direct and indirect paths have the same sign. With AND logic it
filters out brief input pulses (a sign-sensitive delay, or persistence detection). In an incoherent loop
the signs are opposite, which can generate a pulse, speed the response, or give adaptation and fold-change
detection.
