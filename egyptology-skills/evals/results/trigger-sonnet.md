# Trigger results: egyptology-skills

Engine direct. Agent model claude-sonnet-5-5, judge model claude-sonnet-5-5 (3 votes per verdict), 2 runs per case. Trigger runs stop at the first skill call, so their cost is not tallied.

Each skill has a should-trigger prompt (written without naming the skill) and a near-miss prompt that shares vocabulary but belongs elsewhere; there are also unrelated prompts that should trigger nothing. Every prompt was run several times with the skills installed and the first skill the agent invoked was recorded from its tool calls. A should-trigger run passes when the expected skill was invoked; a near-miss run passes when the named skill was not.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Measure | Value |
|---|---|
| Recall on should-trigger prompts | 88% (64-97) |
| Specificity on near-miss prompts | 100% (81-100) |
| Precision (invoked when it should be) | 100% (78-100) |
| Unrelated prompts that triggered a skill | 0/4 |

Recall 0.88, precision 1.00, specificity 1.00. Wilson 95% intervals; runs of one prompt are not independent.

## By skill

| Skill | Should-trigger runs hit | Near-miss runs that falsely triggered |
|---|---|---|
| `accuracy-review` | 2/2 | 0/2 |
| `edition-conventions` | 2/2 | 0/2 |
| `egyptology-literature` | 2/2 | 0/2 |
| `gardiner-sign-lookup` | 0/2 | 0/2 |
| `hieroglyph-app-builder` | 2/2 | 0/2 |
| `provenance-research-ethics` | 2/2 | 0/2 |
| `text-annotation` | 2/2 | 0/2 |
| `transliteration` | 2/2 | 0/2 |
