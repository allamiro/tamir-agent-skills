# Model-judged pairwise comparison

A claude-sonnet-5-5 judge compared the first with-skill answer and the first no-skill answer for each skill, in both orders. A skill wins only if the judge prefers the same answer in both orders; otherwise the pair is counted as inconsistent (position bias) or a tie. This is a model's opinion, from the same family as the answers, and one answer pair per skill: not a substitute for human graders (`evals/human/`).

| Skill preferred | Baseline preferred | Tie | Inconsistent across orders | Share preferring the skill, ties and inconsistent set aside (95%% interval) | Sign test p |
|---|---|---|---|---|---|
| 15 | 3 | 3 | 2 | 83% (61-94) | 0.008 |

| Skill | Verdict |
|---|---|
| `bioinformatics-learning-path` | skill |
| `bioinformatics-programming` | skill |
| `bioinformatics-review` | skill |
| `bioinformatics-workflow` | skill |
| `biological-databases` | baseline |
| `data-governance-ethics` | skill |
| `experimental-design` | skill |
| `gene-finding-translation` | skill |
| `information-theory-sequences` | inconsistent |
| `literature-search-appraisal` | skill |
| `machine-learning-biology` | skill |
| `method-benchmarking` | baseline |
| `ngs-pipelines` | baseline |
| `omics-data-analysis` | tie |
| `phylogenetics` | tie |
| `protein-analysis` | skill |
| `reproducible-research-code` | skill |
| `research-proposal-planning` | skill |
| `research-writing-reporting` | skill |
| `sequence-alignment` | inconsistent |
| `sequence-formats` | skill |
| `sequence-statistics` | tie |
| `variants-population-genetics` | skill |
