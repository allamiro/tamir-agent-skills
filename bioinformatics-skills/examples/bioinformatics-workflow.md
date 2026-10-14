# `bioinformatics-workflow`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I have RNA-seq from treated and untreated cells, three replicates each, sequenced in two batches. Plan the analysis. State the claim so the data could show it false, name the null model, list what to record about the data, and say which skill handles each step.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,572 | 3,669 |
| Input tokens read across all turns (including cached context) | 30,390 | 113,463 |
| Extra input tokens when the skill is installed | | +83,073 |
| Cost, US dollars at list price | 0.111 | 0.220 |
| Skills invoked in the sample run | none | `bioinformatics-workflow` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 270 tokens for its name and description, which are in every session where the skill is installed, and about 2,400 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Analysis plan: treated vs untreated RNA-seq (3 vs 3, two batches)

Status: draft, not yet run. One thing decides whether this design can answer the question: **which samples went into which batch.**

- **Split across batches** (for example batch A = T1, T2, U1 and batch B = T3, U2, U3): batch can be estimated separately from treatment. Go ahead with the plan below.
- **Confounded** (all treated in one batch, all untreated in the other): the treatment effect and the batch effect cannot be separated, and no software can fix that. The honest options are to re-sequence with a split layout or to report the result as "treatment-or-batch". `experimental-design` handles the re-layout.

## 1. Claim

> In [cell line], [treatment] at [dose/time] changes the mRNA abundance of a set of genes compared with untreated cells, after accounting for sequencing batch. The change is a log2 fold change ≠ 0 at 5% FDR, and it points the same way in both batches.

If you expect specific genes or a pathway, add them to the claim (e.g. "...including upregulation of [target genes]"). A directional, named prediction is much easier to disprove than "something changes".

**These results would show the claim is false:**
- No genes pass 5% FDR, and the p-value histogram is flat (uniform).
- Genes pass when batch is left out of the model but disappear once batch is included. That means the "signal" was batch.
- The effects run in opposite directions in the two batches.
- Your pre-named target genes move the wrong way or not at all.

## 2. Null model

- **What "no signal" looks like:** for every gene, the treatment coefficient is 0 in a negative binomial GLM with design `~ batch + condition`. Counts vary only by library size, batch and biological dispersion.
- **How it is calculated:** a Wald or likelihood-ratio test per gene, then Benjamini–Hochberg across all tested genes.
- **Empirical check:** shuffle the treatment labels within batch and rerun. With 3 vs 3 there are only a handful of distinct relabelings, so this is a sanity check that shuffled labels give few hits. It is not a source of p-values (the smallest possible permutation p is too coarse).
- **Power:** the model has 6 samples and 3 parameters, so 3 residual degrees of freedom. You can expect to detect large effects in well-expressed genes. Write that limit down now, so that "nothing found" isn't later read as "no effect".

## 3. What to record about the data

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# RNA-seq analysis plan: treated vs. untreated, 3 vs. 3, two batches

## About the skills

None of my installed skills cover RNA-seq or statistics. The only one that fits a step here is **dataviz**, which handles the plots: PCA, MA, volcano and QC charts. The other steps use standard tools that I'd run directly (named below). I'm not going to make up skill names to fill the column.

## 0. First check: does batch overlap with treatment?

Before anything else, write down which samples went into which batch.

| Layout | What it means |
|---|---|
| All treated in batch 1, all untreated in batch 2 | **Batch and treatment can't be separated.** No statistical method can tell the treatment effect from the batch effect. Stop and re-sequence or re-design. |
| Each batch has both groups (e.g. 2T+1U / 1T+2U) | Fine. Model it as `~ batch + condition`. |

Adjusting for batch costs one degree of freedom. That leaves 6 − 3 = **3 residual df**, so the analysis only has power for fairly large effects. Say this in the write-up.

## 1. The claim, written so the data could prove it wrong

Write this down **before** looking at the results:

> "Treatment changes the expression of [named genes or a named pathway] by at least 1.5-fold (|log2FC| ≥ 0.585), after adjusting for batch, at FDR ≤ 0.05."

The claim is **false** if:
- the named genes' batch-adjusted log2FC confidence intervals include the region |log2FC| < 0.585, or
- the number of genes passing the threshold is no greater than what you get by permuting treatment labels within batch (see step 2).

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
