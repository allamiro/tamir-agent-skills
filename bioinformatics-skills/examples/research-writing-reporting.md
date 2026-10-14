# `research-writing-reporting`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Write the methods section for this analysis from my methods record: Reads: SRR1234567 (3 treated, 3 control) aligned to GRCh38 with tool A v1.2; counts from tool B v3.1; differential test with Benjamini-Hochberg correction at 0.05; seed 42.. Use exact versions and parameters, and list anything the record does not give me so I can fill it in.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,059 | 2,030 |
| Input tokens read across all turns (including cached context) | 30,441 | 99,634 |
| Extra input tokens when the skill is installed | | +69,194 |
| Cost, US dollars at list price | 0.081 | 0.178 |
| Skills invoked in the sample run | none | `research-writing-reporting` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 250 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
## Methods (draft)

Every value below comes from your record. Anything in **[brackets]** is something the record doesn't give, so you'll need to fill it in.

### Data

Sequencing reads were obtained from the NCBI Sequence Read Archive (SRA), accession **SRR1234567** [see gap 1: one run accession can't hold six samples; list the accession for each sample], retrieved **[date]**. The dataset contains six samples of **[organism, presumably *Homo sapiens*]**: three treated and three control. **[Describe the treatment, the cell line or tissue, and whether these are biological or technical replicates.]** Library type: **[single-end or paired-end, read length, stranded or unstranded, poly-A or rRNA-depleted]**.

### Processing

**[Read QC and trimming tools, versions and parameters, or say that none were run.]** Reads were aligned to the human reference genome GRCh38 (**[source and release, e.g. GENCODE vX / Ensembl rX; primary assembly or with alt contigs]**) with **tool A v1.2** (**[non-default parameters; say "default parameters" if none were changed]**). **[n of n reads (%) mapped per sample.]** **[Duplicate handling: marked, removed, or neither.]** **[Exclusion criteria and any samples excluded, or "no samples were excluded".]**

### Quantification and differential analysis

Read counts per **[gene / transcript]** were generated with **tool B v3.1** against **[annotation file and release]** (**[parameters: strandedness, how multi-mapping reads were handled, feature type]**). **[Filter for low-count features, if any.]** Differential expression between treated (n = 3) and control (n = 3) samples was tested with **[test and package, with version, e.g. a negative binomial Wald test in package X vX]** using **[model design, e.g. ~ condition, plus any covariates]**. **[Number of features tested]** p-values were adjusted with the Benjamini–Hochberg procedure, and features with adjusted p < 0.05 are reported as differentially expressed. Effect sizes are given as **[log2 fold change, with or without shrinkage (state the method), and with what interval]**. Random steps used seed 42 **[say which steps were random]**.

### Software and code

Analyses were run with **[language and version]**, and package versions are listed in **[environment file]**. Code is available at **[URL]**, version **[tag or commit]**, archived as **[DOI]**.

### Statistics at a glance

| Item | Value |
|---|---|
| Independent samples per group | 3 treated, 3 control **[confirm these are biological replicates]** |
| Number of tests | **[fill]** |
| Correction | Benjamini–Hochberg |
| Threshold | adjusted p < 0.05 |
| Seed | 42 |

---

## What the record leaves out

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
## Methods

### RNA-seq read alignment and quantification

Sequencing reads (accession SRR1234567; n = 6 samples, 3 treated and 3 control) were aligned to the human reference genome GRCh38 [**patch release / source, e.g., GENCODE/Ensembl release**] using tool A v1.2 [**alignment parameters**]. Gene-level read counts were generated with tool B v3.1 [**counting parameters; annotation file and version**].

### Differential expression analysis

Differential expression between treated and control samples was tested using [**statistical test / package and version**] [**model design, normalization method, filtering of low-count genes**]. P-values were adjusted for multiple testing using the Benjamini–Hochberg procedure. Genes with an adjusted p-value < 0.05 were considered differentially expressed [**plus any fold-change threshold**]. The random seed was set to 42 [**state which step uses randomness**].

---

### What the record doesn't give you

**Check these first (the record may be inconsistent):**
1. **Accession vs. sample count.** SRR1234567 is one run accession, but the record lists 6 samples. Check whether this should be a BioProject/SRP/GEO series accession, or a list of six SRR IDs.
2. **Tool names.** "Tool A" and "tool B" look like placeholders. You need the real software names (e.g., STAR, HISAT2, featureCounts, HTSeq) plus citations.
3. **Differential test.** The record names the correction method but not the test or package (e.g., DESeq2 Wald test, edgeR QL F-test, limma-voom) or its version.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
