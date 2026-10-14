# Trigger results: egyptology-skills

Engine direct. Agent model claude-opus-5-5, judge model claude-sonnet-5-5 (1 vote per verdict), 3 runs per case. Trigger runs stop at the first skill call, so their cost is not tallied.

Each skill has a should-trigger prompt (written without naming the skill) and a near-miss prompt that shares vocabulary but belongs elsewhere; there are also unrelated prompts that should trigger nothing. Every prompt was run several times with the skills installed and the first skill the agent invoked was recorded from its tool calls. A should-trigger run passes when the expected skill was invoked; a near-miss run passes when the named skill was not.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Measure | Value |
|---|---|
| Recall on should-trigger prompts | 100% (86-100) |
| Specificity on near-miss prompts | 100% (86-100) |
| Precision (invoked when it should be) | 100% (86-100) |
| Unrelated prompts that triggered a skill | 0/6 |

Recall 1.00, precision 1.00, specificity 1.00. Wilson 95% intervals; runs of one prompt are not independent.

## By skill

| Skill | Should-trigger runs hit | Near-miss runs that falsely triggered |
|---|---|---|
| `accuracy-review` | 3/3 | 0/3 |
| `edition-conventions` | 3/3 | 0/3 |
| `egyptology-literature` | 3/3 | 0/3 |
| `gardiner-sign-lookup` | 3/3 | 0/3 |
| `hieroglyph-app-builder` | 3/3 | 0/3 |
| `provenance-research-ethics` | 3/3 | 0/3 |
| `text-annotation` | 3/3 | 0/3 |
| `transliteration` | 3/3 | 0/3 |
