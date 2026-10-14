# Outcome results: egyptology-skills

Engine direct. Agent model claude-opus-5-5, judge model claude-sonnet-5-5 (1 vote per verdict), 3 runs per case. Cost of this run, agent and judge at list price: 11.98 US dollars.

Each skill's starter prompt was run 3 times with the skills installed and 3 times with none, each in a fresh Claude Code project. Three kinds of check are reported separately: **facts** (regular expressions for the key facts in the answer), **rubric** (a model judges the answer against the prompt's own "a good answer" description) and **limits stated** (a model checks that the answer marks specific items as unverified or assumed and says what it did check). The judge is a model, not a person.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Check | With the skills | No skills | Difference (95% interval) |
|---|---|---|---|
| Every expected fact present | 100% (88-100) | 89% (72-96) | +11 points (-3 to +28) |
| Rubric passed | 96% (82-99) | 30% (16-48) | +67 points (+43 to +81) |
| States its limits | 93% (77-98) | 59% (41-75) | +33 points (+11 to +53) |
| **Only prompts that do not presuppose the skill (7 skills)** | | | |
| Every expected fact present | 100% (85-100) | 90% (71-97) | +10 points (-7 to +29) |
| Rubric passed | 95% (77-99) | 33% (17-55) | +62 points (+34 to +79) |
| States its limits | 90% (71-97) | 48% (28-68) | +43 points (+15 to +63) |
| Expected skill invoked | 100% (88-100) | n/a | |
| Its script run (skills that ship one, and not denied) | 100% (76-100) | n/a | |

Some starter prompts ask for the skill's own table, checker or template (`gardiner-sign-lookup`, `provenance-research-ethics`). A run without the skill cannot supply those, so the difference on those prompts overstates what the skill adds; the second block leaves them out.

Cells are the share of runs, with a Wilson 95% interval. Runs: 27 with, 27 without (9 skills). Runs of the same skill are not independent, so the intervals are narrower than the true uncertainty.

Runs in which the permission mode denied at least one tool call: 0 of 27 with the skills, 0 of 27 without. Denied calls do not count as a script run.

Consistency (pass^3: the chance that all 3 runs of a skill pass): facts 1.00 with the skills, 0.78 without; rubric 0.89 with, 0.11 without.

Tokens and cost, mean per run: output tokens 2,840 with and 2,568 without; input tokens processed (including cached) 147,249 with and 64,294 without; cost 0.193 with and 0.123 without US dollars; total spent on these runs 8.54 (agent runs only, judge calls excluded).

## By skill

| Skill | Facts with | Facts without | Rubric with | Rubric without | Limits with | Limits without | Skill invoked | Script run |
|---|---|---|---|---|---|---|---|---|
| `accuracy-review` | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | n/a |
| `edition-conventions` | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 0/3 | 3/3 | 3/3 |
| `egyptology-literature` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `egyptology-research-writing` | 3/3 | 1/3 | 2/3 | 0/3 | 2/3 | 1/3 | 3/3 | n/a |
| `gardiner-sign-lookup` | 3/3 | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `hieroglyph-app-builder` | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | n/a |
| `provenance-research-ethics` | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `text-annotation` | 3/3 | 3/3 | 3/3 | 0/3 | 2/3 | 0/3 | 3/3 | n/a |
| `transliteration` | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 0/3 | 3/3 | n/a |
