# `systems-research-writing`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I built a distributed scheduler that cuts tail latency by 30% in our cluster. Help me turn it into a paper: write the claim, at most three contributions, a claims-evidence matrix with the limit of each claim, and an outline for a systems conference.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,676 | 2,981 |
| Input tokens read across all turns (including cached context) | 30,396 | 110,582 |
| Extra input tokens when the skill is installed | | +80,186 |
| Cost, US dollars at list price | 0.113 | 0.196 |
| Skills invoked in the sample run | none | `systems-research-writing` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 2,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I don't yet know how your scheduler works or how you measured the 30%, so below is a structured draft. Anything in `[brackets]` is a gap you need to fill. I wrote it so you can see exactly what a reviewer will ask for.

## The claim (one sentence)

> **[Scheduler name] cuts p[99] job/request latency by 30% relative to [baseline, e.g. the cluster's tuned production scheduler] on [workload] in a [N]-node production cluster, by [the one insight, e.g. "placing tasks using predicted queueing delay instead of current load"], at a cost of [overhead: CPU, decision latency, throughput].**

There are four places a reviewer will push on this:
- **"Tail latency" must name a percentile** (p99, p99.9) and the unit: per request, per task or per job.
- **"30%" needs a baseline.** Compared with what, and was that baseline tuned? An untuned default is the most common reason reviewers reject this kind of paper.
- **"Our cluster" is a single environment.** The headline holds for that environment. Generalising needs trace replay or a second workload (see contribution 3).
- **The insight is the paper.** "We built a scheduler" is a component, not a contribution. You need the reason existing schedulers lose at the tail and the idea that fixes it.

## Contributions (at most three, each falsifiable)

1. **Problem analysis.** A measurement study of [cluster] showing that [X% of tail latency comes from cause Y, e.g. head-of-line blocking or stale load information], which [existing schedulers A, B] do not address because [assumption].
2. **Design.** [Scheduler], which uses [mechanism] to [effect], with decision latency of [Z µs] at [N] nodes.
3. **Evaluation.** On [production workload] and [K replayed or public traces], [Scheduler] reduces p99 latency by [30% ± CI] compared with [tuned baselines], keeps throughput within [x%] of the baseline, and the ablation attributes [most] of the gain to [mechanism].

## Claims-evidence matrix

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Turning the scheduler into a systems paper

I don't know how your scheduler works yet, so I've written everything below as a template. Brackets mark what you need to fill in, and I've put an example in italics where it helps. Most of the work is in the claim: reviewers at OSDI, NSDI, EuroSys, SoCC or ATC won't accept "our scheduler cuts tail latency by 30%" as a contribution on its own. They want to know **why** it works and **when** it stops working.

---

## 1. The central claim

**Template:**
> Tail latency in [setting] is driven by [root cause] that existing schedulers can't see because [blind spot]. [System name] [mechanism], which reduces P[99/99.9] latency by [X]% compared with [strongest baseline] at [load level], with [cost] overhead.

*Example:* "Tail latency in multi-tenant clusters running microservices comes mainly from head-of-line blocking behind short-lived interference bursts. Centralized schedulers react to these bursts too slowly to help. Bolt makes placement decisions on each node using sub-millisecond interference signals. On production traces it cuts P99 latency by 30% compared with [baseline], with under 2% throughput loss."

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
