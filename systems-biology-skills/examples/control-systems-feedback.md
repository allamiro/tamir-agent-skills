# `control-systems-feedback`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> My linearised two-state model has A with rows (0, 1) and (-2, -3), input matrix B = (0, 1) and output C = (1, 0). Is the system controllable and observable? Give the transfer function, poles and steady-state gain.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 878 | 1,087 |
| Input tokens read across all turns (including cached context) | 30,392 | 36,400 |
| Extra input tokens when the skill is installed | | +6,008 |
| Cost, US dollars at list price | 0.077 | 0.130 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 310 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**Yes, the system is both controllable and observable.** The transfer function is G(s) = 1/((s+1)(s+2)), the poles are −1 and −2, and the steady-state gain is ½.

Model: A = [[0, 1], [−2, −3]], B = [0, 1]ᵀ, C = [1, 0], D = 0.

## Controllability
AB = [1, −3]ᵀ, so the controllability matrix is

  𝒞 = [B  AB] = [[0, 1], [1, −3]], with det 𝒞 = −1 ≠ 0.

It has rank 2, so the system is **controllable**.

## Observability
CA = [0, 1], so the observability matrix is

  𝒪 = [C; CA] = [[1, 0], [0, 1]], with det 𝒪 = 1 ≠ 0.

It has rank 2, so the system is **observable**. Because 𝒪 is the identity matrix, both states can be read directly from y and ẏ.

## Transfer function
det(sI − A) = s² + 3s + 2, and

  G(s) = C(sI − A)⁻¹B = **1 / (s² + 3s + 2) = 1 / ((s + 1)(s + 2))**

There are no zeros. Because the system is controllable and observable, this realisation is minimal: no poles cancel, and the transfer function shows all the internal dynamics.

## Poles
**s = −1 and s = −2.** These are the eigenvalues of A. Both are real and negative, so the system is asymptotically stable. Matching s² + 3s + 2 to the standard form s² + 2ζωₙs + ωₙ² gives ωₙ = √2 ≈ 1.41 rad per time unit and ζ = 3/(2√2) ≈ 1.06. Since ζ > 1, the system is **overdamped**: a step input gives no overshoot. The slow pole at −1 sets the timescale, with τ ≈ 1 time unit, so the output settles in about 4–5 time units.

## Steady-state gain
G(0) = −CA⁻¹B = **1/2**. A unit step in u brings y to 0.5.
````

## Answer without the skill (excerpt)

````text
The system is **controllable and observable**. Its transfer function is **G(s) = 1/((s+1)(s+2))**, the poles are at **−1 and −2**, and the steady-state gain is **0.5**. I've assumed there is no direct feedthrough term (D = 0).

**System**

A = [0 1; −2 −3], B = [0; 1], C = [1 0]

### Controllability
𝒞 = [B  AB] = [0 1; 1 −3]

det 𝒞 = −1 ≠ 0, so 𝒞 has rank 2. **The system is controllable.**

### Observability
𝒪 = [C; CA] = [1 0; 0 1]

det 𝒪 = 1 ≠ 0, so 𝒪 has rank 2. **The system is observable.**

### Transfer function
G(s) = C(sI − A)⁻¹B

sI − A = [s −1; 2 s+3], so det(sI − A) = s² + 3s + 2.

(sI − A)⁻¹B = [1; s] / (s² + 3s + 2), and multiplying by C picks out the first entry:

**G(s) = 1 / (s² + 3s + 2) = 1 / ((s+1)(s+2))**

### Poles
**s = −1 and s = −2.** These are the eigenvalues of A. Both are real and in the left half-plane, so the system is asymptotically stable and overdamped (ωₙ = √2, ζ = 3/(2√2) ≈ 1.06). Because the system is both controllable and observable, there are no pole-zero cancellations, and G(s) has no finite zeros.

### Steady-state (DC) gain
G(0) = 1/2 = **0.5**

The system is stable, so by the final value theorem a unit step input settles at y = 0.5. You get the same value from the state equations: setting ẋ = 0 gives x = −A⁻¹B·u = [0.5; 0]u, so y = 0.5u.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
