# Production Readiness Checklist

Gate for first launch and for major changes. Each item needs a link or note as evidence.
Items marked **(blocker)** must be Y before go-live unless a risk acceptance is signed.

Service: ______  Owner: ______  Launch date: ______  Tier (criticality): ______

## Design and capacity

- [ ] Requirements and SLOs written and agreed **(blocker)**
- [ ] Capacity worksheet reviewed; load test hit 1.5× expected peak with p99 within target **(blocker)**
- [ ] Failure analysis done for every dependency; top risks mitigated
- [ ] Scaling triggers and limits (connections, quotas, rate limits of vendors) documented

## Deployment

- [ ] Automated build, test, deploy pipeline; same artifact promoted across environments **(blocker)**
- [ ] Strategy chosen (rolling/canary/blue-green) with automatic rollback criteria
- [ ] Schema changes are expand/contract; previous version works with new schema **(blocker)**
- [ ] Config and feature flags versioned; kill switch for risky features
- [ ] Rollback rehearsed in a non-production environment

## Data

- [ ] Backups automated, encrypted, and restored successfully in a drill (date: ____) **(blocker)**
- [ ] RPO/RTO stated and consistent with backup/replication design
- [ ] Retention and deletion policy implemented; PII mapped

## Reliability

- [ ] Timeouts, retries with backoff and jitter, idempotency for retried writes **(blocker)**
- [ ] Overload behavior defined (shed, queue bound, degrade)
- [ ] Redundancy across failure domains; failover tested

## Security

- [ ] Security architecture checklist passed or exceptions accepted **(blocker)**
- [ ] Secrets managed; least-privilege roles; dependencies scanned
- [ ] Rate limiting/abuse controls on public endpoints

## Observability and operations

- [ ] SLIs instrumented; dashboards exist; alerts tied to SLOs with runbooks **(blocker)**
- [ ] Logs structured with correlation ids; trace propagation works
- [ ] On-call rotation, escalation path, incident template ready
- [ ] Status communication plan (who tells customers)

## Launch plan

- [ ] Staged rollout (internal → 1% → 10% → 100%) with go/no-go criteria
- [ ] Dependencies notified of expected load
- [ ] Cost alarms set

## Sign-off

| Role | Name | Decision | Date |
|---|---|---|---|
| Service owner | | | |
| Security | | | |
| Operations / SRE | | | |
