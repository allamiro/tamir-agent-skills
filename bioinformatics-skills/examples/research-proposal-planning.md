# `research-proposal-planning`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Here is my plan: data access 6 weeks, quality control 2, alignment 3, statistics 4, then writing 5 weeks and figures 2 weeks in parallel with writing. I have 24 weeks. Does it fit if I add a 30 percent buffer?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 708 | 921 |
| Input tokens read across all turns (including cached context) | 30,400 | 35,688 |
| Extra input tokens when the skill is installed | | +5,288 |
| Cost, US dollars at list price | 0.074 | 0.121 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 2,300 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**No. With a 30% buffer it comes to about 26 weeks, which is 2 weeks over your 24.**

**Critical path:**

| Phase | Weeks | Cumulative |
|---|---|---|
| Data access | 6 | 6 |
| Quality control | 2 | 8 |
| Alignment | 3 | 11 |
| Statistics | 4 | 15 |
| Writing (figures done alongside) | 5 | 20 |

- Planned work: **20 weeks**. Figures take no extra time because they fit inside the 5 weeks of writing.
- With the 30% buffer: 20 × 1.3 = **26 weeks**.
- Over by **2 weeks**.

Another way to see it: with 24 weeks and a 30% buffer, the planned work can be at most 24 / 1.3 ≈ **18.5 weeks**. You need to cut about 1.5 weeks.

**Ways to make it fit:**

1. **Overlap phases on the critical path.** This is the most useful change. Write and test the QC and alignment pipeline on public or pilot data while you wait for data access. If that cuts 2–3 weeks from QC and alignment, you fit with the full buffer.
2. **Start writing early.** Draft the introduction and methods during alignment and statistics. This can take 1–2 weeks off the final writing phase.
3. **Accept a smaller buffer.** 20 weeks of work in 24 weeks leaves a 20% buffer. That may be too little, because data access is often the phase most likely to slip.

**Two risks:**
- **Data access** is your biggest risk. It depends on other people, such as approvals and data agreements, and you can't speed it up by working harder. If part of your buffer is meant for it, put that part early.
- **Figures** depend on the final statistics. If the statistics change late, the figures have to change too, so the plan to run them alongside writing only works if the statistics are actually finished.
````

## Answer without the skill (excerpt)

````text
**No, it doesn't fit.** You're about 2 weeks over.

**How it adds up**
- Data access, quality control, alignment and statistics run one after another: 6 + 2 + 3 + 4 = **15 weeks**
- Writing takes 5 weeks, and figures (2 weeks) run inside that window, so they add nothing: **5 weeks**
- Base plan: **20 weeks**
- Plus the 30% buffer: 20 × 1.3 = **26 weeks**, against the 24 you have

**Ways to make it fit**
1. **Use a smaller buffer.** The 4 spare weeks are a 20% buffer. That's on the thin side, especially with data access in the plan, since it often slips.
2. **Cut about 1.5 weeks of work.** With a 30% buffer, the base plan can be at most 24 / 1.3 ≈ 18.5 weeks.
3. **Overlap more phases.** For example, start figures during statistics, or start writing the methods while statistics is still running. That shortens the critical path without cutting any work.
4. **Put the buffer where the risk is.** Most of the uncertainty is probably in data access, so a 30% buffer on those 6 weeks alone is about 2 weeks. That lets you keep a solid buffer while staying inside 24 weeks.

I'd combine 3 and 4: overlap figures and methods writing with statistics, and put most of the buffer on data access. That should get you to 24 weeks.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
