<p align="center">
  <img src="assets/banner.svg" alt="Bioinformatics Skills: research, data, analysis, code and review, with the checks shown" width="100%">
</p>

<p align="center">
  <img alt="20 skills" src="https://img.shields.io/badge/skills-20-6c64eb?style=flat-square&labelColor=0c3b3a">
  <img alt="13 tested scripts" src="https://img.shields.io/badge/tested%20scripts-13-096efb?style=flat-square&labelColor=0c3b3a">
  <img alt="skills-ref valid" src="https://img.shields.io/badge/skills--ref-valid-9cc464?style=flat-square&labelColor=0c3b3a">
  <img alt="License Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-fb6373?style=flat-square&labelColor=0c3b3a">
</p>

Twenty skills for the whole of a bioinformatics project, not only the code: planning and study
design, finding and citing data, privacy and ethics, file formats, sequencing pipelines, alignment,
genes and proteins, trees, variants, omics tables, statistics, machine learning, programming,
reproducibility, writing up, review, and learning the field. They treat bioinformatics as information
science applied to biology, so every skill asks what chance would give before it reports a pattern.
Every output is a draft for someone who knows the data; the skills show where the doubt is instead of
hiding it.

## Which one is for my tool?

| I use | Read | Install | Status |
|---|---|---|---|
| **Claude Code** | [`claude/`](claude/README.md) | `bash scripts/install.sh --claude --project DIR` | Works |
| **OpenAI Codex** | [`openai/`](openai/README.md#codex) | `bash scripts/install.sh --codex --project DIR` | Works |
| **ChatGPT desktop app** | [`openai/`](openai/README.md#chatgpt) | [20 zips](openai/chatgpt/) | Zips built; how the app takes them is not confirmed |
| **OpenAI Skills API** | [`openai/`](openai/README.md#openai-skills-api) | [20 zips](openai/chatgpt/) | Zips built to the documented format and limits |

Claude Code and Codex read the same files from [`skills/`](skills/). Nothing is copied per platform,
so there is one place to fix a skill. The zips are built from `skills/` and checked for being current.

## What is in this folder

```text
bioinformatics-skills/
├── skills/     the 20 skills (SKILL.md plus references, scripts and templates)
├── claude/     Claude Code: install and use
├── openai/     OpenAI: Codex, ChatGPT and the Skills API, with chatgpt/ holding one zip per skill
├── prompts/    ready-to-paste prompts, one file per skill
├── scripts/    install.sh, build_chatgpt.py, validate_collection.py, check_routing.py, check_answers.py
└── assets/     banner
```

## Skills

### Plan and research context

| Skill | Use it for | Prompts |
|---|---|---|
| [`bioinformatics-workflow`](skills/bioinformatics-workflow/) | The coordinator: a claim the data could refute, the null model, data provenance, controls, and which skill does each step | [5](prompts/bioinformatics-workflow.md) |
| [`experimental-design`](skills/experimental-design/) | Replicates, controls, batch layout, sample size and power before data are collected | [6](prompts/experimental-design.md) |
| [`biological-databases`](skills/biological-databases/) | Identifiers, versions and builds, ID mapping, annotation reliability, citing and depositing data | [6](prompts/biological-databases.md) |
| [`data-governance-ethics`](skills/data-governance-ethics/) | Consent, privacy, controlled access, sharing, and care with online tools (guidance, not legal advice) | [6](prompts/data-governance-ethics.md) |
| [`research-writing-reporting`](skills/research-writing-reporting/) | Methods sections, claim wording, figures, availability statements, reviewer replies | [6](prompts/research-writing-reporting.md) |
| [`bioinformatics-learning-path`](skills/bioinformatics-learning-path/) | A study plan for your background, exercises with checkable answers, projects | [5](prompts/bioinformatics-learning-path.md) |

### Sequences and genomes

| Skill | Use it for | Prompts |
|---|---|---|
| [`sequence-formats`](skills/sequence-formats/) | FASTA, FASTQ, GFF3, BED and SAM, Phred qualities, and 0-based versus 1-based coordinates | [6](prompts/sequence-formats.md) |
| [`ngs-pipelines`](skills/ngs-pipelines/) | Reads to alignments, variants or counts; SAM flags, CIGAR strings, coverage and depth | [6](prompts/ngs-pipelines.md) |
| [`sequence-alignment`](skills/sequence-alignment/) | Global and local alignment, scoring choices, a shuffle test for the score | [6](prompts/sequence-alignment.md) |
| [`gene-finding-translation`](skills/gene-finding-translation/) | Reverse complement, GC, k-mers, translation, open reading frames and their chance level | [6](prompts/gene-finding-translation.md) |
| [`protein-analysis`](skills/protein-analysis/) | Protein mass, composition, hydropathy, structure and function evidence | [6](prompts/protein-analysis.md) |
| [`phylogenetics`](skills/phylogenetics/) | Distances, UPGMA and neighbour-joining trees, Newick, rooting and support | [6](prompts/phylogenetics.md) |
| [`variants-population-genetics`](skills/variants-population-genetics/) | VCF files, allele frequencies, Hardy-Weinberg, linkage, association caveats | [6](prompts/variants-population-genetics.md) |

### Omics, statistics and models

| Skill | Use it for | Prompts |
|---|---|---|
| [`omics-data-analysis`](skills/omics-data-analysis/) | Design checks, batch effects, clustering, PCA, enrichment and networks for omics tables | [6](prompts/omics-data-analysis.md) |
| [`information-theory-sequences`](skills/information-theory-sequences/) | Entropy, diversity numbers, motif information, mutual information, compression distance | [6](prompts/information-theory-sequences.md) |
| [`sequence-statistics`](skills/sequence-statistics/) | Counting, binomial and hypergeometric tails, expected word counts, Markov chains, multiple testing | [6](prompts/sequence-statistics.md) |
| [`machine-learning-biology`](skills/machine-learning-biology/) | Leakage-safe splits, metrics for imbalanced data, near-duplicate checks, model cards | [6](prompts/machine-learning-biology.md) |

### Code, reproducibility and review

| Skill | Use it for | Prompts |
|---|---|---|
| [`bioinformatics-programming`](skills/bioinformatics-programming/) | Large files, packed sequences, log-space arithmetic, linear windows, common bugs | [6](prompts/bioinformatics-programming.md) |
| [`reproducible-research-code`](skills/reproducible-research-code/) | Data records, pinned environments, seeds, tests that can fail, sensitive data | [6](prompts/reproducible-research-code.md) |
| [`bioinformatics-review`](skills/bioinformatics-review/) | Audit of an analysis or claim: sources, null models, leakage, batch, ranked findings | [6](prompts/bioinformatics-review.md) |

## How researchers would use them

- Turn a loose question into a plan with a null model, controls and a sample size before running anything.
- Identify and pin the exact records, builds and releases an analysis used, and cite them.
- Check a list of p-values, a motif count or an alignment score against what chance gives.
- Read a FASTQ, GFF3, BED or VCF file without the off-by-one error that quietly shifts every feature.
- Translate and find open reading frames, and see how often chance alone gives one that long.
- Decode a SAM flag or a CIGAR string, and work out how much sequencing is enough.
- Evaluate a classifier without leakage, and write up the result at the strength the evidence supports.
- Learn the field from your own starting point, with exercises you can check by running something.

## Install

Run from this folder. Install all 20 skills together: the coordinator hands work to the others.

```bash
bash scripts/install.sh --claude --project /path/to/your/repo   # Claude Code
bash scripts/install.sh --codex --project /path/to/your/repo    # OpenAI Codex
```

Add `--user` to install for every project on the machine, `--symlink` to link instead of copy,
`--force` to replace, or `--dry-run` to preview. Details: [`claude/`](claude/README.md) and
[`openai/`](openai/README.md).

## Scripts you can run

Each needs only Python 3.9 or later and has a `--selftest` with hand-computed values.

| Script | Skill | What it does |
|---|---|---|
| `seqinfo.py` | `information-theory-sequences` | Entropy, diversity numbers, mutual information, compression distance |
| `seqstats.py` | `sequence-statistics` | Sampling counts, binomial and hypergeometric tails, expected counts, p-value adjustment |
| `align.py` | `sequence-alignment` | Global and local alignment, shuffle significance |
| `seqformats.py` | `sequence-formats` | FASTA, FASTQ and GFF3 checks, coordinate conversion |
| `genecode.py` | `gene-finding-translation` | Reverse complement, translation, ORFs, chance level of open frames |
| `tree.py` | `phylogenetics` | Distances, UPGMA, neighbour-joining, Newick |
| `design.py` | `experimental-design` | Sample size, power, batch layout, confounding check |
| `accessions.py` | `biological-databases` | Identifier formats, versions, ambiguity |
| `ngs.py` | `ngs-pipelines` | SAM flags, CIGAR arithmetic, coverage |
| `popgen.py` | `variants-population-genetics` | Hardy-Weinberg, linkage, VCF summary |
| `protein.py` | `protein-analysis` | Composition, mass, hydropathy |
| `mlmetrics.py` | `machine-learning-biology` | Metrics, group folds, near-duplicates |
| `bioprog.py` | `bioinformatics-programming` | Two-bit packing, canonical k-mers, log-sum-exp, streaming |

## Try it

Pick a skill's prompt file from [`prompts/`](prompts/README.md). Or run a script directly:

```bash
python3 skills/gene-finding-translation/scripts/genecode.py orfs CATGAAATAGCCCC --min-aa 2
python3 skills/sequence-alignment/scripts/align.py global GCATGCG GATTACA
python3 skills/experimental-design/scripts/design.py n --d 0.5
python3 skills/ngs-pipelines/scripts/ngs.py flags 99
python3 skills/protein-analysis/scripts/protein.py mass DRVYIHPF --mono
python3 skills/machine-learning-biology/scripts/mlmetrics.py auc 0,0,1,1 0.1,0.4,0.35,0.8
```

## Check it

```bash
python3 scripts/validate_collection.py          # structure, links, prompts, script self-tests, bundles current
python3 scripts/check_answers.py                # exercises and good-answer lines against the scripts
python3 scripts/check_routing.py                # description routing for the starter prompts
python3 scripts/build_chatgpt.py --fresh        # zips are valid and match the skills
skills-ref validate skills/<name>               # official Agent Skills validator
claude plugin validate skills                   # Claude Code's own check of the skill files
python3 scripts/live_check.py --dry-run         # free; add --run to spend API credit on live runs
```

Last run, 2026-10-14: the collection validator reports 0 errors on Python 3.9 and 3.14 (20 skills, 13
scripts); the 13 script self-tests pass with 2,274 checks in all; a mutation run that breaks the scripts in
89 places is caught every time; `skills-ref` accepts all 20 skills and all 20 zips; `claude plugin
validate` accepts the skills; markdownlint reports 0 issues; 71 answer checks pass; and all 20 starter
prompts route to their own skill. Routing is a word-match check, not a model of how an LLM picks a skill.

### Live runs

The 20 starter prompts were also run once each through a real Claude Code session (2.1.296, model
claude-opus-5-5) with the skills installed ([results](evals/live-results.md)), and again with no skills
installed ([baseline](evals/live-results-baseline.md)). Grading is by regular expression for the key facts,
one run per prompt, on one day.

| | Expected skill invoked | Answers with every expected fact | Cost |
|---|---|---|---|
| With the skills | 9 of 20 | 20 of 20 | 3.13 US dollars |
| No skills installed | 0 of 20 | 19 of 20 | 2.01 US dollars |

What this does and does not show: on these prompts a strong model already knew the key facts, so the
skills made little difference to the facts and added cost for loading them. The skills fired mostly on
planning and judgement prompts and less on self-contained calculations, where the model often worked the
answer out itself. The checks cannot see what the skills are for: using the verified scripts, flagging
doubt, and ranking findings. Not run: independent human grading of answer quality, or repeated runs.

## Contribute

See [CONTRIBUTING.md](../CONTRIBUTING.md). Add a script only with a self-test that uses hand-computed
values or an independent cross-check, and check that the test can fail.

## License

Apache-2.0

## Citation

Ramsden, Jeremy J. 2009. *Bioinformatics: An Introduction*. 2nd ed. Computational Biology Series.
London: Springer. DOI 10.1007/978-1-84800-257-9.
