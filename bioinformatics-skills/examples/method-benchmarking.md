# `method-benchmarking`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> A new variant caller scores 0.83 accuracy against 0.81 for the established one on my 200-item test set. Is that a real improvement? Tell me what the test could detect at all and what I would need.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,109 | 2,326 |
| Input tokens read across all turns (including cached context) | 30,375 | 114,783 |
| Extra input tokens when the skill is installed | | +84,408 |
| Cost, US dollars at list price | 0.102 | 0.187 |
| Skills invoked in the sample run | none | `method-benchmarking` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 270 tokens for its name and description, which are in every session where the skill is installed, and about 2,600 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**No. This test can't show it.** On 200 items, 0.83 vs 0.81 means the new caller got 4 more items right (166 vs 162). That gap is well within what chance produces.

## What a 200-item test can detect

- **Smallest detectable difference:** about **11 points** (0.81 vs about 0.92), at 80% power and α = 0.05. Your gap is 2 points, about a fifth of that.
- **Paired test (McNemar):** both callers ran on the same items, so the right test uses only the items where they disagree. Even in the best case, where the new caller wins all 4 disagreements and loses none, p = 0.125. More realistic splits are much weaker: 10 wins vs 6 losses gives p = 0.45, and 20 vs 16 gives p = 0.62. Count your actual disagreements and run `benchstats.py mcnemar --b <old right, new wrong> --c <old wrong, new right>`.
- **Chance alone:** if two equally good callers are scored on 200 items, the better-looking one is ahead by about 1.6 points on average. Your 2-point lead is about that size.

## Test size needed to detect a 2-point gain

| Test items | Smallest detectable gap (unpaired) |
|---|---|
| 200 | 0.110 |
| 1,000 | 0.049 |
| 2,000 | 0.035 |
| ~6,000 | 0.020 |

A paired design needs fewer items. How many depends on how often the callers disagree: if they disagree on about 10% of items, roughly 2,000 items would detect a 2-point gain. Two cheap ways to get that many: score every truth-set variant site, not a 200-item sample, and use the GIAB benchmark regions.

## Beyond test size

1. **Use better metrics than accuracy.** For variant calling, report precision, recall and F1 separately for SNVs and indels (e.g. hap.py/vcfeval against GIAB truth sets). A caller can gain accuracy by trading recall for precision, and that trade may not suit your use.
2. **Test on several samples, not one.** Use more than one sample (e.g. several GIAB genomes), and if possible more than one sequencing platform or coverage depth. Treat each sample as one unit and report the paired difference with a confidence interval across samples. Many sites from one genome are not independent evidence.
3. **Break results down by region type.** Look at easy regions, homopolymers, segmental duplications and low-mappability regions separately. A real gain is often concentrated in one of these, or one caller collapses in one.
4. **Tune both callers the same way.** Give them the same filtering effort and thresholds, set on data kept apart from the test set. Pin versions and use the same compute limits.
5. **Count failures.** Sites the caller crashed on or didn't call count as errors, not as missing values.

**What you can claim now:** "No detectable difference on this test set; 200 items can only detect gaps of about 11 points or more."
````

## Answer without the skill (excerpt)

````text
# No. Your test can't tell these two callers apart.

## Your result

0.83 vs 0.81 on 200 items is 166 vs 162 correct, a net difference of **4 calls**.

- **If you treat the two runs as independent samples:** the standard error of the difference is about 0.038, so the 95% CI for the gap is about **−5.5 to +9.5 points**. That range easily includes zero, and it also includes the new caller being worse.
- **If you compare both callers on the same 200 items (McNemar test):** only the items where they disagree matter. Even in the best case, where they disagree on just 4 items and the new caller wins all 4, the exact two-sided p is 2 × 0.5⁴ = **0.125**. A net gain of 4 can never reach p < 0.05 with any split. A more realistic split, such as winning 12 and losing 8, gives p ≈ 0.5.

## The smallest difference n=200 can detect (80% power, α=0.05)

| Design | Detectable gap |
|---|---|
| Independent samples, ~82% accuracy | **~11 points** |
| Paired, callers disagree on 10% of items | ~6 points |
| Paired, callers disagree on 5% of items | ~4–5 points |

A 2-point gain is well below all of these. A non-significant result here is not evidence that the callers are equal either. The test simply has almost no power at this effect size.

## Sample size needed to detect a real 2-point gain (80% power)

| Design | Items needed |
|---|---|
| Independent samples | ~5,800 per caller |
| Paired, 5% disagreement | ~1,000 |
| Paired, 10% disagreement | ~2,000 |
| Paired, 20% disagreement | ~3,900 |

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
