# Trigger results: system-design-skills

Engine direct. Agent model claude-opus-5-5, judge model default (1 vote per verdict), 3 runs per case. Trigger runs stop at the first skill call, so their cost is not tallied.

Each skill has a should-trigger prompt (written without naming the skill) and a near-miss prompt that shares vocabulary but belongs elsewhere; there are also unrelated prompts that should trigger nothing. Every prompt was run several times with the skills installed and the first skill the agent invoked was recorded from its tool calls. A should-trigger run passes when the expected skill was invoked; a near-miss run passes when the named skill was not.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Measure | Value |
|---|---|
| Recall on should-trigger prompts | 60% (47-71) |
| Specificity on near-miss prompts | 100% (94-100) |
| Precision (invoked when it should be) | 100% (90-100) |
| Unrelated prompts that triggered a skill | 0/6 |

Recall 0.60, precision 1.00, specificity 1.00. Wilson 95% intervals; runs of one prompt are not independent.

## By skill

| Skill | Should-trigger runs hit | Near-miss runs that falsely triggered |
|---|---|---|
| `api-networking` | 0/3 | 0/3 |
| `architecture-scaling` | 1/3 | 0/3 |
| `caching-performance` | 3/3 | 0/3 |
| `database-selection` | 1/3 | 0/3 |
| `deployment-delivery` | 2/3 | 0/3 |
| `geospatial-design` | 3/3 | 0/3 |
| `identity-security` | 3/3 | 0/3 |
| `messaging-streaming` | 3/3 | 0/3 |
| `observability` | 2/3 | 0/3 |
| `payment-systems` | 2/3 | 0/3 |
| `performance-evaluation-methodology` | 1/3 | 0/3 |
| `reliability-resilience` | 2/3 | 0/3 |
| `requirements-capacity` | 0/3 | 0/3 |
| `sharding-replication` | 3/3 | 0/3 |
| `storage-systems` | 1/3 | 0/3 |
| `system-design` | 2/3 | 0/3 |
| `system-design-review` | 3/3 | 0/3 |
| `systems-literature-reading` | 1/3 | 0/3 |
| `systems-research-writing` | 3/3 | 0/3 |
| `transactions-consistency` | 0/3 | 0/3 |
