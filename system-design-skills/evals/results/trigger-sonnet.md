# Trigger results: system-design-skills

Engine direct. Agent model claude-sonnet-5-5, judge model claude-sonnet-5-5 (3 votes per verdict), 2 runs per case. Trigger runs stop at the first skill call, so their cost is not tallied.

Each skill has a should-trigger prompt (written without naming the skill) and a near-miss prompt that shares vocabulary but belongs elsewhere; there are also unrelated prompts that should trigger nothing. Every prompt was run several times with the skills installed and the first skill the agent invoked was recorded from its tool calls. A should-trigger run passes when the expected skill was invoked; a near-miss run passes when the named skill was not.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Measure | Value |
|---|---|
| Recall on should-trigger prompts | 58% (42-71) |
| Specificity on near-miss prompts | 100% (91-100) |
| Precision (invoked when it should be) | 100% (86-100) |
| Unrelated prompts that triggered a skill | 0/4 |

Recall 0.57, precision 1.00, specificity 1.00. Wilson 95% intervals; runs of one prompt are not independent.

## By skill

| Skill | Should-trigger runs hit | Near-miss runs that falsely triggered |
|---|---|---|
| `api-networking` | 0/2 | 0/2 |
| `architecture-scaling` | 0/2 | 0/2 |
| `caching-performance` | 2/2 | 0/2 |
| `database-selection` | 0/2 | 0/2 |
| `deployment-delivery` | 1/2 | 0/2 |
| `geospatial-design` | 2/2 | 0/2 |
| `identity-security` | 2/2 | 0/2 |
| `messaging-streaming` | 1/2 | 0/2 |
| `observability` | 2/2 | 0/2 |
| `payment-systems` | 2/2 | 0/2 |
| `performance-evaluation-methodology` | 0/2 | 0/2 |
| `reliability-resilience` | 2/2 | 0/2 |
| `requirements-capacity` | 0/2 | 0/2 |
| `sharding-replication` | 2/2 | 0/2 |
| `storage-systems` | 2/2 | 0/2 |
| `system-design` | 0/2 | 0/2 |
| `system-design-review` | 2/2 | 0/2 |
| `systems-literature-reading` | 0/2 | 0/2 |
| `systems-research-writing` | 2/2 | 0/2 |
| `transactions-consistency` | 1/2 | 0/2 |
