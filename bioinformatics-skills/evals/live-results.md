# Live runs

Measured on 2026-10-14 with 2.1.296 (Claude Code), model claude-opus-5-5. Each row is one starter prompt run once in a clean project with the skills installed (`python3 scripts/live_check.py --run`). Grading is by regular expression on the final answer, not a judgement of quality. This is one run per prompt on one day: it shows what happened, not what always happens.

- The expected skill was invoked in **9 of 20** runs; some skill was invoked in 9.
- The answer matched every expected fact in **20 of 20** runs.
- Total cost 3.13 US dollars.

| Skill | Expected skill invoked | Skills invoked | Script run | Facts matched | Cost (USD) | Seconds |
|---|---|---|---|---|---|---|
| `bioinformatics-workflow` | yes | bioinformatics-workflow | none | 3 of 3 | 0.20 | 36 |
| `experimental-design` | no | none | none | 2 of 2 | 0.14 | 22 |
| `biological-databases` | yes | biological-databases | `accessions.py` | 2 of 2 | 0.14 | 17 |
| `data-governance-ethics` | yes | data-governance-ethics | none | 3 of 3 | 0.13 | 17 |
| `sequence-formats` | no | none | none | 3 of 3 | 0.11 | 18 |
| `ngs-pipelines` | no | none | none | 3 of 3 | 0.10 | 11 |
| `sequence-alignment` | no | none | `nw.py` | 2 of 2 | 0.13 | 17 |
| `gene-finding-translation` | no | none | none | 2 of 2 | 0.09 | 5 |
| `protein-analysis` | no | none | none | 1 of 1 | 0.10 | 10 |
| `phylogenetics` | no | none | none | 2 of 2 | 0.10 | 13 |
| `variants-population-genetics` | no | none | none | 3 of 3 | 0.11 | 13 |
| `omics-data-analysis` | yes | omics-data-analysis | `preflight.py` | 3 of 3 | 0.33 | 67 |
| `information-theory-sequences` | no | none | none | 2 of 2 | 0.12 | 22 |
| `sequence-statistics` | no | none | none | 3 of 3 | 0.09 | 5 |
| `machine-learning-biology` | no | none | none | 2 of 2 | 0.10 | 14 |
| `bioinformatics-programming` | yes | bioinformatics-programming | `bioprog.py` | 2 of 2 | 0.15 | 19 |
| `reproducible-research-code` | yes | reproducible-research-code | `__init__.py`, `fetch_data.py`, `provenance.py`, `test_provenance.py`, `verify_data.py` | 3 of 3 | 0.46 | 93 |
| `research-writing-reporting` | yes | research-writing-reporting | none | 3 of 3 | 0.14 | 20 |
| `bioinformatics-review` | yes | bioinformatics-review | none | 3 of 3 | 0.16 | 30 |
| `bioinformatics-learning-path` | yes | bioinformatics-learning-path | none | 2 of 2 | 0.19 | 36 |

## What the facts were

| Skill | A correct answer matches all of |
|---|---|
| `bioinformatics-workflow` | `null`; `batch`; `claim` |
| `experimental-design` | `\b64\b`; `\b2[45]\d\b` |
| `biological-databases` | `RefSeq`; `version` |
| `data-governance-ethics` | `not (be )?anonymous\|identif\|re-identif`; `relative\|unique`; `consent\|agreement` |
| `sequence-formats` | `duplicate\|repeated`; `protein`; `empty` |
| `ngs-pipelines` | `\b99\b\|paired`; `147`; `reverse` |
| `sequence-alignment` | `score[^.\n]{0,25}\b0\b\|\*\*0\*\*`; `three\|3 (optimal\|alignments)` |
| `gene-finding-translation` | `MK\*`; `stop` |
| `protein-analysis` | `1045\.5` |
| `phylogenetics` | `0\.107`; `saturat\|0\.75\|undefined` |
| `variants-population-genetics` | `1-based`; `unphased`; `phased` |
| `omics-data-analysis` | `batch`; `PCA`; `replicate\|confound` |
| `information-theory-sequences` | `2(\.0+)? bits\|\b2\.0+\b`; `2\.8` |
| `sequence-statistics` | `\b16\b`; `\b12\b`; `\b10\b` |
| `machine-learning-biology` | `baseline\|always (predict\|say)\|majority`; `average precision\|MCC\|precision-recall\|AUPRC` |
| `bioinformatics-programming` | `stream\|one record at a time\|line by line`; `memory` |
| `reproducible-research-code` | `checksum`; `seed`; `environment\|lock` |
| `research-writing-reporting` | `GRCh38`; `SRR1234567`; `Benjamini\|BH` |
| `bioinformatics-review` | `batch`; `correct\|multiple`; `critical\|major` |
| `bioinformatics-learning-path` | `week`; `program\|Python\|script` |
