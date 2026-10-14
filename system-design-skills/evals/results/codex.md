# Codex smoke test: system-design-skills

The same starter prompts were run once with the skills installed in `.agents/skills` and once with none, using `codex exec` (Codex CLI codex-cli 0.162.1, model default). Grading is by the same regular expressions as the Claude runs. A skill counts as used when the agent reads its SKILL.md. Codex reports tokens but not cost, and there is no model judge here, so this checks that the skills are found and used in Codex, not how good the answers are. One run per prompt and arm.

| | Every expected fact | Expected skill used | Any skill used | Mean output tokens | Mean input tokens |
|---|---|---|---|---|---|
| With the skills | 18/20 | 20/20 | 20/20 | 1,940 | 136,639 |
| No skills | 19/20 | n/a | n/a | 1,479 | 102,171 |

| Skill | Facts with | Facts without | Skill used |
|---|---|---|---|
| `api-networking` | 3/3 | 3/3 | yes |
| `architecture-scaling` | 3/3 | 3/3 | yes |
| `caching-performance` | 3/3 | 3/3 | yes |
| `database-selection` | 3/3 | 3/3 | yes |
| `deployment-delivery` | 3/3 | 3/3 | yes |
| `geospatial-design` | 3/3 | 3/3 | yes |
| `identity-security` | 3/3 | 3/3 | yes |
| `messaging-streaming` | 3/3 | 3/3 | yes |
| `observability` | 3/3 | 3/3 | yes |
| `payment-systems` | 3/3 | 3/3 | yes |
| `performance-evaluation-methodology` | 3/3 | 1/3 | yes |
| `reliability-resilience` | 2/3 | 3/3 | yes |
| `requirements-capacity` | 3/3 | 3/3 | yes |
| `sharding-replication` | 3/3 | 3/3 | yes |
| `storage-systems` | 3/3 | 3/3 | yes |
| `system-design` | 3/3 | 3/3 | yes |
| `system-design-review` | 3/3 | 3/3 | yes |
| `systems-literature-reading` | 2/3 | 3/3 | yes |
| `systems-research-writing` | 3/3 | 3/3 | yes |
| `transactions-consistency` | 2/2 | 2/2 | yes |
