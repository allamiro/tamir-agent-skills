# Observability design reference

Illustrative numbers.

## 1. Cardinality worked example

Metric: `http_request_duration_seconds` histogram with labels.

| Label | Distinct values |
|---|---|
| service | 40 |
| route (template, not raw URL) | 25 per service on average |
| method | 5 |
| status class (2xx, 3xx, 4xx, 5xx) | 4 |
| histogram buckets | 12 |

Series ≈ services × routes × methods × status × buckets, but combinations that never occur
are not created. Upper bound: 40 × 25 × 5 × 4 × 12 = 240,000 series for this one metric.
Now add `user_id` with 1,000,000 distinct users: 240,000 × 1,000,000 = 2.4 × 10^11 possible
series. Even if only 0.1% of combinations occur, that is 2.4 × 10^8 series - far beyond
what most stores handle. Fix: remove `user_id`; record per-user detail in logs or traces.
Add `instance`/`pod` labels cautiously: churn creates new series on every restart.

## 2. Ingestion and storage sizing

Active series S = 2,000,000; scrape interval 15 s.

- Samples/s = S / 15 = 133,333.
- Samples/day = 133,333 × 86,400 = 11.52 × 10^9.
- With an assumed compressed cost of ~1.5 bytes per sample (assumption: measure with your
  engine; may differ by several times): ≈ 17 GB/day → 15 days raw ≈ 260 GB.
- Downsample to 5-minute rollups after 15 days: 1/20 of samples. Keep 13 months of rollups.

Planning rule: size from measured bytes per sample after a pilot, include replication, and
leave 30-50% headroom for query load and growth.

## 3. Alert definition template

| Field | Example |
|---|---|
| Name | CheckoutAvailabilityFastBurn |
| Type | SLO burn |
| Condition | error ratio over 1 h > 14.4 × 0.001 AND over 5 min > 14.4 × 0.001 |
| Severity | page |
| Owner | payments on-call |
| Runbook | link; first three checks; rollback steps |
| User impact statement | "Checkout failing for more than 1.4% of requests" |
| Dashboard | link |
| Test | synthetic failure injection monthly |

## 4. Burn-rate arithmetic (verify with the script)

Budget fraction consumed = burn rate × alert window ÷ SLO window.

- 14.4 × 1 h ÷ 720 h = 2%
- 6 × 6 h ÷ 720 h = 5%
- 1 × 72 h ÷ 720 h = 10%

Time to exhaust the whole budget at burn rate b = window ÷ b (14.4 → 50 h for 30 days).

## 5. Golden-signal dashboard checklist

- [ ] Traffic (requests/s) by route and status
- [ ] Errors (rate and ratio), split by cause where possible
- [ ] Latency p50/p95/p99 (histograms), plus slow-request count
- [ ] Saturation: CPU, memory, connection pool use, queue depth, thread pool
- [ ] Dependencies: call rate, errors, latency per downstream
- [ ] Deploy/config change markers
- [ ] SLO status and remaining error budget

## 6. Logging standard (fields)

`ts, level, service, version, env, trace_id, span_id, request_id, user_hash (not raw id),
route, status, duration_ms, error_code, message`. Never log credentials, tokens, full
card numbers, or unneeded personal data. Set per-level volume budgets; sample debug logs.

## 7. Host triage sequence (no product assumptions)

1. Is the whole host busy or one process? (load/run queue, CPU by process)
2. Memory: free vs cache, swapping, per-process growth over time (leak?).
3. Disk: utilization, IO wait, queue depth, which process reads/writes.
4. Network: connections by state, retransmits, saturation.
5. Drill into the process: thread/stack dump, profiler/flame graph, system-call trace.
6. Correlate with deploys, traffic changes, dependency latency.
