# `omics-data-analysis`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Analyse this expression matrix: 20,000 genes by 12 samples, with a sample sheet giving condition, batch and date. Before any differential test, check the design, run quality control and a PCA coloured by batch and by condition, and tell me what would make me stop.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 5,930 | 6,241 |
| Input tokens read across all turns (including cached context) | 198,748 | 188,388 |
| Extra input tokens when the skill is installed | | -10,360 |
| Cost, US dollars at list price | 0.255 | 0.319 |
| Skills invoked in the sample run | none | `omics-data-analysis` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 260 tokens for its name and description, which are in every session where the skill is installed, and about 2,200 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I couldn't analyse your data because there's no matrix or sample sheet in the working directory; it only contains a `.claude` folder. Please send the two files or their paths and I'll run everything below on them.

In the meantime I wrote the full pre-test script: `scratchpad/qc_design.py`. It has **not been run**. The system Python has no numpy, and the command to install packages and test it on simulated data wasn't approved. If you'd like it tested first, approve that install or tell me which Python or R environment to use.

Run it with:

```
python -I qc_design.py matrix.csv samples.csv outdir
```

## What the script does

**1. Design check (before looking at expression values)**
- Checks that sample names match between the matrix and the sheet.
- Prints condition × batch, condition × date and batch × date tables, plus Cramér's V for condition against batch.
- Counts biological replicates per condition. If any samples are technical replicates, tell me: they aren't independent and the counts would need redoing.
- Flags a date that holds only one condition, since date often acts as a hidden batch.

**2. Quality control**
- Missing values per sample.
- Whether the values look like raw counts or already-transformed data. Negative values mean someone has already logged or centred them.
- Library sizes and the number of genes detected per sample.
- log-CPM distribution boxplots.
- A sample correlation heatmap labelled with condition and batch.
- Outliers: samples whose mean correlation with the others is unusually low.
- The low-expression filter doesn't use condition labels, so it can't bias a later test.

**3. PCA**
- Uses the 2,000 most variable genes, centred per gene.
- Plots PC1 against PC2 coloured by batch, by condition and by date.
- Gives the R² of each of PC1–PC5 against each factor, which turns "PC1 is batch" into a number.

## What would make you stop

**Hard stops: don't run a differential test**
1. **Batch is perfectly confounded with condition**, for example 6 controls in batch A and 6 treated in batch B. Batch and condition can't be separated, and no correction method can fix this. The only fix is new samples that cross the batches.
2. **Fewer than 2 biological replicates in a group**, or "replicates" that are technical repeats of one sample. You can't estimate the variance.
3. **The sample sheet doesn't match the matrix** (missing, extra or mislabelled samples). Fix where the data came from first.
4. **The top PCs separate samples by batch or date, and condition is mixed inside those groups.** Find out what the batch is before testing. Never "correct" batch with ComBat and then test on the corrected data as if those samples were independent.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
I couldn't analyse anything yet because there's no data here. The working directory is empty: no expression matrix and no sample sheet. Please send me the two file paths, or put the files in this folder.

So you aren't waiting on me, I wrote a script that runs every check you asked for: `scratchpad/preflight_qc.py`. **I haven't run or tested it.** This machine has no pandas or R, and there was no data to try it on. To run it you'll need `pip install pandas numpy scipy matplotlib`, then:

```
python preflight_qc.py counts.tsv samples.tsv qc_out
```

## What the script does
1. **Sample identity:** checks that the matrix columns and the sample-sheet rows match exactly, and flags duplicated gene IDs and missing values.
2. **Value type:** guesses whether the values are raw counts, log values or TPM/normalised values. DESeq2 and edgeR need raw integer counts.
3. **Design:** prints condition × batch, condition × date and batch × date tables, plus Cramér's V (how strongly two labels are linked, from 0 to 1) and the number of replicates per condition.
4. **Sample QC:** library size and number of genes detected per sample, outlier scores, expression boxplots and a sample-to-sample correlation heatmap.
5. **PCA:** uses the 2,000 most variable genes after filtering out low-expression genes. It plots PC1 against PC2 three times, coloured by batch, by condition and by date. It also reports how much of each of the first five PCs is explained by each label (R²), so you aren't relying only on how the plot looks.
6. At the end it prints a list of every STOP, WARN and CHECK flag it raised.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
