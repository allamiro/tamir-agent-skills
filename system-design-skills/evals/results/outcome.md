# Outcome results: system-design-skills

Engine direct. Agent model claude-opus-5-5, judge model claude-sonnet-5-5 (1 vote per verdict), 3 runs per case. Cost of this run, agent and judge at list price: 38.03 US dollars.

Each skill's starter prompt was run 3 times with the skills installed and 3 times with none, each in a fresh Claude Code project. Three kinds of check are reported separately: **facts** (regular expressions for the key facts in the answer), **rubric** (a model judges the answer against the prompt's own "a good answer" description) and **limits stated** (a model checks that the answer marks specific items as unverified or assumed and says what it did check). The judge is a model, not a person.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Check | With the skills | No skills | Difference (95% interval) |
|---|---|---|---|
| Every expected fact present | 98% (91-100) | 97% (89-99) | +2 points (-6 to +10) |
| Rubric passed | 100% (94-100) | 93% (84-97) | +7 points (-1 to +16) |
| States its limits | 52% (39-64) | 30% (20-43) | +22 points (+4 to +37) |
| Expected skill invoked | 98% (91-100) | n/a | |
| Its script run (skills that ship one, and not denied) | 42% (19-68) | n/a | |

Cells are the share of runs, with a Wilson 95% interval. Runs: 60 with, 60 without (20 skills). Runs of the same skill are not independent, so the intervals are narrower than the true uncertainty.

Runs in which the permission mode denied at least one tool call: 0 of 60 with the skills, 0 of 60 without. Denied calls do not count as a script run.

Consistency (pass^3: the chance that all 3 runs of a skill pass): facts 0.95 with the skills, 0.95 without; rubric 1.00 with, 0.85 without.

Tokens and cost, mean per run: output tokens 4,760 with and 5,242 without; input tokens processed (including cached) 105,806 with and 72,908 without; cost 0.246 with and 0.197 without US dollars; total spent on these runs 26.56 (agent runs only, judge calls excluded).

## By skill

| Skill | Facts with | Facts without | Rubric with | Rubric without | Limits with | Limits without | Skill invoked | Script run |
|---|---|---|---|---|---|---|---|---|
| `api-networking` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | n/a |
| `architecture-scaling` | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | n/a |
| `caching-performance` | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 0/3 | 3/3 | n/a |
| `database-selection` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | n/a |
| `deployment-delivery` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | n/a |
| `geospatial-design` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | n/a |
| `identity-security` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | n/a |
| `messaging-streaming` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | n/a |
| `observability` | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `payment-systems` | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 0/3 | 3/3 | n/a |
| `performance-evaluation-methodology` | 3/3 | 3/3 | 3/3 | 1/3 | 0/3 | 0/3 | 3/3 | 0/3 |
| `reliability-resilience` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | n/a |
| `requirements-capacity` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 0/3 |
| `sharding-replication` | 3/3 | 3/3 | 3/3 | 2/3 | 0/3 | 0/3 | 3/3 | n/a |
| `storage-systems` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | n/a |
| `system-design` | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 | n/a |
| `system-design-review` | 2/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | n/a |
| `systems-literature-reading` | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 |
| `systems-research-writing` | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 3/3 | n/a |
| `transactions-consistency` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | n/a |
