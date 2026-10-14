# `experimental-design`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I want to compare treated and untreated cells and expect a difference of half a standard deviation. How many samples per group do I need at 80% power, and what changes if I will test 20,000 genes?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,877 | 1,532 |
| Input tokens read across all turns (including cached context) | 30,373 | 138,320 |
| Extra input tokens when the skill is installed | | +107,947 |
| Cost, US dollars at list price | 0.097 | 0.178 |
| Skills invoked in the sample run | none | `experimental-design` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 190 tokens for its name and description, which are in every session where the skill is installed, and about 2,100 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
For one comparison you need **about 64 samples per group (128 in total)**. Across 20,000 genes with Bonferroni correction, that rises to **about 252 per group (504 in total)**.

These figures assume a two-sided test, α = 0.05, 80% power and an effect of d = 0.5 (the difference in means divided by the standard deviation). I calculated them with the normal approximation plus a small-sample correction.

### One test
- **64 per group.** This matches the standard table value for d = 0.5.

### 20,000 genes
- **Bonferroni:** the per-gene threshold becomes 0.05 / 20,000 = 2.5 × 10⁻⁶. That needs **about 252 per group**, roughly four times as many.
- **If you stay at 64 per group:** a gene with a true 0.5-SD difference would be detected only about **3% of the time** after correction (my hand calculation). Nearly every real effect would be missed.
- **False discovery rate (Benjamini–Hochberg):** this is what most expression studies use, and it is less strict. The required n depends on how many genes truly change. If about 1% (200 genes) do, you need very roughly **150 per group** (also a hand estimate). The fewer real changes there are, the closer you get to the Bonferroni number.

### Things that change the answer more than the formula does
1. **Count what an independent sample is.** If "cells" means single cells or wells from one culture, those are not independent samples. The unit should be the biological replicate: separate cultures, passages or donors. Pseudoreplication is the most common way a study like this goes wrong.
2. **Check whether d = 0.5 is realistic.** In expression data the size of the change varies a lot from gene to gene. A d of 0.5 is modest, and an estimate taken from a small pilot that looked significant is usually too large.
3. **RNA-seq counts aren't normally distributed.** For counts, treat these numbers as a rough guide. Confirm with a count-based power tool such as RNASeqPower, PROPER or ssizeRNA, which models depth and dispersion.
4. **Pairing helps.** If each treated sample has a matched control (same donor or same passage), a paired design can cut the required n a lot.
5. **Balance batches.** Put treated and control samples in every extraction and sequencing batch, never one condition per batch. Add a margin of 10–20% for samples lost to QC.

A practical approach: decide on FDR control in advance and estimate the dispersion from a small pilot. Then size the study with a count-based tool, using these numbers as bounds: 64 per group for one test and about 252 under Bonferroni.
````

## Answer without the skill (excerpt)

````text
# Sample size for d = 0.5 at 80% power, with and without 20,000 genes

**For one comparison, you need about 64 samples per group.** That assumes a two-sample t-test, a two-sided α of 0.05, and an effect size d = 0.5.

The approximate formula is n per group ≈ 2(z₁₋α/₂ + z₁₋β)² / d² = 2(1.96 + 0.84)² / 0.25 ≈ 63. A small correction for using the t distribution brings it to 64.

## Testing 20,000 genes

When you test 20,000 genes, about 1,000 would be "significant" at p < 0.05 by chance alone. You have to correct for this, and the correction lowers the p-value cutoff each gene must pass. That raises the sample size a lot.

| Multiple-testing approach | Per-gene α | n per group |
|---|---|---|
| None (single test) | 0.05 | ~64 |
| FDR 5%, ~10% of genes truly changed | ~0.005 | ~109 |
| FDR 5%, ~1% of genes truly changed | ~0.0004 | ~153 |
| Bonferroni (family-wise error rate 5%) | 2.5 × 10⁻⁶ | ~248 |

- **Bonferroni** keeps the chance of even one false positive at 5%. It is very strict, and it needs about 4 times as many samples as a single test.
- **FDR (Benjamini–Hochberg)** is the usual choice for genomics. It accepts that about 5% of your hits may be false. The cutoff it uses depends on what fraction of genes are truly changed (π₁). I estimated that cutoff from α ≈ q·π₁·power / ((1−q)(1−π₁)), with q = 0.05. The fewer genes that truly change, the more samples you need.
- "80% power" now means you detect about 80% of the truly changed genes that have d = 0.5. It is no longer about one specific gene.

## Practical caveats

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
