# Outcome results: egyptology-skills

Engine direct. Agent model claude-opus-5-5, judge model claude-sonnet-5-5 (3 votes per verdict), 3 runs per case. Cost of this run, agent and judge at list price: 10.65 US dollars.

Each skill's starter prompt was run 3 times with the skills installed and 3 times with none, each in a fresh Claude Code project. Three kinds of check are reported separately: **facts** (regular expressions for the key facts in the answer), **rubric** (a model judges the answer against the prompt's own "a good answer" description) and **limits stated** (a model checks that the answer marks specific items as unverified or assumed and says what it did check). The judge is a model, not a person.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Check | With the skills | No skills | Difference (95% interval) |
|---|---|---|---|
| Every expected fact present | 100% (86-100) | 96% (80-99) | +4 points (-10 to +20) |
| Rubric passed | 100% (86-100) | 33% (18-53) | +67 points (+42 to +82) |
| States its limits | 96% (80-99) | 62% (43-79) | +33 points (+10 to +53) |
| **Only prompts that do not presuppose the skill (6 skills)** | | | |
| Every expected fact present | 100% (82-100) | 100% (82-100) | +0 points (-18 to +18) |
| Rubric passed | 100% (82-100) | 39% (20-61) | +61 points (+33 to +80) |
| States its limits | 94% (74-99) | 50% (29-71) | +44 points (+15 to +66) |
| Expected skill invoked | 100% (86-100) | n/a | |
| Its script run (skills that ship one, and not denied) | 100% (76-100) | n/a | |

Some starter prompts ask for the skill's own table, checker or template (`gardiner-sign-lookup`, `provenance-research-ethics`). A run without the skill cannot supply those, so the difference on those prompts overstates what the skill adds; the second block leaves them out.

Cells are the share of runs, with a Wilson 95% interval. Runs: 24 with, 24 without (8 skills). Runs of the same skill are not independent, so the intervals are narrower than the true uncertainty.

Runs in which the permission mode denied at least one tool call: 0 of 24 with the skills, 0 of 24 without. Denied calls do not count as a script run.

Consistency (pass^3: the chance that all 3 runs of a skill pass): facts 1.00 with the skills, 0.88 without; rubric 1.00 with, 0.12 without.

Tokens and cost, mean per run: output tokens 2,820 with and 2,461 without; input tokens processed (including cached) 152,795 with and 68,533 without; cost 0.196 with and 0.122 without US dollars; total spent on these runs 7.62 (agent runs only, judge calls excluded).

## By skill

| Skill | Facts with | Facts without | Rubric with | Rubric without | Limits with | Limits without | Skill invoked | Script run |
|---|---|---|---|---|---|---|---|---|
| `accuracy-review` | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | n/a |
| `edition-conventions` | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 0/3 | 3/3 | 3/3 |
| `egyptology-literature` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `gardiner-sign-lookup` | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `hieroglyph-app-builder` | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | n/a |
| `provenance-research-ethics` | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `text-annotation` | 3/3 | 3/3 | 3/3 | 0/3 | 2/3 | 0/3 | 3/3 | n/a |
| `transliteration` | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 0/3 | 3/3 | n/a |
