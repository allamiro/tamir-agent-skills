# Codex smoke test: bioinformatics-skills

The same starter prompts were run once with the skills installed in `.agents/skills` and once with none, using `codex exec` (Codex CLI codex-cli 0.162.1, model default). Grading is by the same regular expressions as the Claude runs. A skill counts as used when the agent reads its SKILL.md. Codex reports tokens but not cost, and there is no model judge here, so this checks that the skills are found and used in Codex, not how good the answers are. One run per prompt and arm.

| | Every expected fact | Expected skill used | Any skill used | Mean output tokens | Mean input tokens |
|---|---|---|---|---|---|
| With the skills | 21/23 | 23/23 | 23/23 | 836 | 90,496 |
| No skills | 21/23 | n/a | n/a | 703 | 51,173 |

| Skill | Facts with | Facts without | Skill used |
|---|---|---|---|
| `bioinformatics-learning-path` | 2/2 | 2/2 | yes |
| `bioinformatics-programming` | 2/2 | 2/2 | yes |
| `bioinformatics-review` | 3/3 | 3/3 | yes |
| `bioinformatics-workflow` | 3/3 | 3/3 | yes |
| `biological-databases` | 2/2 | 2/2 | yes |
| `data-governance-ethics` | 3/3 | 2/3 | yes |
| `experimental-design` | 2/2 | 2/2 | yes |
| `gene-finding-translation` | 2/2 | 2/2 | yes |
| `information-theory-sequences` | 2/2 | 2/2 | yes |
| `literature-search-appraisal` | 3/3 | 3/3 | yes |
| `machine-learning-biology` | 1/2 | 2/2 | yes |
| `method-benchmarking` | 3/3 | 3/3 | yes |
| `ngs-pipelines` | 3/3 | 3/3 | yes |
| `omics-data-analysis` | 3/3 | 3/3 | yes |
| `phylogenetics` | 2/2 | 2/2 | yes |
| `protein-analysis` | 1/1 | 1/1 | yes |
| `reproducible-research-code` | 3/3 | 3/3 | yes |
| `research-proposal-planning` | 2/3 | 2/3 | yes |
| `research-writing-reporting` | 3/3 | 3/3 | yes |
| `sequence-alignment` | 2/2 | 2/2 | yes |
| `sequence-formats` | 3/3 | 3/3 | yes |
| `sequence-statistics` | 3/3 | 3/3 | yes |
| `variants-population-genetics` | 3/3 | 3/3 | yes |
