# Evaluation files

How this collection is tested is explained once for the whole repository in [TESTING.md](../../TESTING.md). This folder holds the
inputs and the results for `systems-biology-skills`.

| File | What it is |
|---|---|
| `cases.json` | The test cases: one outcome case per skill (its starter prompt, regular expressions for the key facts, a rubric) and trigger prompts (should-trigger, near-miss and unrelated). Edit it when you add a skill |
| `results/outcome.md` | Starter prompts run with and without the skills, three repeats each: facts, rubric, limits stated, tokens and cost |
| `results/trigger.md` | Whether the agent picks the right skill on prompts that do not name it, and leaves it alone on near misses |
| `results/pairwise.md` | A judge model's preference between the with-skill and no-skill answers, in both orders |
| `results/judge-check.md` | How steady the judge is when it grades the same answers twice |
| `results/codex.md` | A smoke test of the same prompts in OpenAI Codex, where it was run |
| `results/*.json` | The same results as data |
| `human/` | The blind sheet for human graders, once generated (`python3 ../tools/run_evals.py sheet .`) |
| `runs/` | Saved runs with the full answers; not committed |

Run the tools from the repository root, for example `python3 tools/run_evals.py plan systems-biology-skills`. Live runs spend API credit.
