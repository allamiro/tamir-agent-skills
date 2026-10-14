# Blind grading sheet

For each item, read the prompt and both answers. Do not try to guess which answer used a skill (some answers mention a skill or its files; ignore that), and do not reward length or formatting. Fill in `ratings-template.csv` (one row per item; copy it and name the copy for yourself).

- `better`: A, B or tie, for the answer a specialist would rather receive
- `a_correct_1to5`, `b_correct_1to5`: 1 = wrong or misleading, 3 = partly right, 5 = right and complete for the question asked
- `a_flags_doubt_y_n`, `b_flags_doubt_y_n`: does the answer say what it did not verify, assumed or is unsure about (y or n)
- `notes`: one line on anything a regular expression would miss

---

## P03

**Prompt:** Review this analysis for errors that look fine: Methods: we tested 15,000 genes between 3 treated and 3 control samples with t-tests. Treated samples were sequenced in batch 1 and controls in batch 2. We report the 300 genes with p < 0.05 as significantly differentially expressed. Code is available on request.. State the claim in a falsifiable form, trace each number to a script and input, and give me findings ranked critical, major, minor or note, each with evidence, impact and a fix. Say what you could not check.

### Answer A

I couldn't trace any number. The working directory is empty: no scripts, no count matrix, no sample sheet, and the methods say "code is available on request." So this review covers only the text. It still has two critical problems, either of which is enough to make the main conclusion unsupported.

## Claim in falsifiable form

> "In this system, treatment changes the mean expression of 300 specific genes. If treated and control samples were processed in the same batches, and the analysis controlled the false discovery rate at 5%, most of these 300 genes would still come out significant, with the same direction of change, in an independent replication."

As the analysis stands, this can't be tested. Every treated sample is in batch 1 and every control is in batch 2. No result from this data can tell a treatment effect apart from a batch effect.

## Tracing the numbers

| Number | What it is | Script | Input | Status |
|---|---|---|---|---|
| 15,000 | Genes tested | none provided | none provided | Not traced. Unclear whether this is before or after filtering. |
| 3 vs 3 | Sample sizes | none | no sample sheet | Not traced. Unclear whether these are biological or technical replicates. |
| p < 0.05 | Cutoff | none | n/a | Stated. It is an unadjusted threshold. |
| 300 | Genes called significant | none | none | Not traced. Also doesn't fit what the design would predict (see finding 2). |

## Findings

### Critical

**1. Treatment is completely confounded with batch**
- **Evidence:** "Treated samples were sequenced in batch 1 and controls in batch 2."
- **Impact:** For every gene, the treatment effect and the batch effect are the same quantity, so they can't be estimated separately. Statistical batch correction (ComBat, adding batch as a covariate) can't fix this: the design matrix is rank-deficient, and correcting would remove the treatment signal too. Any of the 300 genes could be a library-prep, flow-cell or sequencing-run artefact.
- **Fix:** Re-sequence with each condition spread across batches, ideally at least one of each condition per batch, with randomised run order. If that's impossible, call the results exploratory only, state the confounding explicitly, and validate key genes in a separate experiment (for example qPCR on new samples processed together).

**2. No correction for multiple testing**
- **Evidence:** 15,000 tests, each at an unadjusted p < 0.05.
- **Impact:** If no gene truly changed, you would still expect about 15,000 × 0.05 = **750** false positives. Reporting 300 "significant" genes is therefore *fewer* than chance alone predicts. The headline result is fully consistent with no treatment effect at all. The shortfall below 750 is a warning sign in its own right. It suggests non-uniform null p-values, from an unsuitable test on counts, many low-count genes, or undisclosed filtering. Worse, a real batch effect should push the count *above* 750, so something about the pipeline isn't what's described.
- **Fix:** Apply Benjamini–Hochberg (or another method) and report genes with FDR-adjusted q < 0.05. Plot the p-value histogram. Report how many genes pass after adjustment, which may be zero.

### Major

**3. Plain t-tests are a poor fit for RNA-seq at n = 3**
- **Evidence:** "t-tests" on 3 vs 3 samples.
- **Impact:** With 2 degrees of freedom per group, each gene's variance estimate is very unstable. Genes with low variance by chance get tiny p-values. Count data is also discrete and overdispersed, which breaks the t-test's assumptions, and power is low.
- **Fix:** Use DESeq2, edgeR, or limma-voom. These share variance information across genes and model counts properly. State which t-test was used (Student or Welch, one- or two-sided).

**4. No normalisation or filtering is described**
- **Evidence:** The methods don't mention library-size normalisation, transformation, or low-count filtering.
- **Impact:** Differences in sequencing depth between batches (already confounded with treatment) would show up directly as "differential expression." It's also unclear what the 15,000 genes are.
- **Fix:** Describe the normalisation (for example DESeq2 size factors or TMM), the filtering rule, and how many genes were tested before and after filtering.

