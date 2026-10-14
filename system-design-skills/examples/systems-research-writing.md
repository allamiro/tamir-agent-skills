# `systems-research-writing`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I built a distributed scheduler that cuts tail latency by 30% in our cluster. Help me turn it into a paper: write the claim, at most three contributions, a claims-evidence matrix with the limit of each claim, and an outline for a systems conference.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,781 | 3,085 |
| Input tokens read across all turns (including cached context) | 30,394 | 109,845 |
| Extra input tokens when the skill is installed | | +79,451 |
| Cost, US dollars at list price | 0.115 | 0.195 |
| Skills invoked in the sample run | none | `systems-research-writing` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 2,600 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I don't know yet how your scheduler gets its win, so I've written the draft with **[bracketed placeholders]** for the mechanism and the numbers. The structure won't change; you fill in your facts.

One thing to fix first: "Cuts tail latency by 30% in our cluster" is a result, not a claim. Reviewers will ask why it works and whether it works anywhere else. The paper has to rest on the idea that produces the 30%, and the 30% is one piece of evidence for it.

---

## 1. The claim (one sentence)

> **[Existing schedulers] inflate tail latency because they [root cause, e.g. place work using stale or averaged load signals and ignore per-request service-time variance]; a scheduler that [key insight, e.g. uses cheap, fresh per-node queue estimates to place work] reduces p99 latency by [X]% ([CI]) versus [strongest baseline] on [workload class], with [overhead] scheduling overhead.**

Test it: someone outside your sub-area should be able to say *what was broken*, *what the idea is*, and *how much it helped* after reading only this sentence.

## 2. Contributions (at most three, each one testable)

1. **Diagnosis.** Measurements on [cluster/trace] show that [Y]% of tail-latency events come from [root cause]. Current schedulers ([A], [B]) cannot avoid this because [structural reason].
   *Falsified if:* removing the root cause does not move the tail, or the tail comes mainly from something else (GC, network, stragglers).
2. **Mechanism.** [Name], a scheduler that [insight in one clause]. Its design lets it [property, e.g. decide in O(1) without global coordination].
   *Falsified if:* the ablation shows the gain comes from some other part (for example simply more replicas, or more retries).
3. **Evaluation.** On [production cluster + N public traces/benchmarks], [Name] reduces p99 by [X]% and p99.9 by [Z]% versus [tuned baselines], with throughput, cost and median latency staying within [bound].
   *Falsified if:* a properly tuned baseline closes the gap, or the gain disappears at different load or with a different workload mix.

"We built a distributed scheduler" is deliberately left off the list. A component is not a contribution.

## 3. Claims and evidence matrix

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
Your 30% number is a result. A reviewer at OSDI, SOSP, NSDI, EuroSys or ATC will ask why it happens and whether it carries over to other clusters. So the draft below is built around the mechanism, and the 30% serves as evidence for it.

I don't know your design yet. Anything in **[brackets]** is a placeholder for you to fill in. I wrote it assuming a common pattern: the scheduler cuts tail latency by placing work based on queueing delay it predicts, not on CPU or memory use alone. If your mechanism is different, the structure still works; swap in the right insight.

---

## 1. The claim (one sentence)

> In clusters running [latency-critical services alongside batch jobs], most of the tail latency comes from **[short-lived queueing interference that utilization-based schedulers can't see]**. A scheduler that **[estimates per-node queueing delay online and places and migrates work on that estimate]** cuts P99 latency by **~30%** compared with **[baseline, e.g. the Kubernetes default scheduler or your previous production scheduler]**, at **[≤X% throughput or utilization cost]**.

What a reviewer will check in this sentence:
- **Which tail:** P99 or P99.9, measured end to end or per service.
- **Which baseline:** "30% better than our old scheduler" only carries weight if the old one is a strong, well-known system.
- **What it cost:** a tail improvement with no stated throughput or utilization cost will be treated as suspect.

## 2. Contributions (three)

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
