# Live runs

Measured on 2026-10-14 with 2.1.296 (Claude Code), model claude-opus-5-5. Each row is one starter prompt run once in a clean project with the skills installed (`python3 scripts/live_check.py --run`). Grading is by regular expression on the final answer, not a judgement of quality. This is one run per prompt on one day: it shows what happened, not what always happens.

- The expected skill was invoked in **5 of 5** runs; some skill was invoked in 5.
- The answer matched every expected fact in **5 of 5** runs.
- Total cost 0.76 US dollars.

| Skill | Expected skill invoked | Skills invoked | Script run | Facts matched | Cost (USD) | Seconds |
|---|---|---|---|---|---|---|
| `gardiner-sign-lookup` | yes | gardiner-sign-lookup | `signs.py` | 4 of 4 | 0.12 | 11 |
| `transliteration` | yes | transliteration | none | 3 of 3 | 0.12 | 19 |
| `text-annotation` | yes | text-annotation | none | 3 of 3 | 0.12 | 23 |
| `hieroglyph-app-builder` | yes | hieroglyph-app-builder | none | 3 of 3 | 0.20 | 52 |
| `accuracy-review` | yes | accuracy-review | `signs.py` | 3 of 3 | 0.20 | 53 |

## What the facts were

| Skill | A correct answer matches all of |
|---|---|
| `gardiner-sign-lookup` | `13153`; `Bird`; `uniliteral`; `\bm\b` |
| `transliteration` | `sꜣ\|zꜣ\|\bsA\b\|\bs3\b`; `determinative`; `A1` |
| `text-annotation` | `VERIFY`; `grade`; `review` |
| `hieroglyph-app-builder` | `Gardiner`; `fallback\|missing\|box\|code`; `licen` |
| `accuracy-review` | `memory`; `critical\|major\|severity`; `not checked\|could not\|did not check` |
