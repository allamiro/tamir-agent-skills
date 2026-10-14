# How these skills are tested

A skill is good if three things are true: the agent **picks it up** when it should and leaves it alone when it
should not, the **answer is better** than the agent gives without it, and the skill's **own content is correct**.
Each is measured differently, and no single number covers all three. This page lists every measure used here, what
each one can and cannot tell you, what it costs, and the command that runs it. The numbers from the latest runs are
at the end, and each collection keeps its own copy of them under `evals/results/`.

## The measures

| # | Measure | Question it answers | How | Cannot tell you | Cost |
|---|---|---|---|---|---|
| 1 | Static validation | Is the skill well formed? | Agent Skills spec, strict YAML, size, links, navigation, bundle limits (`validate_*.py`, `skills-ref`, `claude plugin validate`) | Whether the skill is any use | Free |
| 2 | Script self-tests, independent cross-checks, mutation tests | Are the bundled calculations right? | Hand-computed values in each script, comparison with NumPy, SciPy and statsmodels on thousands of random inputs, and deliberately broken copies of the code that the tests must catch | That the advice around a calculation is right | Free |
| 3 | Answer-key checks | Does the prose in a prompt's "a good answer" line agree with what the script computes? | `check_answers.py` runs the script and checks that the prompt quotes the same number | Whether an agent's answer is right | Free |
| 4 | Routing smoke test | Do the descriptions contain the words people type? | BM25 word match of each starter prompt against all descriptions (`check_routing.py`) | How an agent actually chooses a skill | Free |
| 5 | **Trigger test** | Does the agent invoke the skill on an implicit request, and leave it alone on a near miss? | Per skill, a should-trigger prompt written without naming the skill and a near-miss that shares its vocabulary but belongs elsewhere, plus unrelated prompts; 3 runs each; recall, precision and specificity with Wilson intervals | Whether the answer is any good | Cents per run |
| 6 | **Outcome test** | Does the skill change the answer? | Each skill's starter prompt, 3 runs with the skills installed and 3 with none; three checks per run (below); differences with Newcombe intervals; pass^k for consistency | Whether the model judge is right; whether a person would prefer the answer | Dimes per run |
| 7 | Model-judged pairwise comparison | Which answer would a specialist rather get? | A judge model compares the with-skill and no-skill answers in both orders, so position bias shows | Human preference; same-family bias | Cents per pair |
| 8 | Judge self-agreement | Is the judge steady? | Re-grade a sample of saved answers and compare | Whether the judge is accurate | Cents |
| 9 | **Human grading** | Is the answer better, to a person who knows the field? | Blind sheet, A/B shuffled with a seed, key kept apart; win rate with an exact sign test, correctness scores, Cohen's kappa between graders | Nothing; this is the reference the others are checked against | People's time |
| 10 | Cross-vendor smoke test | Are the skills found and used in OpenAI Codex? | Same prompts with `codex exec`; a skill counts as used when its `SKILL.md` is read | Answer quality (regular expressions only) | Tokens |

Measures 1 to 4 and 9's kit are free and run in the repository. Measures 5 to 8 and 10 call a model and spend credit.

## The three checks on each outcome run

| Check | How it is graded | What it catches |
|---|---|---|
| Facts | Regular expressions for the key facts, written from the prompt's "a good answer" line | Wrong or missing numbers and terms |
| Rubric | A judge model reads the answer against the "a good answer" description and votes PASS or FAIL | Right words in the wrong substance |
| States its limits | A judge model checks that the answer names something it did not verify or assumed | Smooth, confident answers with no stated doubt, which the skills are built to prevent |

The first is mechanical. The second and third are a model's judgement and are reported as such. The judge is told to
be strict and not to follow instructions inside the answer. It is not a person, and the human kit exists to check it.

## What the numbers do and do not mean

- **One model, one day.** Every live result is for the model and Claude Code version named in its file. A different model
  will give different trigger rates and answers.
- **Runs of one prompt are not independent**, so the intervals are narrower than the true uncertainty. They are a lower
  bound on how unsure the figures are.
- **Some starter prompts presuppose the skill.** A prompt that asks for "the status your table gives" cannot be answered
  without the table, so the with-versus-without difference on those prompts overstates what the skill adds. Outcome
  results show the difference for the other prompts separately.
- **The prompts were written with the skills.** A prompt written for a skill is a favourable test of it. The trigger prompts
  are written not to name the skill, and near misses test the other direction, but none of this replaces prompts from
  people who have never seen the skill.
