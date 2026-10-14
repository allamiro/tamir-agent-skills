# `research-writing-reporting`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Write the methods section for this analysis from my methods record: Reads: SRR1234567 (3 treated, 3 control) aligned to GRCh38 with tool A v1.2; counts from tool B v3.1; differential test with Benjamini-Hochberg correction at 0.05; seed 42.. Use exact versions and parameters, and list anything the record does not give me so I can fill it in.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,034 | 2,002 |
| Input tokens read across all turns (including cached context) | 30,439 | 113,517 |
| Extra input tokens when the skill is installed | | +83,078 |
| Cost, US dollars at list price | 0.081 | 0.186 |
| Skills invoked in the sample run | none | `research-writing-reporting` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 2,300 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
Here's a draft that uses only what your record gives. Anything in **[brackets]** is missing from the record and you'll need to fill it in. I haven't added any defaults.

---

### Methods

**Data.** RNA-seq reads were obtained from [repository, e.g. NCBI SRA] under accession SRR1234567 [see problem 1 below; list the run accession for each sample], retrieved on [date]. The study had six samples: three treated and three control. [Organism, tissue or cell line, and what the treatment was (agent, dose, duration).] [Library type: single- or paired-end, read length, strandedness.]

**Read processing and alignment.** [Quality control and trimming tool, its version and parameters, or a statement that reads were not trimmed.] Reads were aligned to the human reference genome GRCh38 [assembly accession and patch, e.g. GCA_000001405.15 / p14; source such as Ensembl or GENCODE, and release; primary assembly or with alt contigs] using [real name of tool A] v1.2 with [all parameters, including any left at default]. [Mapping rate per sample.] [Duplicate handling.] [Excluded samples and the reason, or "No samples were excluded."]

**Quantification.** Reads per gene were counted with [real name of tool B] v3.1 against the [annotation source and release, e.g. GENCODE v44 GTF] annotation, with [counting parameters: feature type, how multimapping and overlapping reads were handled, strandedness setting].

**Differential expression.** Treated samples (n = 3) were compared with control samples (n = 3) using [test, tool and version, e.g. a negative binomial Wald test]. [Normalisation method.] [Model formula, including any covariates or batch term.] [Pre-filtering of low-count genes, and the number of genes tested.] P-values were adjusted with the Benjamini–Hochberg procedure. Genes with an adjusted p-value below 0.05 were called differentially expressed. [Effect size measure, e.g. log2 fold change, any shrinkage, and any fold-change threshold.] The random seed was set to 42 [say which step uses randomness].

**Software and code availability.** [Language and version, such as R or Python; environment file or container.] Code is available at [URL], version [tag or commit], archived at [DOI].

---

### Problems in the record

1. **The accession can't be right as written.** SRR1234567 is a single run accession, and one run is normally one sequencing run of one library. It can't hold six samples by itself. You probably need either six SRR accessions (one per sample) or a study or project accession (SRP or PRJNA) plus a table mapping each sample to its run. Please check this before submitting.
2. **"Tool A" and "tool B" are placeholders, not tool names.** I kept the versions (v1.2 and v3.1) exactly as recorded, but the real names are needed. Each tool should also be cited.
3. **The differential test isn't named.** The record gives the correction (BH at 0.05) but not the test, the tool that ran it, or its version.

### Missing from the record (fill-in checklist)

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Methods

**Read alignment and quantification.** We analysed RNA-seq reads from SRA accession SRR1234567, comprising six samples: three treated and three control. Reads were aligned to the human reference genome GRCh38 using tool A (v1.2) [parameters: ___]. Gene-level read counts were generated from the alignments with tool B (v3.1) [parameters and annotation: ___].

**Differential expression analysis.** We compared treated and control samples using [test/method: ___]. P-values were adjusted for multiple testing using the Benjamini–Hochberg procedure. Genes with an adjusted p-value below 0.05 were considered differentially expressed. The random seed was set to 42 [for: ___].

---

## Missing from your record

**Data provenance**
1. **Accession mismatch.** SRR1234567 is a single run accession, but you list six samples. Please give the per-sample run accessions (SRR…) or the BioProject/GEO series accession (PRJNA…/GSE…).
2. Library type: single- or paired-end, read length, and whether the library is stranded.
3. Sequencing platform and organism or sample source (cell line, tissue, etc.).

**Preprocessing**
4. Whether reads were quality-checked or trimmed, with tool, version and parameters. If they weren't, say so.

**Alignment**
5. The real name of tool A and its citation.
6. The GRCh38 build source and release, for example Ensembl release ___ or GENCODE v___, and whether the primary assembly or the full assembly with alt contigs was used.
7. Alignment parameters, or a statement that defaults were used.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
