---
name: reliability-resilience
description: Designs for failure - failure domains, redundancy, availability math, timeouts and deadline propagation, retries with exponential backoff and jitter, retry budgets, circuit breakers, bulkheads, load shedding, graceful degradation, high availability, backup and disaster recovery (RPO/RTO), chaos testing and incident handling. Use for "make this highly available", "what happens when X fails", cascading failures, retry storms, DR plans, 99.9%/99.99% targets. Use deployment-delivery for release safety, observability for detection, sharding-replication for data-tier failover, system-design-review to audit an existing system.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Reliability and resilience

## Purpose and activation

Meet the availability and recovery targets by analyzing how the system fails and
choosing the *cheapest* mechanisms that contain each failure. Activate for availability
targets, dependency risk, incident follow-ups, DR planning, and any design where one
component's failure could take down others.

Reliability work is bounded by requirements: a 99.9% target does not justify multi-region
active-active. Spend complexity only where the failure analysis shows a requirement is
not met.

## Required inputs

Availability/latency SLOs and their business cost of violation, RPO/RTO, topology
(components, dependencies, state), traffic profile, current incident history, team
on-call capacity. Missing: use `requirements-capacity` to set the downtime budget.

## Workflow

1. **Set targets** (SLO, RPO, RTO) and convert to a downtime budget.
2. **Map failure domains**: process, host, rack, availability zone, region, shared
   dependency (DNS, identity, database, deploy system), human/config error.
3. **Run the failure-mode analysis** for every component and arrow: down, slow, wrong,
   duplicated, overloaded (`../system-design/assets/templates/failure-analysis.md`).
4. **Compute availability** from the dependency graph (serial/parallel) and compare with
   the target; locate the weakest link.
5. **Choose mechanisms** from the pattern table to close each gap; note which failure
   each pattern does *not* cover.
6. **Define overload behavior**: what is shed, what degrades, what is protected.
7. **Plan backup and DR** to RPO/RTO with a tested restore.
8. **Test**: failure injection, load test beyond limits, DR drill.
9. **Operationalize**: alerts, runbooks, on-call, post-incident review loop
   (`observability`).

## Decision framework

### Availability math (computed; assumptions stated)

- Serial dependencies (all needed): A = a₁ × a₂ × … Example: three 99.9% components in
  series give 0.999³ = 0.997003 (about 99.70%).
- Redundant parallel (any one suffices, failures independent): A = 1 − (1 − a)ⁿ. Two 99.9%
  replicas → 1 − 0.001² = 0.999999 (99.9999%) *in theory*.
- Independence is rarely true: shared deployments, configuration, bugs, and regions
  correlate failures. Treat parallel results as upper bounds and list the shared
  dependencies that cap them (the load balancer, the database, the deploy pipeline).
- A dependency with availability below your target must be made optional (degrade) or
  buffered (queue, cache), or the target is unreachable.

### Pattern selection

| Pattern | Protects against | Does NOT protect against | Cost / risk |
|---|---|---|---|
| Redundant instances across zones | Host/zone loss | Bugs, bad config, data corruption | Capacity N+1 or N+2 |
| Health checks + auto-replace | Crashed/wedged instances | Correlated failures; flapping | False positives remove capacity |
| Timeout | Hung dependencies | Slow but responding dependencies at scale | Too low → false failures |
| Retry with exponential backoff + jitter | Transient errors | Overload (adds load), permanent errors, non-idempotent operations | Retry amplification across layers |
| Retry budget / token bucket | Retry storms | Genuine capacity shortage | Complexity |
| Circuit breaker | Repeated calls to a failing dependency | Failures it cannot detect (wrong data) | Tuning; half-open probing |
| Bulkhead (isolated pools/queues) | One workload exhausting shared resources | Failure of the shared substrate | Lower utilization |
| Load shedding / rate limiting | Overload, resource exhaustion | Capacity planning gaps | Rejects some users deliberately |
| Graceful degradation | Optional dependency failure | Failure of the core path | Degraded modes rarely exercised: test them |
| Backpressure (bounded queues) | Unbounded memory growth, cascading delay | - | Upstream must handle rejection |
| Replication / multi-AZ data | Node/zone loss | Logical corruption, bad deletes | Lag, failover loss window |
| Backups + PITR | Corruption, deletion, ransomware | Time to restore (RTO) | Restore must be tested |
| Multi-region | Region loss | Global bugs; adds consistency complexity | Highest cost |

### DR tiers

| Tier | Idea | Typical RTO / RPO | Cost |
|---|---|---|---|
| Backup & restore | Rebuild from backups in another place | Hours-days / backup interval | Lowest |
| Pilot light | Minimal core running, scale up on failure | Hours / replication lag | Low |
| Warm standby | Scaled-down full copy running | Minutes-hours / replication lag | Medium |
| Active-active | Multiple regions serve traffic | Seconds-minutes / near zero with conflict handling | Highest |

Choose by RTO/RPO and business cost, then verify by drill. RPO/RTO values are targets
you must demonstrate, not properties of a tier name.

