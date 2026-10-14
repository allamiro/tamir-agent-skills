---
name: control-systems-feedback
description: Applies systems and control theory to biological networks, covering the black box concept, block diagrams, open versus closed loop, feedback and feed-forward loops, general system properties, state-space representation, SISO versus MIMO, classification of system types, Laplace and Fourier transforms, time versus frequency domain, transfer functions, poles and zeros, damping, the Routh-Hurwitz criterion, controllability and observability, and synthetic versus systems biology. Use for "draw the block diagram", "write my model in state-space form", "is this system controllable", "can I observe all states from this measurement", "what does negative feedback do here", "derive the transfer function", "is the characteristic polynomial stable". Use ode-dynamics for nonlinear simulation and stability, linear-algebra-networks for eigenvalues, and network-analysis for loop motifs in large networks.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Control systems and feedback

## Purpose and activation

Control theory describes how a system responds to inputs and how feedback shapes that response. In
biology it explains homeostasis (negative feedback), switches and memory (positive feedback), pulse
generation and noise filtering (feed-forward loops), and it asks practical questions: can a drug input
steer every state, and can a measurement reveal every state? Activate when the user works with
inputs, outputs, feedback, block diagrams, state space, transfer functions, or controllability.

## Required inputs

The system as equations or a diagram; the inputs (what can be manipulated), outputs (what is measured) and
states; whether the model is linear or linearised around a steady state; and the question.

## Workflow

1. **Draw the black box,** then open it: inputs, outputs, and the blocks between them. Mark each loop as
   positive or negative by multiplying the signs along it.
2. **Write the state-space form** dx/dt = A x + B u, y = C x + D u (linearise a nonlinear model at a steady state
   first; A is then the Jacobian). Classify: SISO or MIMO, linear or not, time-invariant or not, continuous or discrete.
3. **Controllability:** `python3 scripts/control.py ctrb "A" "B"`. Full rank of [B, AB, ..., A^(n-1) B] means
   the inputs can drive the state anywhere (Kalman).
4. **Observability:** `python3 scripts/control.py obsv "A" "C"`. Full rank means the measured outputs determine every state;
   if not, some states cannot be inferred from these measurements, which matters for experimental design.
5. **Transfer function:** Laplace-transform the linear model, G(s) = C (sI - A)^-1 B + D; poles and zeros with
   `python3 scripts/control.py tf "NUM" "DEN"`. Poles are the eigenvalues of A.
6. **Stability without roots:** `python3 scripts/control.py routh "COEFFS"`; the number of sign changes in the first
   column of the Routh array equals the number of roots with positive real part.
7. **Response shape:** for a second-order system, `python3 scripts/control.py second --wn --zeta` gives overshoot and
   settling time; damping ratio below 1 means oscillation.
8. **Feedback:** `python3 scripts/control.py loop --K --tau` shows how closing a unity negative feedback loop around
   K/(τs+1) lowers the gain to K/(1+K) and speeds the response by 1+K. Explain the biological analogue.

## Decision framework

| Circuit | Typical function | Cost or risk |
|---|---|---|
| Negative feedback | Homeostasis, faster response, robustness to parameter change | Oscillation with delay or high gain |
| Positive feedback | Bistable switch, memory, hysteresis | Irreversible commitment, noise-driven switching |
| Coherent feed-forward loop | Sign-sensitive delay, persistence detection | Slow response |
| Incoherent feed-forward loop | Pulse generation, fold-change detection, faster response | Partial adaptation only |
| Open loop | Simple, predictable | No correction of disturbances |

| Domain | Use for |
|---|---|
| Time domain | Transients, simulations, comparison with time-course data |
| Frequency domain (Laplace, Fourier) | Filtering, resonance, response to periodic inputs, loop stability margins |

## Failure and edge cases

- **Controllability of a linearisation** read as global controllability of the nonlinear system.
- **Structural versus numerical rank:** a matrix can be nearly rank-deficient; report the condition number.
- **Loop sign miscounted** in a long pathway (count the inhibitions).
- **Transfer functions for nonlinear models** without saying where they were linearised.
- **Synthetic biology designs assumed modular** when loading and retroactivity couple the parts.
- **Fourier analysis of short or uneven time series** without windowing.

## Validation

- `python3 scripts/control.py --selftest` passes.
- Poles of the transfer function equal the eigenvalues of A.
- The Routh count of unstable roots matches the roots found numerically.
- The closed-loop step response simulated with `ode-dynamics` matches the predicted gain and time constant.
- Falsifier: an output that, measured over time, reveals a state the observability test says is hidden.

## Expected output

The block diagram with loop signs; the state-space form and its classification; controllability and
observability results with their meaning for experiments or interventions; transfer function, poles, zeros
and stability; response characteristics; and the role of each feedback loop.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 3 (supplied text): black box,
  hysteresis, block diagram, synthetic versus systems biology, general system properties, open versus closed
  loop, feed-forward and feedback loops, state space, system classification, SISO versus MIMO, Laplace and
  Fourier transforms, time versus frequency domain, controllability, observability, transfer function,
  damping and characteristic polynomial are listed topics. Chapter text not seen
- Feed-forward loop functions: Alon 2007, doi:10.1038/nrg2102 (record checked 2026-10-15; content from author
  knowledge, VERIFY); control formulas: standard, author knowledge, VERIFY
- `references/loop-examples.md` gives biological examples, all illustrative
