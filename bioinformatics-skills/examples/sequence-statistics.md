# `sequence-statistics`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> How many sequences of length 2 are possible from 4 letters? Give the four counts: ordered or unordered, with or without replacement.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 366 | 466 |
| Input tokens read across all turns (including cached context) | 30,355 | 35,639 |
| Extra input tokens when the skill is installed | | +5,284 |
| Cost, US dollars at list price | 0.067 | 0.111 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 240 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
With n = 4 letters (for example A, C, G, T) and length k = 2:

| | With replacement | Without replacement |
|---|---|---|
| **Ordered** | 4² = **16** | 4 × 3 = **12** |
| **Unordered** | C(4+2−1, 2) = C(5,2) = **10** | C(4,2) = **6** |

- **Ordered, with replacement (16):** each of the 2 positions can be any of the 4 letters. These are all the DNA dinucleotides (AA, AC, …, TT).
- **Ordered, without replacement (12):** the 16 above minus the 4 that repeat a letter (AA, CC, GG, TT).
- **Unordered, without replacement (6):** the 12 ordered pairs counted once each, since AC and CA are the same pair. So 12 ÷ 2 = 6.
- **Unordered, with replacement (10):** the 6 unordered pairs plus the 4 same-letter pairs.

**Which one to use:** a sequence like DNA is ordered and allows repeated letters, so the answer for sequences is **16**.
````

## Answer without the skill (excerpt)

````text
With n = 4 letters and length k = 2:

| | With replacement | Without replacement |
|---|---|---|
| **Ordered** | nᵏ = 4² = **16** | n!/(n−k)! = 4·3 = **12** |
| **Unordered** | C(n+k−1, k) = C(5,2) = **10** | C(n, k) = C(4,2) = **6** |

Example with letters {A, B, C, D}:
- **Ordered, with replacement (16):** AA, AB, BA, … — every pair, repeats allowed.
- **Ordered, without replacement (12):** AB, BA, AC, CA, … — no repeated letters.
- **Unordered, without replacement (6):** AB, AC, AD, BC, BD, CD.
- **Unordered, with replacement (10):** the 6 above plus AA, BB, CC, DD.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
