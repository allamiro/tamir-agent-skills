---
name: observability
description: Designs monitoring and observability - metrics, logs, traces, pull vs push collection, service discovery, time-series storage and cardinality, dashboards (golden signals, RED, USE), alerting, SLIs, SLOs, error budgets and burn-rate alerts, capacity monitoring, and triage of a high-CPU/memory/IO process. Use for "what should we monitor", "set SLOs", "alert design", "metrics system design", "too many alerts", cardinality or retention problems, debugging production slowness. Use reliability-resilience for failure handling and deployment-delivery for rollout guardrails.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Observability

## Purpose and activation

Make the system's behavior visible enough to detect user-impacting problems quickly,
diagnose them, and plan capacity, at a cost you can afford. Activate when designing the
monitoring for a service, designing a metrics platform itself, defining SLOs, or fixing
noisy/missing alerts. Tools named here (Prometheus, Grafana, OpenTelemetry, and so on) are
examples; no skill step requires a particular product.

## Required inputs

Critical user journeys, availability and latency expectations, architecture and
dependencies, deployment platform, expected metric volume (hosts, services, labels),
retention needs, who is on call, existing tools and budget.

## Workflow

1. **Define user journeys and SLIs**: for each critical journey choose measurable
   indicators of good service (success ratio, latency under a threshold, freshness,
   correctness) measured as close to the user as practical.
2. **Set SLOs and error budgets**: target and window; compute the budget with
   `python3 scripts/slo_budget.py --help`.
3. **Choose signals**: metrics for trends and alerts, logs for events and detail, traces
   for latency attribution across services. Instrument the golden signals per service
   and per dependency.
4. **Choose collection**: pull vs push, service discovery, agents/collectors.
5. **Choose storage**: time-series database sizing from series count and retention;
   cardinality control; downsampling.
6. **Design alerting**: symptom-based alerts on SLO burn; cause-based alerts only for
   imminent saturation; each alert with an owner, severity and runbook.
7. **Design dashboards**: overview per service, dependency health, capacity, deploy
   markers; make them answer "is it broken, where, since when".
8. **Plan capacity monitoring**: saturation metrics, growth trends, forecast and review.
9. **Validate**: test that alerts fire (inject faults), that dashboards load under
   incident, and review pages per week.
10. Fill `../system-design/assets/templates/observability-reliability-review.md`.

## Decision framework

### Signals

| Signal | Best for | Cost driver | Caveat |
|---|---|---|---|
| Metrics | Alerts, trends, capacity, SLOs | Series count (cardinality) | Aggregates; no per-request detail |
| Logs | Discrete events, debugging, audit | Volume and retention | Unstructured text is expensive to query; PII risk |
| Traces | Latency breakdown across services, dependency maps | Sampling and storage | Needs context propagation everywhere |
| Profiles | CPU/memory hotspots | Overhead | Continuous profiling optional |

### Pull vs push

| | Pull (monitoring system scrapes endpoints) | Push (producers send) |
|---|---|---|
| Discovery | Needs service discovery; monitoring knows what *should* exist and can see "target down" | Producers need the destination address |
| Health signal | Failed scrape is itself a signal | Silence is ambiguous (down or idle?) |
| Short-lived jobs | Hard (may finish before scrape) - use a push gateway/intermediary | Natural |
| Network | Scraper must reach targets (firewalls, NAT) | Targets only need outbound access |
| Control | Central control of rate and targets | Producers can overload the collector; needs back-pressure |

Common outcome: pull for long-running services, push (via gateway or collector) for batch
jobs, edge devices and serverless. Prometheus describes itself as pull-based over HTTP,
with discovery and a push gateway for short-lived jobs (docs read 2026-10-14). The book
covers pull vs push at printed p. 117 (TOC-anchored only).

### Alert type

| Alert on | Example | Page? |
|---|---|---|
| Symptom: SLO burn | 14.4× burn over 1 h (and 5 min) | Yes |
| Symptom: user-visible failure from synthetic probe | Checkout probe fails 3 times | Yes |
| Imminent saturation | Disk full in < 4 h at current growth | Page if irreversible soon, else ticket |
| Cause metrics (CPU 90%) | Host CPU high | Usually no: dashboard only |
| Slow burn | 1× burn over 3 days | Ticket |

## Architecture and implementation guidance

### SLOs and error budgets

- SLI = good events ÷ valid events. SLO = target for the SLI over a window. Error budget =
  1 − SLO.
- Budgets (30 days = 43,200 min): 99.9% → 43.2 min; 99.95% → 21.6 min; 99.99% → 4.32 min.
  For request-based SLIs this is a time-equivalent, not literal downtime.
- Burn rate = observed error ratio ÷ (1 − SLO); 1 means the budget lasts exactly the window.
- Budget policy: when exhausted, freeze risky releases and prioritize reliability work.

