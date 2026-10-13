# Distributed Systems Failure Analysis

Use at workflow step 8 and when reviewing a design. Walk every dependency and every arrow
in the architecture diagram. "Handled by retry" is not an answer until you have said what
state the retry leaves behind.

## 1. Inventory

| ID | Component or dependency | Type (own service, datastore, queue, third party, network, config) | State held | Criticality |
|---|---|---|---|---|

## 2. Failure-mode matrix (one row per dependency × failure)

Failure kinds to test for each: **down**, **slow** (latency spike, partial brownout),
**wrong** (corrupt or stale data), **duplicated** (message or request delivered twice),
**reordered**, **partitioned** (A can reach B but not C), **overloaded**.

| ID | Dependency | Failure kind | Trigger | User-visible effect | Detection (metric/alert) | Automatic mitigation | Data left in what state? | Recovery action | RPO / RTO | Residual risk |
|---|---|---|---|---|---|---|---|---|---|---|
| FM-1 | Payment provider API | slow (30 s) | provider incident | checkout spinner | p99 provider latency, open-circuit count | 3 s timeout, circuit breaker, order set to PENDING | order PENDING, charge outcome UNKNOWN | reconcile via provider query job | n/a / 15 min | customer sees pending for up to 15 min |
| FM-2 | Queue consumer | duplicated message | at-least-once redelivery | none if idempotent | duplicate-detected counter | idempotency key check | single effect applied | none | 0 / 0 | key store loss |

## 3. Cross-cutting questions

- Retries: who retries, how many layers multiply (3 layers × 3 tries = 27 attempts), is there
  a retry budget, backoff with jitter, and are retried operations idempotent?
- Timeouts: does every network call have one, and does the caller's timeout exceed the
  sum of its callees' (deadline propagation)?
- Overload: what is shed first, and is there a queue bound? What happens at 2× peak?
- Partial failure: after a crash between step N and N+1 of a multi-step operation, what
  does the data look like and who fixes it (outbox, saga compensation, reconciliation)?
- Concurrency: two writers on the same record, a stale read driving a write, clock skew.
- Failover: what is lost in the failover window, can two nodes both think they are primary
  (fencing), is the failover tested?
- Dependency of the recovery path: do restores/deploys need the failed system itself?

## 4. Scenario drills to schedule

| Drill | Hypothesis | Pass criteria | Date |
|---|---|---|---|

## 5. Findings

| ID | Gap | Evidence | Severity | Remediation |
|---|---|---|---|---|
