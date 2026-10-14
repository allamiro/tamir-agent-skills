# `bioinformatics-review`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Review this analysis for errors that look fine: Methods: we tested 15,000 genes between 3 treated and 3 control samples with t-tests. Treated samples were sequenced in batch 1 and controls in batch 2. We report the 300 genes with p < 0.05 as significantly differentially expressed. Code is available on request.. State the claim in a falsifiable form, trace each number to a script and input, and give me findings ranked critical, major, minor or note, each with evidence, impact and a fix. Say what you could not check.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 3,399 | 3,624 |
| Input tokens read across all turns (including cached context) | 61,202 | 86,942 |
| Extra input tokens when the skill is installed | | +25,740 |
| Cost, US dollars at list price | 0.137 | 0.207 |
| Skills invoked in the sample run | none | `bioinformatics-review` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 250 tokens for its name and description, which are in every session where the skill is installed, and about 1,800 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Review: 3 vs 3 differential expression methods paragraph

**Scope:** I reviewed only the five-sentence methods paragraph you gave me. There were no code, data, accessions, figures or gene list, so none of the numbers could be traced to a script or rerun. I checked them by arithmetic and from the design alone.

**Overall verdict:** Not ready to publish. In this design, treatment and batch cannot be separated. The 300 "significant" genes are also fewer than the 750 you would expect if no gene changed at all. As written, the paragraph does not support any claim of differential expression.

---

## 1. The claim

**As written:** "300 genes are significantly differentially expressed" between treated and control.

**Falsifiable form:** "For each of the 300 named genes, mean expression differs between treated and control samples because of the treatment, at a stated false discovery rate (e.g. FDR < 0.05). Each difference has a stated direction and size. The claim is contradicted if (a) Benjamini–Hochberg adjustment leaves few or none of these genes below the threshold, (b) the genes are not recovered in a batch-balanced repeat, or (c) a comparable number of 'hits' appears when samples are grouped by batch alone, or when labels are permuted within the limits of the design."

As written, the claim cannot be falsified in a useful way. Any batch difference would satisfy it. That is the problem behind Finding C1.

## 2. Number tracing

| Number | Script | Input | Parameters | Status |
|---|---|---|---|---|
| 15,000 genes tested | none given | none given (no accession, no annotation or genome build) | filtering rule unknown: raw total or after removing low counts? | **Unverified** |
| 3 vs 3 samples | none | no sample sheet | — | **Unverified** |
| p < 0.05 | none | — | t-test type (Student or Welch), one- or two-sided, input scale (raw counts, CPM, log) all unknown | **Unverified** |
| 300 significant genes | none | — | no adjustment | **Unverified, and contradicted by arithmetic (see M1)** |

Traced to a source: 0 of 4 numbers.

## 3. Findings

### Critical

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
The working directory is empty and the code is only "available on request," so I couldn't trace any number to a script or input. This review is based only on the text.

## The claim in falsifiable form

> "Treatment changes the expression of ~300 specific genes. If you repeat the experiment with treatment and sequencing batch balanced, and apply proper false discovery rate control, most of those 300 genes will again differ between treated and control, in the same direction."

As written, the analysis can't test this claim. The design can't tell treatment apart from batch, and the statistics can't tell real hits apart from chance.

## Tracing the numbers

| Number | Claimed meaning | Script | Input | Status |
|---|---|---|---|---|
| 15,000 | Genes tested | none provided | none provided | Not traceable. Unclear if this is before or after filtering |
| 3 vs 3 | Biological replicates per group | none | no sample sheet | Not traceable. Biological or technical replicates? |
| p < 0.05 | Per-gene cutoff | none | none | Not traceable. Unadjusted |
| 300 | "Significant" genes | none | none | Not traceable. **Doesn't fit the other numbers (see M3)** |

## Findings

### Critical

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
