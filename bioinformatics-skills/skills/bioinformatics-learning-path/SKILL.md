---
name: bioinformatics-learning-path
description: Builds a learning plan for bioinformatics from the learner's background, with a route through information, biology and applications, exercises with checkable answers, projects, and habits for reading papers and tools critically. Use for "how do I learn bioinformatics", "I am a biologist, what programming do I need", "I am a programmer, what biology do I need", "give me exercises", "plan a six-month study", "what projects should I build", "what should I learn first". Use bioinformatics-workflow once there is a real analysis to plan, and the specialist skills for the topic of each exercise.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Bioinformatics learning path

## Purpose and activation

Give a newcomer a route that fits where they start, with work they can check for themselves. The
field draws people from biology, from computing, from mathematics and statistics, and each is missing
a different third of it. Activate when someone asks how to start, what to learn next, what to
practise on, or how to judge their own progress.

## Required inputs

The learner's background in biology, programming, mathematics and statistics, with honest levels;
the goal (a research project, a job, reading the literature, running a core facility); the time per
week and the time frame; the data or organism of interest; and what they have already tried.

## Workflow

1. **Place the learner** on each of the four strands: biology, programming, mathematics and
   statistics, and bioinformatics itself. Do not assume the strong strand is complete.
2. **Choose the route** in `references/curriculum.md`. The source book is organised in three parts:
   information (chapters 2 to 8), biology (chapters 9 to 11) and applications (chapters 12 to 18).
   Someone from biology starts with the information part and programming; someone from computing
   starts with the biology part.
3. **Set stage goals** that can be checked, such as "compute the entropy of a sequence and explain the
   number" or "translate and find the open reading frames in a bacterial contig and say how many are
   expected by chance".
4. **Give exercises with answers the learner can verify.** `references/exercises.md` lists exercises
   with the command that produces the answer and the expected output.
5. **Add a project per stage,** small and real: a dataset, a question, a plan from `bioinformatics-workflow`,
   and a review with `bioinformatics-review`.
6. **Teach reading critically:** for every paper or tool, write the claim, the null model, the data
   and the limits.
7. **Build habits early:** write down versions, test on tiny known cases, and keep a log of mistakes
   (`reproducible-research-code`).
8. **Check progress** against the stage goals, and adjust the route.

## Decision framework

| Learner | Start with |
|---|---|
| Biologist, little programming | A scripting language and the file formats, then information and statistics |
| Programmer, little biology | The molecular biology and genome basics, then the data types |
| Statistician or mathematician | Biology basics and the data types, then the pipelines |
| Wants to read papers | Statistics and the review checklist before tools |
| Wants to analyse their own data | Experimental design and the analysis plan first, then the specialist skill for the data type |
| Short on time | One data type, one project, depth before breadth |

## Implementation guidance

- Keep the stages short and the projects real. A learner finishes what they care about.
- An exercise is worth more when the answer can be checked by running something. The exercises here
  use the scripts of this collection, so a learner can compare their own working with the output.
- Pair each new tool with a failure: what goes wrong, and how a known-answer test would show it.
- Recommend primary documentation over memory for anything version-dependent.
- The time estimates in `assets/templates/study-plan.md` are suggestions to adapt, not measured.

## Failure and edge cases

- **Tool-first learning:** running pipelines without understanding the data or the null model.
- **Skipping statistics,** then over-reading results.
- **Skipping the biology,** then analysing the wrong thing.
- **Tutorial loops:** following guides without a question of one's own.
- **Too broad:** touching every data type and mastering none.
- **No checks:** nothing in the plan lets the learner know they are wrong.
- **Outdated advice:** tools and versions change faster than a plan.
- **Assuming one background fits all** the strands.

## Validation

- The collection's answer check (check_answers.py, in the collection's own scripts folder, outside
  this skill) must pass: every exercise's command still produces the expected output.
- Each stage has a goal the learner can test and a project with a deliverable.
- Falsifier: a learner cannot explain, in their own words, what a result from the stage means and
  what would make it wrong.

## Expected output

The learner profile, the chosen route with stages, goals and exercises per stage, projects with
deliverables, reading habits, a progress check for each stage, and the first week's tasks.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: the table of contents (three parts and 18
  chapters) and the prefaces (supplied text): the book is meant as a self-contained guide for newcomers
  from either biology or informatics, with chapters grouped as fundamentals of information science,
  an overview of biology, and applications; its problems are open-ended. The chapter text beyond
  chapter 2 was not supplied
- Routes, stage goals, time suggestions and projects: own design from general teaching practice
- Exercises: answers computed by the scripts in this collection and checked in `check_answers.py`
- Not covered: wet-lab training, degree programme advice, specific courses or books beyond the source
