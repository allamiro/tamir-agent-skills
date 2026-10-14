# `multivariate-omics`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Run a PCA on my omics data and tell me whether to scale: sample,g1,g2,g3 with rows s1 1,2,0.5; s2 2,4,0.4; s3 3,6,0.6; s4 4,8,0.5; s5 5,10,0.45.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,112 | 2,670 |
| Input tokens read across all turns (including cached context) | 61,270 | 167,487 |
| Extra input tokens when the skill is installed | | +106,218 |
| Cost, US dollars at list price | 0.112 | 0.218 |
| Skills invoked in the sample run | none | `multivariate-omics` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 300 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I ran the PCA both ways on your 5 samples × 3 genes. Both results are below, and my answer on scaling comes after them.

## Results

**Unscaled (centred only)**

| PC | Eigenvalue | Explained | Loadings (g1, g2, g3) |
|---|---|---|---|
| PC1 | 12.5 | 99.96% | 0.447, 0.894, 0 |
| PC2 | 0.0055 | 0.04% | 0, 0, 1 |
| PC3 | 0 | 0% | — |

**Scaled (each gene set to variance 1)**

| PC | Eigenvalue | Explained | Loadings (g1, g2, g3) |
|---|---|---|---|
| PC1 | 2 | 66.7% | 0.707, 0.707, 0 |
| PC2 | 1 | 33.3% | 0, 0, 1 |
| PC3 | 0 | 0% | — |

## What the data contains

- **g2 is exactly 2 × g1.** They carry the same information, which is why PC3 is exactly zero in both runs. In practice you have 2 independent variables, not 3.
- **g3 has no correlation with g1/g2.** Its covariance with g1 is exactly 0. It just varies a little around 0.49 (variance 0.0055, compared with 2.5 for g1 and 10 for g2).
- The samples spread out along PC1 in order s1 → s5. That trend is the g1/g2 increase.

## Should you scale?

The choice decides the story. Without scaling, g3 is invisible (0.04%). With scaling, g3 gets a full third of the variance. Which one is right depends on what g3's variation means:

- **Don't scale** if all three genes are on the same measurement scale (e.g., the same log-expression units). In that case g3's small spread is a real result: it barely changes across samples, and the unscaled PCA shows that correctly. Scaling would inflate what is probably measurement noise to the same weight as a 5-fold trend.
- **Scale** if the variables have different units or dynamic ranges, or if you care about relative patterns whatever their size. Scaling is the usual default for metabolomics/proteomics panels with mixed abundance ranges.

**My recommendation:** if these are expression values in common units, **don't scale**, or at most use Pareto scaling as a compromise. Whichever you pick, note two things:

1. **Remove or merge the redundant g2.** Because it duplicates g1, the scaled PCA counts the g1 trend twice. That is the only reason PC1 gets 66.7% rather than 50%.
2. **If these are raw intensities, log-transform first.** With logs, g2 = g1 + log 2, so after centring g1 and g2 become identical. Their unscaled variances then match, and much of the reason to scale goes away.

**Caveat:** 5 samples is very few. You can't tell whether g3's variation is biology or noise without replicates. Also check whether s1–s5 line up with batch or run order before reading PC1 as biology.
````

## Answer without the skill (excerpt)

````text
I couldn't run it here because numpy isn't installed, so I worked it out by hand. The data is small and has a simple structure, so the exact answer is easy to get.

## The data

| | g1 | g2 | g3 |
|---|---|---|---|
| mean | 3 | 6 | 0.49 |
| variance | 2.5 | 10 | 0.0055 |

- **g2 is exactly 2 × g1**, so their correlation is 1.
- **g3 has zero correlation with g1 and g2.** Its covariance with them is exactly 0. It's just small noise around 0.49.

## PCA without scaling (centered only)

| | Variance explained | Loadings (g1, g2, g3) |
|---|---|---|
| PC1 | **99.96%** | (0.447, 0.894, 0) |
| PC2 | 0.04% | (0, 0, 1) |
| PC3 | 0% | n/a |

PC1 scores for s1–s5: −4.47, −2.24, 0, 2.24, 4.47

g2 carries most of PC1 because it has 4× the variance of g1. g3 barely shows up.

## PCA with scaling (each gene set to unit variance)

| | Variance explained | Loadings (g1, g2, g3) |
|---|---|---|
| PC1 | **66.7%** | (0.707, 0.707, 0) |
| PC2 | **33.3%** | (0, 0, 1) |
| PC3 | 0% | n/a |

- PC1 scores: −1.79, −0.89, 0, 0.89, 1.79
- PC2 scores: 0.13, −1.21, 1.48, 0.13, −0.54

The signs of the components are arbitrary.

## Should you scale?

**It depends on what g3's variation means. The data alone can't tell you.**

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
