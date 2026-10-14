# `quantities-units-balances`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Are my units consistent? My model has dC/dt = k1*C*E with C and E in mM, k1 = 1e6 per molar per second, and time in seconds. Convert k1 to per micromolar per second and per millimolar per second.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 771 | 926 |
| Input tokens read across all turns (including cached context) | 30,391 | 36,395 |
| Extra input tokens when the skill is installed | | +6,004 |
| Cost, US dollars at list price | 0.075 | 0.126 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 260 tokens for its name and description, which are in every session where the skill is installed, and about 1,700 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**No, not as written.** Your concentrations are in mM but k1 is in M⁻¹ s⁻¹. If you put the number 10⁶ into the model with mM concentrations, every rate comes out **1000× too fast**.

## The conversion

k1 = 10⁶ M⁻¹ s⁻¹. Because the concentration unit sits in the denominator, a bigger concentration unit gives a bigger number.

- **Per µM:** 1 M = 10⁶ µM, so 1 M⁻¹ = 10⁻⁶ µM⁻¹
 k1 = 10⁶ × 10⁻⁶ = **1 µM⁻¹ s⁻¹**
- **Per mM:** 1 M = 10³ mM, so 1 M⁻¹ = 10⁻³ mM⁻¹
 k1 = 10⁶ × 10⁻³ = **10³ mM⁻¹ s⁻¹**

## Dimension check with mM

dC/dt = k1 · C · E
[mM s⁻¹] = [mM⁻¹ s⁻¹] · [mM] · [mM] = mM s⁻¹ ✓

So with C and E in mM and time in s, use **k1 = 1000 mM⁻¹ s⁻¹**.

## Two things to check

1. **Sign:** dC/dt = +k1·C·E means C makes more of itself, which is autocatalytic. If C is a substrate that gets used up by E, the term should be −k1·C·E.
2. **Size:** 10⁶ M⁻¹ s⁻¹ is fast but plausible for a bimolecular rate. At mM concentrations the timescale is about 1/(k1·E) ≈ 1 ms when E = 1 mM, so the ODE may be stiff. Use a stiff solver (e.g. `solve_ivp(..., method="LSODA")` or `"BDF"`) if the run is slow or blows up.
````

## Answer without the skill (excerpt)

````text
**No, your units aren't consistent as written.** k1 is in M⁻¹s⁻¹, but C and E are in mM. If you plug in k1 = 1e6 directly, your rate comes out **1000× too fast**.

## Conversions

Start from k1 = 1×10⁶ M⁻¹s⁻¹. Because k1 has concentration in the denominator, a bigger concentration unit gives a bigger number.

**Per micromolar** (1 M = 10⁶ µM):

k1 = 10⁶ M⁻¹s⁻¹ × (1 M / 10⁶ µM) = **1 µM⁻¹s⁻¹**

**Per millimolar** (1 M = 10³ mM):

k1 = 10⁶ M⁻¹s⁻¹ × (1 M / 10³ mM) = **1×10³ mM⁻¹s⁻¹**

## Check with C and E in mM

dC/dt = k1 · C · E
→ (mM⁻¹s⁻¹)(mM)(mM) = mM/s ✓

So keep C and E in mM, set **k1 = 1000 mM⁻¹s⁻¹**, keep time in seconds, and dC/dt comes out in mM/s.

**Check the sign too:** if C is consumed by reacting with E, the equation should be dC/dt = −k1·C·E. The positive form makes C grow.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
