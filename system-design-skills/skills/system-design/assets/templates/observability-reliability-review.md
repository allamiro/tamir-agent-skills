# Observability and Reliability Review

## 1. Service level objectives

| User journey | SLI (good events / valid events) | SLO | Window | Error budget (minutes or events) | Measured where |
|---|---|---|---|---|---|
| Checkout success | HTTP 2xx/3xx non-timeout ÷ valid checkout requests | 99.9% | 30 d | 43.2 min equivalent | load balancer + app |
| Search latency | requests < 300 ms ÷ valid requests | 99% | 30 d | 1% | app histogram |

Check: SLIs reflect what users experience, not host health; the SLO is achievable given
dependencies (serial availability multiplies); the budget has a written policy (what
happens when exhausted).

## 2. Signals

| Signal | Present? | Coverage notes |
|---|---|---|
| Metrics: rate, errors, duration per endpoint and dependency | | |
| Saturation: CPU, memory, disk, connection pools, queue depth, consumer lag | | |
| Structured logs with correlation id; PII scrubbed | | |
| Traces across service boundaries; sampling policy | | |
| Business metrics (orders/min) | | |
| Synthetic probes from outside | | |

Cardinality check: series count = product of distinct label values per metric. No user id,
request id or URL-with-ids as labels. Estimate total series: ______ vs backend limit ______.

## 3. Alerting

| Alert | Condition | Window | Severity (page/ticket) | Runbook link | Fires on symptom or cause? |
|---|---|---|---|---|---|

Rules: page only on user-impacting symptoms or imminent budget exhaustion; every page has
an owner and runbook; multi-window burn-rate alerts for SLOs; no alert without an action.
Review noise: pages per week ______ actionable ______.

## 4. Dashboards

Overview (golden signals per service), dependency health, deploy markers, capacity trend.

## 5. Reliability controls

| Control | Present | Evidence |
|---|---|---|
| Timeouts on every outbound call | | |
| Retries with backoff + jitter and budget; idempotent operations only | | |
| Circuit breaker / load shedding / bulkheads for critical dependencies | | |
| Graceful degradation path defined | | |
| Multi-AZ for stateful and stateless tiers | | |
| Backups, PITR, restore tested (date, duration) | | |
| DR plan with RPO/RTO and last drill | | |
| Capacity headroom and scaling triggers | | |
| Runbooks for top failure modes; on-call rotation | | |

## 6. Findings

| ID | Gap | Evidence | Severity | Remediation | Owner |
|---|---|---|---|---|---|
