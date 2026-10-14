# `bioinformatics-learning-path`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I am a biologist with no programming. I have 6 hours a week for 12 weeks and want to analyse my own sequencing data at the end. Plan it, with a goal I can test at the end of each stage.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 3,493 | 3,931 |
| Input tokens read across all turns (including cached context) | 30,378 | 100,351 |
| Extra input tokens when the skill is installed | | +69,973 |
| Cost, US dollars at list price | 0.129 | 0.223 |
| Skills invoked in the sample run | none | `bioinformatics-learning-path` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 210 tokens for its name and description, which are in every session where the skill is installed, and about 1,800 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# 12-week plan: from no programming to analysing your own sequencing data

**Total time:** 72 hours. Three 2-hour sessions a week works better than one 6-hour block.
**Approach:** learn only what your own data needs. The route goes from files, to the command line, to R and statistics, to a practice run on public data, and then to your own data.
**Main risk:** following tutorials without checking anything. So each stage ends with a test that has a known answer. If you can't pass it, repeat the stage before going on.

One thing changes weeks 7–12: **what kind of sequencing data do you have?** For example RNA-seq, whole-genome or variant data, 16S/amplicon, ChIP/ATAC, or single-cell. I've written those weeks for bulk RNA-seq, the most common case. Tell me your data type and I'll adapt them.

---

## Stage 0 — Week 1: Your question and your data (6 h)
- Write one paragraph covering: the biological question, the result you expect, and **the result that would show you were wrong**.
- Make a sample sheet as a spreadsheet. One row per sample, with columns for condition, replicate, sequencing date or batch, and file name.
- Get your files from the sequencing facility, with their checksums (md5). Keep an untouched copy that you never edit.
- Set up your tools: a terminal (built in on Mac), plus R and RStudio.
- Start a **logbook**, a plain text file where you record what you ran, which software versions, and any mistakes.

**Test:** Someone else can read your sample sheet and see whether condition and batch are confounded. For example, if all controls were sequenced on one day and all treated samples on another, the two can't be separated. If they are confounded, find out now. No analysis can fix it later.

## Stage 1 — Weeks 2–3: Command line and file formats (12 h)
- **Shell basics:** `cd`, `ls`, `head`, `less`, `wc`, `grep`, `zcat`, pipes (`|`), and `md5sum`/`md5`. The Software Carpentry "Unix Shell" lesson is free and covers these.
- **File formats:**
  - FASTQ: 4 lines per read; Phred+33 quality scores, where `I` = Q40 and `#` = Q2.
  - FASTA.
  - SAM/BAM: FLAG and CIGAR fields.
  - BED (0-based) versus GFF (1-based) coordinates.

**Test (work these out by hand first, then check):**
1. Count the reads in one of your FASTQ files: `zcat file.fastq.gz | wc -l`, then divide by 4. Does it match the facility's report?
2. Verify your checksums against the facility's list.
3. BED interval 2–5 in 1-based closed coordinates. Answer: **3–5**.
4. What does SAM FLAG 99 mean? Answer: paired, properly aligned, mate on the reverse strand, first in pair.
5. A read at POS 100 with CIGAR `5S10M3D10M2S`: where does it end on the reference? Answer: **122**.

## Stage 2 — Weeks 4–6: R and the statistics you'll need (18 h)
- **R:** vectors, data frames, reading a CSV, `ggplot2` plots, installing Bioconductor packages. The Data Carpentry "R for ecologists/genomics" lessons cover these.
- **Statistics:**
  - What a p-value is.
  - Why testing 20,000 genes needs multiple-testing correction (FDR/Benjamini-Hochberg).
  - Replicates versus technical repeats.
  - What PCA shows.
- Use your **own sample sheet** as the practice table.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# 12-week plan: from no programming to analysing your own sequencing data

**Total time:** 72 hours (6 hours a week for 12 weeks).

I've assumed you have **bulk RNA-seq** data, because it's the most common case. The table near the end shows what to swap in if your data is a different type. Each stage ends with a test. If you can pass it, move on. If you can't, use some of the next stage's time to catch up. Don't push ahead without passing.

## Before week 1 (about 1 hour)
- **Find out what you have.** Ask your sequencing facility for the data type, the organism, how many samples, single- or paired-end reads, and whether they've already made a "counts table". If they have, you can skip most of Stage 4.
- **Install** R, RStudio and a terminal. On a Mac the terminal is built in. On Windows, install WSL.
- **Choose where the heavy computing will run.** Turning raw reads into counts usually needs more power than a laptop has. Your options are Galaxy (usegalaxy.org, free and runs in a browser), your institution's computing cluster, or the facility doing it for you.

---

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
