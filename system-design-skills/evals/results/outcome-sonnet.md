# Outcome results: system-design-skills

Engine direct. Agent model claude-sonnet-5-5, judge model claude-sonnet-5-5 (3 votes per verdict), 2 runs per case. Cost of this run, agent and judge at list price: 13.05 US dollars.

Each skill's starter prompt was run 2 times with the skills installed and 2 times with none, each in a fresh Claude Code project. Three kinds of check are reported separately: **facts** (regular expressions for the key facts in the answer), **rubric** (a model judges the answer against the prompt's own "a good answer" description) and **limits stated** (a model checks that the answer marks specific items as unverified or assumed and says what it did check). The judge is a model, not a person.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Check | With the skills | No skills | Difference (95% interval) |
|---|---|---|---|
| Every expected fact present | 95% (83-99) | 95% (83-99) | +0 points (-12 to +12) |
| Rubric passed | 100% (91-100) | 90% (77-96) | +10 points (-1 to +23) |
| States its limits | 65% (50-78) | 40% (26-55) | +25 points (+3 to +44) |
| Expected skill invoked | 95% (83-99) | n/a | |
| Its script run (skills that ship one, and not denied) | 25% (7-59) | n/a | |

Cells are the share of runs, with a Wilson 95% interval. Runs: 40 with, 40 without (20 skills). Runs of the same skill are not independent, so the intervals are narrower than the true uncertainty.

Runs in which the permission mode denied at least one tool call: 0 of 40 with the skills, 0 of 40 without. Denied calls do not count as a script run.

Consistency (pass^2: the chance that all 2 runs of a skill pass): facts 0.95 with the skills, 0.90 without; rubric 1.00 with, 0.90 without.

Tokens and cost, mean per run: output tokens 3,460 with and 4,209 without; input tokens processed (including cached) 90,418 with and 64,279 without; cost 0.105 with and 0.085 without US dollars; total spent on these runs 7.59 (agent runs only, judge calls excluded).

## By skill

| Skill | Facts with | Facts without | Rubric with | Rubric without | Limits with | Limits without | Skill invoked | Script run |
|---|---|---|---|---|---|---|---|---|
| `api-networking` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | n/a |
| `architecture-scaling` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 2/2 | n/a |
| `caching-performance` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 2/2 | n/a |
| `database-selection` | 2/2 | 2/2 | 2/2 | 0/2 | 1/2 | 0/2 | 2/2 | n/a |
| `deployment-delivery` | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 0/2 | 2/2 | n/a |
| `geospatial-design` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 2/2 | n/a |
| `identity-security` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | n/a |
| `messaging-streaming` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 2/2 | n/a |
| `observability` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| `payment-systems` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | n/a |
| `performance-evaluation-methodology` | 2/2 | 2/2 | 2/2 | 0/2 | 1/2 | 0/2 | 2/2 | 0/2 |
| `reliability-resilience` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | n/a |
| `requirements-capacity` | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 2/2 | 0/2 | 0/2 |
| `sharding-replication` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | n/a |
| `storage-systems` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 2/2 | n/a |
| `system-design` | 2/2 | 1/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | n/a |
| `system-design-review` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | n/a |
| `systems-literature-reading` | 0/2 | 1/2 | 2/2 | 2/2 | 2/2 | 1/2 | 2/2 | 0/2 |
| `systems-research-writing` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | n/a |
| `transactions-consistency` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | n/a |
