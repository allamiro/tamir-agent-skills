# `flux-balance-analysis`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Run flux balance analysis on this network to maximise R6, check whether the solution is unique with flux variability analysis, and say which reactions are essential: R1: -> A, R2: A -> B, R3: A -> C, R4: B -> D, R5: C -> 2 D, R6: D ->, with bounds R1 0 to 10 and R4 0 to 3.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,332 | 2,302 |
| Input tokens read across all turns (including cached context) | 73,273 | 170,526 |
| Extra input tokens when the skill is installed | | +97,253 |
| Cost, US dollars at list price | 0.127 | 0.208 |
| Skills invoked in the sample run | none | `flux-balance-analysis` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 270 tokens for its name and description, which are in every session where the skill is installed, and about 1,700 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
The maximum R6 flux is **20**, the optimal solution is unique, and only **R1 and R6 are strictly essential**. I ran this with the skill's exact simplex solver; its built-in self-test was not run.

**Problem:** maximise v6 subject to N·v = 0. R1 is bounded 0 to 10 and R4 0 to 3. The other reactions are irreversible with a default bound of 0 to 1000, which means effectively unbounded.

**FBA result:**

| Reaction | Flux |
|---|---|
| R1: → A | 10 |
| R2: A → B | 0 |
| R3: A → C | 10 |
| R4: B → D | 0 |
| R5: C → 2 D | 10 |
| R6: D → | **20** |

All of A goes through the C branch because each A gives 2 D that way, against 1 D through B. Written out, v6 = v2 + 2·v3 with v2 + v3 = v1 ≤ 10, so v6 = 20 − v2, which is largest when v2 = 0. The cap on R4 never comes into play at the optimum.

**FVA at 100% of the optimum:** every flux range has zero width (R1 [10,10], R2 [0,0], R3 [10,10], R4 [0,0], R5 [10,10], R6 [20,20]). There are no alternative optima, so this flux distribution is the only one that gives R6 = 20.

**Single-reaction knockouts:**

| Knockout | Max R6 | Verdict |
|---|---|---|
| R1 | 0 | **Essential** (the only source of A) |
| R6 | 0 | **Essential** (it is the objective) |
| R3 or R5 | 3 | Not essential, but R6 drops by 85%. Flux goes through R2 → R4, which is limited to 3. |
| R2 or R4 | 20 | Not needed: they carry no flux at the optimum. |

Under a stricter definition, such as "R6 falls below some fraction of the wild-type value", R3 and R5 would also count as essential.

The result depends entirely on the R1 uptake limit: R6 = 2 × R1 as long as the C route is open.
````

## Answer without the skill (excerpt)

````text
I couldn't run a solver because numpy and scipy aren't installed here. The network is small enough to solve exactly by hand, so these results are derived, not computed.

**Assumptions:** every reaction is irreversible. R1 is bounded 0 to 10 and R4 is bounded 0 to 3. All other reactions are bounded 0 to ∞.

## Steady-state constraints
- A: R1 = R2 + R3
- B: R2 = R4, so R2 ≤ 3
- C: R3 = R5
- D: R6 = R4 + 2·R5 = R2 + 2·R3

## FBA (maximise R6)
R6 = R2 + 2·R3 = R1 + R3. To make this as large as possible, R1 goes to its maximum of 10 and all of A goes through R3.

| Reaction | Flux |
|---|---|
| R1 | 10 |
| R2 | 0 |
| R3 | 10 |
| R4 | 0 |
| R5 | 10 |
| **R6** | **20** |

## FVA at the optimum (R6 fixed at 20)
If R6 = 20, then R1 + R3 = 20. Since R3 ≤ R1 ≤ 10, both R1 and R3 must equal 10, which forces R2 = 0. That gives every flux a minimum equal to its maximum:

| Reaction | Min | Max |
|---|---|---|
| R1 | 10 | 10 |
| R2 | 0 | 0 |
| R3 | 10 | 10 |
| R4 | 0 | 0 |
| R5 | 10 | 10 |
| R6 | 20 | 20 |

**The optimal solution is unique.** Every flux range has zero width. Each unit of A sent through R2 gives 1 D, while each unit sent through R3 gives 2 D. So the B branch is never used at the optimum, even though R4's cap of 3 would allow some flux there.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
