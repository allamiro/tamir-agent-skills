# Live runs, no skills installed (baseline)

Measured on 2026-10-14 with 2.1.296 (Claude Code), model claude-opus-5-5. Each row is one starter prompt run once in a clean project with NO skills installed, for comparison with live-results.md (`python3 scripts/live_check.py --run --baseline`). Grading is by regular expression on the final answer, not a judgement of quality. This is one run per prompt on one day: it shows what happened, not what always happens.

- The expected skill was invoked in **0 of 5** runs; some skill was invoked in 0.
- The answer matched every expected fact in **4 of 5** runs.
- Total cost 0.54 US dollars.

| Skill | Expected skill invoked | Skills invoked | Script run | Facts matched | Cost (USD) | Seconds |
|---|---|---|---|---|---|---|
| `gardiner-sign-lookup` | no | none | none | 4 of 4 | 0.10 | 16 |
| `transliteration` | no | none | none | 3 of 3 | 0.07 | 14 |
| `text-annotation` | no | none | none | 3 of 3 | 0.06 | 11 |
| `hieroglyph-app-builder` | no | none | none | 3 of 3 | 0.20 | 68 |
| `accuracy-review` | no | none | none | 2 of 3 | 0.10 | 35 |

## What the facts were

| Skill | A correct answer matches all of |
|---|---|
| `gardiner-sign-lookup` | `13153`; `Bird`; `uniliteral`; `\bm\b` |
| `transliteration` | `sꜣ\|zꜣ\|\bsA\b\|\bs3\b`; `determinative`; `A1` |
| `text-annotation` | `VERIFY`; `grade`; `review` |
| `hieroglyph-app-builder` | `Gardiner`; `fallback\|missing\|box\|code`; `licen` |
| `accuracy-review` | `memory`; `critical\|major\|severity`; `not checked\|could not\|did not check` |
