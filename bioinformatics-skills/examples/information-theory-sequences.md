# `information-theory-sequences`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> What is the Shannon entropy of the base composition of ACGTACGTAACCGGTT, and of its overlapping 2-mers? Give bits, the maximum possible in each case, and say how reliable the estimate is for a sequence this short.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,299 | 1,744 |
| Input tokens read across all turns (including cached context) | 30,387 | 86,905 |
| Extra input tokens when the skill is installed | | +56,518 |
| Cost, US dollars at list price | 0.106 | 0.163 |
| Skills invoked in the sample run | none | `information-theory-sequences` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 230 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
Per-base entropy is **2.00 bits**, which is the maximum. For overlapping 2-mers it is **2.82 bits out of a possible 4.00**. At this length the base result tells you almost nothing, and the 2-mer result is a rough estimate.

**Single bases (16 bases, 4-letter DNA alphabet)**
- Counts: A = C = G = T = 4, so all four bases are equally common.
- H = **2.00 bits per base**, and the maximum is log₂4 = **2 bits**.
- This means the composition is perfectly balanced. It does not mean the sequence is random: AAAACCCCGGGGTTTT would also give exactly 2 bits.

**Overlapping 2-mers (15 2-mers, 16 possible kinds)**
- Counts: AC 3, CG 3, GT 3, TA 2, AA 1, CC 1, GG 1, TT 1. Only 8 of the 16 kinds appear.
- H = **2.82 bits per 2-mer**, or 1.41 bits per base. The theoretical maximum is log₂16 = **4 bits**.
- With only 15 2-mers, the highest value this sequence could reach is log₂15 ≈ 3.91 bits, which needs all 15 to be different.
- The gap from the maximum reflects real word-level structure. The repeated ACGT gives AC, CG and GT three times each, and 8 kinds never appear at all.

**How reliable these numbers are**
- Both values come from simply plugging the observed frequencies into the formula. That kind of estimate is biased low when there are few observations.
- **Bases:** 16 observations for 4 kinds is just about enough to estimate the frequencies. But even a truly random 16-base sequence rarely comes out exactly 4/4/4/4, so getting exactly 2.00 is weak evidence of anything. With only 16 bases, each frequency has a sampling error of roughly ±0.1.
- **2-mers:** 15 observations for 16 possible kinds is fewer than one per kind, and you'd want several per kind. The 8 missing 2-mers may be missing by chance rather than because they are rare. A rough correction for this bias (Miller–Madow) adds about (8−1)/(2·15·ln2) ≈ 0.34 bits, giving roughly 3.2 bits. Even that is only a ballpark figure at this sample size.
- The overlapping 2-mers are not independent of each other, because each base sits in two of them. That makes the effective sample even smaller.
- **Baseline:** to decide whether 2.82 bits really shows structure, compare it with the 2-mer entropy of many shuffles of the same 16 bases. A sequence of a few hundred bases or more would be needed for the 2-mer estimate to be trustworthy.

Values were computed with the information-theory skill's `seqinfo.py` script, and I checked the 2-mer counts by hand.
````

## Answer without the skill (excerpt)

````text
The base composition is perfectly even at 2.00 bits, which is the maximum. The overlapping 2-mers give about 2.82 bits against a maximum of 4. At 16 bases, both numbers are very rough estimates.

## 1. Base composition (1-mers)

ACGTACGTAACCGGTT has 16 bases: A = 4, C = 4, G = 4, T = 4. Each base has p = 0.25.

- **H₁ = −4 × 0.25 × log₂(0.25) = 2.000 bits**
- **Maximum = log₂ 4 = 2 bits.** The sequence reaches it exactly.

## 2. Overlapping 2-mers

There are 15 overlapping 2-mers: AC, CG, GT, TA, AC, CG, GT, TA, AA, AC, CC, CG, GG, GT, TT.

| 2-mer | AC | CG | GT | TA | AA | CC | GG | TT |
|---|---|---|---|---|---|---|---|---|
| count | 3 | 3 | 3 | 2 | 1 | 1 | 1 | 1 |

- **H₂ = 3·(0.2·log₂5) + 2·(2/15)·log₂7.5 + 4·(1/15)·log₂15 ≈ 1.393 + 0.388 + 1.042 = 2.823 bits**
- **Maximum = log₂ 16 = 4 bits.** With only 15 observations, no more than 15 distinct 2-mers can appear, so the most this sequence could reach is log₂ 15 ≈ 3.91 bits.
- Only 8 of the 16 possible dinucleotides appear. The other 8 never occur, including AG, CA, GA, TC and TG.
- The conditional entropy H₂ − H₁ ≈ 0.82 bits per base, compared with 2 bits for a random sequence. That reflects the ACGT repeat.

## 3. How reliable these estimates are

These are plug-in (maximum-likelihood) estimates, and the sample is far too small to trust them much.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
