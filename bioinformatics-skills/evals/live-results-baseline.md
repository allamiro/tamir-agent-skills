# Live runs, no skills installed (baseline)

Measured on 2026-10-14 with 2.1.296 (Claude Code), model claude-opus-5-5. Each row is one starter prompt run once in a clean project with NO skills installed, for comparison with live-results.md (`python3 scripts/live_check.py --run --baseline`). Grading is by regular expression on the final answer, not a judgement of quality. This is one run per prompt on one day: it shows what happened, not what always happens.

- The expected skill was invoked in **0 of 20** runs; some skill was invoked in 0.
- The answer matched every expected fact in **19 of 20** runs.
- Total cost 2.01 US dollars.

| Skill | Expected skill invoked | Skills invoked | Script run | Facts matched | Cost (USD) | Seconds |
|---|---|---|---|---|---|---|
| `bioinformatics-workflow` | no | none | none | 3 of 3 | 0.13 | 37 |
| `experimental-design` | no | none | none | 2 of 2 | 0.10 | 32 |
| `biological-databases` | no | none | none | 2 of 2 | 0.07 | 13 |
| `data-governance-ethics` | no | none | none | 3 of 3 | 0.07 | 15 |
| `sequence-formats` | no | none | none | 3 of 3 | 0.08 | 17 |
| `ngs-pipelines` | no | none | none | 3 of 3 | 0.06 | 9 |
| `sequence-alignment` | no | none | `nw.py` | 2 of 2 | 0.09 | 15 |
| `gene-finding-translation` | no | none | none | 1 of 2 | 0.05 | 4 |
| `protein-analysis` | no | none | none | 1 of 1 | 0.06 | 9 |
| `phylogenetics` | no | none | none | 2 of 2 | 0.07 | 12 |
| `variants-population-genetics` | no | none | none | 3 of 3 | 0.06 | 13 |
| `omics-data-analysis` | no | none | none | 3 of 3 | 0.19 | 46 |
| `information-theory-sequences` | no | none | none | 2 of 2 | 0.09 | 22 |
| `sequence-statistics` | no | none | none | 3 of 3 | 0.05 | 4 |
| `machine-learning-biology` | no | none | none | 2 of 2 | 0.06 | 11 |
| `bioinformatics-programming` | no | none | none | 2 of 2 | 0.07 | 16 |
| `reproducible-research-code` | no | none | `__init__.py`, `checksums.py`, `fetch.py`, `platform.py`, `run.py`, `test_checksums.py`, `verify.py` | 3 of 3 | 0.42 | 92 |
| `research-writing-reporting` | no | none | none | 3 of 3 | 0.07 | 12 |
| `bioinformatics-review` | no | none | none | 3 of 3 | 0.12 | 39 |
| `bioinformatics-learning-path` | no | none | none | 2 of 2 | 0.10 | 29 |

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
