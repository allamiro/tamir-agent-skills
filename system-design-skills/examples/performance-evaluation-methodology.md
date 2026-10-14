# `performance-evaluation-methodology`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I benchmarked old and new builds, 5 runs each: mean latency 41 ms for the old and 38 ms for the new. My manager wants to ship it as "7% faster". Is that supportable? Tell me what to check, what to run, and what I can honestly say today.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,839 | 1,912 |
| Input tokens read across all turns (including cached context) | 30,399 | 72,529 |
| Extra input tokens when the skill is installed | | +42,130 |
| Cost, US dollars at list price | 0.097 | 0.165 |
| Skills invoked in the sample run | none | `performance-evaluation-methodology` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 270 tokens for its name and description, which are in every session where the skill is installed, and about 2,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**Short answer: not yet.** The 7% figure is just arithmetic: (41 − 38) / 41 = 7.3%. Whether it's a real speedup depends on how much the 5 runs varied, and you haven't said. Two means alone can't support any claim.

## The deciding check: run-to-run spread

Take the 5 per-run means for each build and run a Welch t-test. With 5 runs each, a 3 ms gap only clears 95% confidence if the standard deviation between runs is **below about 2 ms** (roughly 5% of the mean):

| Run-to-run SD | 95% CI on the 3 ms gap (approx.) | Verdict |
|---|---|---|
| 1 ms | about 1.5 to 4.5 ms | Real, somewhere between 4% and 11% faster |
| 2 ms | about 0.1 to 5.9 ms | Borderline, the low end is close to zero |
| 3 ms | about −1.4 to 7.4 ms | Can't tell apart from noise |

Even in the best case, the honest claim is a range ("4–11%"), not exactly "7%".

## What to check

1. **Were the runs independent?** Each run should be a fresh process or instance. Five samples from one process don't count as five runs.
2. **Were the builds interleaved?** If you ran all old runs and then all new ones, drift (thermal, background jobs, cloud neighbours, cache state) can look like a speedup. Rerun in alternating or random order.
3. **A/A noise floor.** Benchmark the old build against itself the same way. If two copies of the same build differ by 2–3 ms, your 3 ms means nothing.
4. **Did both builds get the same treatment?** Same hardware, config, data size and warm-up. A warm cache for one build and a cold one for the other is a classic accident.
5. **Is the mean the right metric?** "Faster" to users usually means the median and p99. A lower mean can hide a worse tail. Compare percentiles, and make sure each percentile you quote has enough samples behind it (at least ~10 above it, so p99 needs about 1,000+ requests).
6. **Resource use.** Check CPU and memory too, so you'd notice a speedup that just uses more cores.
7. **Load model.** If the load generator waits for each reply before sending the next request, it under-reports latency spikes (coordinated omission). Make sure both builds were measured the same way, ideally at the load level you actually care about.

## What to run

Put one value per line in files (per-run means, or raw per-request latencies):

```bash
S=.claude/skills/performance-evaluation-methodology/scripts/perfstats.py
python3 $S compare old_runs.txt new_runs.txt --stat mean    # difference + CI + effect size + rank test
python3 $S compare old_raw.txt  new_raw.txt  --stat p99     # check the tail too
python3 $S runs --cv <your observed CV> --rel 0.07          # how many runs you need to resolve 7%
python3 $S tail --q 0.99 --k 10                             # samples needed for a trustworthy p99
```

Plus the A/A run (old against old) through the same `compare` command.

If the spread turns out to be around 5%, plan on **at least 8–10 interleaved runs per build**. With a spread of 3% or less, 5 runs is enough.

## What you can honestly say today

> "In an initial benchmark (5 runs each), mean latency was 38 ms for the new build vs 41 ms for the old. We're confirming this with repeated, interleaved runs and a noise check before quoting a speedup figure."

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
## Short answer

**Not yet.** The arithmetic is right: (41 − 38) / 41 ≈ 7.3% lower mean latency. Two things are missing before you can claim it. First, you don't know whether a 3 ms gap is bigger than the normal run-to-run noise. Second, you don't know whether a mean measured under your conditions reflects what users will see. With only 5 runs per build, the answer depends almost entirely on how much the runs vary, and two means don't tell you that.

## What to check first (using the data you already have)

1. **Spread of the 5 runs in each build.** Look at the standard deviation or the min–max range. Here's roughly how it plays out for a Welch t-test with n=5 per group:
   - SD ≈ 1 ms: t ≈ 4.7. The difference is clearly real.
   - SD ≈ 2 ms: t ≈ 2.4, p ≈ 0.05. Borderline.
   - SD ≈ 3 ms or more: t ≈ 1.6. You can't tell it apart from noise.
   
   If the two builds' ranges overlap a lot, stop there. You don't have a result yet.
2. **Unit of replication.** If each "run" contains thousands of requests, n is still 5, not thousands. Pooling all the requests and running a test on them makes the result look far more certain than it is.
3. **Run order.** Did all the old runs happen before all the new ones? If so, warm caches, thermal throttling, CPU frequency boost or a background job could explain the 3 ms on their own.
4. **Same conditions.** Check that both builds ran on the same machine, inputs, configuration, build flags (release vs debug, same compiler or JIT settings), warm-up and dataset state.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