### Multi-window, multi-burn-rate alerts (Google SRE Workbook, read 2026-10-14)

For a 99.9% SLO over 30 days the Workbook recommends:

| Severity | Long window | Short window | Burn rate | Budget consumed |
|---|---|---|---|---|
| Page | 1 h | 5 min | 14.4 | 2% |
| Page | 6 h | 30 min | 6 | 5% |
| Ticket | 3 d | 6 h | 1 | 10% |

Both windows must exceed the threshold; the short window makes the alert reset quickly
after the problem ends (suggested ratio: short ≈ 1/12 of long). Verify with
`python3 scripts/slo_budget.py --slo 99.9 --burn-rate 14.4 --alert-window-hours 1`
(prints 2.00% consumed).

### Cardinality (time-series cost)

Number of series for a metric = product of the distinct values of each label. Labels like
`user_id`, `request_id`, raw URL with ids, or container id churn produce unbounded series.
Rules: keep label values bounded and low-cardinality (route template, status class,
region); put high-cardinality identifiers in logs/traces; set per-metric series budgets and
alert on growth. Worked example and sizing:
[references/observability-design.md](references/observability-design.md).

### Metrics platform sizing (when you build one)

Ingest rate = active series ÷ scrape interval (samples/s). Storage ≈ samples/s × seconds of
retention × bytes per sample (compressed; measure for your engine). Plan downsampling
tiers (raw short, rollups long) and a federation/sharding path by team or region.
The book's metrics-system design (printed p. 126-130, TOC-anchored) is the structural
reference: collectors, a time-series store, query, alerting and visualization.

### Dashboards

Per service: traffic, errors, latency percentiles (not averages), saturation - the four
golden signals; for request services RED (rate, errors, duration); for resources USE
(utilization, saturation, errors). Add deploy/change markers and dependency panels.

### Logs and traces

Structured (JSON) logs with timestamp, level, service, version, trace/correlation id,
and no secrets or raw PII. Sampling for traces: head-based (cheap, may miss rare errors)
vs tail-based (keeps slow/error traces, needs buffering). Propagate trace context across
all hops including queues.

### Capacity monitoring

Track saturation (CPU run queue, memory, disk fill rate, IOPS, connections, queue depth,
consumer lag, thread pools) and growth; forecast time-to-limit; alert on forecast
exhaustion; review monthly against the capacity worksheet (`requirements-capacity`).

### Process-level diagnosis (host triage)

When a process uses too much CPU, memory or IO: confirm with system-wide views first (CPU
vs run queue, memory/swap, IO wait, network), then per-process views, then profile or trace
(flame graph, system-call tracing, heap analysis). Tool names are OS-specific examples.
Record findings in the incident. (The book discusses this at printed p. 70, TOC-anchored.)

## Failure and edge cases

- Monitoring itself fails: it must be more reliable than the systems it watches; add a
  dead-man's-switch alert and monitor the monitor from outside.
- Alert fatigue: many pages that need no action; remove or demote.
- Cardinality explosion from a deploy that adds a label; ingestion throttled or billing spike.
- Clock skew corrupting time series and traces.
- Missing data treated as healthy; ensure "no data" alerts for critical signals.
- Sampling hides rare failures; averages hide tails.
- Logs leaking secrets/PII; unbounded log volume during an incident.
- Dashboards slow during the incident that most needs them.
- Metrics accuracy: monitoring systems are not for billing-grade counts (Prometheus docs
  state this for per-request billing).

## Validation

- Fault injection: raise the error rate and confirm the expected alert fires in the
  expected time; stop a target and confirm "target down" and "no data" behavior.
- Replay a past incident: would current signals have detected it, and how fast?
- `python3 scripts/slo_budget.py --selftest` verifies the budget math.
- Review: pages per week, percent actionable, time to detect, time to acknowledge.
- Series count and ingestion rate versus limits; query latency of key dashboards.
- Falsifier: a user-visible outage with no page, or a page with no action.

## Expected output

SLI/SLO table with budgets; signal inventory; collection design (pull/push/discovery);
storage sizing with cardinality plan; alert table (condition, window, severity, runbook);
dashboard list; capacity monitors; completed observability-reliability review template.

## Sources and confidence

- Book (direct): none verified in the supplied text (diagnosing a high-CPU process p. 70; pull vs push p. 117-118; metrics database and monitoring/alerting system p. 124-130) — TOC-anchored only
- Book (synthesized): signal/alert design combines the above with the Builders' Library items named on p. 33
- Modern: Google SRE Workbook "Alerting on SLOs" burn-rate table — fetched 2026-10-14; Prometheus overview (pull model, discovery, push gateway, accuracy caveat) — fetched 2026-10-14; golden signals / RED / USE definitions — from author knowledge, VERIFY
- Needs workload validation: thresholds, series counts, retention, sampling rates
