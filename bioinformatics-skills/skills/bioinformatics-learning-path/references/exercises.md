# Exercises

Each exercise has a command that produces the answer. Try the exercise by hand first, then run the
command to check your answer. The collection's answer check (check_answers.py) runs every command in
this table and confirms it still prints the expected text, so the answers do not drift.

A command names a script from the collection (for example `seqinfo.py`) followed by its arguments.
Scripts live in the `scripts/` folder of the skill that owns them and need only Python 3.9 or later.

| # | Stage | Exercise | Command | Expected output contains |
|---|---|---|---|---|
| 1 | Information | How many bits does it take to name one of 12 equally likely lengths | `seqinfo.py bits 12` | `3.5850 bits` |
| 2 | Information | How many bits to name one of 3 equally likely kinds | `seqinfo.py bits 3` | `1.5850 bits` |
| 3 | Information | What is the entropy of the base composition of AACC | `seqinfo.py entropy AACC` | `entropy 1.0000 bits` |
| 4 | Probability | P(at least 8 heads in 10 fair tosses) | `seqstats.py binom 10 8 0.5` | `0.0546875` |
| 5 | Probability | Adjust p = 0.01, 0.04, 0.03, 0.005 with Benjamini-Hochberg | `seqstats.py adjust 0.01 0.04 0.03 0.005` | `0.005 -> 0.02` |
| 6 | Probability | Long-run fractions of a chain with rows (0.9, 0.1) and (0.5, 0.5) | `seqstats.py stationary "0.9,0.1;0.5,0.5"` | `0.833333, 0.166667` |
| 7 | Biology | Translate ATGAAATAG with the standard code | `genecode.py translate ATGAAATAG` | `MK*` |
| 8 | Biology | Reverse complement of ATGCRY | `genecode.py revcomp ATGCRY` | `RYGCAT` |
| 9 | Biology | GC skew of GGGCAATT | `genecode.py gc GGGCAATT` | `skew 0.5000` |
| 10 | Biology | Find the ORFs of at least 2 amino acids in CATGAAATAGCCCC | `genecode.py orfs CATGAAATAGCCCC --min-aa 2` | `+ 2-10 2 aa  MK` |
| 11 | Biology | Mass of the peptide GG | `protein.py mass GG` | `132.1190 Da` |
| 12 | Data | Convert BED 2 to 5 into 1-based closed coordinates | `seqformats.py coords bed2gff 2 5` | `3 5` |
| 13 | Data | Which database might NM_000546.6 come from, and what is its version | `accessions.py classify NM_000546.6` | `version 6` |
| 14 | Data | What does FLAG 99 mean | `ngs.py flags 99` | `properly aligned` |
| 15 | Data | Where does 5S10M3D10M2S at POS 100 end | `ngs.py cigar 5S10M3D10M2S --pos 100` | `end 122` |
| 16 | Comparison | Globally align GCATGCG and GATTACA with +1, -1, -1 | `align.py global GCATGCG GATTACA` | `score 0` |
| 17 | Comparison | Jukes-Cantor distance for ACGTACGTAC and ACGTACGTAA | `tree.py jc ACGTACGTAC ACGTACGTAA` | `Jukes-Cantor 0.107326` |
| 18 | Genetics | Hardy-Weinberg test for genotype counts 36, 48, 16 | `popgen.py hwe 36 48 16` | `chi-square 0.000` |
| 19 | Genetics | r squared for haplotype counts 40, 10, 10, 40 | `popgen.py ld 40 10 10 40` | `r^2 0.3600` |
| 20 | Design | Samples per group to detect d = 0.5 | `design.py n --d 0.5` | `64 per group` |
| 21 | Pipelines | Mean depth for 1,000,000 reads of 150 over 5,000,000 bases | `ngs.py coverage --reads 1000000 --length 150 --genome 5000000` | `mean depth 30.00x` |
| 22 | Modelling | AUROC and average precision for the standard four-point example | `mlmetrics.py auc 0,0,1,1 0.1,0.4,0.35,0.8` | `AUROC 0.7500` |
| 23 | Programming | Canonical form of the k-mer GTT | `bioprog.py canonical GTT` | `AAC` |

## Exercises with no single command

1. Draw the UPGMA tree by hand for distances A-B 2, A-C 4, A-D 6, B-C 4, B-D 6, C-D 6, then check it
   with `tree.py upgma` on a matrix file. The answer is `(((A:1,B:1):1,C:2):1,D:3);`.
2. Explain why the compression distance of a 10-base sequence with itself is not 0 (compressor
   overhead), and what length makes it close to 0.
3. Explain why an open reading frame of 100 codons is weak evidence for a gene in a 70% GC genome;
   `gene-finding-methods.md` has the numbers.
4. Take a published analysis and find its null model, its number of tests and its controls.
5. Plan a study with `experimental-design` and then break the design on purpose by putting each
   condition in its own batch; run `design.py confound` and read the result.
