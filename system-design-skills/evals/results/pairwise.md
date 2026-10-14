# Model-judged pairwise comparison

A claude-sonnet-5-5 judge compared the first with-skill answer and the first no-skill answer for each skill, in both orders. A skill wins only if the judge prefers the same answer in both orders; otherwise the pair is counted as inconsistent (position bias) or a tie. This is a model's opinion, from the same family as the answers, and one answer pair per skill: not a substitute for human graders (`evals/human/`).

| Skill preferred | Baseline preferred | Tie | Inconsistent across orders | Share preferring the skill, ties and inconsistent set aside (95%% interval) | Sign test p |
|---|---|---|---|---|---|
| 14 | 4 | 0 | 2 | 78% (55-91) | 0.031 |

| Skill | Verdict |
|---|---|
| `api-networking` | baseline |
| `architecture-scaling` | skill |
| `caching-performance` | skill |
| `database-selection` | skill |
| `deployment-delivery` | inconsistent |
| `geospatial-design` | skill |
| `identity-security` | skill |
| `messaging-streaming` | baseline |
| `observability` | baseline |
| `payment-systems` | skill |
| `performance-evaluation-methodology` | skill |
| `reliability-resilience` | inconsistent |
| `requirements-capacity` | skill |
| `sharding-replication` | skill |
| `storage-systems` | skill |
| `system-design` | skill |
| `system-design-review` | skill |
| `systems-literature-reading` | baseline |
| `systems-research-writing` | skill |
| `transactions-consistency` | skill |