## Architecture and implementation guidance

### Timeouts and deadlines

Every remote call has a timeout; choose from the callee's latency percentile (for
example its p99.9) plus margin rather than defaults (AWS Builders' Library, read
2026-10-14). Propagate an absolute deadline down the call tree; callees skip work that
cannot finish in time and cancel downstream work (Google SRE book, read 2026-10-14).

### Retries

- Retry only idempotent operations (or those with idempotency keys); do not retry
  permanent errors.
- Exponential backoff with a cap, **plus jitter** so clients do not retry in lockstep.
- Limit attempts per request and add a client-side retry budget (for example a token
  bucket) so retries stay a small fraction of traffic.
- **Retry at one layer only.** Three retries at each of five layers can multiply load on a
  failing dependency (Builders' Library); the SRE book likewise names retry amplification
  as a cause of cascading failure.

```
delay = random(0, min(cap, base * 2^attempt))      # "full jitter"
```

### Overload and cascading failure (Google SRE book chapter, read 2026-10-14)

Cascades start with server overload or resource exhaustion and feed on themselves.
Controls: reject excess requests early and cheaply (503), bound queues relative to
worker capacity, prefer serving fresh requests over doomed old ones (LIFO/CoDel-style
queueing), degrade by doing less work, and load-test beyond limits including recovery
behavior. Health checks that remove overloaded servers can shift their load onto others
and worsen the cascade; use capacity-aware routing and slow-start.

### Circuit breaker

States: closed (calls pass) → open (fail fast after N failures in a window) → half-open
(allow few probes) → closed. Define what the fallback returns (cache, default, error) and
who is told (metric, alert).

### Graceful degradation

Classify features: critical path vs optional. For each optional dependency define the
degraded behavior (hide recommendations, serve stale cache, queue for later). Exercise
degraded modes in game days.

### Backup, restore and DR

Back up with PITR; keep copies in another failure domain and account; encrypt; restore to
a clean environment regularly and measure the time. Document DR runbooks with owners,
decision criteria for declaring a disaster, DNS/traffic switch steps, data reconciliation
after failback. Replicas are not backups.

### Game days and chaos

Start small: kill an instance, then a zone, then add latency or errors to a dependency;
define hypothesis, abort conditions and success criteria; fix findings before widening.

### Incident basics

Detect (symptom alerts) → triage and communicate → mitigate first (rollback, shed load,
fail over) → restore → blameless review with action items tracked to completion. The book
(printed p. 49-50) discusses handling a large-scale outage (TOC-anchored only).

## Failure and edge cases

- Retry storm after a brief outage, extending it.
- Cascading failure: one slow dependency fills thread pools of all callers.
- Thundering herd on recovery (cold caches, all clients reconnecting): use jitter,
  warm-up, rate-limited recovery.
- Split brain and double leaders after partitions.
- Failure detectors wrong (false positives drain capacity; false negatives route to dead nodes).
- Correlated failure: same bad config pushed to all zones; shared certificate expiry;
  clock issues.
- Recovery path depends on the failed system (secrets, container registry, DNS, identity).
- Backups present but unrestorable; restore slower than RTO.
- Degraded mode itself is broken because it was never exercised.
- Queues hiding failure until they overflow.

## Validation

- Failure-injection tests mapped to the failure-mode table: for each row, a test and an
  expected user-visible result.
- Load test to 2× peak and beyond; observe shedding, latency and recovery after load drops.
- DR drill with a stopwatch: measure actual RTO and data loss (RPO) versus targets.
- Verify retry behavior: capture attempts per request under dependency failure; total
  attempts must stay within the retry budget.
- Metrics: error budget burn, saturation, breaker state, shed count, retry rate,
  backup age, last restore date.
- Falsifier: measured availability under injected failure below SLO, or a drill missing
  RTO/RPO.

## Expected output

Targets and downtime budget; failure-domain map; completed failure-mode matrix; availability
calculation with correlated-failure caveats; pattern choices with the failure each does not
cover; overload and degradation design; backup/DR plan with drill schedule; runbook list;
ADRs for expensive choices (multi-region, active-active).

## Sources and confidence

- Book (direct): reading list naming "Timeouts, retries, and backoff with jitter", "Beyond five 9s", "Challenges with distributed systems", "Amazon's approach to high-availability deployment" (printed p. 33-34, titles only) — verified against supplied text; microservice orchestration as a single point of failure (p. 38-39) — verified
- Book (synthesized): large-scale outage handling (p. 49-50), read replica pattern (p. 103-106) — TOC-anchored only
- Modern: Google SRE book "Addressing Cascading Failures" — fetched 2026-10-14; AWS Builders' Library "Timeouts, retries, and backoff with jitter" — fetched 2026-10-14; circuit breaker and bulkhead patterns, DR tier names — from author knowledge, VERIFY
- Needs workload validation: timeouts, breaker thresholds, retry budgets, RPO/RTO feasibility
