# `performance-evaluation-methodology`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I benchmarked old and new builds, 5 runs each: mean latency 41 ms for the old and 38 ms for the new. My manager wants to ship it as "7% faster". Is that supportable? Tell me what to check, what to run, and what I can honestly say today.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,985 | 1,817 |
| Input tokens read across all turns (including cached context) | 30,398 | 59,818 |
| Extra input tokens when the skill is installed | | +29,420 |
| Cost, US dollars at list price | 0.100 | 0.151 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 270 tokens for its name and description, which are in every session where the skill is installed, and about 2,800 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**Not yet.** The arithmetic is right: (41 − 38) / 41 ≈ 7.3% lower mean latency. But two means from 5 runs each don't tell you whether that 3 ms gap is real or just run-to-run noise. Whether you can claim it depends on numbers you haven't shown: the spread of the 10 individual runs.

## Why the spread decides it

With n = 5 per build, here is how the 95% confidence interval on the 3 ms difference changes with the per-run standard deviation (SD):

| Per-run SD | 95% CI on the difference | What you can say |
|---|---|---|
| ~1 ms | ≈ 1.5 to 4.5 ms (about 4% to 11%) | It's a real improvement, but "7%" is only the midpoint of a wide range |
| ~3 ms | ≈ −1.4 to 7.4 ms (includes 0) | You can't tell it apart from noise |

Even in the best case, "7% faster" claims more precision than you have.

## What to check

1. **The raw per-run numbers.** Compute the SD for each build and a CI on the difference using Welch's t-test or a bootstrap. This tells you right now which row of the table you're in.
2. **"Faster" at what?** You measured lower mean latency. That isn't the same as throughput, and it isn't tail latency. Check p50 and p99 as well. A mean can improve while p99 gets worse.
3. **Run order.** If you ran all the old runs and then all the new ones, drift (thermals, background jobs, caches, CPU frequency scaling) can produce a gap like this on its own.
4. **Same conditions.** Confirm both builds used the same machine, inputs, build flags, warm-up and config, and that nothing else changed between runs.
5. **Noise floor (A/A test).** Benchmark the old build against itself the same way. If two identical builds differ by 2–3 ms, a 3 ms gap means nothing.
6. **Representativeness.** Check that the workload resembles production. If this is a load test, use an open-loop load generator so slow requests aren't hidden (coordinated omission).

## What to run

- **Interleave and randomise the order** (ABBA…), with warm-up runs discarded, and do at least 20–30 runs per build.
  - For a CLI program: `hyperfine --warmup 3 --runs 30 './old ...' './new ...'` reports mean ± SD and the relative difference.
- **Run an A/A test** with the same harness.
- **Analyse the per-run results:**

```python
import numpy as np
from scipy import stats
old = np.array([...]); new = np.array([...])   # per-run latencies (ms)
print(stats.ttest_ind(old, new, equal_var=False))
boot = [np.mean(np.random.choice(old, len(old))) - np.mean(np.random.choice(new, len(new)))
        for _ in range(10000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"diff CI: {lo:.2f}–{hi:.2f} ms ({lo/old.mean():.1%}–{hi/old.mean():.1%})")
```

- **Look at percentiles** (p50, p99) across all requests, not just the mean of per-run means.

## What you can honestly say today

> "In a preliminary benchmark (5 runs per build, [machine/workload]), mean latency dropped from 41 ms to 38 ms (~7%). We haven't yet confirmed that this is outside run-to-run noise; a larger interleaved run is in progress."

If the SD turns out to be small (about 1 ms or less), you can upgrade that to: "mean latency improved by roughly 4–11% (95% CI) on [workload]."

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Can you claim "7% faster" from 5 runs at 41 ms vs 38 ms?

**Not yet.** The arithmetic is right: 3/41 is a 7.3% drop in mean latency. But two means from 5 runs each don't show whether that 3 ms is a real improvement or ordinary run-to-run noise. Whether it holds up depends almost entirely on how much your runs vary, and you haven't measured that yet.

## Why 5 runs may not be enough

The answer depends on the standard deviation (SD) across runs:

| SD per build | 95% CI on the difference | Verdict |
|---|---|---|
| ~1 ms | roughly 1.5 to 4.5 ms (4–11%) | Real improvement, but "7%" is still loose |
| ~2 ms | roughly 0.1 to 5.9 ms (0–14%) | Barely distinguishable from zero |
| ~3 ms | roughly −1.4 to 7.4 ms | Can't tell it apart from no change |

A 2–3 ms spread is very common for latency benchmarks on a laptop. It's especially likely on a Mac, where thermal throttling, power state and background processes all add noise.

Rounding alone also matters. If 41 and 38 are rounded values, the true difference could be anywhere from about 2 to 4 ms, which is 5–10%.

## What to check

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
