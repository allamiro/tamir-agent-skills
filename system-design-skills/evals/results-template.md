# Evaluation results

Fill one block per run. Do not record a result as PASS unless the run was actually executed
and graded against `scenarios.md`.

| Date | Agent / model | Library installed? | Scenario | Skills activated | Grade (pass/partial/fail) | Failures observed | Notes |
|---|---|---|---|---|---|---|---|
| | | yes / no (baseline) | A | | | | |
| | | | B | | | | |
| | | | C | | | | |
| | | | D | | | | |
| | | | E | | | | |
| | | | N1-N8 | | | | |

## Automated checks (re-run on every change)

| Check | Command | Last result |
|---|---|---|
| Structure and links | `python3 scripts/validate_library.py` | |
| Routing smoke test | `python3 scripts/check_routing.py` | |
| Spec validator | `skills-ref validate skills/<name>` for each skill | |
