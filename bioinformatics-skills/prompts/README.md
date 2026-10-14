# Prompts

Each skill has its own file of ready-to-paste prompts. Open the skill you need, copy a prompt, and
replace the `<angle-bracket>` parts with your own sequences, tables and files.

## Plan and research context

| Skill | Prompts | Use them to |
|---|---|---|
| `bioinformatics-workflow` | [5 prompts](bioinformatics-workflow.md) | Plan an analysis from question to result, with a null model and controls |
| `experimental-design` | [6 prompts](experimental-design.md) | Work out samples, replicates, controls and batch layout before collecting data |
| `biological-databases` | [6 prompts](biological-databases.md) | Identify, version, map, cite and deposit data |
| `data-governance-ethics` | [6 prompts](data-governance-ethics.md) | Work carefully with human and sensitive data |
| `research-writing-reporting` | [6 prompts](research-writing-reporting.md) | Write methods, word claims honestly, answer reviewers |
| `bioinformatics-learning-path` | [5 prompts](bioinformatics-learning-path.md) | Get a study plan, exercises and projects that fit your background |

## Academic and research

| Skill | Prompts | Use them to |
|---|---|---|
| `literature-search-appraisal` | [6 prompts](literature-search-appraisal.md) | Build and log a search, appraise a method paper, and check references for invented citations |
| `method-benchmarking` | [6 prompts](method-benchmarking.md) | Design or audit a tool comparison and test whether a gain is real |
| `research-proposal-planning` | [6 prompts](research-proposal-planning.md) | Turn an idea into aims, a data management plan, a schedule and a risk list |

## Sequences and genomes

| Skill | Prompts | Use them to |
|---|---|---|
| `sequence-formats` | [6 prompts](sequence-formats.md) | Read and check FASTA, FASTQ and GFF3, and settle coordinates |
| `ngs-pipelines` | [6 prompts](ngs-pipelines.md) | Plan and check pipelines from reads to alignments, variants or counts |
| `sequence-alignment` | [6 prompts](sequence-alignment.md) | Align two sequences, explain the score, test it against shuffles |
| `gene-finding-translation` | [6 prompts](gene-finding-translation.md) | Translate, find open reading frames, and judge them against chance |
| `protein-analysis` | [6 prompts](protein-analysis.md) | Compute protein mass and hydropathy, and grade structure and function claims |
| `phylogenetics` | [6 prompts](phylogenetics.md) | Build distance trees and read Newick strings |
| `variants-population-genetics` | [6 prompts](variants-population-genetics.md) | Read VCF files, test Hardy-Weinberg, measure linkage |

## Omics, statistics and models

| Skill | Prompts | Use them to |
|---|---|---|
| `omics-data-analysis` | [6 prompts](omics-data-analysis.md) | Check the design, cluster, test and build networks from omics tables |
| `information-theory-sequences` | [6 prompts](information-theory-sequences.md) | Measure entropy, diversity, conservation and compression distance |
| `sequence-statistics` | [6 prompts](sequence-statistics.md) | Count possibilities, test enrichment, correct for many tests |
| `machine-learning-biology` | [6 prompts](machine-learning-biology.md) | Evaluate models without leakage, choose metrics, write a model card |

## Code, reproducibility and review

| Skill | Prompts | Use them to |
|---|---|---|
| `bioinformatics-programming` | [6 prompts](bioinformatics-programming.md) | Handle large files, underflow, compact sequences and slow loops |
| `reproducible-research-code` | [6 prompts](reproducible-research-code.md) | Structure, test and record an analysis so it can be rerun |
| `bioinformatics-review` | [6 prompts](bioinformatics-review.md) | Audit a finished analysis or claim and rank what is wrong |

## Which tool are these for

All of them. A prompt is plain text, so the same wording works in every tool that has the skills
installed: Claude Code ([`claude/`](../claude/README.md)) and OpenAI Codex or ChatGPT
([`openai/`](../openai/README.md)).

You never need to type a skill name. Describe the task and the agent picks the skill.

## Where to start

```text
bioinformatics-workflow  ->  the specialist for each step  ->  bioinformatics-review
   plan, null, controls      design, data, formats, pipelines,    audit before you claim
                             alignment, genes, proteins, trees,
                             variants, omics, statistics, models
```

`reproducible-research-code`, `bioinformatics-programming` and `data-governance-ethics` run alongside
the whole chain, and `research-writing-reporting` comes at the end. New to the field? Start with
`bioinformatics-learning-path`.

The numbers in the "a good answer" lines were computed with the scripts in the skills or checked by
hand, and `scripts/check_answers.py` reruns the computable ones. They show what a correct answer
contains, not what any agent will say.
