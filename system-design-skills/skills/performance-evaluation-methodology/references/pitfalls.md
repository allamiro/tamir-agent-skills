# Benchmark pitfalls and what to ask for

Each row is a claim a report might make, what usually goes wrong, and what to request before
believing it. Sources for the categories are listed in `SKILL.md`; the questions are the skill's own.

| Claim | What goes wrong | Ask for |
|---|---|---|
| "Latency is 3 ms" | Mean of a skewed distribution, or coordinated omission | Percentiles, the load model, and the send-time rule |
| "X is 20 percent faster" | One run, one workload, no variance | Runs per arm, an interval, the A/A difference |
| "Handles 100k requests per second" | A queue grew while it "held" the rate, or the generator was the limit | Latency against offered load, generator CPU |
| "Scales linearly" | Measured on a range that fits in memory, or one workload | The range, the resource that saturates first |
| "p99 is 80 ms" | Averaged per-instance p99s, or too few samples | Raw samples or merged histograms; tail sample count |
| "Beats the competitor" | The competitor ran with defaults, or a different durability setting | Both configurations, durability and replication settings |
| "No regression" | Underpowered comparison | The smallest detectable difference for the run count |
| "Geometric mean speedup 1.1" | Hides a large regression on one benchmark | The per-benchmark table |

## Measurement bias

Results can change with factors unrelated to the design under test, such as link order, environment
size, background load, CPU frequency policy and which machine in a fleet ran the job (Mytkowicz et
al., ASPLOS 2009). Counter it by randomising or interleaving arms, repeating across setups, and
recording the environment.

## A/A test

Run the same build as both arms with the same procedure. Differences between the arms estimate the
noise floor for that method, machine and run count. A claimed effect smaller than the A/A spread is not
supported.

## Sample counts for tail percentiles

To have about k samples beyond quantile q, a run needs n of roughly k divided by (1 - q). For q = 0.99
and k = 10 that is 1,000; for q = 0.999 it is 10,000. `perfstats.py tail` computes it exactly.