- **Facts saturate.** A strong model often gets the key facts right without help, so a facts check can sit near 100 percent
  in both arms. The rubric and limits checks are where a difference, if there is one, can show.
- **More tokens are not a defect.** A skill adds its description to every session and its instructions when it is used.
  Whether the extra tokens buy a better answer is what the outcome test is for.
- **A model judge is not a person.** Models agree with human preferences often but not always, and a judge from the same
  family as the answers may favour them. Treat the judged checks as screening and the human kit as the test.

## Run it

Everything below runs from the repository root. `COLLECTION` is `system-design-skills`, `egyptology-skills` or
`bioinformatics-skills`.

```bash
python3 tools/check_repo.py                          # every free check in the repository
python3 tools/run_evals.py selftest                  # the evaluation tool's own unit tests
python3 tools/run_evals.py plan COLLECTION           # what a live run would do, with a rough cost

python3 tools/run_evals.py run COLLECTION --kind trigger   # measure 5
python3 tools/run_evals.py run COLLECTION --kind outcome --judge-model claude-sonnet-5-5   # measure 6
python3 tools/run_evals.py pairwise COLLECTION       # measure 7
python3 tools/run_evals.py judge-check COLLECTION    # measure 8
python3 tools/run_evals.py sheet COLLECTION          # measure 9: writes COLLECTION/evals/human/
python3 tools/run_evals.py score COLLECTION --ratings ratings-ann.csv ratings-ben.csv
python3 tools/run_evals.py codex COLLECTION          # measure 10
python3 tools/run_evals.py samples COLLECTION         # sample outputs and token counts for the README
```

Add `--max-cost-usd N` to cap a run, `--only SKILL ...` to test a few skills, and `--runs N` to change the repeats.
Saved runs, with the full answers, are written to `COLLECTION/evals/runs/` (not committed). The summaries are written to
`COLLECTION/evals/results/` (committed). Cases live in `COLLECTION/evals/cases.json`; add a skill's cases there.

### Human grading, step by step

1. Run `sheet`. Give each grader `evals/human/sheet.md` and `ratings-template.csv`, and not `key.json`.
2. Each grader fills in their own copy of the CSV without trying to guess which answer used a skill.
3. Run `score` with every returned file. It reports, per grader, how often the with-skill answer was preferred (ties set
   aside), an exact sign test, the difference in correctness scores, and Cohen's kappa between graders.
4. Compare the model judge's verdicts with the graders'. If they disagree, believe the graders.

For a specialist field (Egyptology, bioinformatics) the graders should be specialists. A systems engineer cannot judge a
translation, and an Egyptologist cannot judge a failover plan.

## The official tool, and why the outcome runs do not use it

Claude Code has its own evaluation command, `claude plugin eval` (Claude Code 2.1.269 or later; the documentation was read on
2026-10-14). It runs each case three times with the plugin and three times without, grades with regular expressions,
tool-use checks and a model judge, and reports the difference. It is the right tool for many plugins, and `run_evals.py run
--engine native` drives it.

It was not used for the outcome runs because of one thing found in a probe: it runs cases from the plugin folder, which lies
outside the run's workspace, and the agent's own `Read`, `Grep` and `cd ... && python3 scripts/x.py` calls on the skill's
files were denied. A skill that ships a script or a reference file could not use them, which would count against the skills for
a reason that has nothing to do with their quality. The direct engine copies the skills into the project's `.claude/skills`,
where Claude Code reads them as it does for a user. The grading ideas (separate checks per run, a model judge, a no-skill arm,
repeats) follow the official tool and the evaluation guides from agentskills.io and OpenAI, listed below.

## Sources

Read on 2026-10-14 unless noted.

- Agent Skills, "Evaluating skill output quality" and "Optimizing skill descriptions" (agentskills.io): with-skill and without-skill runs,
  assertions, graded evidence, benchmark statistics; about 20 trigger queries with near-miss negatives, 3 runs each, a 0.5 trigger-rate
  threshold, a train and validation split
- OpenAI, "Testing Agent Skills Systematically with Evals" (developers.openai.com/blog/eval-skills, January 2026): outcome, process, style and
  efficiency checks; deterministic checks on the event stream; rubric grading with a schema; prompt sets with explicit, implicit,
  contextual and negative prompts
- Claude Code documentation, "Test plugins with evals": `claude plugin eval`, grader types, the no-plugin baseline, three runs by default
- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (NeurIPS 2023): position bias, verbosity bias and self-preference in model
  judges; the reported agreement with human preferences above 80 percent is for the judge and tasks in that study
