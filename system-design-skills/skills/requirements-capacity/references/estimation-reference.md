# Estimation reference: formulas, worked example, sensitivity

All numbers here are illustrative and use decimal units (1 GB = 10^9 B). They are not
benchmarks. Replace every input with your own.

## 1. Unit conversions to keep handy

- Seconds per day: 86,400. Per 30 days: 2,592,000. Per year: 31,536,000.
- 1 request/s sustained = 86,400 requests/day = about 2.6 million per 30 days.
- Bits = bytes × 8. Mbit/s = bytes/s × 8 ÷ 10^6.
- Rule: always attach a unit symbol to each cell in a worksheet.

## 2. Core formulas

| Quantity | Formula | Unit |
|---|---|---|
| Requests per day | DAU × requests per user per day | req/day |
| Average QPS | requests per day ÷ 86,400 | req/s |
| Peak QPS | average QPS × peak factor | req/s |
| Write QPS / Read QPS | peak × w / peak × (1 − w) | req/s |
| Egress | peak QPS × response bytes × 8 | bit/s |
| Daily new data | req/day × w × bytes per write | B/day |
| Retained data | daily new data × retention days | B |
| Provisioned storage | retained × replication × headroom (+ indexes, backups) | B |
| Concurrent connections (Little's law) | arrival rate × average time in system | connections |
| Servers needed | peak QPS ÷ (per-node measured QPS at target latency) → round up, add N+1 | nodes |
| Cache memory | hot working set bytes (not total data) | B |
| Fan-out writes | writes × recipients per write | writes/s |

Adjust storage for index overhead (often 20-100% for heavily indexed relational tables;
measure) and for compression if your store compresses (measure).

## 3. Worked example: photo-comments service (illustrative)

Inputs: DAU 2,000,000; 40 requests/user/day; peak factor 4; 5% writes; 2 KB per write;
8 KB average response; 365-day retention; replication 3; headroom 1.5.

| Step | Calculation | Result |
|---|---|---|
| Requests/day | 2,000,000 × 40 | 80,000,000 |
| Average QPS | 80,000,000 ÷ 86,400 | 926 req/s |
| Peak QPS | 926 × 4 | 3,704 req/s |
| Peak writes | 3,704 × 0.05 | 185 /s |
| Peak reads | 3,704 − 185 | 3,519 /s |
| Egress | 3,704 × 8,000 × 8 | 237 Mbit/s |
| New data/day | 80,000,000 × 0.05 × 2,000 | 8 GB |
| Raw storage | 8 GB × 365 | 2.92 TB |
| Provisioned | 2.92 × 3 × 1.5 | 13.1 TB |

Interpretation: 185 writes/s and 13 TB are within what one well-configured relational
primary with replicas can plausibly handle *if measured per-node limits confirm it*
(UNMEASURED here). Nothing in these numbers justifies sharding. 237 Mbit/s of egress points
to a CDN or caching for static payloads, not to more app servers.

## 4. Sensitivity analysis procedure

1. Write inputs in a table. 2. Scale one input ×2 and ×10, recompute outputs. 3. Rank by

effect. 4. Decide for each high-impact input: measure it, cap it (rate limit), or design a
headroom plan.

Result for the example (from `scripts/capacity.py --sensitivity`):

| Input ×10 | Peak QPS | Write QPS | Storage |
|---|---|---|---|
| DAU | ×10 | ×10 | ×10 |
| peak factor | ×10 | ×10 | ×1 |
| write fraction | ×1 | ×10 | ×10 |
| retention | ×1 | ×1 | ×10 |

Reading it: the peak factor and the write fraction are the cheapest things to get wrong
and the most expensive consequences (write QPS ×10 = 1,850/s hits the primary first).
Measure them early.

## 5. Latency budget method

1. Write the end-to-end target at a percentile (for example p99 < 300 ms).
2. List the hops on the critical path; mark sequential vs parallel.
3. Assign each hop a budget so sequential budgets sum to ≤ target minus a safety margin.
4. For parallel fan-out of n calls, the chance that at least one is slow is
   1 − (1 − p)^n where p is the per-call tail probability: with p = 1% and n = 10, about 9.6%
   of requests see a p99-slow call. Reduce fan-out, hedge, or set per-call timeouts.
5. Validate with histograms from a load test, not averages.

## 6. Availability and recovery targets

- Downtime budget = (1 − SLO) × window. See the table in `SKILL.md`.
- RPO (data you may lose) drives replication/backup frequency; RTO (time to recover)
  drives standby readiness. Both need an owner and a drill date.
- Composite availability: serial product; parallel 1 − Π(1 − a_i), upper bound under
  independence.

## 7. Common estimation mistakes

- Using DAU as concurrent users.
- Forgetting replication, indexes, backups and logs in storage.
- Treating average QPS as the sizing number.
- Ignoring that writes may be amplified (fan-out, secondary indexes, search indexing).
- Presenting precise-looking numbers from imprecise inputs: carry ranges.
