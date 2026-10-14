# `experimental-design`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I want to compare treated and untreated cells and expect a difference of half a standard deviation. How many samples per group do I need at 80% power, and what changes if I will test 20,000 genes?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,113 | 2,149 |
| Input tokens read across all turns (including cached context) | 72,557 | 151,375 |
| Extra input tokens when the skill is installed | | +78,818 |
| Cost, US dollars at list price | 0.118 | 0.194 |
| Skills invoked in the sample run | none | `experimental-design` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 190 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
For one test you need **64 independent samples per group (128 in all)**. If you test 20,000 genes with a Bonferroni correction, you need **about 252 per group (504 in all)**. If you control the false discovery rate instead, which is what most expression studies do, the number falls somewhere in between.

## One comparison

These assumptions give 64 per group:
- standardized difference d = 0.5
- two-sided α = 0.05
- 80% power
- a two-sample t-test

## 20,000 genes

With 20,000 tests, a 5% threshold per gene would give about 1,000 false positives by chance alone. You have to correct for this, and the correction raises the bar each gene must clear.

| Correction | Per-gene threshold | n per group for 80% power at d = 0.5 |
|---|---|---|
| None (one test) | 0.05 | 64 |
| Bonferroni, family-wise error 5% | 0.05 / 20,000 = 2.5 × 10⁻⁶ | ~252 |
| Benjamini–Hochberg, FDR 5% | depends on how many genes truly change | roughly 100–150 (rough estimate) |

- **If you keep 64 per group,** power per gene under Bonferroni drops to about **3%**. You would miss almost every real effect of that size.
- **FDR control is the usual choice for genome-wide screens.** Its effective threshold depends on what fraction of genes truly change and on power, so there is no single formula for it. As a rough guide, if about 5% of genes change by d = 0.5, the threshold works out to around 10⁻³, which needs about 125 per group.
- **The trade-off:** with a fixed budget you either accept lower power per gene, or you target larger effects. At d = 1.0 the Bonferroni case needs only about 70 per group.

## Before you rely on these numbers

1. **Count independent samples, not cells.** A replicate is an independent culture, passage, donor or animal, meaning something that could have turned out differently by chance. Many cells or wells from one culture are technical replicates. Counting them as samples is pseudoreplication, and it makes the study look much more powerful than it is.
2. **For RNA-seq, check the number with a count-based tool.** These figures assume a t-test on continuous data. Read counts are usually planned in terms of fold change, dispersion and sequencing depth, with tools such as RNASeqPower, PROPER or ssizeRNA. Effect sizes also differ from gene to gene, so a single d is a simplification.
3. **Find a source for d = 0.5.** Use a pilot or published data. An effect taken from a small pilot that happened to look significant is usually an overestimate.
4. **Avoid confounding with batch.** Put treated and untreated samples into every processing batch and sequencing lane. Never run one condition per day or per lane.
5. **Allow for dropout.** Add 10–20% for samples that fail quality control.

The 64 and 252 figures come from a normal approximation with a small-sample correction; the script's self-test passed. The FDR figures and the 3% and ~70 figures are my own back-of-envelope estimates. If you tell me your assay (bulk RNA-seq, qPCR, etc.), expected fold change, number of batches and budget, I can work out a concrete design and batch layout.
````

## Answer without the skill (excerpt)

````text
For a single comparison you need **64 samples per group**. If you test 20,000 genes, that rises to roughly **110–250 per group**, depending on how you correct for multiple testing.

## One test (two-sample t-test, d = 0.5, two-sided α = 0.05, 80% power)

**n = 64 per group**, or 128 in total. This is the standard Cohen value: the normal approximation gives 62.8, and the t-distribution correction rounds it up to 64.

## Testing 20,000 genes

If you use α = 0.05 for every gene, you would expect about 1,000 false positives by chance alone. You need to correct for that, and the correction you choose sets the sample size:

| Correction | Per-gene α | n per group |
|---|---|---|
| None | 0.05 | 64 |
| FDR 5%, about 10% of genes truly change | ≈ 0.0047 | **≈ 110** |
| FDR 5%, about 1% of genes truly change | ≈ 0.0004 | **≈ 155** |
| Bonferroni / family-wise error rate (FWER) 5% | 2.5 × 10⁻⁶ | **≈ 250** |

- **Bonferroni:** this controls the chance of even one false positive, so it is very strict. It roughly quadruples the sample size.
- **FDR (Benjamini–Hochberg):** this is the usual choice for genomics. The per-gene α it implies depends on how many genes really change, so the sample size does too. I used the approximation α* ≈ q·π₁·power / ((1−q)·π₀). Here q is the FDR level, π₁ is the fraction of genes that truly change and π₀ = 1 − π₁. The more genes that truly change, the cheaper the correction.
- **80% power now means something different:** it is the average proportion of truly changed genes that you detect. It no longer means the chance of detecting one particular effect.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
