# `architecture-scaling`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Our monolith slows down at 1,200 requests per second. Should we split it into microservices, scale up, or do something else? Find the bottleneck before recommending anything.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,366 | 1,881 |
| Input tokens read across all turns (including cached context) | 61,029 | 113,760 |
| Extra input tokens when the skill is installed | | +52,731 |
| Cost, US dollars at list price | 0.095 | 0.194 |
| Skills invoked in the sample run | none | `architecture-scaling` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 200 tokens for its name and description, which are in every session where the skill is installed, and about 3,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I can't find the bottleneck yet because there's nothing to measure. The working directory has no code, metrics, profiles or load-test results, so any recommendation now would be a guess. Here's what I need from you and how each answer leads to a decision.

## My recommendation until we have data

**Don't split into microservices and don't scale up yet.** Splitting the code doesn't make a slow resource faster. If the database is what's saturated at 1,200 req/s, microservices that share that database (or call each other over the network) will be slower. The only good reason to split is that your teams are blocking each other's releases, and that has nothing to do with request rate. Scaling up only helps if the thing you make bigger is the thing that's saturated.

## Step 1: Describe "slows down" as a number

For example: "p99 goes from 150 ms at 800 req/s to 2.5 s at 1,200 req/s; target is 300 ms." Also tell me whether errors or timeouts rise, and whether every endpoint slows or only a few.

## Step 2: Capture these readings at 1,200 req/s

Either at your production peak or in a load test at about 1.5× that load.

| Resource | What to capture | It's the bottleneck if… |
|---|---|---|
| App CPU (per instance) | CPU %, run queue, a flame graph | >75% CPU and latency rises with it |
| App memory / GC | GC pause times, heap size, swapping | GC pauses grow with load |
| App threads / connection pools | busy worker threads, time spent waiting for a DB connection | CPU is low but requests queue, waiting for a pool |
| Database | CPU, IO wait, slow query log, lock waits, active connections vs `max_connections` | DB CPU or IO >75%, or one query dominates |
| Locks | thread dumps, DB lock-wait views | low CPU everywhere but latency is high |
| Downstream APIs | latency histograms, 429s or timeouts | a dependency's latency jumps at this load |
| Network / LB | connection counts, retransmits, LB queueing | connection limits or bandwidth near the cap |

A useful clue: **if nothing is busy but latency is high, the problem is waiting, not lack of capacity.** That means pool sizes, locks or a slow dependency. Adding machines won't fix it.

## Step 3: Apply the cheapest fix that clears the bottleneck

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
I couldn't find the bottleneck. The working directory is empty: there's no code, config, load-test output or metrics to look at. So I can't make a recommendation yet, and any answer about microservices or scaling up would be a guess.

You'd usually find the cause by measuring at 1,200 req/s in this order.

**1. Find which resource is saturated at the moment it slows down.** Run a load test that ramps past 1,200 req/s and record these at the same time:
- **App CPU per core.** One core at 100% while the others sit idle means a single-threaded hot path, a global lock or a GIL.
- **Worker or thread pool usage.** Check Puma/Gunicorn/Tomcat workers and Node event-loop lag. A full pool with low CPU means you're waiting on I/O.
- **DB connection pool.** Wait time to get a connection is the most common cause of a sudden slowdown at a fixed rate.
- **Database itself.** Check CPU, slow query log, lock waits and the top queries by total time (`pg_stat_statements` or the MySQL performance schema).
- **Downstream calls.** Check latency and timeouts for caches, external APIs and queues.
- **Memory and GC.** Look at GC pause time and whether heap use climbs under load.
- **Network and OS.** Check file descriptors, ephemeral ports, conntrack and the load-balancer connection limits.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