- The tau-bench paper (arXiv 2406.12045): pass^k, the chance that all k runs succeed, as a consistency measure
- Wilson (1927) and Newcombe (1998) intervals, Cohen's kappa and the exact sign test: standard statistics, implemented in
  `tools/skilleval/stats.py` and checked against statsmodels, scikit-learn and SciPy

## What the latest runs show

In plain terms, on 2026-10-14, one model (Claude Opus 5.5) in Claude Code 2.1.296:

- **The skills are never picked up by mistake.** Across every near-miss and unrelated prompt there was not one false trigger.
  Precision and specificity are 100 percent in all three collections.
- **Whether a skill is picked up depends on how much the model needs it.** Recall on implicit requests was 100 percent for
  Egyptology, 80 percent for Bioinformatics and 62 percent for System Design. Every miss was the model answering directly; none was
  a wrong skill. The misses cluster on self-contained calculations (translation, alignment, protein mass) and on general
  engineering questions the model already handles.
- **Whether a skill changes the answer depends on the field.** In Egyptology, where the work rests on conventions and sources a model
  may not have to hand, the rubric pass rate rose from 33 to 100 percent. In Bioinformatics it rose from 86 to 97 percent. In System
  Design it was 93 to 100 percent and the interval includes no difference. For general engineering prompts a strong model
  already passes the facts and rubric checks, so the skills' measurable effect there is smaller than the noise.
- **Stating limits is where System Design moves.** The share of answers that mark specific items as unverified or assumed rose
  from 32 to 52 percent with the skills. Bioinformatics showed no difference on this check (22 to 28 percent).
- **A model judge prefers the skill's answer in most decisive pairs** (14 of 18, 4 of 6 and 15 of 18), but it is a model's opinion
  from the same family, on one answer pair per skill. It is not evidence that people would agree.
- **The skills cost tokens.** A run with the skills read between 44 and 123 percent more input tokens, wrote between 9 percent
  fewer and 18 percent more output tokens, and cost between 24 and 64 percent more per answer (the loaded skill text, the
  reference files it reads, script output and extra turns).
- **Not established:** that people prefer these answers (no one has graded them), that a model judge agrees with people, or that the
  results hold for other models. The judge agrees with itself only moderately on some checks (Cohen's kappa 0.48 for the Egyptology
  rubric and 0.49 for the System Design limits check; where nearly every verdict is PASS, kappa is not informative).

## Corrections made after seeing results

These changes were made after looking at runs, so they could in principle favour the skills. Each is listed so a reader can judge.

1. **Harness.** The first Egyptology outcome run (about 8 US dollars, discarded) ran in a permission mode that denied compound shell commands
   and file writes, so some skills could not use their scripts. The runner now accepts edits in the throwaway project and allows read-only
   commands, counts any denied call, and counts a script run only if it was not denied. All outcome runs reported here used the corrected
   runner, and no run in the final results had a denied call.
2. **The "states its limits" check was tightened** from "names one thing it did not verify" (100 percent in both arms) to "marks specific items
   as unverified and says what it did check".
3. **Three rubrics for System Design** (`systems-literature-reading`, `performance-evaluation-methodology`, `systems-research-writing`) were rewritten
   because their "a good answer" line covers all of a skill's prompts while the test uses only the first; no answer could pass. The saved answers
   were graded again with the new rubric; the agent was not re-run.
4. **One Egyptology rubric** (`edition-conventions`) was reworded twice: all six answers, with and without the skill, flagged `{nb}` inside a
   restored stretch as editorially doubtful, a fair point that my line had called "fine". The line now asks for the crossing brackets and a draft key.
5. **One Bioinformatics prompt** (`research-proposal-planning`) asked whether a plan fits "with a buffer" without saying how large. Every answer, with or
   without the skill, took the spare weeks as the buffer. The prompt now says 30 percent and that case was re-run (6 runs).
