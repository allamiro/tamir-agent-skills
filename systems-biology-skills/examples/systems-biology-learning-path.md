# `systems-biology-learning-path`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I want to learn systems biology. I'm a biologist with school-level maths and have 6 weeks, about 8 hours per week. Make me a study plan.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 3,116 | 3,330 |
| Input tokens read across all turns (including cached context) | 30,363 | 145,726 |
| Extra input tokens when the skill is installed | | +115,363 |
| Cost, US dollars at list price | 0.122 | 0.250 |
| Skills invoked in the sample run | none | `systems-biology-learning-path` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 330 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Your 6-week systems biology plan (about 48 hours)

**Who it's for:** a biologist with school-level maths.
**Goal:** understand and work through the core of systems biology.
**Book:** Sauter & Albrecht, *Systems Biology: A Workbook* (2023). It's free and open access at doi:10.11647/OBP.0291. The plan follows its four parts and covers only the topics it marks as **priority 1**. That's what fits in 48 hours. The priority 2 topics can come later.

## Two rules that matter more than the timetable
1. **Spend about 70% of your time solving problems and about 30% reading.** For a biologist, maths takes few facts but a lot of practice. Expect the first two weeks to feel slow. That's normal, and progress often comes suddenly once you've practised enough.
2. **Try every problem before you look at the solution**, ideally leaving a day in between. Reading solutions first makes the material feel familiar without making you able to do it.

**Weekly rhythm:** 4 sessions of 2 hours each. Session 1 is mostly concepts and worked examples. Sessions 2–4 are problems. In the last 20 minutes of each week, write down your mistakes in a log (what went wrong and why) and redo one of them the following week.

## Day 0 diagnostic (15 min, no looking things up)
1. Multiply the rows (1, 2) and (3, 4) as a matrix by the column (1, 1).
2. Solve x + y = 3, x − y = 1.
3. Solve x² − 3x + 2 = 0.
4. Differentiate e^(−2t).
5. Enzyme rate: v = Vmax·S/(Km + S). What is v when S = Km?
6. Write how the amount of A changes over time for A → B with rate constant k.

Tell me your answers and I'll adjust the plan. If you get questions 3–4 wrong, spend extra time in weeks 2 and 4. If you get 5–6 right, week 6 will go faster.

## The plan

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# 6-Week Systems Biology Study Plan
*About 48 hours total, for a biologist with school-level maths*

## The approach
Systems biology mostly asks one question: **how do interactions between molecules produce behaviour over time?** You need a small amount of maths for that: rates of change, simple differential equations and graphs. You don't need advanced calculus. The plan teaches the maths only when a topic needs it, and has you simulate every concept so you can see what it does.

## Core resources (all free or cheap)
| Resource | Use |
|---|---|
| **Uri Alon, *An Introduction to Systems Biology*** (2nd ed.) | Main textbook. It's written for biologists. |
| **Uri Alon's YouTube lecture series** ("Systems Biology" course) | Watch alongside the book |
| **Brian Ingalls, *Mathematical Modeling in Systems Biology*** (free PDF on the author's site) | Gentler maths and worked examples |
| **Khan Academy**: derivatives intro, exponential growth/decay | To fill maths gaps |
| **COPASI** (free desktop app, no coding) | Building and simulating models |
| *Optional:* **Tellurium** (Python) | If you want to learn some coding |

## Weekly rhythm (8 h)
- **3 h**: reading and lectures
- **3 h**: hands-on modelling in COPASI
- **1 h**: maths practice
- **1 h**: review. Write a one-page summary and answer that week's check questions without notes.

---

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
