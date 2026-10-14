---
name: bioinformatics-workflow
description: Plans a bioinformatics project from question to result by turning the biological question into a claim the data could contradict, naming the null model, fixing data provenance, picking the specialist skill for each step, and setting controls, a stopping rule and what to hand back. Use for "plan an analysis of my sequencing data", "where do I start with this dataset", "which method should I use", "design a bioinformatics pipeline", "what could go wrong with this analysis", "what bioinformatics help do I need". It routes to the specialists, for example experimental-design before data are collected, sequence-formats to read files, omics-data-analysis for expression tables, reproducible-research-code to build it, and bioinformatics-review to check the finished work.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Bioinformatics workflow

## Purpose and activation

Turn a loose request ("analyse these reads", "find the genes", "is this conserved?") into a plan
that can be run, checked and defended. This is the coordinator: it decides which specialist skill
does each step and what would count as a wrong answer. Activate at the start of any analysis, or
when the user cannot say what they would accept as evidence.

The framing comes from the source text: bioinformatics is the application of information science
to biology, and a living thing's sequence must depart from randomness, so the core job is to find
and test those departures. A plan therefore always names the random baseline it departs from.

## Required inputs

The biological question in the user's words; the data (type, organism, size, where it came from,
accession and version if public); what has already been done; the deadline and compute available;
and who will use the result (a bench scientist, a paper, a database). If the data are human, ask
about consent and access rules before anything else (`data-governance-ethics`).

## Workflow

1. **Write the claim.** One sentence of the form "X differs from Y in way Z", phrased so that the
   data could show it false. A question like "what is in this genome?" is not yet a claim.
2. **Name the null model.** What does "no signal" look like: a random sequence of the same
   composition, shuffled sample labels, a permuted network? Hand the numbers to
   `sequence-statistics` and `information-theory-sequences`.
3. **Pin the data.** Record accession and version, organism, genome build and annotation release,
   file format, and licence or consent (`biological-databases`). A result without these cannot be repeated.
4. **Route each step** with the table below. Say which skill, which input and which output, and
   run each step on a toy input with a known answer before the real data.
5. **Plan the controls and the design** with `experimental-design` when samples are still to be
   collected. At least one positive control (a case where the answer is known to be
   yes), one negative control (known to be no), and one independent method or dataset.
6. **Plan the build.** Hand environment, seeds, tests and records to `reproducible-research-code`.
7. **Set the stopping rule** before looking: which results end the work, which trigger a second
   look, and the number of comparisons being made.
8. **Review before claiming.** Pass the result to `bioinformatics-review`. A finding that has not
   survived review is a lead, not a result.
9. **Hand back** the plan using `assets/templates/analysis-plan.md`.

## Decision framework

| The question is about | Use |
|---|---|
| How many samples, replicates, controls, batches, power | `experimental-design` |
| Finding data, identifiers, versions, annotation reliability, depositing data | `biological-databases` |
| Consent, privacy, controlled-access data, sharing, using online tools with sensitive data | `data-governance-ethics` |
| Opening, checking or converting FASTA, FASTQ, GFF3, SAM or BED, or a coordinate mix-up | `sequence-formats` |
| Reads to alignments, variants or counts; flags, CIGAR strings, depth | `ngs-pipelines` |
| How alike two sequences are, or whether a match is more than chance | `sequence-alignment` |
| Genes, open reading frames, translation, GC content, codon or word counts | `gene-finding-translation` |
| Protein mass, composition, hydropathy, structure, function claims | `protein-analysis` |
| Relationships between sequences, trees, distances | `phylogenetics` |
| VCF files, allele frequencies, Hardy-Weinberg, linkage, association results | `variants-population-genetics` |
| Expression, protein or metabolite tables, clustering, networks | `omics-data-analysis` |
| Entropy, complexity, conservation, compression, mutual information | `information-theory-sequences` |
| Counting, probabilities, likelihood, p-values, multiple testing | `sequence-statistics` |
| Predictive models, validation, leakage, metrics | `machine-learning-biology` |
| Writing code, large files, speed, memory, numerical problems | `bioinformatics-programming` |
| Environments, tests, records, pipelines, data rules | `reproducible-research-code` |
| Writing methods, wording claims, figures, availability statements, reviewer replies | `research-writing-reporting` |
| Whether a finished analysis or paper can be trusted | `bioinformatics-review` |
| Learning bioinformatics, a study plan, exercises, projects | `bioinformatics-learning-path` |

`references/book-map.md` lists which chapters of the source text sit behind each skill.

## Implementation guidance

- Start small. A 1,000-base toy input with a hand-checked answer finds the mistakes that a
  3-gigabase run hides.
- Prefer the simplest method that answers the claim. Every added step is a new place to be wrong.
- Keep the question, the null and the stopping rule in the repository next to the code.
- When two skills overlap, run both and compare. Disagreement is information.

## Failure and edge cases

- **No null model.** A pattern is reported with no statement of how often chance makes it.
- **Pipeline before toy test.** The first real run is also the first test.
- **Moving target.** Reference genome, annotation or database updated mid-project.
- **Circular evidence.** A database annotation that was itself copied from the method under test.
- **Too many looks.** Many parameter settings tried, the best one reported as if it were the plan.
- **Scale hides error.** An off-by-one coordinate or a swapped label affects millions of rows
  quietly; only a known-answer test sees it.
- **Wrong tool for the data type,** for example clustering on a table of mixed units.

## Validation

- Every step in the plan has an input, an output, an owner skill and a check.
- The claim can be false: write the result that would falsify it.
- The toy run reproduces its known answer before the real run starts.
- Falsifier: a reviewer reading only the plan cannot tell what would change your mind.

## Expected output

A plan: claim, null model, data and provenance, steps with the skill for each, controls, stopping
rule, build notes, and the review step. Use `assets/templates/analysis-plan.md`.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed., chs. 1.1-1.2 (supplied text): the definition
  as information science applied to biology; the sequence must depart from randomness; the -omics
  in scope; practical programming and database handling are explicitly left out
- Chapter map: from the table of contents (supplied), see `references/book-map.md`
- Workflow structure, controls, stopping rules: own design from general practice; VERIFY against
  the conventions of the user's field
- Not covered: wet-lab design, clinical interpretation, regulatory submission
