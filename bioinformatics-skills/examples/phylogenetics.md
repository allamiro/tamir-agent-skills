# `phylogenetics`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Compute the p-distance and the Jukes-Cantor distance between ACGTACGTAC and ACGTACGTAA. Say when the Jukes-Cantor correction stops being usable.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 917 | 1,094 |
| Input tokens read across all turns (including cached context) | 30,374 | 35,665 |
| Extra input tokens when the skill is installed | | +5,290 |
| Cost, US dollars at list price | 0.078 | 0.124 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 210 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# p-distance and Jukes-Cantor distance

The two sequences are the same length and have no gaps, so they line up position by position with no alignment step:

```
ACGTACGTAC
ACGTACGTAA
         ^  position 10: C vs A
```

## p-distance

p = mismatches ÷ compared sites = 1 / 10 = **0.100**

## Jukes-Cantor distance

d = −(3/4) · ln(1 − (4/3)·p)
  = −0.75 · ln(1 − 0.13333)
  = −0.75 · ln(0.86667)
  = −0.75 · (−0.14310)
  = **0.1073 substitutions per site**

The corrected distance is a little larger than p. The correction adds back substitutions that happened but can't be seen, such as two changes at the same site or a change that reverted to the original base.

**This estimate is very uncertain.** With only 10 sites, the approximate standard error is √[p(1−p) / (n(1−4p/3)²)] ≈ √(0.09 / 7.51) ≈ **0.11**, about the same size as the distance itself. One mismatch more or fewer would change the answer a lot.

## When the Jukes-Cantor correction stops being usable

- **It is undefined when p ≥ 0.75.** The log argument 1 − 4p/3 becomes zero or negative. At p = 0.75 the sequences are no more similar than two random DNA sequences, which match at 1/4 of sites by chance. That is saturation, and the formula gives infinity or no value.
- **It is unreliable well before 0.75.** As p approaches 0.75, the variance grows as 1/(1−4p/3)², so small counting errors turn into very large distance errors. In practice, treat distances above about p ≈ 0.5 (d ≈ 0.82) with suspicion. At that point, use a slower-evolving marker, protein sequences, or a model-based method such as maximum likelihood.
- **Its assumptions may not hold.** Jukes-Cantor assumes equal base frequencies, the same rate for every type of substitution (no transition/transversion bias) and the same rate at every site. If those assumptions fail, it underestimates distance. Use K80, HKY or GTR, with gamma-distributed rates across sites, instead.
````

## Answer without the skill (excerpt)

````text
# p-distance and Jukes-Cantor distance

**Comparing the two sequences**

```
Seq1: A C G T A C G T A C
Seq2: A C G T A C G T A A
                        ^  position 10: C vs A
```

The sequences differ at 1 of 10 sites.

**p-distance**

p = differences / sites compared = 1 / 10 = **0.100**

**Jukes-Cantor distance**

d = −(3/4) · ln(1 − (4/3)·p)
  = −0.75 · ln(1 − 0.13333)
  = −0.75 · ln(0.86667)
  = −0.75 · (−0.14310)
  = **≈ 0.1073 substitutions per site**

The JC distance is a little larger than p. It adds back an estimate of hidden substitutions, such as two changes at the same site or a change that later reverted.

**When the Jukes-Cantor correction stops being usable**

- **It fails completely at p ≥ 0.75.** At that point 1 − (4/3)p ≤ 0, and the logarithm of zero or a negative number is undefined. The value 0.75 is the expected p between two unrelated random sequences with equal base frequencies. Such sequences are said to be saturated: they carry no signal about distance.
- **It becomes unreliable well before 0.75.** As p gets close to 0.75, d rises steeply toward infinity, and its variance grows quickly too:

  Var(d) ≈ p(1−p) / [n(1 − 4p/3)²]

  Small sampling errors in p then produce very large errors in d. In practice, JC estimates are usually treated as unreliable once p goes above about 0.5–0.6. With short sequences the safe range is even smaller.
- **This example has a caveat.** With only 10 sites, p = 0.1 is a very rough estimate. One more difference would change it by 0.1, so the 0.107 figure has a wide confidence interval.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
