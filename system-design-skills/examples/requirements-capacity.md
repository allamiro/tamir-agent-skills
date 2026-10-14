# `requirements-capacity`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> We expect 2 million daily users making 40 requests each, with a 4x evening peak and 5% writes. How many requests per second and how much storage per year do we need, and which availability target is realistic?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,254 | 1,752 |
| Input tokens read across all turns (including cached context) | 30,373 | 71,747 |
| Extra input tokens when the skill is installed | | +41,375 |
| Cost, US dollars at list price | 0.085 | 0.156 |
| Skills invoked in the sample run | none | `requirements-capacity` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 200 tokens for its name and description, which are in every session where the skill is installed, and about 2,100 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
## Requests per second

| Figure | Formula | Result |
|---|---|---|
| Requests per day | 2M users × 40 | 80M/day |
| Average QPS | 80M ÷ 86,400 s | **~930 req/s** |
| Peak QPS | 930 × 4 | **~3,700 req/s** |
| Peak reads (95%) | 3,700 × 0.95 | ~3,500 req/s |
| Peak writes (5%) | 3,700 × 0.05 | **~185 req/s** (about 46/s on average) |

**Plan for about 10k req/s.** The 4× factor is an hourly average. Traffic within the peak hour comes in short bursts, and during an incident retries multiply load further: three layers each retrying three times can turn one request into 27. Sizing for about 2.5× the computed peak covers both.

**What this means for the design:** 3,500 reads/s is easy for a cache plus a few app servers. 185 writes/s is light for a single well-tuned relational primary. This load does not justify sharding. Load-test at 1.5× peak (about 5.5k req/s) before committing to node counts.

## Storage per year

You didn't give a record size, so this part is an assumption.

- Writes per year: 4M per day × 365 = **~1.46 billion records/year**

| Average record size (ASSUMPTION) | Raw data/year | With indexes (×1.5) and 3 replicas |
|---|---|---|
| 200 B | 0.3 TB | ~1.3 TB |
| **1 KB (expected)** | **1.5 TB** | **~6.6 TB** |
| 10 KB | 14.6 TB | ~66 TB |

- **Record size is the input that matters most for storage.** Pin it down before buying anything.
- If writes include images or other media, keep those in object storage and size them separately. They would dwarf these numbers.
- Storage adds up year after year: with flat traffic, year 3 holds 3× this amount. Apply your growth rate to user count, not to storage alone.
- Backups (for example, 30 days of snapshots) add roughly another 1× the data.

## Availability target

| Target | Downtime allowed per year | Downtime allowed per month | What it takes |
|---|---|---|---|
| **99.9%** | 8.8 h | 43 min | Single region, multiple availability zones (separate data centres in one region), automatic database failover, safe rollbacks |
| 99.95% | 4.4 h | 22 min | Same as 99.9%, plus a mature on-call rotation, canary deploys and tested failover |
| 99.99% | 53 min | 4.3 min | Multiple regions (usually all serving traffic at once), automated recovery, and a lot more cost and complexity |

**Recommendation: commit to 99.9% and aim internally for 99.95%.**

- Availability multiplies across serial dependencies. Four components at 99.95% each give about 99.8% end to end, so every hard dependency eats into the budget.
- A single bad deploy or a slow database failover can use up a whole month's 99.99% allowance (4.3 minutes).
- At this scale, 99.99% only makes sense if the business can show that an hour of downtime costs more than running a second region.

## Assumptions to confirm

- **Average record size:** this moves storage by 10× or more.
- **Peak factor:** the 4× is an hourly average; bursts within the hour may be higher.
- **Retention:** whether data is kept forever or deleted after N days.
- **Latency target:** you didn't state one; p99 under 200 ms is a typical starting point.

If you give me the record size and retention, I can tighten the storage numbers and turn them into a cost estimate.
````

## Answer without the skill (excerpt)

````text
# Capacity estimate: 2M daily users, 40 requests each

## Requests per second

| | Per day | Average RPS | Peak RPS (4×) |
|---|---|---|---|
| **Total** | 2M × 40 = **80M** | 80M ÷ 86,400 ≈ **~930** | **~3,700** |
| Reads (95%) | 76M | ~880 | ~3,500 |
| Writes (5%) | 4M | ~46 | **~185** |

Size the system for about **7,500 RPS**. That is twice the evening peak, which leaves room for retries, traffic spikes, one node failing, and a year of growth.

## Storage per year

You didn't give a record size, so the figures below assume each write stores about **1 KB**:

- 4M writes/day × 1 KB = **~4 GB/day**
- × 365 = **~1.5 TB/year** of raw data
- × 3 replicas = **~4.4 TB/year**
- With indexes, logs and backups (about 1.5–2× more): **about 7–9 TB/year provisioned**

The total scales directly with record size:

| Avg write size | Raw/year | Provisioned/year (3× replication + overhead) |
|---|---|---|
| 0.5 KB | ~0.7 TB | ~4 TB |
| 1 KB | ~1.5 TB | ~8 TB |
| 10 KB | ~15 TB | ~80 TB |

If writes include media such as images, store those in object storage and budget for them separately.

## Availability target

**99.9% to 99.95% is realistic.**

| Target | Downtime/year | Downtime/month | What it takes |
|---|---|---|---|
| 99.9% | ~8.8 h | ~43 min | Redundant app servers and a DB replica with failover, in one region |
| **99.95%** | ~4.4 h | ~22 min | Multi-AZ, automated failover, zero-downtime deploys, good monitoring |
| 99.99% | ~53 min | ~4.3 min | Multi-region active-active, mature on-call, much more cost and complexity |

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
