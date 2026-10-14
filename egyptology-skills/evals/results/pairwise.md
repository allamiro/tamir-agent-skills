# Model-judged pairwise comparison

A claude-sonnet-5-5 judge compared the first with-skill answer and the first no-skill answer for each skill, in both orders. A skill wins only if the judge prefers the same answer in both orders; otherwise the pair is counted as inconsistent (position bias) or a tie. This is a model's opinion, from the same family as the answers, and one answer pair per skill: not a substitute for human graders (`evals/human/`).

| Skill preferred | Baseline preferred | Tie | Inconsistent across orders | Share preferring the skill, ties and inconsistent set aside (95%% interval) | Sign test p |
|---|---|---|---|---|---|
| 4 | 2 | 0 | 2 | 67% (30-90) | 0.688 |

| Skill | Verdict |
|---|---|
| `accuracy-review` | baseline |
| `edition-conventions` | skill |
| `egyptology-literature` | baseline |
| `gardiner-sign-lookup` | skill |
| `hieroglyph-app-builder` | inconsistent |
| `provenance-research-ethics` | skill |
| `text-annotation` | inconsistent |
| `transliteration` | skill |
