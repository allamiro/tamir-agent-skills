---
name: performance-evaluation-methodology
description: Designs, runs and critiques performance experiments and benchmarks for software systems, covering the question and hypothesis, open versus closed load generation, coordinated omission, warm-up, repetitions, percentiles with confidence intervals, A/A noise checks, baselines and ablations, comparison tests, and the usual ways a benchmark claim misleads. Use for "design a benchmark", "is this benchmark valid", "how many runs do I need", "why is my p99 wrong", "compare two builds", "can I claim a 10 percent speedup", "load test plan", "review the evaluation section of this paper". Use caching-performance for tuning, observability for production measurement, requirements-capacity for sizing, and systems-literature-reading to judge published results.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Performance evaluation methodology

## Purpose and activation

A benchmark is an experiment, and most misleading ones fail before any statistics: no stated
question, a workload that fits in cache, a load generator that slows down when the server does, one
run, a mean where the tail matters. This skill plans or audits an experiment so that its number
can be defended. Activate when someone wants to measure, compare or claim a performance result, or
asks why measurements disagree. It decides what the data can support; it does not tune the system.

## Required inputs

The question or claim, with the smallest difference that would matter; the system, version and
configuration; the workload (real trace or synthetic, mix, sizes, key distribution); the environment
(hardware, OS, shared or dedicated, noise); the metric (throughput, latency percentiles, cost,
resource use); the comparison (baseline, previous build, competitor); and any data already collected.

## Workflow

1. **Write the claim as a falsifiable statement** with a threshold: "p99 under 200 ms at 5,000
   requests per second", "build B sustains 10 percent more throughput than build A".
2. **Choose the load model to match the question.** Open loop: requests arrive on a schedule
   regardless of the server's speed, as with independent users. Closed loop: a fixed number of clients
   each wait for a reply before sending again, as with a worker pool. A closed-loop generator that
   measures only completed requests under-reports delays (see coordinated omission below).
3. **Make the workload representative:** data size against cache size, key skew, read and write mix,
   request sizes, connection reuse, think time, and whether the system should be cold, warm or steady.
4. **Control the environment.** Same hardware and configuration for every arm, versions pinned,
   noise sources recorded, arms interleaved or run in randomised order so drift does not look like an
   effect. Small setup changes can shift results, so record them (`references/pitfalls.md`).
5. **Define warm-up and steady state** with a stated rule, and run long enough to see the slow
   events: garbage collection, compaction, cache fill, autoscaling, thermal limits.
6. **Repeat with independent runs** (fresh process or instance), not only more samples from one run.
   Estimate the count from the variation: `python3 scripts/perfstats.py runs --cv 0.1 --rel 0.02`.
7. **Measure latency from the intended send time,** record the whole distribution, and check that the
   tail has enough samples: `python3 scripts/perfstats.py tail --q 0.999 --k 10`.
8. **Run an A/A test:** the same build against itself. Its difference is the noise floor, and a claimed
   effect inside it is not an effect.
9. **Summarise and compare:** percentiles with bootstrap intervals, the difference with its interval,
   an effect size and a rank test: `python3 scripts/perfstats.py compare A.txt B.txt --stat p99`.
10. **Sweep the load** to find the knee where latency rises, rather than reporting one point.
11. **Sanity-check with Little's law:** concurrency should equal throughput times time in system;
    `python3 scripts/perfstats.py little --lam 1000 --w 0.2`.
12. **Report** the setup, the raw data location, the limits, and what the data cannot support
    (`assets/templates/experiment-plan.md`).

## Decision framework

| Question | Load model | Report |
|---|---|---|
| Will users see good latency at a given arrival rate? | Open loop at several rates | Percentiles against offered load, with intervals |
| How fast can a fixed pool of workers finish a job? | Closed loop | Throughput and completion time per run |
| What is the capacity? | Open loop ramp | The load where latency leaves its bound, not peak throughput |
| Is build B better than A? | Same model, interleaved, A/A included | Difference with interval and effect size |

| Summary | Use when | Avoid when |
|---|---|---|
| Mean | Totals and throughput | Latency with a long tail |
| Median | Typical experience, robust to outliers | The tail is the requirement |
| High percentile | A latency objective | Fewer than about ten samples beyond it |
| Ratio across benchmarks | Comparing speedups | Averaging with an arithmetic mean; use the geometric mean |
| Averaged per-instance percentiles | Never | Always; merge the raw samples or histograms instead |

## Architecture and implementation guidance

- Keep one file of raw measurements per run (one number per line), so the commands above can be rerun.
- Percentile definitions differ on small samples. `perfstats.py` implements nearest-rank and linear
  interpolation (the NumPy default); say which one you used.
- Coordinated omission: when a generator waits for a slow reply before sending the next request,
  the requests that should have been sent during the stall are never measured. Prefer a generator that
  sends on a schedule. `perfstats.py co` back-fills an estimate for data already collected.
- Bootstrap intervals over raw samples assume independent samples, which successive requests in one
  run often are not. Prefer one summary per independent run and an interval over those.
- Report resource use (CPU, memory, I/O) with throughput, so a speedup bought with 3 times the cores is visible.
- Distinguish the measurement bias in the setup from the effect under test (`references/pitfalls.md`).

## Failure and edge cases

- **Coordinated omission** making every percentile look better than users' experience.
- **A load generator that is the bottleneck,** so the system under test never saturates.
- **Cherry-picked benchmarks or only the favourable configuration** (selective benchmarking).
- **No variance shown,** or a significance claim from one run.
- **Warm cache against cold baseline,** or tuned system against default competitor.
- **Mean of percentiles** or averaging ratios arithmetically.
- **Throughput that "holds" while a queue grows,** so latency is unbounded.
- **Shared cloud noise** between arms run at different times.
- **A tail estimate from too few samples,** such as p99.9 from 500 requests.
- **Treating a p-value as importance:** a tiny effect can be significant, a large one can be noisy.
- **Many metrics, one lucky win.** Decide the primary metric before the run.

## Validation

- Run the self-test: `python3 scripts/perfstats.py --selftest`.
- The A/A difference is smaller than the claimed effect, with the same method and run count.
- Repeating the whole experiment on another day gives a difference whose interval overlaps the first.
- The tail check passes for every percentile quoted.
- Falsifier: a reported speedup that disappears when the arms are run in the other order.

## Expected output

An experiment plan or a critique: the claim and threshold, load model and why, workload, environment,
run counts, the commands to compute each number, results as estimates with intervals, an A/A
noise floor, threats to validity, and a plain statement of what the data does and does not show.

## Sources and confidence

- Book (direct): none; this skill extends the library to research work and is not taken from the book
- Book (synthesized): none
- Modern: measurement validity (does the metric measure the claimed property) adapted from Teo (Ed.), *Handbook of Quantitative Methods for Educational Research*, Sense 2013, doi:10.1007/978-94-6209-404-8, paraphrased; percentile, bootstrap and rank-test code cross-checked 2026-10-14 against NumPy and SciPy on 6,101 random comparisons; Heiser's *Systems Benchmarking Crimes* page (headings seen 2026-10-14, bodies not read); Georges et al. (OOPSLA 2007), Mytkowicz et al. (ASPLOS 2009), Fleming and Wallace (CACM 1986) and Little (1961), records fetched from Crossref 2026-10-14; coordinated omission from Tene's talk and a secondary description of the HdrHistogram back-fill, from author knowledge, VERIFY; Jain's textbook recommended but not checked
- Needs workload validation: run counts, warm-up length, the load model and the smallest difference that matters all depend on the system; not covered are simulation, queueing-network solutions and tuning advice
