# `model-building-design`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Here is my model: dS/dt = -Vmax*S/(Km+S), dP/dt = Vmax*S/(Km+S). What assumptions does it make, and is S a variable or a parameter? Classify every quantity and fill in an assumption register.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,608 | 3,964 |
| Input tokens read across all turns (including cached context) | 30,398 | 114,218 |
| Extra input tokens when the skill is installed | | +83,820 |
| Cost, US dollars at list price | 0.112 | 0.224 |
| Skills invoked in the sample run | none | `model-building-design` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 250 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**S is a state variable, not a parameter.** It changes with time as the model runs, and it has its own differential equation. What you fix before each run is its **initial value S₀**, and that is a parameter (an initial condition). Vmax and Km are the parameters of the rate law.

You didn't state the purpose, so I've assumed an **in vitro enzyme assay**: a progress curve of substrate turning into product. Change the "why acceptable" column if your purpose is different, for example a step inside a cell model.

---

## 1. Quantities

| Symbol | Meaning | Class | Unit (example) | Notes |
|---|---|---|---|---|
| t | time | independent variable | min | |
| S(t) | substrate concentration | **state variable** | mM | has its own ODE |
| P(t) | product concentration | **state variable** (redundant) | mM | P = S₀ + P₀ − S, see below |
| S₀, P₀ | initial concentrations | parameters (initial conditions) | mM | set by the experimenter, so also inputs |
| Vmax | maximal rate | parameter (lumped) | mM/min | equals k_cat·E_T, so it hides two quantities |
| Km | Michaelis constant | parameter | mM | equals (k₋₁+k_cat)/k₁ under QSSA |
| E_T | total enzyme concentration | hidden parameter | mM | not in the equations, only inside Vmax |
| −1, +1 | stoichiometric coefficients | coefficients | dimensionless | assume 1 S → 1 P |
| v = Vmax·S/(Km+S) | reaction rate | derived quantity | mM/min | |
| measured S(t) or P(t) | what you compare with data | output | mM | |

**Dimension check:** Km + S is mM + mM, which is consistent. Vmax·S/(Km+S) comes out in mM/min, matching dS/dt. It passes.

**Structural point:** d(S+P)/dt = 0, so S + P = S₀ + P₀ for all time. The model is really one-dimensional, and P adds no independent dynamics.

## 2. Assumption register

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
## Short answer

**S is a state variable, not a parameter.** It changes over time and has its own equation (dS/dt). It also appears on the right-hand side, which makes the system nonlinear. The parameters are **Vmax** and **Km**. They are fixed for a given run and are what you would estimate from data.

## Classifying every quantity

| Symbol | Class | Role / units (typical) | Notes |
|---|---|---|---|
| t | Independent variable | time (s, min) | Everything else is a function of t |
| S(t) | State variable (dependent) | concentration (mM) | Substrate. It has its own ODE and feeds back into the rate |
| P(t) | State variable (dependent) | concentration (mM) | Product. It appears on no right-hand side, so it doesn't affect the dynamics and is fully determined by S |
| Vmax | Parameter | concentration/time (mM/min) | Maximum rate. It is really a composite, Vmax = k_cat·E₀ |
| Km | Parameter | concentration (mM) | The value of S at which the rate is Vmax/2. It is a composite, (k₋₁ + k_cat)/k₁ |
| S(0) = S₀ | Initial condition (parameter of the run) | mM | Needed to solve the system |
| P(0) = P₀ | Initial condition (parameter of the run) | mM | Usually 0 |
| v = Vmax·S/(Km+S) | Derived quantity / flux | mM/min | A function of the state, not an independent quantity |
| S + P | Conserved quantity (invariant) | mM | d(S+P)/dt = 0, so S + P = S₀ + P₀ for all t |
| k_cat, E₀, k₁, k₋₁ | Hidden (lumped) parameters | — | They are absorbed into Vmax and Km. The model can't identify them separately |

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