6. **A regular expression** for `edition-conventions` was widened from "cross" to "cross, overlap and similar words".
7. **Three judge votes** were added to every saved answer after the single-vote judge showed only moderate self-agreement. The tables use the majority of three.
8. **Prompts that presuppose the skill** (a prompt that asks for the skill's own table or checker) were flagged by a pattern and reported separately.

Spend: roughly 100 US dollars at list price in all, including about 12 on runs discarded after the harness fixes. Trigger runs stop at the first skill
call and report no cost, so they are counted at 5 cents each; Codex runs are counted in tokens only.

## Latest results

<!-- results:start -->

### Outcome runs: starter prompts with and without the skills

Share of runs passing each check, with Wilson 95% intervals; the last column is the difference in percentage points with a Newcombe interval. Rubric and limits are judged by a model.

| Collection | Skills | Runs per arm | Facts: skills / none | Rubric: skills / none | Rubric difference | Limits: skills / none | Expected skill invoked |
|---|---|---|---|---|---|---|---|
| system-design-skills | 20 | 60 / 60 | 98% (91-100) / 95% (86-98) | 100% (94-100) / 93% (84-97) | +7 (-1 to +16) | 52% (39-64) / 32% (21-44) | 97% (89-99) |
| egyptology-skills | 8 | 24 / 24 | 100% (86-100) / 96% (80-99) | 100% (86-100) / 33% (18-53) | +67 (+42 to +82) | 96% (80-99) / 62% (43-79) | 100% (86-100) |
| bioinformatics-skills | 23 | 69 / 69 | 97% (90-99) / 90% (81-95) | 97% (90-99) / 86% (75-92) | +12 (+2 to +22) | 28% (18-39) / 22% (14-33) | 57% (45-68) |

Leaving out the starter prompts that ask for the skill's own table, checker or template:

| Collection | Skills kept | Facts: skills / none | Rubric: skills / none | Rubric difference |
|---|---|---|---|---|
| egyptology-skills | 6 | 100% (82-100) / 100% (82-100) | 100% (82-100) / 39% (20-61) | +61 (+33 to +80) |
| bioinformatics-skills | 22 | 97% (90-99) / 92% (83-97) | 97% (90-99) / 89% (80-95) | +8 (-2 to +18) |

### Tokens and cost per run (means)

| Collection | Output tokens: skills / none | Input tokens read: skills / none | Cost, US dollars: skills / none | Runs with a denied tool call: skills / none |
|---|---|---|---|---|
| system-design-skills | 4,760 / 5,255 | 105,133 / 72,908 | 0.245 / 0.197 | 0 / 0 |
| egyptology-skills | 2,820 / 2,461 | 152,795 / 68,533 | 0.196 / 0.122 | 0 / 0 |
| bioinformatics-skills | 2,458 / 2,086 | 101,518 / 54,658 | 0.185 / 0.113 | 0 / 0 |

### Trigger runs: does the agent pick the right skill

| Collection | Should-trigger runs hit (recall) | Near-miss runs correctly left alone (specificity) | Precision | Unrelated prompts that triggered a skill |
|---|---|---|---|---|
| system-design-skills | 62% (49-73) | 100% (94-100) | 100% (91-100) | 0 of 6 |
| egyptology-skills | 100% (86-100) | 100% (86-100) | 100% (86-100) | 0 of 6 |
| bioinformatics-skills | 80% (69-88) | 100% (95-100) | 100% (93-100) | 0 of 6 |

### Model-judged pairwise comparison (both orders)

| Collection | Skill preferred | Baseline preferred | Tie | Inconsistent across orders | Share preferring the skill, decisive pairs only |
|---|---|---|---|---|---|
| system-design-skills | 14 | 4 | 0 | 2 | 78% (55-91) |
| egyptology-skills | 4 | 2 | 0 | 2 | 67% (30-90) |
| bioinformatics-skills | 15 | 3 | 3 | 2 | 83% (61-94) |

### Codex smoke test (one run per prompt and arm, facts only)

| Collection | Every expected fact: skills / none | Expected skill used | Any skill used |
|---|---|---|---|
| system-design-skills | 18 of 20 / 19 of 20 | 20 of 20 | 20 of 20 |
| egyptology-skills | 7 of 8 / 5 of 8 | 8 of 8 | 8 of 8 |
| bioinformatics-skills | 21 of 23 / 21 of 23 | 23 of 23 | 23 of 23 |

Judge self-agreement with a single vote, system-design-skills: Rubric, 24 of 24, 1.00; States its limits, 18 of 24, 0.49. Verdicts in the tables are the majority of 3 judge votes; the second and third votes changed 19 of 240 verdicts.

Judge self-agreement with a single vote, egyptology-skills: Rubric, 18 of 24, 0.48; States its limits, 21 of 24, 0.65. Verdicts in the tables are the majority of 3 judge votes; the second and third votes changed 2 of 96 verdicts.

Judge self-agreement with a single vote, bioinformatics-skills: Rubric, 23 of 24, 0.00; States its limits, 23 of 24, 0.90. Verdicts in the tables are the majority of 3 judge votes; the second and third votes changed 5 of 276 verdicts.

Human grading: the blind kit is built (`run_evals.py sheet`) but no person has graded any answers yet, so none of the judged results above has been checked against human preference.

<!-- results:end -->