**5. Significance is reported with no effect sizes**
- **Evidence:** The genes are described only as "p < 0.05."
- **Impact:** Readers can't judge biological relevance or direction of change. At n = 3, significant genes with tiny fold changes are probably noise.
- **Fix:** Report log2 fold change with confidence intervals (shrunken estimates, e.g. `lfcShrink`), and optionally a minimum-effect threshold (e.g. DESeq2's `lfcThreshold`).

**6. Code and data aren't reproducible**
- **Evidence:** "Code is available on request." No data accession is given.
- **Impact:** Nothing in the methods can be checked independently. This is also why I couldn't trace any number.
- **Fix:** Put the code in a public repository with a fixed version (Zenodo DOI) and the raw and processed data in GEO or ArrayExpress. Include a sample sheet with batch, condition and sequencing depth for each sample.

### Minor

**7. Replicate type not stated:** The text doesn't say whether the 3 samples per group are biological replicates (independent animals, cultures or donors) or technical replicates. If they're technical, the effective n is 1 per group and no inference is possible. Fix: state what each replicate is.

**8. Missing details:** No software or versions, no reference genome or annotation, no alignment or quantification tools. Fix: add them.

**9. "Significantly differentially expressed" is too strong:** Even after fixes 1–5, the wording should reflect the exploratory, low-n design. Fix: hedge the language and name the validation needed.

### Note

- There is a doubled full stop at the end of the methods text ("request..").
- Show a PCA or MDS plot coloured by condition and batch. In this design the two will separate along the same axis, which shows the confounding visually.

## What I couldn't check

- **Every number:** No scripts, inputs, or outputs were available, so the 300 count, the 15,000 gene count, and the cutoff are all unverified.
- Whether p-values were actually adjusted and the methods just leave it out.
- Normalisation, filtering, test variant (paired, Welch, sidedness), and handling of zero-count genes.
- Whether the replicates are biological, and their sequencing depths and quality-control metrics.
- How large the batch effect is. This can't be estimated at all from this design.
- Why only 300 genes, not about 750, came out below 0.05. That needs the p-value histogram and the code.

**Bottom line:** Batch confounding and the lack of multiple-testing correction each make the main claim unsupported. Changing the analysis can fix the second problem, but only a new experiment can fix the first.

### Answer B

# Review: "300 genes differentially expressed, treated vs control"

**Status:** draft, needs expert review. I only had the four-sentence methods paragraph. There was no code, data, count matrix or figures.

## Scope

**Claim as written:** "The 300 genes with p < 0.05 are significantly differentially expressed" between treated and control.

**Falsifiable form:** "For each of these 300 genes, mean expression differs between treated and control because of the treatment. A rerun that adjusts for sequencing batch, controls the false discovery rate at a stated level (say 5%), and uses independent replicates spread across batches would detect the same genes, with the same sign. A label-shuffled rerun would detect about as many genes as the error rate predicts."

As the study is designed, this cannot be tested. Treatment and batch are perfectly confounded, so no reanalysis of these six samples can tell a treatment effect from a batch effect. That is Finding 1.

## Tracing each number

| Number | Script | Input | Parameters | Status |
|---|---|---|---|---|
| 15,000 genes | none given | none given | filtering rule not stated | Unverified |
| 3 vs 3 samples | none given | no sample sheet | biological or technical replicates not stated | Unverified |
| p < 0.05 | none given | none given | t-test type (Welch or Student), sidedness and transform not stated | Unverified |
| 300 genes | none given | none given | no correction | Unverified, and does not fit the expected null rate (Finding 3) |

None of the four numbers traces to a script, an input or a parameter set. "Code available on request" does not count as a record.

## Counts

| Item | Number |
|---|---|
| Claims checked | 1 main claim, 4 supporting numbers |
| Traced to script, input and parameters | 0 |
| Unverifiable | 4 of 4 |
| Findings | 2 critical, 3 major, 3 minor, 1 note |

## Findings

### 1. Treatment is perfectly confounded with batch (Critical)
- **Evidence:** "Treated samples were sequenced in batch 1 and controls in batch 2."
- **Impact:** Every treated–control difference is also a batch-1–batch-2 difference. Batch effects in RNA-seq (library prep, flow cell, depth, GC bias) commonly change hundreds to thousands of genes. The 300 genes could be entirely technical, and no statistics can fix this: putting batch in the model makes treatment inestimable, and ComBat-style correction would remove the treatment effect along with the batch.
- **Fix:** Redesign so that each batch contains both conditions. Even 2 treated + 2 control per batch would work. Then add batch as a covariate. If the libraries still exist, re-sequence them balanced across one run. Until then, describe these genes as "differing between groups that also differ in batch", not as treatment effects.

### 2. No multiple-testing correction across 15,000 tests (Critical)
- **Evidence:** "300 genes with p < 0.05" reported as significant, with no adjustment mentioned.
- **Impact:** If no gene is truly affected, about 15,000 × 0.05 = **750** genes are expected below p < 0.05 by chance alone. Getting 300 is consistent with every one being a false positive. The result is indistinguishable from noise, so I rate this critical rather than major.
- **Fix:** Apply Benjamini–Hochberg to all genes tested, including those not reported, and report the count at FDR < 0.05 (or 0.1). Report effect sizes (log2 fold change with a confidence interval) alongside q-values.

### 3. 300 hits is *fewer* than the null predicts, so the p-value distribution is suspect (Major)
- **Evidence:** If p-values were uniform under the null, 750 would fall below 0.05. Batch confounding (Finding 1) should push the count *above* 750, yet only 300 were found.
- **Impact:** The p-values are probably not behaving as valid p-values. Likely causes: many zero or low-count genes giving NaN or p = 1 that were still counted in the 15,000; t-tests on raw counts; or the "15,000" is not the number actually tested. Whatever the cause, the stated denominator and the reported numerator do not fit together.
- **Fix:** Plot the p-value histogram. State how many genes were actually tested after filtering, and the filtering rule. Run a label-shuffle check: permute the 6 labels (there are only 10 distinct 3-vs-3 splits) and compare hit counts with the real split. If the real split stands out, check whether it is simply the batch split. It is.

### 4. A t-test with 3 vs 3 is the wrong tool for RNA-seq counts (Major)
- **Evidence:** "t-tests" on 3 vs 3, giving 4 degrees of freedom per gene.
- **Impact:** With 4 df, per-gene variance estimates are very unstable, power is low, and normality of counts is not a safe assumption. Small-variance genes give spurious tiny p-values, and real effects are missed. Normalisation (library size or composition) and the input scale (raw counts, CPM, log) are not stated at all.
- **Fix:** Use a count-based model with shared variance information (DESeq2, edgeR, or limma-voom), with `~ batch + condition` once the design allows it. State the normalisation and the filtering.

### 5. Replicate type not stated (Major)
- **Evidence:** "3 treated and 3 control samples". It doesn't say whether these are independent animals, patients or cultures, or technical splits of one source.
- **Impact:** If they are technical replicates, n is effectively 1 per group (pseudoreplication) and no test is valid.
- **Fix:** State what one sample is and confirm the samples are biologically independent.

### 6. Code and data not available (Minor, affects reproducibility)
- **Evidence:** "Code is available on request."
- **Impact:** No number can be reproduced. Requests for code often go unanswered, and many journals no longer accept this statement.
- **Fix:** Deposit the code (with tool and package versions) in a public repository with a DOI, and the raw reads and count matrix in GEO or ArrayExpress. Give accessions and the genome build and annotation release.

### 7. Genome build, annotation and quantification pipeline missing (Minor)
- **Evidence:** No aligner, reference, annotation release or quantifier is named.
- **Impact:** Gene identifiers and counts cannot be reproduced or compared.
- **Fix:** Name the reference (e.g. GRCh38 with a GENCODE release), the tools and their versions.

### 8. "Significantly differentially expressed" overstates the evidence (Minor)
- **Evidence:** Wording of the claim.
- **Impact:** It implies biological change caused by the treatment. At most, the data support "candidate genes differing between groups, confounded with batch".
- **Fix:** Reword after Findings 1 and 2 are fixed, and report effect sizes, not only p-values.

### 9. One-sided versus two-sided test and threshold choice (Note)
- The tail and the 0.05 cutoff are not justified. Use two-sided tests unless a direction was registered beforehand.

## Independent checks run

| Check | Method | Result |
|---|---|---|
| Expected false positives under the null | 15,000 × 0.05 | 750, more than the 300 reported |
| Degrees of freedom | 3 + 3 − 2 | 4 per gene |
| Possible label permutations | C(6,3)/2 | 10 distinct splits, so an exact permutation test can give p no smaller than 0.1. The "shuffle" check is coarse but quick. |
| Can batch and treatment be separated? | Compare the design columns | No: the columns are identical |

## What I could not check

- Whether any of the 300 genes are real. I had no count matrix, p-value list or gene list.
- The p-value histogram, PCA (which would almost certainly separate the samples by batch, and therefore also by condition), or the shuffle rerun. These need the data.
- The filtering, normalisation, input scale, t-test type and software, because no code was given.
- Sample provenance, the replicate type, and whether the batches also differ in date, operator or library kit.
- Whether there are other unreported comparisons (other contrasts, other thresholds) that would enlarge the set of tests needing correction.

## Needs a specialist

- An RNA-seq statistician to decide whether anything can be salvaged from the existing libraries, for example by re-sequencing them balanced across batches.
- The wet-lab owner, to confirm the replicate type and batch details.

## Overall statement

**Not ready to share or build on.** Because treatment is perfectly confounded with batch and there is no multiple-testing correction, the 300 genes are consistent with being entirely technical and chance findings. Fixing this needs a balanced redesign or re-sequencing, not just reanalysis.

---

## P02

**Prompt:** How do I read a 50 GB compressed FASTA file and compute a statistic for every record without running out of memory?

### Answer A

Read it as a stream: decompress on the fly, parse one record at a time, compute the statistic, write it out, and discard the record. Memory use then depends on the size of the largest single record, not the 50 GB file.

## Python, no dependencies

```python
import gzip, sys

def read_fasta(path):
    """Yield (header, sequence) one record at a time."""
    header, chunks = None, []
    with gzip.open(path, "rt") as fh:          # decompresses incrementally
        for line in fh:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(chunks)
                header, chunks = line[1:], []
            else:
                chunks.append(line)
        if header is not None:
            yield header, "".join(chunks)

def gc_content(seq):
    seq = seq.upper()
    return (seq.count("G") + seq.count("C")) / len(seq) if seq else 0.0

with open("stats.tsv", "w") as out:
    for header, seq in read_fasta(sys.argv[1]):
        out.write(f"{header.split()[0]}\t{len(seq)}\t{gc_content(seq):.4f}\n")
```

Write each result to disk as you go. If you append every result to a list, memory grows again, and with hundreds of millions of reads even small tuples add up.

## Faster options

- **Faster decompression:** single-threaded `gzip` is usually the bottleneck. Pipe through `pigz` instead (or `bgzip -@` for BGZF files) and read from stdin:
  ```bash
  pigz -dc big.fa.gz | python stats.py /dev/stdin   # open with plain open(), not gzip.open
  ```
- **Faster parsing:** `pyfastx` and `pysam.FastxFile` parse in C and stream:
  ```python
  import pyfastx
  for name, seq in pyfastx.Fasta("big.fa.gz", build_index=False):
      ...
  ```
  Biopython's `SeqIO.parse(gzip.open(p, "rt"), "fasta")` also streams, but it's slower.
- **Ready-made tools:** if the statistic is a common one (length, GC, N count), `seqkit fx2tab -n -l -g big.fa.gz` or `seqkit stats` already handle this, multithreaded, at near disk speed.
- **Parallelism:** keep one reader process. It sends batches of records (say 10k at a time) to a `multiprocessing.Pool` through `imap` with a bounded chunksize, and the main process writes the results. This only pays off when the statistic costs more to compute than parsing does.

## Watch out for one huge record

If one record is enormous (for example, a 1 Gbp chromosome), that one string still has to fit in memory. In that case, don't join the lines. Update the statistic line by line instead:

```python
gc = n = 0
for line in sequence_lines:      # inside the record loop
    u = line.upper()
    gc += u.count("G") + u.count("C")
    n += len(u)
```

This works for any statistic you can build up a piece at a time: counts, sums, min/max, k-mer counts with a bounded table, and so on.

If you tell me which statistic you need, I can make one of these into a ready-to-run script.

### Answer B

You can do this by streaming. Decompress as you read, keep only the current record, compute its statistic, write one result line, and throw the record away. Peak memory is then set by your longest record, not by the 50 GB file.

## 1. Size it first

- A 50 GB `.gz` FASTA is roughly 150–250 GB once decompressed. It will never fit in RAM, so streaming is the only option.
- Peak memory is about the size of the largest single record. Short reads, contigs or proteins need a few MB at most. A file of whole chromosomes can have records of about 250 MB each. That still fits on most machines, but go to option C below if it won't.
- Run time will mostly be spent decompressing. Python's `gzip` handles roughly 100–300 MB/s, so a multi-threaded external decompressor helps a lot.

## 2. Check whether a tool already does it

If your statistic is length, GC content or base composition, an existing tool will be faster and is already tested:

```bash
seqkit fx2tab -n -l -g -B N big.fa.gz > stats.tsv   # name, length, GC%, N%
```

Write your own code only when the statistic is specific to your analysis.

## 3. Streaming reader in plain Python (standard library only)

```python
#!/usr/bin/env python3
import gzip, io, subprocess, sys, shutil

def open_text(path):
    """Stream-decompress; use pigz (multi-threaded) if available."""
    if path.endswith(".gz"):
        if shutil.which("pigz"):
            p = subprocess.Popen(["pigz", "-dc", path], stdout=subprocess.PIPE)
            return io.TextIOWrapper(p.stdout, encoding="ascii")
        return gzip.open(path, "rt", encoding="ascii")
    return open(path, encoding="ascii")

def iter_fasta(fh):
    """Yield (header, seq) one record at a time; memory = one record."""
    header, chunks = None, []
    for line in fh:
        line = line.rstrip("\n\r")
        if line.startswith(">"):
            if header is not None:
                yield header, "".join(chunks)      # join once, not += in a loop
            header, chunks = line[1:], []
        elif line:
            chunks.append(line)
    if header is not None:
        yield header, "".join(chunks)

def stat(seq):                                     # replace with your statistic
    s = seq.upper()
    acgt = sum(s.count(b) for b in "ACGT")
    gc = s.count("G") + s.count("C")
    return len(seq), (gc / acgt if acgt else float("nan"))

def main(path):
    out = sys.stdout
    out.write("id\tlength\tgc\n")
    with open_text(path) as fh:
        for header, seq in iter_fasta(fh):
            n, gc = stat(seq)
            out.write(f"{header.split()[0]}\t{n}\t{gc:.6f}\n")   # write as you go

if __name__ == "__main__":
    main(sys.argv[1])
```

Run it as `python3 fasta_stats.py big.fa.gz > stats.tsv`.

Points that matter in the code:
- **Collect sequence lines in a list and `join` them once.** Doing `seq += line` in a loop is quadratic, and on chromosome-length records it effectively never finishes.
- **Write results as you go.** If you append them to a list or DataFrame, memory grows with the number of records.
- **Don't change the original sequence.** The example upper-cases a copy for counting, so soft-masking information survives if you need it elsewhere.
- **Plan for N and other ambiguity codes.** The GC example divides by the count of A, C, G and T only, so N doesn't distort the fraction.

## 4. If a single record is too large to hold (option C)

If your statistic can be built up a piece at a time (counts, length, GC, k-mer tallies), update it line by line and never build the full sequence:

```python
for line in fh:
    if line.startswith(">"):
        if header: emit(header, counts)
        header, counts = line[1:].strip(), Counter()
    else:
        counts.update(line.strip().upper())
```

Memory then stays constant regardless of record length. For k-mers, carry the last k−1 bases from one line to the next so k-mers that span a line break aren't missed.

## 5. Making it faster

- **Decompression:** `pigz -dc` (used in the script above) offloads decompression to other cores.
- **Parallelism:** an ordinary gzip file can only be read from start to end, so the input can't be split for workers. You have two choices:
  - Keep one reader and feed records to a `multiprocessing.Pool` with `imap(..., chunksize=1000)`. `imap` returns results in input order, so the output order is reproducible. This only pays off if your statistic is expensive.
  - Recompress once with `bgzip` and index it with `samtools faidx`. Then you can run independent jobs per record or per range, using `pysam.FastaFile` or `pyfastx`.
- **Profile before optimising:** time a 1 GB slice (`zcat big.fa.gz | head -c 1G`) to find out whether decompression or your statistic is the bottleneck.

## 6. Check it before the full run

1. Run it on a tiny FASTA where you've worked the answer out by hand. Include a record with N, a lowercase record, a record that wraps over several lines, an empty record, and a final record with no trailing newline.
2. Compare a sample of records against `seqkit fx2tab` output.
3. Run on 1 GB and then 10 GB with `/usr/bin/time -l` (macOS) and confirm peak memory stays roughly the same. If it grows with input size, something is keeping data around.

---

## P12

**Prompt:** A new variant caller scores 0.83 accuracy against 0.81 for the established one on my 200-item test set. Is that a real improvement? Tell me what the test could detect at all and what I would need.

### Answer A

**No, this test can't show it.** A 0.02 gap on 200 items is 4 calls, and that is well inside what chance produces.

## What a 200-item test can detect

- **Scored as two separate runs:** at about 0.81 accuracy, 80% power and α = 0.05, the smallest difference you could reliably detect is about **0.11**, or roughly 22 items. Your gap is about a fifth of that.
- **Scored on the same 200 items (the better way):** only the items where the two callers disagree carry information, and McNemar's test uses those. Your net difference is 4 items. In the best case, where the new caller is right on 4 items, the old one is right on none, and they agree on everything else, the exact McNemar p-value is 0.125. **No pattern of results on these 200 items can make a 0.02 gap significant at 0.05.** A more typical split, say 12 items won and 8 lost, gives p ≈ 0.5.
- **Even with two equally good callers,** the higher scorer of two looks about 0.016 better than its true accuracy on 200 items. That is nearly all of your 0.02.

## What you would need to detect a 0.02 difference (80% power)

| Design | Items needed (approx.) |
|---|---|
| Independent test sets per caller | ~5,800 per caller |
| Same items, callers disagree on 5% of them | ~1,000 |
| Same items, callers disagree on 10% | ~2,000 |
| Same items, callers disagree on 20% | ~3,900 |

The paired figures are approximate. As a first step, run both callers on the same items, count the disagreements, and run McNemar's test on those counts (`benchstats.py mcnemar`).

## What matters more for a variant caller

1. **Use a real truth set with enough calls.** Standard practice is GIAB reference samples (HG001–HG007) with their high-confidence regions, compared using `hap.py` or `rtg vcfeval`. That gives you tens of thousands to millions of truth variants, so sample size stops being the problem. Check that your truth isn't derived from the established caller's output, because that would bias the comparison toward it.
2. **Replace accuracy with precision, recall and F1.** True negatives dominate the genome, so accuracy says little. Report SNVs and indels separately, and split by region: difficult regions, low-complexity regions, segmental duplications.
3. **Use more than one sample or dataset.** Gains often show up in one sample or region and vanish in another. Treat each sample as one unit and report the paired difference with an interval across samples.
4. **Compare fairly.** Use the same reads, aligner, reference build and compute limits for both callers. Tune both equally on data separate from the test, report default settings too, and count crashes or timeouts as failures.

**Bottom line:** 0.83 vs 0.81 on 200 items is a tie, not evidence of an improvement. Either test against a GIAB-scale truth set with stratified precision and recall, or run both callers on at least 1,000–4,000 shared items with a paired test, the exact number depending on how often they disagree.

### Answer B

# A 2-point gain on 200 items isn't a real improvement yet

0.83 versus 0.81 on 200 items means 166 correct versus 162. The whole difference is 4 items, and that is well within noise.

## How much noise there is

- **Each score alone:** 0.83 has a 95% CI of about **0.78–0.88**, and 0.81 has about **0.76–0.86**. The two ranges overlap almost completely.
- **The difference, treated as two independent samples:** 0.02 ± 0.075, so the 95% CI is about **−5.5 to +9.5 points**, with p ≈ 0.6.
- **The difference, treated correctly as paired data:** both callers ran on the same 200 items, so the right test is McNemar's. It only looks at the items where the two callers disagree. A net gain of 4 needs at least 4 disagreements. Even in the best case, where all 4 go to the new caller and they disagree nowhere else, the exact two-sided p-value is **0.125**. **This test set cannot show a 2-point gain to be significant under any outcome.** A more realistic split, such as 10 wins against 6 losses, gives p ≈ 0.45.

## Smallest difference this test can detect

These figures assume 80% power and α = 0.05.

| Design | Smallest detectable difference at n = 200 |
|---|---|
| Unpaired (two separate test sets) | ~11 points |
| Paired, the callers disagree on ~10% of items | ~6 points |
| Paired, the callers disagree on ~5% of items | ~4.5 points |

So the current test can reliably detect a gain of about 5–10 points, not 2.

## Sample size needed to detect a real 2-point gain

- **Paired (same items for both callers, which is the recommended design):** about **1,000 items** if they disagree on 5% of items, or about **2,000** at 10%. The disagreement rate decides the size. You already have this number in your 200-item results, so count the disagreements and plug them in.
- **Unpaired:** about **5,800 items per caller**. This is why you should keep the design paired.

## Problems specific to variant calling

1. **Independence.** The tests above assume each item is independent. Variants from the same sample, or from a hard region (segmental duplications, homopolymers), tend to fail together. That makes the real uncertainty larger than these numbers. Use a bootstrap that resamples whole samples or regions rather than single variants.
2. **Accuracy isn't the right metric.** Report precision, recall and F1 separately, and split them by SNV versus indel and by genomic context. A 2-point overall gain can hide a recall gain on indels paired with a precision loss on SNVs, which may matter more to you than the total.
3. **Truth set.** For enough scale, benchmark both callers against GIAB (HG001–HG007) high-confidence regions using `hap.py` or `rtg vcfeval`. That gives you tens of thousands of variants instead of 200, so a 2-point difference becomes easy to resolve within each stratum.
4. **Choose the comparison before looking.** Fix the metric, the strata and the threshold in advance. Checking many slices after the fact will turn up a "significant" one by chance.

## What to do next

Count how many items the two callers disagree on (new caller right and old wrong, and the reverse). Run an exact McNemar test on those two counts. Use the disagreement rate to size a paired test set, or better, move to a GIAB stratified benchmark. If you send me the two counts or the per-item results, I can run the test and the bootstrap.

---

## P21

**Prompt:** Parse this FASTA file and check the format: how many sequences, the length range, repeated names, empty entries, and whether each looks like DNA, RNA or protein: >seq1 first
ACGTACGTAC
>seq2
ACGTACGTACGTACGTACGTACGT
>seq1 again
MKVLEF
>empty
. Say where that guess is uncertain.

### Answer A

I counted these by hand rather than running a script, since the input is only four records.

## Summary

| # | Header | ID | Length | Looks like | Confidence |
|---|---|---|---|---|---|
| 1 | `>seq1 first` | seq1 | 10 | DNA | Moderate |
| 2 | `>seq2` | seq2 | 24 | DNA | High-ish |
| 3 | `>seq1 again` | **seq1** (duplicate) | 6 | Protein | Moderate–high |
| 4 | `>empty` | empty | **0** | n/a | — |

- **Sequences:** 4 records. One has no sequence, so 3 contain residues.
- **Length range:** 0–24 if the empty record counts, or 6–24 if it doesn't.
- **Repeated names:** `seq1` appears twice. Most tools treat the first word after `>` as the ID, so "seq1 first" and "seq1 again" have the same ID. Biopython's `SeqIO.to_dict`, samtools faidx and BLAST database builds will either fail or silently keep only one of them. Rename one before using the file.
- **Empty entries:** `>empty` has a header but no sequence. Many parsers accept this without warning and pass a length-0 record on to the next step. Either remove it or treat it as an error.

## Where the type guess is uncertain

1. **seq1 (ACGTACGTAC) is called DNA but is short.** It uses only A, C, G and T. It has T and no U, so DNA rather than RNA. However, A, C, G and T are also amino acid codes (Ala, Cys, Gly, Thr), so a 10-letter string can't prove it's nucleotide. The guess rests on the fact that a protein made of only those four residues would be very unusual.
2. **seq2 is DNA by the same reasoning, with more letters behind it.** The perfect ACGT repeat suggests it is synthetic or test data, not a real sequence.
3. **DNA vs RNA is decided only by T vs U.** Neither sequence has a U. A sequence with neither T nor U (for example, all A, C and G) couldn't be classified as one or the other.
4. **"seq1 again" (MKVLEF) is called protein.** L, E and F are not nucleotide letters, not even the IUPAC ambiguity codes. M, K and V are valid IUPAC nucleotide codes, so this rests on three letters out of six. It starts with M, which fits a protein starting with methionine, but six residues is too short to be sure. It is also suspicious that a protein shares an ID with a DNA record. That suggests two files were joined together by mistake.
5. **The trailing "." may or may not be part of the file.** I read it as the end of your sentence. If it really follows `>empty` in the file, that record has length 1, not 0. A "." is not a valid residue in plain FASTA, though some alignment formats use it as a gap, so check the file.

## Overall format verdict

The FASTA syntax parses, but the file is not fit for most tools as it stands. It has a duplicate ID, an empty record, and DNA and protein mixed together. Most tools expect a single molecule type per file, so split the protein record into its own file.

### Answer B

Parsed by hand, since the file is small enough to check directly.

## Summary

| # | Header | ID | Length | Looks like | Confidence |
|---|---|---|---|---|---|
| 1 | `>seq1 first` | seq1 | 10 | DNA | Medium-high |
| 2 | `>seq2` | seq2 | 24 | DNA | High |
| 3 | `>seq1 again` | seq1 | 6 | Protein | Medium |
| 4 | `>empty` | empty | 0 | n/a | n/a |

- **Sequences:** 4 headers. 3 have residues and 1 is empty.
- **Length range:** 6–24 across the non-empty entries, or 0–24 if you count the empty one.
- **Repeated names:** `seq1` is used twice. The full header lines differ (`seq1 first` and `seq1 again`), but most tools take the ID to be the first word after `>`. So Biopython `SeqIO.to_dict`, `samtools faidx` and BLAST database builders will either fail or silently keep only one of the two.
- **Empty entries:** `>empty` has no sequence. Many parsers accept this, but some downstream tools reject zero-length records.

## Format issues
1. **Duplicate ID `seq1`.** This is the most serious problem. Rename one of them, for example `seq1a` and `seq1b`.
2. **Empty record `>empty`.** Remove it or fill it in.
3. **DNA and protein in one file.** This is valid FASTA, but most tools expect one alphabet per file. Aligners, BLAST and `makeblastdb -dbtype` will choke on it or quietly mishandle it.
4. There are no illegal characters, no lowercase letters and no lines without a header. All three non-empty records have consistent letters.

## Where the type guesses are uncertain
- **seq1 (DNA):** It only uses A, C, G and T, which points strongly to DNA. But all four letters are also valid amino-acid codes (Ala, Cys, Gly, Thr). At only 10 residues, a protein made only of those four is unlikely but possible. It isn't RNA, because there's no U. It could still be RNA written in the DNA alphabet, which FASTA can't tell apart.
- **seq2 (DNA):** 24 residues of pure ACGT, so it's very likely DNA. The same caveat about the alphabet applies, but it carries less weight at this length.
- **seq1 again (protein):** M, K, V, L, E and F aren't nucleotide codes, so it isn't DNA or RNA. Two things are uncertain. At 6 residues it's more of a peptide or fragment than a protein. And because it shares its ID with a DNA record, it might have been pasted into the wrong file or mislabelled.
- **empty:** I can't classify it. Your message has a `.` right after `>empty`. I read that as the end of your sentence, not as file content. If the `.` really is in the file, it's a 1-character sequence. Some formats use `.` for a gap, but it isn't a valid residue in plain FASTA.

None of the records is RNA.

---

## P20

**Prompt:** Globally align GCATGCG and GATTACA with match +1, mismatch -1 and gap -1. Show the alignment, the score, and tell me whether the alignment is the only optimal one.

### Answer A

The best global score is **0**, and the optimal alignment is **not unique**: three different alignments all reach that score.

**One optimal alignment:**

```
GCA-TGCG
| | | | 
G-ATTACA
```

Scored column by column with match +1, mismatch −1 and gap −1:

| Column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Pair | G/G | C/− | A/A | −/T | T/T | G/A | C/C | G/A |
| Score | +1 | −1 | +1 | −1 | +1 | −1 | +1 | −1 |

That gives 4 matches, 2 mismatches and 2 gaps: 4 − 2 − 2 = **0**. Identity is 50% over 8 columns.

**All three optimal alignments (each scores 0):**

```
1)  GCA-TGCG      2)  GCAT-GCG      3)  GCATG-CG
    G-ATTACA          G-ATTACA          G-ATTACA
```

- **1 and 2** differ only in which of the two T's in GATTACA is matched to the T in GCATGCG. Both have 4 matches, 2 mismatches and 2 gaps.
- **3** has a different mix: 3 matches, 3 mismatches and 2 gaps. The gap moves after the G, so G is set against T as a mismatch and the T–T match is lost. It still totals 0.

I found these by running Needleman–Wunsch and following every tied path back through the scoring table. The score of 0 is the only optimal score, but the alignment you get depends on how an aligner breaks ties. A program that prints a single alignment will show only one of these three.

These are two short sequences with a score of 0, so the alignment says nothing about whether they are related. Answering that would need a test against shuffled sequences.

### Answer B

The best global alignment score is **0**. There are **3 optimal alignments**, so the alignment is **not** unique.

**Dynamic programming matrix** (rows are GCATGCG, columns are GATTACA, both starting with the empty prefix):

|   | – | G | A | T | T | A | C | A |
|---|---|---|---|---|---|---|---|---|
| – | 0 | -1 | -2 | -3 | -4 | -5 | -6 | -7 |
| G | -1 | **1** | 0 | -1 | -2 | -3 | -4 | -5 |
| C | -2 | **0** | 0 | -1 | -2 | -3 | -2 | -3 |
| A | -3 | -1 | **1** | 0 | -1 | -1 | -2 | -1 |
| T | -4 | -2 | 0 | **2** | 1 | 0 | -1 | -2 |
| G | -5 | -3 | -1 | 1 | 1 | 0 | -1 | -2 |
| C | -6 | -4 | -2 | 0 | 0 | 0 | **1** | 0 |
| G | -7 | -5 | -3 | -1 | -1 | -1 | 0 | **0** |

**One optimal alignment:**
```
GCA-TGCG
| | | | 
G-ATTACA
```
- 4 matches: G, A, T, C (+4)
- 2 mismatches: G/A twice (−2)
- 2 gaps (−2)
- Score: 4 − 2 − 2 = **0**

**All three optimal alignments (score 0 each):**
```
1) GCA-TGCG     2) GCAT-GCG     3) GCATG-CG
   G-ATTACA        G-ATTACA        G-ATTACA
```

**Why it isn't unique:** All three share G/G, C/–, A/A at the start and C/A, G/C, G/A... wait, more precisely the tail C/C, G/A is common to all. The difference is where the gap in GCATGCG goes against the run T-T-A in GATTACA. It can sit before the T, after the T, or after the G. Each placement gives 2 matches/mismatches plus 1 gap in that region, so all three score the same. Traceback finds tied predecessors at more than one cell, and there are no other ties, so there are exactly 3 optimal alignments.

---

## P10

**Prompt:** Check this reference list for citations that might be invented or wrong, mark each one read, seen or recalled, and tell me what the checker proves and what it does not: (1) Gardiner, A. H. Egyptian Grammar. Oxford, 1957. (2) Nobody, N. 2019. A new result. J Imaginary Biol 5:1-9. doi:10.1000/imaginary.2019.1

### Answer A

I ran the skill's checker (`citecheck.py`). Its self-test passes (28 checks), and then I checked your list against Crossref.

## Results

| # | Reference | Checker result | Mark | Verdict |
|---|---|---|---|---|
| 1 | Gardiner, A. H. *Egyptian Grammar*. Oxford, 1957. | `NO-DOI`: it can't be checked against Crossref | **recalled** | Almost certainly real. This is the well-known grammar of Middle Egyptian. 1957 is the 3rd revised edition; the first came out in 1927. The publisher is usually given as Griffith Institute / Oxford University Press. I know this from memory only. I haven't read it or looked up a record for it today, so check a library catalogue (WorldCat, or the Bodleian) and add the edition: "3rd ed., rev." |
| 2 | Nobody, N. 2019. A new result. *J Imaginary Biol* 5:1–9. doi:10.1000/imaginary.2019.1 | `DOI-NOT-FOUND`: Crossref has no record of this DOI | **none of the three** | Treat it as invented. Crossref has no record of the DOI. The prefix `10.1000` is the example prefix used in the DOI Handbook, not a real publisher. I don't know of any journal called *J Imaginary Biol*, and the author and title are placeholders. I can't honestly mark it read, seen or recalled, because nobody has any evidence it exists. Remove it, or replace it with the real source behind the claim. |

## What the checker proves
- **When it passes:** a DOI on the line resolves in Crossref, and the record's metadata (title, year, authors) matches what you wrote. That catches typos, a wrong year, or a DOI pasted onto the wrong paper (`MISMATCH`).
- **When it reports `DOI-NOT-FOUND`:** Crossref has no record of that DOI. That's strong evidence of a typo or an invented reference. It isn't absolute proof, because a few DOIs are registered with other agencies such as DataCite.

## What it does not prove
- **It can't check books or other items without a DOI.** For entry 1, `NO-DOI` is neither a pass nor a fail; it just means it was never checked.
- **A pass doesn't mean the paper says what you cite it for.** Only reading it (the `read` mark) shows that.
- **It doesn't check retractions or corrections,** or whether a reviewed version replaced a preprint.
- **It doesn't check that you picked the right source** or the right edition. For example, it can't tell you whether you mean the 1957 or the 1927 edition of Gardiner.
- **The read/seen/recalled marks are your declaration of how you know each source.** The checker can't verify them. My "recalled" for Gardiner means I know it from memory and I haven't confirmed it today.

**Next steps:** look up Gardiner in a library catalogue (after that you can mark it **seen**), and remove or replace reference 2.

### Answer B

I couldn't look either reference up. There's no checker script in the working directory, and the DOI and Crossref requests needed approval, so they didn't run. Both labels below are therefore **recalled**: neither is **read** (I didn't open the source) or **seen** (I didn't find it in a live database).

| # | Reference | Label | Verdict |
|---|---|---|---|
| 1 | Gardiner, A. H. *Egyptian Grammar*. Oxford, 1957. | **Recalled** | **Probably real and correct.** This is Sir Alan Gardiner's *Egyptian Grammar: Being an Introduction to the Study of Hieroglyphs*, 3rd revised edition, Griffith Institute, Oxford, 1957. Earlier editions came out in 1927 and 1950. The citation is a bit thin: it should name the edition and the publisher (Griffith Institute / Ashmolean Museum). |
| 2 | Nobody, N. 2019. A new result. *J Imaginary Biol* 5:1-9. doi:10.1000/imaginary.2019.1 | **Recalled** | **Very likely made up or a placeholder.** The prefix `10.1000` is the DOI Foundation's example prefix from its documentation, not a publisher's. I know of no journal called *J Imaginary Biol*. "Nobody, N." and "A new result" look like dummy text. |

**What this check proves:** nothing. Without a lookup it's my memory plus pattern-spotting: a real, well-known book, and a DOI prefix, journal and author that look fake.

**What a proper checker would prove, and what it wouldn't:**
- **A resolving DOI or a Crossref/WorldCat match** shows that a record with that identifier or those details exists. It doesn't show that the author, year, pages or edition in your citation match that record unless you compare them field by field.
- **Even a confirmed match** doesn't show that the source says what your text cites it for. Only reading the source (**read**) can show that.
- **A failed lookup** doesn't prove a reference is fake. Many books, older works and grey literature have no DOI or Crossref entry, so Gardiner might not show up in Crossref at all. That's why a library catalogue is the right check for monographs.

To get **seen**-level evidence, approve the network calls and I'll resolve the DOI and search Crossref and a library catalogue.

---

## P19

**Prompt:** Write the methods section for this analysis from my methods record: Reads: SRR1234567 (3 treated, 3 control) aligned to GRCh38 with tool A v1.2; counts from tool B v3.1; differential test with Benjamini-Hochberg correction at 0.05; seed 42.. Use exact versions and parameters, and list anything the record does not give me so I can fill it in.

### Answer A

## Methods (draft)

**Read alignment.** Sequencing reads (SRA accession SRR1234567; three treated and three control samples) were aligned to the human reference genome GRCh38 using tool A v1.2 [ALIGNMENT PARAMETERS].

**Read quantification.** Gene-level read counts were generated using tool B v3.1 [ANNOTATION SOURCE AND RELEASE; COUNTING PARAMETERS].

**Differential expression analysis.** Differential expression between treated and control samples was tested using [TEST/TOOL AND VERSION]. P-values were adjusted for multiple testing using the Benjamini–Hochberg procedure, and features with an adjusted p-value below 0.05 were considered significant. The random seed was set to 42 [STEP(S) THE SEED APPLIES TO].

---

## Missing from your record (please fill in)

**Things to check first:**
1. **Accession mismatch.** SRR1234567 is a single SRA *run* accession, but you describe six samples. You probably need the six SRR IDs, or the BioProject (PRJNA…) / GEO series (GSE…) accession.
2. **Tool names.** "tool A" and "tool B" look like placeholders. I kept them as written. Please give the real names (for example STAR, HISAT2, featureCounts, HTSeq).
3. **Differential test.** The record gives the correction method and threshold but not the test or software (for example DESeq2 Wald test, edgeR QL F-test, limma-voom), its version, or the R/Python version.

**Alignment:**
- Reference build details: primary assembly or full, source (Ensembl/GENCODE/UCSC), and release
- Non-default aligner parameters, or a note that defaults were used
- Read pre-processing such as adapter or quality trimming, with tool and version
- Library type: single- or paired-end, read length, strandedness

**Quantification:**
- Gene annotation (GTF) source and release, for example GENCODE v44
- Counting level (gene or transcript) and how multi-mapping and overlapping reads were handled
- Strandedness setting

**Differential analysis:**
- Design formula and covariates, if any (batch, pairing)
- Pre-filtering of low-count genes
- Normalization method
- Whether a fold-change threshold or shrinkage was used (for example lfcShrink with apeglm)
- Which step the seed of 42 controls. Many DE tools are deterministic, so name the step it affects.

**Reproducibility (often required):**
- Sequencing platform
- Where the code is available (repository or DOI)
- Compute environment (container or conda environment)

If you send me these details, I'll replace the bracketed placeholders and finish the section.

### Answer B

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

| Item | Missing |
|---|---|
| Data | Repository, run accession for each sample, retrieval date, organism and sample type, treatment details |
| Library | Single- or paired-end, read length, strandedness, sequencing platform |
| Reference | GRCh38 patch and source, primary assembly or with alts |
| Annotation | Source and release (none is given, but counting needs one) |
| QC and trimming | Tool, version, parameters |
| Alignment | Real tool name, all parameters, mapping rates |
| Duplicates | Marked or removed? |
| Counting | Real tool name, parameters, multimapping and strandedness settings |
| Test | Method, tool and version, normalisation, model or design formula, covariates or batch |
| Filtering | Low-count filter and the number of genes tested |
| Effect size | Measure, any shrinkage, any fold-change cutoff |
| Exclusions | Samples dropped and why (or "none") |
| Seed | Which step the seed of 42 applies to |
| Environment | Language and version, environment or container file |
| Code | Repository URL, tag or commit, archive DOI |

One more point for the write-up: with three samples per group, statistical power is limited. When you write the results, report effect sizes alongside the adjusted p-values, and don't read a gene that isn't significant as evidence that it has no effect.

---

## P05

**Prompt:** What kind of identifier is NM_000546.6, and what does the .6 at the end mean? What should I record alongside it?

### Answer A

## What NM_000546.6 is

It's an **NCBI RefSeq accession.version**. Here's how it breaks down:

| Part | Meaning |
|---|---|
| `NM_` | A RefSeq **mRNA (transcript)** record that has been curated. The underscore marks it as RefSeq rather than a GenBank/INSDC accession, which never has one. |
| `000546` | The accession number. It's stable and identifies this record over time. |
| `.6` | The **sequence version**. This is the 6th version of the sequence stored under this accession. |

NM_000546 is the reference transcript for human **TP53**. Keep in mind it identifies a *transcript*. The gene and the protein have their own IDs: the protein is an `NP_` record, and the gene has an NCBI Gene ID.

## What the `.6` means in practice

The version goes up every time the **sequence itself** changes, for example when an exon boundary or a UTR is corrected. Changes to annotation alone don't bump it. So `NM_000546.5` and `NM_000546.6` are **different sequences**. Coordinates such as HGVS variant names like `NM_000546.6:c.215C>G` can point to a different base if you use the wrong version. Without the version, "NM_000546" doesn't pin down one sequence. Before mixing data from two versions, compare their sequences.

The skill's checker confirms the format: it's RefSeq, version 6. The meanings of the `NM_` prefix come from general knowledge, and the script marks them as unverified. NCBI's RefSeq prefix documentation is the authority.

## What to record alongside it

Use separate columns, and store everything as text so a spreadsheet can't reformat it:

1. **Accession** (`NM_000546`) and **version** (`6`) in separate fields, or always the full `NM_000546.6`.
2. **Source database**: NCBI RefSeq, plus the **RefSeq release number** or the annotation release you took it from.
3. **Download or access date**, and ideally a **checksum** of the file you downloaded.
4. **Organism** (*Homo sapiens*) and the **genome build** it was aligned to or annotated on (GRCh38 or GRCh37). Don't mix builds.
5. **The entity type and related IDs**: that it's a transcript, the gene (TP53, NCBI Gene ID 7157, HGNC symbol), and the protein `NP_` accession.version if you use it.
6. **Mapping provenance**, if you mapped it to Ensembl (ENST…) or UniProt: the tool, its release, the date, and how you picked among several matches. Keep the unmapped and ambiguous lists too.
7. Optionally, whether it's a **MANE Select** transcript. Clinical variant reporting usually expects the MANE Select transcript. Check which version MANE currently names before reporting variants against it.

The test of a good record is that someone else can follow it and retrieve exactly the same sequence you used.

### Answer B

**NM_000546.6** is an **NCBI RefSeq accession.versioned identifier** for a nucleotide sequence.

**How to read it**

| Part | Meaning |
|---|---|
| `NM_` | RefSeq prefix for a **curated mRNA (transcript)** record. Compare: `XM_` = predicted mRNA, `NR_` = curated non-coding RNA, `NP_` = curated protein, `NC_` = chromosome, `NG_` = genomic region. |
| `000546` | The stable accession number. NM_000546 is the human **TP53** transcript (variant 1). |
| `.6` | The **sequence version**. NCBI bumps it every time the actual nucleotide sequence changes. `.6` is the sixth sequence revision under this accession. |

**Why the version matters:** different versions of the same accession can have different sequences, UTR lengths, or exon boundaries. That means a coordinate like `c.215C>G` can point to a different base, or not exist, on `.5` versus `.6`. Changes that only touch annotation, such as notes or references, don't bump the version. So `NM_000546.6` always means exactly the same sequence. HGVS nomenclature requires the versioned accession for this reason.

**What to record with it**

1. **The full versioned accession** (`NM_000546.6`), never just `NM_000546`.
2. **Gene symbol and a stable gene ID**, such as `TP53`, HGNC:11998, and NCBI Gene ID 7157.
3. **The matching protein accession** if you report protein changes. For this transcript that's NP_000537.3. Check the record to confirm it.
4. **Genome assembly** (GRCh38 or GRCh37) if you also give genomic coordinates, plus the chromosome accession, e.g. `NC_000017.11` for chr17 on GRCh38.
5. **Transcript-set status.** Note whether it's the **MANE Select** transcript, and its Ensembl equivalent (an `ENST…` ID with its own version). I believe NM_000546.6 is the MANE Select for TP53, but confirm it against the current MANE release.
6. **Provenance.** Record the source (NCBI RefSeq), the annotation release or date you retrieved it, and any tool versions used, such as the VEP, ANNOVAR, or Mutalyzer release.
7. **Variant descriptions in full HGVS form**, e.g. `NM_000546.6:c.743G>A (p.Arg248Gln)`. I'm quoting that example from memory, so validate it with a tool like Mutalyzer or VariantValidator before you use it.

Recording these lets someone else reproduce your result exactly, even after RefSeq updates the transcript to a `.7`.

---

## P16

**Prompt:** What is the monoisotopic mass of the peptide DRVYIHPF? Show how you got it and say whether you used average or monoisotopic residue masses.

### Answer A

**The monoisotopic mass of DRVYIHPF (angiotensin II) is 1045.5345 Da** (neutral molecule, M).

I used **monoisotopic residue masses**: each residue's mass is built from the most abundant isotope of every element (¹²C, ¹H, ¹⁴N, ¹⁶O). Average masses would not work here because they give the average molecular weight instead.

**How I got it:** the mass is the sum of the residue masses, plus one water (H₂O) for the free N- and C-termini.

| Residue | Monoisotopic residue mass (Da) | Running total |
|---|---|---|
| D (Asp) | 115.02694 | 115.02694 |
| R (Arg) | 156.10111 | 271.12805 |
| V (Val) | 99.06841 | 370.19646 |
| Y (Tyr) | 163.06333 | 533.25979 |
| I (Ile) | 113.08406 | 646.34385 |
| H (His) | 137.05891 | 783.40276 |
| P (Pro) | 97.05276 | 880.45552 |
| F (Phe) | 147.06841 | 1027.52393 |
| + H₂O (termini) | 18.01056 | **1045.53449** |

The elemental formula is C₅₀H₇₁N₁₃O₁₂.

- **[M+H]⁺:** 1045.5345 + 1.00728 (proton) = **1046.5418 m/z**. This is the value you'd look for in ESI or MALDI mass spectrometry.
- **Average mass**, for comparison: about 1046.2 Da.

### Answer B

**Monoisotopic mass of DRVYIHPF = 1045.5345 Da** (neutral peptide). This sequence is angiotensin II.

I used **monoisotopic** residue masses, meaning each residue is built from the most abundant isotope of each element (¹²C, ¹H, ¹⁴N, ¹⁶O). I did not use average residue masses.

### Calculation

A peptide's mass is the sum of its residue masses plus one water (H₂O) for the free N-terminal H and C-terminal OH.

| Residue | Monoisotopic residue mass (Da) | Running total |
|---|---|---|
| D (Asp) | 115.02694 | 115.02694 |
| R (Arg) | 156.10111 | 271.12805 |
| V (Val) | 99.06841 | 370.19646 |
| Y (Tyr) | 163.06333 | 533.25979 |
| I (Ile) | 113.08406 | 646.34385 |
| H (His) | 137.05891 | 783.40276 |
| P (Pro) | 97.05276 | 880.45552 |
| F (Phe) | 147.06841 | 1027.52393 |
| + H₂O | 18.01056 | **1045.53449** |

Molecular formula: C₅₀H₇₁N₁₃O₁₂.

### Related values
- **[M+H]⁺** = 1045.5345 + 1.00728 (proton) = **1046.5418**, which is the singly charged ion you'd see by mass spectrometry.
- **[M+2H]²⁺** = (1045.5345 + 2 × 1.00728) / 2 = **523.7745**.
- **Average mass**, from average residue masses, is about **1046.19 Da**. It is about 0.65 Da higher because it includes the natural ¹³C and other heavy isotopes. Don't use it to match high-resolution MS peaks.

This assumes free termini and no modifications, such as N-terminal acetylation or C-terminal amidation.

---

## P11

**Prompt:** My classifier gets 98% accuracy on a dataset where 2% of the examples are positive. Is that good? What should I report instead?

### Answer A

**Probably not.** A model that predicts "negative" for every example also gets 98% accuracy, so your number doesn't show the classifier has learned anything. Accuracy is dominated by the 98% majority class and barely moves no matter how well you handle positives.

## What to report instead

**1. The confusion matrix (TP, FP, FN, TN).** Always include it, because it lets readers compute any other metric themselves.

**2. Precision and recall for the positive class**
- **Recall (sensitivity)** = TP / (TP + FN): the share of real positives you catch.
- **Precision** = TP / (TP + FP): the share of your positive predictions that are correct.
- The all-negative baseline scores **0 recall**, which exposes it right away.

**3. F1 (or F-beta).** This is the harmonic mean of precision and recall. Use F2 if missing a positive costs more than a false alarm, or F0.5 if the reverse is true.

**4. PR-AUC (average precision)** for a threshold-independent summary.
- A random classifier's PR-AUC is about **0.02**, the base rate. That makes the baseline obvious, and 0.40 vs 0.60 is a meaningful difference.
- Prefer it over **ROC-AUC** for rare positives. ROC-AUC can look great (e.g. 0.95) while precision is poor, because the huge negative pool keeps the false positive rate low even when there are many false positives. ROC-AUC is still fine to report alongside it.

**5. Optional extras**
- **Balanced accuracy** = (recall + specificity) / 2. The trivial model scores 0.5.
- **MCC (Matthews correlation coefficient)** gives one number that accounts for all four cells. 0 means no better than chance.
- **Precision at k / recall at a fixed precision** if you'll act on a top-k list or need to stay under a false alarm budget.

## Practical tips
- **Compare against baselines.** Report the majority-class predictor and a random classifier at the 2% base rate next to your model.
- **Choose the threshold on purpose.** The default of 0.5 is often wrong for imbalanced data. Choose it on a validation set based on what errors cost.
- **Use stratified splits** so every fold has positives. Also report how many positives the test set contains: with 2% positives, 1,000 test examples give only about 20, so your metrics will be noisy. Add confidence intervals (e.g. bootstrap).
- **Check calibration** if you'll use the probabilities themselves. Resampling or class weights during training distort them.

**Bottom line:** Report the confusion matrix, precision, recall, F1 and PR-AUC, each next to the trivial baseline. Accuracy by itself doesn't tell you much here.

### Answer B

**No, 98% accuracy tells you almost nothing here.** A model that always predicts "negative" also gets 98%, because 98% of your examples are negative. Your classifier might be finding no positives at all.

## What to report instead

**1. The confusion matrix.** Give the raw counts of true positives (TP), false positives (FP), false negatives (FN) and true negatives (TN) on the test set. Every other metric comes from these, and readers can check your numbers.

**2. Metrics that focus on the positive class:**

| Metric | Question it answers | Trivial "all negative" model gets |
|---|---|---|
| **Recall** (sensitivity) = TP/(TP+FN) | Of the real positives, how many did we find? | 0 |
| **Precision** (PPV) = TP/(TP+FP) | Of the examples we flagged, how many are really positive? | undefined / 0 |
| **F1** | Combines precision and recall into one number | 0 |
| **MCC** (Matthews correlation coefficient) | Uses all four cells; 0 means chance level | 0 |
| **Balanced accuracy** | The average of recall on each class | 0.5 |

**3. Metrics that don't depend on a threshold:**
- **Average precision (AUPRC)** is the best single number for rare positives. The random baseline equals the prevalence, so **0.02**. Always state that baseline next to your score.
- **AUROC** is fine to report, but it can look good (for example 0.95) while precision is still poor. That happens because even a small false-positive rate on the large negative class produces many false positives. Report it alongside AUPRC, not instead of it.

**4. Baselines.** Include the majority-class predictor and a simple model, such as logistic regression on obvious features. This shows how much your model actually adds.

**5. Uncertainty.** With only 2% positives, a test set of 1,000 has about 20 positives. One extra hit moves recall by 5 percentage points. Report the number of positives in the test set and give confidence intervals, for example by bootstrapping the test set.

**6. How you chose the threshold.** Choose it on validation data, not test data, and base it on the real cost of a missed positive compared with a false alarm. If the prevalence in real use differs from 2%, precision will change too, so say what prevalence you assumed.

## Also check
- **Splits.** If your data has related groups (the same patient, similar sequences, the same batch), split by group. Otherwise the test scores will be too high.
- **Resampling.** If you oversampled or used SMOTE, apply it only to the training folds. Evaluate on data with the true 2% prevalence.

**What to write in the paper:** something like "Recall 0.70 [95% CI …], precision 0.35, AUPRC 0.41 (baseline 0.02), MCC 0.48, with 40 positives in the test set," plus the confusion matrix. Report accuracy only as a side note, if at all.

---

## P23

**Prompt:** What do the columns of this VCF line mean, including the genotype codes? chr1	100	.	A	G	50	PASS	.	GT:DP	0/1:12	1|1:9. Is the position 0-based or 1-based?

### Answer A

## The columns, in order

| # | Column | Value | Meaning |
|---|--------|-------|---------|
| 1 | **CHROM** | `chr1` | Chromosome or contig name |
| 2 | **POS** | `100` | Position of the first base in REF, **1-based** |
| 3 | **ID** | `.` | Variant identifier, such as an rsID. `.` means missing |
| 4 | **REF** | `A` | Reference allele at that position |
| 5 | **ALT** | `G` | Alternate allele(s), comma-separated if there are several |
| 6 | **QUAL** | `50` | Phred-scaled quality of the variant call. 50 means P(no variant) = 10⁻⁵ |
| 7 | **FILTER** | `PASS` | Passed all filters. Otherwise this column lists the names of the filters it failed |
| 8 | **INFO** | `.` | Site-level annotations as `key=value;...`. None here |
| 9 | **FORMAT** | `GT:DP` | Defines the order of the per-sample fields that follow |
| 10 | **Sample 1** | `0/1:12` | GT=`0/1`, DP=12 |
| 11 | **Sample 2** | `1\|1:9` | GT=`1\|1`, DP=9 |

## Genotype (GT) codes

Each number is an index into the alleles: **0 = REF (A)**, **1 = first ALT (G)**, 2 = second ALT, and so on. `.` means a missing allele, for example `./.`.

The separator matters:
- **`/`** means **unphased**. The two alleles are known, but not which chromosome copy each one is on.
- **`|`** means **phased**. The order is meaningful: the left allele is on one haplotype and the right allele is on the other.

So:
- **Sample 1, `0/1`**: heterozygous A/G, unphased.
- **Sample 2, `1|1`**: homozygous alternate G/G, marked as phased. For a homozygous call, phasing makes no practical difference.

**DP** is read depth, meaning the number of reads covering the site in that sample (12 and 9 here).

## Coordinates

**VCF positions are 1-based.** `POS=100` means the 100th base of chr1. For indels, POS points to the padding base just before the event.

This differs from **BED** and BAM's internal representation, which are 0-based, half-open. The same SNP would be written in BED as `chr1  99  100`.

### Answer B

This is one data line from a VCF file. It has the 8 fixed columns, a FORMAT column, and then one column per sample.

| # | Column | Value | Meaning |
|---|---|---|---|
| 1 | **CHROM** | `chr1` | Chromosome or contig name. The `chr` prefix is a UCSC/GENCODE-style name. Ensembl uses `1`, so check that this matches your reference. |
| 2 | **POS** | `100` | Position of the first base of REF on the chromosome. It is **1-based** (see below). |
| 3 | **ID** | `.` | Variant identifier, such as an rsID. `.` means there isn't one. |
| 4 | **REF** | `A` | Reference allele, the base in the reference genome at this position. |
| 5 | **ALT** | `G` | Alternate allele(s), comma-separated if there are several. Here it is a single A→G SNV. |
| 6 | **QUAL** | `50` | Phred-scaled quality for the site: the probability the ALT call is wrong is 10^(−50/10) = 10⁻⁵. It applies to the whole site, not to each sample. |
| 7 | **FILTER** | `PASS` | The site passed all filters. Otherwise this column lists the names of the filters that failed, or `.` if no filtering was done. |
| 8 | **INFO** | `.` | Site-level annotations such as `DP=21;AF=0.75`. `.` means none. |
| 9 | **FORMAT** | `GT:DP` | Lists the colon-separated fields in each sample column, in order. |
| 10 | Sample 1 | `0/1:12` | GT = `0/1`, DP = 12 |
| 11 | Sample 2 | `1\|1:9` | GT = `1\|1`, DP = 9 |

### Genotype (GT) codes
- Each number is an allele index: **0 = REF** (`A`), **1 = first ALT** (`G`), 2 = second ALT, and so on. `.` means a missing allele, as in `./.`.
- The separator shows phasing:
  - **`/` = unphased.** You know which alleles are present but not which chromosome copy each one is on.
  - **`|` = phased.** The left allele and the right allele are on specific haplotypes, and that order is consistent with other phased sites in the same phase set.
- **Sample 1, `0/1`:** heterozygous A/G, unphased.
- **Sample 2, `1|1`:** homozygous alternate G/G. It is marked phased, but phasing tells you nothing for a homozygote because both copies are the same.

### DP (FORMAT field)
DP is the read depth for each sample at this site: 12 reads for sample 1 and 9 for sample 2. The header defines what counts. Callers often count only reads that pass quality filters. A depth of 9–12 is modest. For a heterozygous call like `0/1`, check allele depths (`AD`) if they are available. With 12 reads, a 0/1 call could come from a split like 10:2, which may be an error rather than a true het.

### 0-based or 1-based?
**VCF POS is 1-based.** `POS=100` means the 100th base of chr1, with the first base counted as 1.
- **BED** files are 0-based and half-open, so this SNV would be `chr1  99  100` in BED. Mixing the two conventions is the most common source of off-by-one errors.
- **BCF** (binary VCF) stores positions 0-based internally, but tools such as `bcftools` show them 1-based.
- For **indels**, POS is the base *before* the event, and REF/ALT include that padding base. For example, a deletion of C after A at 100 is written `POS=100 REF=AC ALT=A`.

The meaning of each field (DP, any AD or GQ, and the FILTER names) is defined in the `##INFO`, `##FORMAT` and `##FILTER` lines in the file's header. Check those, because callers differ in how they define DP.

---

## P06

**Prompt:** I have whole-genome sequences from patients with coded sample IDs only. Is this patient data anonymous, and can I share it?

### Answer A

**No, it isn't anonymous, and you shouldn't share it openly.** Whether you can share it in a restricted way depends on what the participants consented to and what your approvals and agreements say, not on how the IDs are coded.

## Why coded IDs don't make a genome anonymous

- **Coded isn't anonymous.** A coded ID means a key exists somewhere that links the code back to the person. Most legal frameworks treat that as pseudonymised data, which is still personal data. Under GDPR, for example, pseudonymised genetic data is still special-category personal data.
- **The genome itself identifies the person.** Each whole genome belongs to one person. Even with no ID at all, it can be matched against consumer genealogy databases, forensic databases or other research datasets. People have been re-identified from genomic data alone, for example by inferring surnames from Y-chromosome markers.
- **It also reveals relatives.** Parents, siblings and children share large parts of the genome and never consented to anything. Sharing one person's genome exposes their family too.
- **Linked information makes it worse.** Phenotype, age, diagnosis, hospital or a rare variant can each narrow down who the person is.
- **Summaries can leak too.** Even allele-frequency summaries of a cohort can sometimes reveal whether a given person was in the study. Check current guidance before releasing them.

## Before sharing anything

1. **Read the consent form.** Does it allow data sharing, with whom, for what purpose, and outside your institution or country? If it says nothing, assume sharing isn't allowed.
2. **Check the ethics approval and any data-use agreement.** A new collaborator, a new purpose, a commercial partner or a transfer abroad may each need new approval.
3. **Talk to your institution's data steward, privacy office or ethics committee.** They can give a definitive answer and I can't.
4. **Choose the right sharing route:**

| Option | When it fits |
|---|---|
| Controlled-access repository (e.g. EGA, dbGaP, or a national equivalent) | The usual route for patient whole genomes when consent allows sharing. Requesters apply and sign an agreement. |
| A data-use agreement directly with a named collaborator | One-off sharing with a known group, with secure transfer and no email attachments. |
| Summary results, code and checksums only | When the consent doesn't cover sharing the raw data. Avoid tables with counts of 1 or 2. |
| Public or open release | Almost never right for patient whole genomes unless participants explicitly agreed to open release. |

## Keep the data protected meanwhile

- Store the code key separately from the data and restrict who can open it.
- Keep sample IDs out of file names, code, logs, git history and public repositories.
- Don't upload the sequences to online tools, cloud services or AI chat assistants unless your data agreement allows it and the service's terms on keeping or training on data are acceptable. Use local or approved secure computing.
- Record a retention and deletion date, and who has access.

This is general guidance, not legal advice. The rules differ by country (GDPR, HIPAA and others) and by institution. If you tell me the country, what the consent form says and who you want to share with, I can help draft the questions for your data steward or a data-sharing checklist.

### Answer B

# Coded WGS data is not anonymous

Coded sample IDs make the data **pseudonymized**, not anonymous. Whole-genome data is also identifying by nature, so removing names and IDs can't fully de-identify it.

## Why coding isn't enough

1. **Someone still holds a key.** Usually a clinic, biobank or collaborator can link the codes back to patients. While that key exists anywhere, the data counts as personal data under most frameworks.
2. **The genome identifies the person.** A whole genome is unique to one individual and stays the same for life. It also reveals information about their relatives. Known ways to re-identify people from genomes include:
   - **Surname inference:** Y-chromosome markers can be matched against genealogy databases (Gymrek et al., *Science* 2013).
   - **Consumer genealogy matching:** uploading a genome to GEDmatch or similar sites can find relatives and then the person. This is how the Golden State Killer was identified.
   - **Linking to other genotype data** the person has elsewhere, such as clinical tests, other studies or direct-to-consumer services.
   - **Predicting visible traits** and inferring ancestry.
   - **Membership inference:** even pooled summary statistics can sometimes show whether a person was in a study (Homer et al., 2008).
3. **The files themselves may leak identity.** VCF and BAM headers, read-group tags, file names, dates, rare diseases and small cohorts can all point to individuals.

## What the main rules say

- **GDPR (EU/UK):** Pseudonymized data is still personal data (Recital 26). Genetic data is a special category under Article 9, so you need a legal basis plus an Article 9 condition, and often a DPIA. Sending it outside the EEA has its own transfer rules.
- **HIPAA (US):** Coded data can sometimes count as de-identified under Safe Harbor. That requires the code not to be derived from patient information and the key not to be shared. For whole genomes, most institutions don't treat Safe Harbor as sufficient and use Expert Determination or a limited data set with a data use agreement instead.
- **US Common Rule and NIH:** OHRP guidance on coded data may mean your work isn't "human subjects research" if you can't access the key. That's separate from whether you can share the data. Under the NIH Genomic Data Sharing Policy, consent for broad sharing is expected, and data usually goes to controlled-access repositories like dbGaP.
- **Other countries** have their own rules (Canada, Australia, China's HGRAC rules, and others), and some limit genomic data leaving the country.

## Can you share it?

Probably yes, but only through controlled channels, not openly. Check these first:

1. **Consent:** Did the patients agree to data sharing, and to what scope (open, controlled access, particular research uses)? The consent forms set the upper limit on what you can do.
2. **Ethics approval:** Does your IRB or ethics committee approval cover sharing with this recipient?
3. **Agreements:** Do your data use or material transfer agreements with the data source allow passing it on?
4. **Recipient and location:** Who will receive it and where? A collaborator under a data use agreement is very different from a public repository or another country.

Common ways to share WGS data safely:
- **Controlled-access repositories** such as dbGaP, EGA, AnVIL or a national equivalent, with a data access committee reviewing requests.
- **A data use agreement** with each recipient that bans re-identification attempts and onward sharing and sets security requirements.
- **Federated or trusted research environments**, where others run analyses without downloading the data.
- **Sharing less:** aggregate results, variant-level summaries or specific regions instead of full genomes. These still carry some risk and may need controls of their own.
- **Cleaning the files:** strip identifying metadata from headers and file names, keep the code key away from the recipient, and record how you did it.

**Next step:** talk to your institution's privacy or data protection officer (or HIPAA privacy officer) and your IRB or ethics committee before sending anything. This is general information, not legal advice, and the answer depends on your country, the consent forms and the recipient.

If you tell me your country, what the consent forms say and who you want to share with, I can narrow this down.

---

## P04

**Prompt:** I have RNA-seq from treated and untreated cells, three replicates each, sequenced in two batches. Plan the analysis. State the claim so the data could show it false, name the null model, list what to record about the data, and say which skill handles each step.

### Answer A

# RNA-seq analysis plan: treated vs untreated, 3 + 3, two batches

**Check the batch layout first.** Everything below depends on which samples went into which batch. If all treated samples are in one batch and all untreated in the other, treatment and batch are confounded. No model can separate them, and the data cannot support a treatment claim. If the split is something like batch A = 2 treated + 1 untreated and batch B = 1 treated + 2 untreated, you can proceed. With a model of `~ batch + condition`, 6 samples leave only **3 residual degrees of freedom**, so power is low. Only large effects on well-expressed genes will be found.

## 1. Claim

> In these cells, treatment changes the mean expression of a set of genes. The change is beyond what batch and replicate-to-replicate variation explain, and its size is at least |log2 fold change| > 1 (twofold), set before looking.

**What would show it false:**
- No gene passes FDR < 0.05 with |log2FC| > 1 in the batch-adjusted model, or
- the number of hits is no greater than you get from swapping treatment labels within batches, or
- after removing batch, samples do not separate by treatment on PC1/PC2 and replicates do not group together.

If you have a specific pathway or gene set in mind, add it as a second claim now, before looking, and name its direction.

## 2. Null model

- **Main null:** for each gene, a negative-binomial GLM `counts ~ batch + condition` where the treatment coefficient is 0. Dispersion is shrunk across genes (DESeq2 or edgeR).
- **Empirical check:** swap treatment labels within batches and rerun. With 3 vs 3 there are only 10 distinct splits, and fewer once you keep them inside batches. So this is a sanity check on how many hits chance produces, not a precise p-value.
- **Enrichment null:** a gene set is compared against a background of genes that were expressed and tested, not the whole genome. Correct for gene length or expression level if the method needs it.

## 3. What to record about the data

| Item | Record |
|---|---|
| Samples | ID, condition, replicate, **batch**, RNA extraction date, library prep date and kit, sequencing run, lane, index |
| Biology | Organism, cell line and source, passage number, authentication or mycoplasma test, treatment agent, dose, duration, vehicle control |
| Library | Stranded or not, poly-A or rRNA depletion, read length, single or paired end, RIN |
| Reference | Genome build (e.g. GRCh38) and annotation release (e.g. GENCODE v__/Ensembl __), never mixed |
| Raw files | FASTQ names, read counts, md5 checksums, date received |
| Software | Versions and parameters for QC, trimming, aligner or quantifier, DE package |
| Access | Licence or consent; whether the data will be deposited in GEO/ENA, and the accession |
| Decisions | Claim, null, thresholds, stopping rule, all fixed and committed **before** the DE results are seen |

## 4. Steps and the skill for each

| # | Step | Skill | Output | Check |
|---|---|---|---|---|
| 0 | Confirm the batch × condition layout; work out what effect size 3+3 can detect | `experimental-design` | Layout table, detectable effect | Batch is not confounded with treatment |
| 1 | Pin the genome build, annotation and IDs | `biological-databases` | Versioned reference | Build matches across all files |
| 2 | Validate the FASTQ files (Phred+33, pairing) | `sequence-formats` | Validated inputs | Read counts match the facility report |
| 3 | QC, trimming, mapping or quantification (STAR + featureCounts, or salmon), strandedness | `ngs-pipelines` | Count matrix, QC report | Mapping rate, assigned rate, inferred strand all consistent across samples |
| 4 | Sample QC: library sizes, PCA, correlation heatmap, before and after batch | `omics-data-analysis` | Plots, outlier list | Replicates group together; batch is visible and then accounted for |
| 5 | DE test with `~ batch + condition`, log fold changes shrunk | `omics-data-analysis` | DE table | p-value histogram looks right (flat with a spike near 0) |
| 6 | Multiple testing (BH), label-swap null, enrichment against the tested background | `sequence-statistics` | FDR, hit count compared with null | Real hits exceed the label-swap hits |
| 7 | Environment, seeds, pipeline, tests | `reproducible-research-code` | Repository, lockfile | A clean rerun gives identical counts |
| 8 | Audit before any claim | `bioinformatics-review` | Ranked findings | No unresolved high-severity findings |
| 9 | Methods and figures | `research-writing-reporting` | Write-up | Claim wording matches the evidence |

**Toy run before the real data:** take a small subset (e.g. 100k reads per sample, one chromosome). Add a known fold change to about 50 genes in a simulated count matrix and confirm the pipeline recovers them. Also confirm a label-swap run finds about nothing.

## 5. Controls

- **Positive:** genes known to respond to this treatment, e.g. direct targets of the pathway it hits. Write the list down now. If they don't move, suspect the treatment or a label swap before trusting the other results.
- **Negative:** housekeeping genes, plus the label-swap null. Also check for a swap directly with sex genes (XIST/Y genes) or SNP genotypes if the samples could differ.
- **Independent:** qPCR on a few top hits using new biological replicates, or a public dataset with the same treatment.

## 6. Comparisons and stopping rule

- About 15–20k expressed genes are tested, all corrected with BH at FDR 0.05 and |log2FC| > 1. Gene sets get their own BH correction.
- **Fixed before looking:** one model (`~ batch + condition`), one filter for low-count genes, one threshold. A sample is dropped only by a QC rule written beforehand, never because the DE results improve without it. Do not try ComBat, RUV, DESeq2 and edgeR and report whichever looks best. If you run a second method, report both.
- **What triggers a second look:** positive controls don't move; PC1 tracks batch even after correction; the p-value histogram is U-shaped or slopes up; a replicate is an outlier on its own.
- **What ends it:** the hit count clearly beats the null, positive controls behave, and qPCR confirms at least the top hits. Otherwise report it as a negative or underpowered result.

## 7. Limits

- With 3 vs 3 and two batches, small changes and low-expressed genes will be missed. A gene not passing is not proof it didn't change.
- Cell-line replicates are usually technical or passage replicates, not independent biological units. Say which yours are.
- Bulk RNA-seq cannot tell a change in expression per cell from a change in which cell states make up the culture.

If you tell me the batch layout, I'll check whether it is confounded and work out the smallest fold change you can realistically detect. I can also save this as a filled-in `analysis-plan.md`.

### Answer B

# RNA-seq analysis plan: treated vs untreated, 3 replicates each, 2 batches

## About skills

None of the skills available to me covers RNA-seq. I have no alignment, quantification, or differential-expression skill, and I won't make one up. The only one that applies is **dataviz**, for the plots. Everything else is ordinary analysis code (R/Bioconductor or Python) that I would write and run directly. The table at the end lists each step against this.

## 0. Check the batch layout first

This decides whether the experiment can answer the question at all.

| Layout | Consequence |
|---|---|
| All treated in batch A, all untreated in batch B | **Fully confounded.** The treatment effect can't be separated from the batch effect, and no statistical method fixes that. You would need more samples or have to re-sequence. |
| 2T+1U in batch A, 1T+2U in batch B (or similar) | Batch and treatment are partly crossed, so you can estimate both. |
| Balanced across batches | Best case. |

Write down the sample-to-batch table before any analysis.

## 1. The claim, stated so the data could prove it wrong

Settle these before looking at any results:

- **Primary claim:** "Treatment changes the expression of gene G (or a named gene set S) by more than 1.5-fold (|log2FC| > 0.585), after adjusting for batch."
  - It is false if the batch-adjusted estimate's confidence interval lies inside ±0.585, or if the test against that threshold fails at the chosen FDR.
- **Secondary, exploratory claim:** "Treatment changes the expression of at least some genes, transcriptome-wide." This one is weaker. With n=3 it can only fail by finding zero genes at FDR 0.05, and that result also fits low statistical power. So report it as exploratory, not as a test.
- Fix in advance: the fold-change threshold, the FDR level (0.05), the gene-filtering rule, and the rule for excluding outlier samples.

## 2. Null model

- **Model:** a negative binomial GLM for each gene, with design `~ batch + condition` (DESeq2 or edgeR).
- **H₀:** for the primary claim, the condition coefficient satisfies |β| ≤ 0.585 (DESeq2 `lfcThreshold`, `altHypothesis="greaterAbs"`). For the exploratory scan, β = 0.
- **Multiple testing:** Benjamini–Hochberg across the genes tested.
- **Permutation as a check:** 3 vs 3 allows only C(6,3)=20 relabelings, and fewer if they must stay within batch. The smallest achievable p-value is then about 0.05–0.1, so a permutation test can only be a sanity check here, not the main test.
- **Power warning:** with 3 replicates per group, only fairly large effects will be detected. "Not significant" does not mean "no effect."

## 3. What to record about the data

- **Samples:** ID, condition, batch, replicate, collection date, operator, passage number, treatment dose and duration.
- **RNA and libraries:** extraction date, RIN, kit, library-prep batch, any spike-ins.
- **Sequencing:** platform, run or lane, read length, single- or paired-end, strandedness, raw read count.
- **Processing:** reference genome and annotation version (e.g. GENCODE vXX), aligner or quantifier with version and parameters, mapping rate, assigned-read rate, duplication rate.
- **Analysis:** package versions, random seeds, gene-filter rule, every excluded sample with its reason, and the pre-registered claim from section 1 with a date.
- **Raw files:** checksums of the raw FASTQs and count matrices.

## 4. Steps and who handles them

| # | Step | Handled by |
|---|---|---|
| 1 | Write down the claim, thresholds and sample/batch table | You. I can draft it with no skill. |
| 2 | QC of raw reads (FastQC, MultiQC) | Direct commands, no skill |
| 3 | Quantification (salmon, or STAR + featureCounts) | Direct commands, no skill |
| 4 | Filtering and normalization (DESeq2 size factors / edgeR TMM) | Analysis code, no skill |
| 5 | Exploratory checks: PCA and sample-distance heatmap. Do samples group by batch or by condition? Any outliers? | Code, with **dataviz** for the plots |
| 6 | Model fit with `~ batch + condition` and the primary threshold test | Analysis code, no skill |
| 7 | Diagnostics: dispersion plot, p-value histogram, MA plot | Code, with **dataviz** for the plots |
| 8 | Sensitivity checks: results with and without the batch term, leave-one-replicate-out, permutation check | Analysis code, no skill |
| 9 | Exploratory: genome-wide DE, gene-set enrichment (fgsea/camera), labelled as exploratory | Analysis code, with **dataviz** for the volcano plot |
| 10 | Report for collaborators | **artifact-design** if you want it as a shared page |

Two things would let me move to code: the sample-to-batch layout, and whether you're starting from FASTQs or a count matrix.

---

## P09

**Prompt:** What is the Shannon entropy of the base composition of ACGTACGTAACCGGTT, and of its overlapping 2-mers? Give bits, the maximum possible in each case, and say how reliable the estimate is for a sequence this short.

### Answer A

## Results

**Sequence:** `ACGTACGTAACCGGTT` (16 bases)

### Single bases (k = 1)

| Base | Count | p |
|---|---|---|
| A | 4 | 0.25 |
| C | 4 | 0.25 |
| G | 4 | 0.25 |
| T | 4 | 0.25 |

**H₁ = 2.000 bits.** The maximum for 4 symbols is log₂4 = **2 bits**, so this sequence reaches it.

### Overlapping 2-mers (k = 2)

A 16-base sequence has 15 overlapping 2-mers:

| 2-mer | Count | p |
|---|---|---|
| AC, CG, GT | 3 each | 0.200 |
| TA | 2 | 0.133 |
| AA, CC, GG, TT | 1 each | 0.067 |
| other 8 of the 16 | 0 | 0 |

H₂ = 3·(0.2·log₂5) + (2/15)·log₂7.5 + 4·(1/15)·log₂15
  = 1.393 + 0.388 + 1.042 = **2.823 bits**

- **Theoretical maximum:** log₂16 = **4 bits** (all 16 dinucleotides equally frequent).
- **Highest value possible with 15 observations:** log₂15 ≈ 3.91 bits. Fifteen counts cannot fill 16 categories, so 4 bits is out of reach at this length.

## How reliable this is

The estimates are not very reliable.

1. **The simple count-based estimate runs low.** Entropy calculated from raw counts (the "plug-in" estimate) underestimates the true value, and the error grows when there are few observations per category. The Miller–Madow correction adds (K−1)/(2N ln 2), where K is the number of categories seen and N the number of observations:
   - Bases: +3/(32·ln 2) ≈ +0.14 → ~2.14 bits. This is above the 2-bit ceiling, which only shows how rough the correction is at N = 16. In practice, call it "about 2".
   - 2-mers: +7/(30·ln 2) ≈ +0.34 → **~3.16 bits**. The 2.82 figure is almost certainly too low for whatever process produced the sequence.
2. **The 2-mer counts are badly undersampled.** There are about 0.9 observations per category, and 8 of the 16 dinucleotides never appear. A missing dinucleotide here could just be chance. A common rule of thumb is to have N well above 4ᵏ, ideally 10 or more observations per cell. That means roughly 160+ bases for 2-mers.
3. **Overlapping 2-mers are not independent.** Each base sits in two 2-mers, so the 15 counts carry less information than 15 independent draws would. Any confidence interval should come from a block bootstrap or from shuffling the sequence, not from multinomial formulas.
4. **Composition entropy ignores order.** The bases score the maximum 2 bits, yet the sequence is clearly patterned: it is ACGT repeated, then each base doubled. The 2-mer level shows this. H₂ − H₁ ≈ 0.82 bits, against 2 bits for a random sequence, so knowing one base strongly predicts the next. Even this difference is noisy at this length.

**Bottom line:** For these 16 bases, the counts give 2.00 of 2 bits for bases and 2.82 of 4 bits for 2-mers. Treat these as descriptions of this particular string, not as estimates of a source's true entropy. The base value is reasonable. The 2-mer value is low and uncertain by several tenths of a bit.

### Answer B

**Sequence:** `ACGTACGTAACCGGTT` (length 16)

## 1. Base composition (1-mers)

| Base | Count | p |
|---|---|---|
| A | 4 | 0.25 |
| C | 4 | 0.25 |
| G | 4 | 0.25 |
| T | 4 | 0.25 |

H = −Σ p log₂ p = 4 × (0.25 × 2) = **2.000 bits**

**Maximum:** log₂ 4 = **2 bits**. The composition is perfectly uniform, so the entropy is at its maximum.

## 2. Overlapping 2-mers (15 windows)

| 2-mer | Count | p |
|---|---|---|
| AC | 3 | 0.200 |
| CG | 3 | 0.200 |
| GT | 3 | 0.200 |
| TA | 2 | 0.133 |
| AA, CC, GG, TT | 1 each | 0.067 each |
| other 8 dimers | 0 | 0 |

H = 3(0.2·log₂5) + 2/15·log₂7.5 + 4(1/15·log₂15)
  = 1.393 + 0.388 + 1.042 = **≈ 2.82 bits**

**Maximum:** log₂ 16 = **4 bits** in principle. With only 15 windows, the highest entropy you could actually observe is log₂ 15 ≈ 3.91 bits, which needs 15 different dimers each seen once. Only 8 of the 16 possible dimers appear here.

The 2-mer entropy is well below 2 × H₁ = 4 bits. The conditional entropy H₂ − H₁ ≈ 0.82 bits is far below the 2 bits you'd expect if neighbouring bases were independent. That matches the visible structure: the ACGT repeat and the doubled bases (AA, CC, GG, TT) make the next base quite predictable.

## 3. How reliable is this?

Not very, especially for the 2-mers.

- **The plug-in estimator is biased low.** The Miller–Madow correction adds about (K−1)/(2N ln 2):
  - 1-mers: about +0.14 bits. The true value can't exceed 2, so this only says the estimate is already at the ceiling.
  - 2-mers: about +0.34 bits using the 8 observed dimers, or about +0.72 bits using all 16 possible ones. A rough corrected value is 3.2–3.5 bits, which is a big change compared with the 2.82 measured.
- **There is too little data for 16 categories.** With 15 observations across 16 cells, most counts are 0 or 1. You can't tell a rare dimer from an absent one, so the 2-mer distribution is essentially undetermined.
- **Overlapping windows aren't independent.** Each base sits in two windows, so the effective sample size is below 15, and standard error formulas understate the uncertainty.
- **The perfect 4/4/4/4 composition is partly luck.** A random uniform 16-mer comes out exactly balanced only about 1.5% of the time (16!/(4!⁴)/4¹⁶). Small samples swing widely, so a 16-nt sequence can't distinguish "truly uniform" from "mildly biased."
- **For comparison:** a uniformly random 16-mer typically gives a plug-in 2-mer entropy of about 3.3–3.5 bits. The 2.82 here really is lower than that, because of the repeats. Still, the exact value carries roughly ±0.3–0.5 bits of uncertainty.

**Summary:** the 1-mer entropy is 2.00 out of 2 bits, and the 2-mer entropy is about 2.82 out of 4 bits. The 1-mer figure is a fair description of this particular string but says little about any source it came from. The 2-mer figure is a rough, downward-biased estimate. As a rule of thumb, you need N ≫ 4ᵏ (hundreds of bases for k = 2) before k-mer entropies are stable. For short sequences, use bias-corrected estimators such as Miller–Madow, NSB or Chao–Shen, or bootstrap confidence intervals.

---

## P18

**Prompt:** Here is my plan: data access 6 weeks, quality control 2, alignment 3, statistics 4, then writing 5 weeks and figures 2 weeks in parallel with writing. I have 24 weeks. Does it fit if I add a 30 percent buffer?

### Answer A

No. It falls short by about 2 weeks.

**The math**
- Sequential work: data access 6 + quality control 2 + alignment 3 + statistics 4 + writing 5 = **20 weeks**. Figures fit inside the writing block, so they add no time.
- With a 30% buffer: 20 × 1.3 = **26 weeks**. You have 24, so you're **2 weeks over**.
- If you keep 24 weeks, your buffer is 4 weeks, or **20%**.

**How to make 30% fit**
For a 30% buffer to fit in 24 weeks, the base plan can be at most 24 / 1.3 ≈ **18.5 weeks**. You need to cut about 1.5 weeks, for example:
1. **Overlap quality control with data access.** Start checking data as it arrives instead of waiting for all 6 weeks of access. This alone could save 1–2 weeks.
2. **Start writing the methods section during alignment or statistics.** Methods can be drafted early, which shortens the final writing block.
3. **Put the buffer where the risk is.** Data access is usually the least predictable step. You could give it a large buffer and the steps you control a smaller one, rather than a flat 30%.

Data access is both your longest step and the one most likely to slip, so pushing to start it now matters more than the exact buffer percentage.

### Answer B

**No, it doesn't fit. You'd be about 2 weeks over.**

**Critical path**
- Data access → QC → alignment → statistics: 6 + 2 + 3 + 4 = **15 weeks**, one after the other.
- Writing: **5 weeks**. Figures run alongside it, so they add no time.
- Total: **20 weeks**.

**With a 30% buffer**
- 20 × 1.3 = **26 weeks**, against the 24 you have.
- 24 weeks leaves 4 weeks of slack. That's a **20% buffer**, not 30%.
- To keep 30%, the work itself has to fit in 24 / 1.3 ≈ **18.5 weeks**. That means cutting about 1.5 weeks.

**Ways to close the gap**
1. **Overlap the start with data access.** If data arrives in batches, you can start QC and alignment on the first batch while waiting for the rest. This usually saves the most time.
2. **Write the methods section during statistics.** Methods, data description and QC results are known by then. That could shorten the writing phase by 1–2 weeks.
3. **Make the figures pipeline while statistics runs.** Write the plotting scripts against early results. Then the 2 figure weeks are only about refreshing outputs, and they stay safely inside the writing window.
4. **Put the buffer where the risk is.** Data access depends on other people, so it's the most likely task to slip. A flat 30% across every task protects the wrong things. Most of your 4 weeks of slack should sit after data access.

**Check one assumption:** figures can only run in parallel with writing if they don't need final results that arrive late. If reviewers or co-authors change the analysis, figures go back on the critical path.

Overlapping the start (option 1) and drafting methods early (option 2) should bring the critical path to about 17–18 weeks, which fits 24 weeks with a 30% buffer.

---

## P15

**Prompt:** Compute the p-distance and the Jukes-Cantor distance between ACGTACGTAC and ACGTACGTAA. Say when the Jukes-Cantor correction stops being usable.

### Answer A

**p-distance = 0.1** and **Jukes-Cantor distance ≈ 0.107** substitutions per site.

**Comparison**

```
ACGTACGTAC
ACGTACGTAA
         *
```

Both sequences are 10 bases long and there are no gaps. They differ at one site, position 10 (C against A).

**p-distance**

p = mismatches / sites = 1/10 = **0.1**

**Jukes-Cantor distance**

d = −(3/4) · ln(1 − (4/3)·p)
  = −0.75 · ln(1 − 0.1333)
  = −0.75 · ln(0.86667)
  = −0.75 · (−0.14310)
  = **0.1073**

The corrected distance is a little larger than p. The correction adds back substitutions you can't see, because a site that changed more than once can look as if it changed once or not at all. When p is small, d and p are nearly the same.

**When the Jukes-Cantor correction stops being usable**

- **It fails outright at p ≥ 0.75.** At p = 0.75 the term inside the log is 0, so d is infinite. Above 0.75 the log of a negative number is undefined. Under the JC model, two unrelated random sequences already differ at 3/4 of sites, so p = 0.75 means the sequences look completely saturated.
- **It becomes unreliable well before 0.75.** As p gets close to 0.75, the sampling variance of d grows without limit: Var(d) = p(1−p) / [L·(1 − 4p/3)²]. A tiny change in p then causes a huge swing in d. In practice, JC distances above roughly p ≈ 0.5–0.6 are too noisy to trust, especially for short alignments.
- **It fails when its assumptions are wrong.** The model assumes equal base frequencies, equal rates for all substitution types (no transition/transversion bias), the same rate at every site, and no gaps. If those assumptions are clearly violated, use K2P, F81/HKY or GTR, with a gamma rate model if rates vary across sites.

**Caveat for this example:** 10 sites is far too few for a precise estimate. The standard error of p is √(0.1·0.9/10) ≈ 0.095, which is about the same size as p itself. So both distances are rough point estimates, not reliable measurements.

### Answer B

The Jukes–Cantor distance is about **0.1073** substitutions per site, against a p-distance of 0.1.

## Alignment

```
Seq1: A C G T A C G T A C
Seq2: A C G T A C G T A A
                        ^  position 10: C ↔ A
```

The sequences differ at 1 of 10 sites.

## p-distance

$$p = \frac{\text{differences}}{\text{sites}} = \frac{1}{10} = \mathbf{0.1}$$

## Jukes–Cantor distance

$$d_{JC} = -\tfrac{3}{4}\ln\!\left(1 - \tfrac{4}{3}p\right)$$

$$1 - \tfrac{4}{3}(0.1) = 0.86667 \quad\Rightarrow\quad \ln(0.86667) = -0.14310$$

$$d_{JC} = -0.75 \times (-0.14310) \approx \mathbf{0.1073}$$

The correction is small, about 7% above p. At low divergence, few sites are likely to have changed more than once, so little needs correcting.

## When the Jukes–Cantor correction stops being usable

- **Hard limit, p ≥ 0.75:** At this point $1 - \tfrac{4}{3}p \le 0$, so the logarithm is undefined and the distance is infinite or can't be computed. Under JC, two unrelated random sequences match at 1/4 of sites, so p = 0.75 is full saturation: the sequences carry no remaining signal about how far apart they are.
- **Practical limit, well before 0.75:** As p approaches 0.75, $d_{JC}$ rises very steeply. Its variance, $\frac{p(1-p)}{n\,(1-\frac{4}{3}p)^2}$, also blows up, so one extra mismatch changes the estimate a lot. Above roughly p ≈ 0.5, which corresponds to d_JC ≈ 0.82, the estimates are generally too noisy to trust.
- **Model violations:** JC assumes equal base frequencies, equal rates for every type of substitution, and the same rate at every site. Real data with a transition/transversion bias, skewed base composition, or rate variation across sites should use K2P, F81/HKY, GTR, or a +Γ model. Otherwise JC underestimates the true distance.

Also, with only 10 sites, a single substitution moves p by 0.1, so this estimate has very large sampling error.

---

## P08

**Prompt:** Translate ATGAAATAG in frame 1 under the standard genetic code and tell me what each symbol in the answer means.

### Answer A

ATG AAA TAG gives **M K \***. This is the usual single-letter notation for proteins.

| Codon | Symbol | Meaning |
|---|---|---|
| ATG | **M** | Methionine. ATG is also the standard **start codon**, which is where translation begins. |
| AAA | **K** | Lysine. Its one-letter code is K because L was already taken by leucine. |
| TAG | **\*** | **Stop codon**, also called "amber." It does not code for an amino acid. It tells the ribosome to stop translating. |

The sequence encodes the two-amino-acid peptide **Met-Lys (MK)** followed by a stop. In three-letter notation this is Met-Lys-Stop.

### Answer B

**Translation: `MK*`**

| Codon | Symbol | Meaning |
|---|---|---|
| ATG | **M** | Methionine (Met). ATG is also the usual start codon. |
| AAA | **K** | Lysine (Lys). The one-letter code is K because L is already used for leucine. |
| TAG | **\*** | Stop codon, called "amber". It is not an amino acid. It marks where translation ends. |

Frame 1 means the codons are read starting from the first base, with no offset. The encoded peptide is the dipeptide **Met-Lys**. The `*` is a marker for the stop, not part of the protein. Some tools drop it or stop at it, so they would show just `MK`.

Because the sequence runs from a start codon to an in-frame stop, it is technically a complete open reading frame. At only 2 codons it is far too short to be a real gene.

---

## P17

**Prompt:** Set up a project layout for an analysis of public sequencing data in Python. Keep raw data read-only, record accessions and checksums, pin the environment, and say where seeds are recorded.

### Answer A

I've set up the project layout. The seed is set in `config/config.yaml` and saved with every result in `results/<run_id>/run_record.json`.

```
config/config.yaml          parameters, genome build and release, and the seed
data/raw/                   downloaded files, read-only, kept out of git
data/raw/manifest.tsv       accession, URL, md5, sha256, size, download date and licence for each file
data/interim/, data/processed/   files the code can regenerate
scripts/fetch_raw.py        downloads, checks and locks the raw files
src/seqproject/run_record.py    starts each run and records seeds and versions
results/<run_id>/           outputs and run_record.json
tests/test_reproducibility.py
docs/methods-record.md      template to fill in from the run records
environment.yml, pyproject.toml, .gitignore, README.md
```

- **Raw data is read-only.** `fetch_raw.py` downloads to a temporary file and rejects it if its md5 doesn't match the one in the manifest. It then sets the file to read-only. It never overwrites a file that's already there. `--verify` rechecks every file and fails if one is missing, has changed or can be written to.
- **Accessions and checksums** go in `manifest.tsv`, which is committed to git. You fill in the accession, URL, md5 and licence; the README gives the query to get the URL and md5 from ENA. The script adds the sha256, file size and download date.
- **Environment:** `environment.yml` pins exact versions of Python and each package. After the first install, run `conda env export --no-builds > environment.lock.yml` and commit that file. Rebuild once from it to confirm it works.
- **Seeds:**
  - **Set:** only in `config/config.yaml` (`seed: 20261014`).
  - **Used:** only through `start_run()`. It gives each parallel worker its own seed, all derived from the one seed, so no worker ends up with an unseeded random generator.
  - **Recorded:** with each result in `run_record.json`, as the seed and the per-worker seeds. That file also stores the git commit, package versions, config and a sha256 of each input.
  - **Stability check:** `n_seed_replicates` in the config sets how many consecutive seeds a reported result should be rerun with, and the spread across those runs is reported.

**What I tested:** only `fetch_raw.py --verify` on the empty manifest, which reported `0 files OK`. I haven't built the environment, run pytest or tried a real download. A command that would have checked the seed functions needed your approval, so it didn't run.

- **Setup:** the folder isn't a git repository yet, so the commit recorded in each run will show as `unknown` until you run `git init`.
- **Pins:** check the pinned versions against your conda channels when you first install.
- **Reference genome:** fill in `fasta_sha256` in the config once you've downloaded it.

### Answer B

I've set up the project layout in the working directory. I haven't run any of it: my attempt to run the tests was blocked at a permission prompt, and I didn't try downloading real data.

**Layout**
```
config/config.yaml        list of accessions to fetch, plus the master seed
data/raw/                 downloaded data, read-only, not committed to git
data/raw/MANIFEST.tsv     one row per file: accession, URL, size, md5, sha256, download time (committed)
data/{external,interim,processed}/
src/seqproject/           checksums.py, seeds.py
scripts/                  fetch_raw.py, verify_raw.py
runs/<run_id>/run.json    a record of each run (committed)
notebooks/  results/  logs/  tests/
environment.yml  pyproject.toml  Makefile  .gitignore  README.md
```

**Read-only raw data:** only `scripts/fetch_raw.py` writes to `data/raw/`. It downloads FASTQ files from ENA and checks each one's size and MD5 against the values ENA publishes. It then removes write permission from the file. Analysis outputs go to `data/interim/` and `data/processed/`. `make protect` puts the read-only permissions back if they get changed.

**Accessions and checksums:** each downloaded file gets one new row in `data/raw/MANIFEST.tsv`. Rows are only ever added, never changed. Each row has the accession, source URL, size, MD5 (checked against ENA's value), SHA-256 (computed locally) and download time. If a file fails the check, it is deleted and no row is written. `make verify` re-checks every row: the file exists, both checksums still match, and it's still read-only.

**Pinned environment:** `environment.yml` (conda-forge and bioconda) gives an exact version for every direct dependency, including Python 3.12.7, numpy, pandas, pysam, samtools, sra-tools and fastp. `make lock` produces `conda-lock.yml`, which also pins every indirect dependency for each platform, and you should commit it. I couldn't create the lock file because conda isn't installed on this machine, so run `make lock` once you have mamba or conda.

**Where seeds are recorded:**
- **Set:** in one place only, `seed:` in `config/config.yaml`.
- **Derived:** each analysis step gets its own seed from the master seed and the step's name, via `seeds.derive_seed` or `seeds.rng`. Adding a new step doesn't change the random numbers of existing steps.
- **Recorded:** `seeds.start_run()` writes `runs/<run_id>/run.json` for every run. It contains the master seed, every per-step seed, the git commit (marked `-dirty` if there were uncommitted changes), the Python version, platform, command-line arguments and the full config. External tools that take a seed, such as `seqtk sample -s`, should be given the per-step seed so it is recorded there too.

The README describes this workflow.

The folder isn't a git repository yet, so the `.gitignore` rules have no effect until you run `git init`. I can do that if you want.

---

## P01

**Prompt:** I am a biologist with no programming. I have 6 hours a week for 12 weeks and want to analyse my own sequencing data at the end. Plan it, with a goal I can test at the end of each stage.

### Answer A

# A 12-week plan: from no programming to analysing your own sequencing data

**Who this plan is for:** a biologist (strong on biology, starting from zero on programming) with 6 h/week × 12 weeks, about 72 hours in total. The goal is to analyse your own sequencing data at the end.
**Approach:** use one data type and one project, and go deep rather than broad. Your own data is the final project, so everything before it is preparation for it.

**One thing I need from you:** what kind of sequencing data is it? For example: RNA-seq (gene expression), whole-genome or exome sequencing (variants), 16S or amplicon (microbial communities), or ChIP/ATAC-seq. Weeks 1–6 are the same for all of them. Weeks 7–12 change depending on the answer, so I've written them for **RNA-seq** as the most common case. Tell me if yours is different and I'll swap those stages.

**Tools:** the command line (to handle sequencing files) plus **R** with RStudio. Most downstream analysis of biological data (DESeq2, phyloseq, plotting) happens in R. Learn one language well rather than two badly.

---

## Stage 1 (Weeks 1–2): The command line and your files
**Learn:** opening a terminal, moving between folders, and the commands `ls`, `cd`, `head`, `wc -l`, `grep` and `|` (pipe). Also what FASTA and FASTQ files look like. Each read in a FASTQ file takes exactly 4 lines, and the quality letters encode Phred scores.
**Resource:** Software Carpentry's "The Unix Shell" lesson (free, online).
**Weekly habit, starting now:** keep a plain-text lab notebook for computing. Write down every command you ran, the version of each tool, and every mistake you made.

✅ **Stage test:** take a FASTQ file (one of your own, or a small public one).
1. Count the reads with `wc -l` divided by 4. Check the number against the read count your sequencing facility reported.
2. Pull out the first 5 reads with `head -n 20`.
3. Count how many reads contain the sequence `AGATCGGAAGAGC` (a common Illumina adapter).
**You pass** if your read count matches the facility's report exactly.

## Stage 2 (Weeks 3–4): R basics
**Learn:** RStudio, variables, vectors, data frames, reading a CSV file, `dplyr` (filter, group, summarise) and `ggplot2`.
**Resource:** Data Carpentry's "R for Ecologists/Genomics", or the free book *R for Data Science* (chapters 1–5).

✅ **Stage test:** use a small table of your own past lab data (qPCR, plate reader, or similar) that you have already analysed in Excel.
1. Load it into R.
2. Compute the mean and SD for each group.
3. Make a plot with points and error bars.
**You pass** if your R numbers match your Excel numbers to the last decimal place, and you can rerun the script from scratch and get the same plot.

## Stage 3 (Weeks 5–6): Statistics you'll need for sequencing data
**Learn:** the t-test and what a p-value actually means; why testing 20,000 genes at p < 0.05 gives about 1,000 false hits by chance; Benjamini–Hochberg FDR correction; why biological replicates matter and technical replicates are not a substitute for them.

✅ **Stage test:** simulate a null experiment in R.
1. Generate 10,000 "genes", each with 3 vs 3 samples drawn from the **same** distribution.
2. t-test every gene.
3. Count how many have p < 0.05, then how many survive `p.adjust(method="BH")` at 0.05.
**You pass** if you get about 500 raw hits and close to 0 after correction, and you can explain in two sentences why.

## Stage 4 (Weeks 7–8): From raw reads to counts (RNA-seq)
**Learn:**
- read quality control (FastQC, MultiQC);
- choosing a reference genome and annotation, and **writing down the exact build and release** (e.g. GRCm39, Ensembl 110);
- quantifying expression (Salmon is fast and runs on a laptop);
- installing tools with conda.

**Practice data:** use a small public dataset with published results first, for example the airway dataset (`airway` package in R), not your own data yet.

✅ **Stage test:** run QC and Salmon on 2–4 samples of a public dataset.
**You pass** if:
- the mapping rate is above 70%;
- you can explain each red or orange flag in the FastQC report and whether it matters for RNA-seq (it often doesn't, for example "sequence duplication");
- your count for one well-known gene (e.g. ACTB) is in the same range as the published counts.

## Stage 5 (Weeks 9–10): Differential expression on known data
**Learn:** DESeq2 (normalisation, design formula, results), PCA to spot outlier samples and batch effects, and volcano plots and MA plots.

✅ **Stage test:** reproduce the published result on `airway` (dexamethasone-treated vs control) by following the DESeq2 vignette.
**You pass** if:
- your list of significant genes at FDR < 0.05 overlaps strongly with the vignette's;
- known dexamethasone targets (e.g. **DUSP1, KLF15, PER1**) come out upregulated;
- the PCA shows that samples separate by cell line as well as by treatment, and you can say why the design formula must include cell line.

This is the key test of the course: it shows you can get a **known answer** before you trust an unknown one.

## Stage 6 (Weeks 11–12): Your own data
**Before you touch the data (week 11, first 2 h):** write a one-page plan.
- What is the question?
- Which comparison answers it?
- What result would show your hypothesis is **wrong**?
- Is any batch (sequencing run, extraction day) confounded with your groups?

**Then:** QC → quantification → DESeq2 → PCA → results table and plots, all as one R script plus one shell script, with versions recorded.

✅ **Final test, which has three parts:**
1. **Positive control:** a gene you *know* should change (from qPCR or the biology) changes in the expected direction.
2. **Sanity check:** replicates cluster together on the PCA. If they don't, find out why before you interpret anything.
3. **Reproducibility:** delete the results folder, rerun the scripts, and get identical results.

You're done when you can explain each figure and say what would make it wrong.

---

## Weekly rhythm (6 h)
- 4 h on the lesson and exercises.
- 1.5 h applying it to something real, ideally your own question.
- 30 min updating your notebook: what you learned, what broke, and how you fixed it.

## Common traps
- **Running tools you don't understand on your own data first.** Always reproduce a known result before analysing unknown data.
- **Getting stuck in tutorials.** If you've done three tutorials without touching a real question, move on.
- **Over-reading p-values** without FDR correction or enough replicates. If you have fewer than 3 biological replicates per group, talk to someone before sequencing more.
- **Hidden batch effects.** If all your controls were sequenced on one day and all your treated samples on another, statistics can't separate the two.

## Week 1 tasks (this week)
1. **Mac:** open Terminal. **Windows:** install WSL.
2. Do episodes 1–3 of Software Carpentry's "The Unix Shell".
3. Ask your sequencing facility for the raw FASTQ files and the read-count report. You'll need both for the Stage 1 test.
4. Start the notebook file.

Tell me your data type (and organism), and I'll rewrite Stages 4–6 for it and add worked exercises with expected answers for each stage.

### Answer B

# 12-week plan: from no programming to analysing your own sequencing data

**Total time:** 72 hours (6 hours a week for 12 weeks).

I've assumed you have **bulk RNA-seq** data, because it's the most common case. The table near the end shows what to swap in if your data is a different type. Each stage ends with a test. If you can pass it, move on. If you can't, use some of the next stage's time to catch up. Don't push ahead without passing.

## Before week 1 (about 1 hour)
- **Find out what you have.** Ask your sequencing facility for the data type, the organism, how many samples, single- or paired-end reads, and whether they've already made a "counts table". If they have, you can skip most of Stage 4.
- **Install** R, RStudio and a terminal. On a Mac the terminal is built in. On Windows, install WSL.
- **Choose where the heavy computing will run.** Turning raw reads into counts usually needs more power than a laptop has. Your options are Galaxy (usegalaxy.org, free and runs in a browser), your institution's computing cluster, or the facility doing it for you.

---

## Stage 1 · Weeks 1–2 · The command line (12 h)
**Learn:** moving between folders, managing files, looking inside files (`head`, `less`), counting and searching (`wc`, `grep`), connecting commands together (pipes), and simple loops.
**Resource:** Software Carpentry, "The Unix Shell" (free, swcarpentry.github.io/shell-novice).
**✅ Test:** Download a small public FASTQ file (a raw-reads file). Within 20 minutes, without notes:
1. Make a project folder containing `raw/`, `results/` and `scripts/`.
2. Count the reads. Each read takes 4 lines, so the answer is the line count divided by 4.
3. Print the first 3 read names (the lines starting with `@`).
4. Write a loop that prints the read count for every FASTQ file in the folder.

## Stage 2 · Weeks 3–5 · R basics (18 h)
**Learn:** variables, data frames, importing CSV files, `dplyr` (filtering, grouping and summarising data), `ggplot2` (plots), and writing scripts instead of typing commands one at a time.
**Resource:** Data Carpentry, "R for Genomics" or "R for Ecologists", plus chapters 1–8 of *R for Data Science* (r4ds.hadley.nz, free).
**✅ Test:** Start from an empty folder and write one script that:
1. reads in a CSV file of your own lab measurements,
2. calculates the mean and standard deviation for each group,
3. saves a labelled plot as a PDF,
4. **runs again correctly after you restart R.** This last point is the real test, because it proves the script works on its own.

## Stage 3 · Week 6 · What sequencing data looks like, and quality control (6 h)
**Learn:** the FASTQ format and its quality scores, adapters (short sequences added during library prep), duplicate reads, and how to run FastQC and MultiQC (quality-report tools).
**Resource:** the Galaxy Training Network tutorial "Quality Control" (training.galaxyproject.org).
**✅ Test:** Run FastQC/MultiQC on **your own** raw data. Write half a page covering every warning it raised: what it means, and whether it matters for RNA-seq. Some warnings are normal for RNA-seq, for example duplication. End with a decision: trim the reads or don't, and why.

## Stage 4 · Weeks 7–8 · Raw reads to a counts table (12 h)
**Learn:** reference genomes and annotation files (GTF), quantifying gene expression with Salmon (or aligning with STAR plus featureCounts), and how to check mapping rates.
**Resource:** the Galaxy Training Network tutorial "Reference-based RNA-Seq data analysis".
**✅ Test:**
1. Work through the tutorial on its own dataset and check that your numbers match the tutorial's.
2. Run the same process on **two of your own samples**. Each should have a mapping rate you can explain (above 70% is typical for a well-annotated organism).
3. Then run all your samples. You should end up with a genes × samples counts table that loads into R.

## Stage 5 · Weeks 9–10 · Statistics: differential expression (12 h)
**Learn:** experimental design (which samples are replicates, which are conditions, and any batch effects), why counts need normalising, the DESeq2 model, adjusted p-values versus fold changes, PCA plots, MA plots and volcano plots.
**Resource:** the Bioconductor *RNA-seq workflow* using the `airway` dataset (by Love, Anders and Huber).
**✅ Test:** Reproduce the airway workflow from scratch in your own script. Your count of genes with adjusted p < 0.1 and your top 10 genes should match the published workflow. Then explain in plain words what a "log2 fold change of 1 with padj = 0.03" means.

## Stage 6 · Weeks 11–12 · Your own data (12 h)
**Do:** QC → counts → PCA → DESeq2 → figures → a short list of genes for follow-up. Write it all in a single Quarto/R Markdown document, which keeps your code, results and notes together in one report.
**✅ Final test, which has three parts:**
1. **Reproducible:** restart R, run the document, and get the same figures.
2. **Biologically sensible:** genes you know should change (for example your knockout gene, or a known marker) behave as expected, and replicates cluster together on the PCA plot.
3. **Defensible:** a bioinformatician or colleague reviews it for 30 minutes and finds no major design error.

---

## If your data isn't bulk RNA-seq
| Data type | Stage 4 replacement | Stage 5 replacement |
|---|---|---|
| 16S/amplicon (microbiome) | DADA2 tutorial | phyloseq: diversity measures and DESeq2/ANCOM-BC |
| Single-cell RNA-seq | facility runs Cell Ranger | Seurat guided clustering tutorial (weeks 9–12 are tight, so cut scope) |
| Whole genome or exome (variants) | BWA plus GATK on Galaxy | variant filtering and annotation (VEP) |
| ChIP/ATAC-seq | Bowtie2 plus MACS2 | DiffBind |

## Habits that make this work
- **Type the code yourself; don't copy and paste it.** Keep a plain-text log of every command that worked.
- **Do 3 sessions of 2 hours a week, not one 6-hour session.** You'll remember more.
- **When stuck for more than 30 minutes, ask.** Biostars and support.bioconductor.org are good places to post. Include your code and the exact error message.
- **Keep a copy of the raw data that you never edit.** All work happens on copies.

If you tell me your data type, organism and number of samples, I can tailor Stages 4–6. I can also turn this plan into a shareable checklist page if that would help.

---

## P14

**Prompt:** Analyse this expression matrix: 20,000 genes by 12 samples, with a sample sheet giving condition, batch and date. Before any differential test, check the design, run quality control and a PCA coloured by batch and by condition, and tell me what would make me stop.

### Answer A

I couldn't find your data. The working directory is empty, so the 20,000 × 12 matrix and the sample sheet aren't here. I haven't analysed anything and have no results for you. What I've done is write the full pre-test check as a script, ready to run as soon as you send the files.

## The script

`<temporary path>`

```
python preflight_qc.py counts.tsv samples.tsv [--counts|--log] outdir
```

**The script hasn't been run.** This machine's Python doesn't have numpy, pandas or matplotlib installed. I didn't install them without asking you, so the smoke test I planned on synthetic data didn't happen.

It never writes over your inputs. It does three things in order:

1. **Design**
   - Checks that the sample IDs in the matrix and the sheet match.
   - Builds condition × batch, condition × date and batch × date tables.
   - Counts the samples in each condition.
   - Flags batches or dates that hold only one condition, either fully or partly.
2. **Quality control**
   - Missing values for each sample.
   - Negative or non-integer values, which show the data aren't raw counts.
   - Library sizes and the number of genes detected in each sample.
   - A boxplot of each sample's log-scale distribution.
   - A sample-to-sample correlation heatmap, labelled with condition and batch.
   - Outlier samples, flagged by low mean correlation to the others.
3. **PCA**
   - Uses the 2,000 most variable genes after log-CPM, centred but not scaled.
   - Plots PC1 against PC2 coloured by condition, then by batch, then by date.
   - Reports a table of how much of each of the first five PCs is explained by condition, batch and date (R²). This makes "PC1 is batch" a number rather than an impression.

## When to stop before any differential test

**Stop completely:**
- **Batch or date is perfectly aligned with condition.** For example, all controls are in batch A and all treated samples in batch B. With 12 samples this is a common layout. The treatment effect can't then be separated from the batch effect, and no correction method can recover it, because adding batch to the model leaves condition with nothing left to estimate. The only fix is more samples run across batches.
- **Fewer than 3 biological replicates in a condition**, or replicates that turn out to be technical: the same RNA sequenced twice, or the same animal sampled twice. Check whether the sheet has pairing or subject information.
- **Sample IDs don't match between the matrix and the sheet.** Also stop if the PCA or correlation suggests a swapped label, such as a "control" that sits inside the treated cluster in every view.
- **You don't know what the values are.** Count-based tests need raw integer counts. If the matrix is already normalised (it has negatives or decimals), those tests can't be used as intended, and you need the raw counts or a method suited to the scale you have.

**Pause and investigate before going on:**
- PC1 is explained mostly by batch or date rather than condition. If batch is crossed with condition, you can include it in the model, but say so in the write-up.
- One sample is an outlier: low correlation, a shifted distribution, a library many times smaller or larger than the others, or few genes detected. Find out why from the lab records before deciding whether to drop it; don't drop it because it spoils the result.
- Library sizes differ by more than 5-fold.
- Condition explains almost nothing in the first few PCs. Your test will have little power, so plan for that before you look at p-values.

**Decide before testing:** the gene filter, the model (for example `~ batch + condition` when batch is crossed with condition) and the comparison. Then run the same pipeline once with shuffled condition labels. That run should find roughly nothing; if it finds many genes, something in the pipeline is wrong.

## To get the results

- Send the matrix and sample sheet, or tell me their paths.
- Say whether the values are raw counts or already normalised, and what platform they came from.
- Say whether I may install numpy, pandas and matplotlib (for example `pip install --user numpy pandas matplotlib`).

I'll then run the script and report the design tables, the PCA plots and which of the stop conditions above apply.

### Answer B

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

## What should make you stop

**Hard stops: don't run the differential test**
- **Condition is fully tied to batch or date**, for example all controls in batch 1 and all treated samples in batch 2. Then the condition effect and the batch effect are the same thing, and no statistical correction can separate them. With only 12 samples this is the most likely real problem, so look at the condition × batch table first.
- **The matrix and the sample sheet don't match**, or a sample's labels look swapped, for example a "treated" sample that clusters with the controls on every PC. That means sample identity can't be trusted.
- **The values aren't raw counts** (log, TPM or already batch-corrected) and you planned to use a count-based method. Go back and get the raw counts.
- **PC1 follows batch or date rather than condition**, and batch is unbalanced across conditions. Adding batch to the model won't rescue that.

**Investigate first, then decide**
- Fewer than 3 replicates in a condition (12 samples split 6/6 is fine; 4 groups of 3 is the bare minimum).
- One sample is an outlier on library size, genes detected, correlation with the others, or sits alone on its own PC. Check its lab records before dropping it, and never drop it because of how it affects the results.
- Library sizes differ by more than about 5-fold, or the expression distributions have clearly different shapes.
- Date separates the samples within a batch. That means hidden processing structure the sample sheet doesn't capture.
- Condition explains little of PC1 or PC2. That isn't a reason to stop, but it means you should expect a small, weak set of significant genes.

**If the checks pass:** when batch and condition are crossed (each batch contains both conditions), model it as `~ batch + condition`. Don't use ComBat-corrected values as input to the test.

Send me the files and I'll run the script, go through the actual tables and plots, and tell you which of these apply.

---

## P07

**Prompt:** I want to compare treated and untreated cells and expect a difference of half a standard deviation. How many samples per group do I need at 80% power, and what changes if I will test 20,000 genes?

### Answer A

# Sample size per group: effect size d = 0.5, 80% power, two-sided test

## One comparison at α = 0.05

You need **64 samples per group** (two-sample t-test).

The formula is n ≈ 2(z₁₋α/₂ + z₁₋β)² / d² = 2(1.96 + 0.84)² / 0.25 ≈ 63. The t-distribution correction adds about one more, which gives 64.

## Testing 20,000 genes

Testing 20,000 genes forces a much stricter per-gene α, so the sample size goes up. How much depends on how you control errors:

| Error control | Per-gene α | n per group |
|---|---|---|
| Single test | 0.05 | **64** |
| FDR 5%, about 5% of genes truly changed (1,000) | ≈ 0.0022 | **~123** |
| FDR 5%, about 1% of genes truly changed (200) | ≈ 0.0004 | **~152** |
| Bonferroni (FWER 5%) | 0.05/20,000 = 2.5×10⁻⁶ | **~248** |

- **Bonferroni** guarantees no false positives across all genes. It is very conservative and roughly quadruples the sample size.
- **FDR (Benjamini–Hochberg)** is what genomics studies normally use. The per-gene α it implies is about α* ≈ m₁·(power)·q / (m₀·(1−q)), where m₁ is the number of truly changed genes, m₀ the unchanged ones, and q the FDR level (Jung 2005). The fewer genes that truly change, the stricter α* gets and the more samples you need. Plan for **roughly 120–150 per group**.

## Caveats for gene expression data

1. **What counts as a sample.** n means independent biological replicates, such as separate cultures, animals or donors. Single cells from the same culture are not independent replicates. Treating them as replicates is pseudoreplication and inflates false positives. For single-cell data, aggregate to pseudobulk per replicate.
2. **d = 0.5 is a small effect** for expression data. Many real treatment effects are larger, often a log₂ fold change of 1 or more relative to the biological coefficient of variation. A pilot study or published data will give a better estimate of effect size and variance.
3. **Variance differs between genes.** RNA-seq counts are overdispersed, and power depends on read depth and on each gene's mean and dispersion. A single d won't capture that. RNA-seq-specific tools give more realistic numbers:
   - R packages: `ssizeRNA`, `RNASeqPower`, `PROPER`
   - Simulations with DESeq2 or edgeR, using dispersions from pilot data
   - These tools usually show that well-designed bulk RNA-seq experiments detect moderate fold changes with far fewer replicates than the d = 0.5 numbers above suggest. Those numbers are for a small effect in every gene.

**Short answer:** about 64 per group for one test. With 20,000 genes, about 120–150 per group under FDR control, or about 250 per group under Bonferroni. Before you commit, get realistic effect sizes and dispersions from pilot data and use an RNA-seq power tool.

### Answer B

For one comparison you need **64 samples per group (128 total)**. If you test 20,000 genes with Bonferroni correction, that rises to **about 252 per group (504 total)**. Both numbers come from a two-sided t-test with α = 0.05 and 80% power. I ran them through the skill's sample-size script, which checks against the standard table values and passed its self-test.

**One test, effect size d = 0.5**
- 64 per group.

**20,000 genes**
- With Bonferroni, each gene is tested at α = 0.05 / 20,000 = 2.5 × 10⁻⁶. To keep 80% power per gene at that threshold you need about 252 per group.
- If you stay at 64 per group, the chance of detecting any one real d = 0.5 effect falls to about **3%**. Most true differences would be missed.

**What to do about it**
1. **Control the false discovery rate instead of using Bonferroni.** Benjamini–Hochberg is the usual choice for gene-level tests. The sample size you need then falls somewhere between 64 and 252, depending on how many genes really change. If many genes change, it's closer to 64. If only a handful do, it's closer to 252. To get an actual number, use an RNA-seq power tool that models FDR and the fraction of changing genes, such as `ssizeRNA`, `PROPER` or `RNASeqPower`.
2. **For count data, d = 0.5 is only a rough guide.** Power for read counts depends on sequencing depth, how highly a gene is expressed, and the dispersion. Low-count genes need more samples to reach the same power.
3. **Ask whether d = 0.5 is realistic for your genes.** In well-controlled cell-line experiments the variation between replicates is often small. Then a given fold change becomes a large d, and far fewer samples are needed. Estimate the variability from a pilot or published data rather than assuming it.
4. **Count independent units, not cells.** Each replicate must be an independent culture, passage or treatment run. Many cells from one dish count as one sample, not many. The exception is single-cell data analysed as pseudobulk, where the replicates are still the cultures or donors.
5. **Spread both conditions across every processing and sequencing batch.** Never put treated samples in one batch and untreated in another. Also add 10–15% extra samples to cover ones that fail quality checks.

If you can share expected fold changes and dispersions from a pilot or a similar dataset, I can work out a count-based sample size.

---

## P22

**Prompt:** How many sequences of length 2 are possible from 4 letters? Give the four counts: ordered or unordered, with or without replacement.

### Answer A

For 4 letters taken 2 at a time (n = 4, k = 2):

| | **With replacement** | **Without replacement** |
|---|---|---|
| **Ordered** | 4² = **16** | 4 × 3 = **12** |
| **Unordered** | C(4+2−1, 2) = C(5, 2) = **10** | C(4, 2) = **6** |

Using the letters A, B, C, D:
- **Ordered, without replacement (12):** AB, BA, AC, CA, AD, DA, BC, CB, BD, DB, CD, DC
- **Unordered, without replacement (6):** {A,B}, {A,C}, {A,D}, {B,C}, {B,D}, {C,D}
- **Ordered, with replacement (16):** the 12 ordered pairs above, plus AA, BB, CC, DD
- **Unordered, with replacement (10):** the 6 unordered pairs above, plus AA, BB, CC, DD

### Answer B

With n = 4 letters (say A, C, G, T) and length k = 2:

| | With replacement | Without replacement |
|---|---|---|
| **Ordered** | nᵏ = 4² = **16** | n!/(n−k)! = 4·3 = **12** |
| **Unordered** | C(n+k−1, k) = C(5,2) = **10** | C(n, k) = C(4,2) = **6** |

How each count is reached:
- **Ordered, with replacement (16):** each position can be any of the 4 letters, giving AA, AC, CA and so on. This is the usual count of DNA dinucleotides.
- **Ordered, without replacement (12):** take the 16 above and remove the 4 doubles (AA, CC, GG, TT).
- **Unordered, without replacement (6):** the 12 ordered pairs each appear twice (AC and CA), so 12 / 2 = 6.
- **Unordered, with replacement (10):** the 6 unordered pairs above plus the 4 doubles.

---

## P13

**Prompt:** What does SAM FLAG 99 mean, bit by bit, and what flag would its mate normally have?

### Answer A

## SAM FLAG 99

99 = 64 + 32 + 2 + 1

| Bit (decimal) | Hex | Set? | Meaning |
|---|---|---|---|
| 1 | 0x1 | ✅ | Read is paired |
| 2 | 0x2 | ✅ | Read is mapped in a proper pair |
| 4 | 0x4 | ❌ | Read is mapped |
| 8 | 0x8 | ❌ | Mate is mapped |
| 16 | 0x10 | ❌ | Read is on the forward strand |
| 32 | 0x20 | ✅ | Mate is on the reverse strand |
| 64 | 0x40 | ✅ | This is the first read in the pair (R1) |
| 128 | 0x80 | ❌ | So it is not the second read |
| 256 | 0x100 | ❌ | Primary alignment, not secondary |
| 512 | 0x200 | ❌ | Passed QC |
| 1024 | 0x400 | ❌ | Not marked as a PCR/optical duplicate |
| 2048 | 0x800 | ❌ | Not a supplementary alignment |

**In short:** this is read 1 of a properly paired, primary alignment. It maps to the forward strand and its mate maps to the reverse strand. That is the normal "forward-reverse" (FR) layout for Illumina paired-end reads.

## The mate's flag: 147

147 = 128 + 16 + 2 + 1

- 0x1: the read is paired
- 0x2: it is in a proper pair
- 0x10: **this read** is on the reverse strand
- 0x80: it is the **second** read in the pair (R2)

The mate has the 0x10 bit set and the 0x20 bit clear, because from its side its own read is reverse and its mate is forward. So **99 and 147** go together. The other usual proper-pair combination is **83 and 163**, where R1 is on the reverse strand and R2 is on the forward strand.

You can check any flag with `samtools flags 99`.

### Answer B

## FLAG 99, bit by bit

99 = 64 + 32 + 2 + 1

| Bit (hex) | Value | Set? | Meaning |
|---|---|---|---|
| 0x1 | 1 | **yes** | The read is paired |
| 0x2 | 2 | **yes** | Both mates aligned as a proper pair, in the orientation and distance the aligner expected |
| 0x4 | 4 | no | The read is mapped |
| 0x8 | 8 | no | The mate is mapped |
| 0x10 | 16 | no | The read maps to the **forward** strand |
| 0x20 | 32 | **yes** | The mate maps to the **reverse** strand |
| 0x40 | 64 | **yes** | This is the **first** read of the pair (R1) |
| 0x80 | 128 | no | It is not the second read |
| 0x100 | 256 | no | Primary alignment (not secondary) |
| 0x200 | 512 | no | Passed QC |
| 0x400 | 1024 | no | Not marked as a duplicate |
| 0x800 | 2048 | no | Not a supplementary alignment |

**In short:** FLAG 99 is read 1 of a properly paired read, mapped forward, with its mate mapped reverse. This is the normal forward-reverse layout of Illumina paired-end reads.

## The mate's flag: 147

147 = 128 + 16 + 2 + 1. The mate has:
- **0x1** paired
- **0x2** proper pair
- **0x10** reverse strand (this read's 0x20 said the mate is reversed)
- **0x80** second in pair

0x20 is unset on the mate because read 1 is on the forward strand.

**99/147** is one of the two usual proper-pair combinations. The other is **83/163**, where read 1 is reverse and read 2 is forward. If a read with FLAG 99 has a mate with any other flag, something is wrong. For example, the BAM could be badly sorted, or a tool could have edited one record without updating its mate. Running `samtools fixmate` will repair the mate information.

You can check any flag with `samtools flags 99`.

