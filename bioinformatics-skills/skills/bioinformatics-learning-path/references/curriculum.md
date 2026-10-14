# Curriculum

The structure follows the source book's three parts. The book's chapter text beyond chapter 2 was
not supplied, so the topics per chapter come from its table of contents. The routes, goals and
projects are suggestions to adapt.

## The three parts and the skills that support them

| Part | Chapters (from the contents) | Topics | Skills in this collection |
|---|---|---|---|
| I Information | 2 to 8 | The nature and transmission of information; sets and combinatorics; probability and likelihood; randomness and complexity; systems, networks and circuits; algorithms | `information-theory-sequences`, `sequence-statistics`, `omics-data-analysis` |
| II Biology | 9 to 11 | Genotype, phenotype and adaptation; cells, the cell cycle, genome and gene structure, gene expression, development, evolution; water, DNA, RNA, proteins, polysaccharides, lipids | `gene-finding-translation`, `protein-analysis`, `phylogenetics` |
| III Applications | 12 to 18 | Genomics; proteomics and transcriptomics; interactomics; metabolomics; medical applications; organization of knowledge | `sequence-alignment`, `ngs-pipelines`, `variants-population-genetics`, `omics-data-analysis`, `biological-databases` |

Skills that cut across all parts: `bioinformatics-workflow`, `experimental-design`,
`sequence-formats`, `bioinformatics-programming`, `reproducible-research-code`,
`machine-learning-biology`, `research-writing-reporting`, `data-governance-ethics`,
`bioinformatics-review`.

## Routes

| Background | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|---|---|---|---|---|
| Biologist | Programming basics and file formats | Information and probability | Alignment, genes, statistics | A data type of your own, with design and review |
| Programmer | Molecular biology and genome basics | Data types and databases | Statistics and the null model | Pipelines, then review |
| Mathematician or statistician | Molecular biology basics | Data types, formats and databases | Pipelines and omics | Design, machine learning, review |

## Stage goals (examples to adapt)

| Stage | Goal a learner can test |
|---|---|
| Information | Compute the entropy of a sequence, say what it means, and say what it does not |
| Probability | Compute how many times a word is expected by chance and a tail probability for the observed count |
| Biology | Translate a sequence, find the reading frames, and say how many are expected by chance in this genome |
| Data | Read FASTA, FASTQ and GFF3 correctly, and convert coordinates both ways |
| Comparison | Align two sequences by hand and by script, and test the score against shuffles |
| Pipelines | Describe each stage from reads to variants or counts and its checks |
| Analysis | Write a plan with a claim, a null model, controls and a stopping rule |
| Review | Find three planted errors in an analysis |

## Projects

| Project | Practises | Deliverable |
|---|---|---|
| Characterise a small bacterial genome | Formats, composition, ORFs, chance level | A short report with the candidate genes and their evidence level |
| Compare two protein families | Alignment, protein analysis, trees | An alignment, a tree and a statement of what is supported |
| Reanalyse a public expression dataset | Databases, design, omics, statistics | A rerun with a record, and a list of differences from the paper |
| Build and test a small tool | Programming, testing | A script with a self-test and a mutation check |
| Review a published analysis | Review, writing | A findings report in the review template |

## Reading papers

For each paper write: the claim; the data and their source; the null model; the number of tests and
the correction; the controls; what was and was not validated independently; and the limits the
authors state and the ones they do not.

## A week in the plan

Read or watch one topic; do the exercises for it and check them by running the commands; apply it to
your own small dataset; write three lines on what could be wrong; and log anything that surprised you.
