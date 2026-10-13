# Capacity Estimation Worksheet

Use at workflow step 3. Keep units on every line. Round only at the end. Run
`python3 skills/requirements-capacity/scripts/capacity.py --help` (path relative to the library root) to compute the same table.
Illustrative numbers below are examples, not benchmarks.

## 1. Inputs (state source: measured / stated / ASSUMPTION)

| Symbol | Meaning | Unit | Value | Source |
|---|---|---|---|---|
| U | daily active users | users/day | 2,000,000 | ASSUMPTION |
| r | requests per user per day | req/user/day | 40 | ASSUMPTION |
| k | peak-to-average factor | ratio | 4 | ASSUMPTION |
| w | write fraction of requests | ratio | 0.05 | ASSUMPTION |
| s | average stored bytes per write | bytes | 2,000 | ASSUMPTION |
| b | average response size | bytes | 8,000 | ASSUMPTION |
| T | retention | days | 365 | stated |
| R | replication factor | copies | 3 | stated |
| h | headroom factor | ratio | 1.5 | policy |

## 2. Derived load

| Quantity | Formula | Example result |
|---|---|---|
| Requests/day | U × r | 80,000,000 |
| Average QPS | requests/day ÷ 86,400 s | ≈ 926 req/s |
| Peak QPS | average QPS × k | ≈ 3,700 req/s |
| Peak write QPS | peak QPS × w | ≈ 185 writes/s |
| Peak read QPS | peak QPS × (1 − w) | ≈ 3,520 reads/s |
| Peak egress | peak QPS × b × 8 | ≈ 237 Mbit/s |
| New data/day | requests/day × w × s | 8 GB/day |
| Raw storage | new data/day × T | 2.9 TB |
| Stored with replicas and headroom | raw × R × h | ≈ 13 TB |

## 3. Provisioning check

| Resource | Per-node measured limit | Nodes for peak | With N+1 |
|---|---|---|---|
| App servers | <measured req/s at p99 target> | peak QPS ÷ limit | +1 |
| DB write capacity | <measured writes/s> | | |
| Cache memory | working set bytes ÷ hit target | | |

A per-node limit must come from a load test or vendor-stated limit. If none exists, write
"UNMEASURED" and put a load test in the validation plan.

## 4. Sensitivity (multiply one input at a time; record the outputs that move)

| Input changed | Factor | Peak QPS | Storage | Dominant effect |
|---|---|---|---|---|
| k (spike) | ×2 | ×2 | – | compute, DB connections |
| r | ×2 | ×2 | ×2 | everything |
| T | ×3 | – | ×3 | storage cost, backup time |
| w | ×4 | write QPS ×4 | ×4 | primary DB is the bottleneck first |

State which inputs the design must tolerate being wrong by ×2 and ×10.

## 5. Latency budget

| Hop | p50 (ms) | p99 (ms) | Evidence |
|---|---|---|---|
| Client → edge | | | |
| Edge → service | | | |
| Service → DB / cache | | | |
| Sum of p99s is a pessimistic bound; fan-out of n parallel calls makes the slowest one dominate. | | | |

## 6. Conclusions

Bottleneck at expected peak: ______. First component to exhaust at 10× load: ______.
Scaling triggers (metric and threshold): ______.
