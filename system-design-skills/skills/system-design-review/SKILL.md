---
name: system-design-review
description: Reviews an existing architecture, design proposal, implementation plan or codebase and produces an evidence-backed report of weaknesses - scalability bottlenecks, consistency risks, security problems, single points of failure, unsupported assumptions, missing operational controls and unjustified complexity - each with evidence, severity, impact and remediation. Use for "review this design/architecture/PR/repo", "what's wrong with this", pre-launch audits, design-doc critique. Use system-design to create a new design, and the specialist skills for deep fixes after findings are agreed.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# System design review

## Purpose and activation

Find what is likely to hurt this system in production and say precisely why, with proof
from the artifacts. The review is only as good as its evidence: unsupported opinions are
questions, not findings. Activate when someone hands over a design, diagram, ADR, plan,
repository or running-system description and wants a critique.

Do not use it to produce a new design (`system-design`). Pull in specialist skills only for
the lenses where the artifacts show a risk.

## Required inputs

The artifacts (design doc, diagrams, ADRs, code/IaC/config, metrics, incident history), the
stated requirements and SLOs (if missing, list the requirements you inferred and flag
them), scale and growth, and scope/time limits. State what you were not given.

## Workflow

1. **Scope and inventory**: list the artifacts reviewed and not reviewed; state the
   requirements being judged against (stated vs inferred).
2. **Reconstruct the real architecture**: from code and config where available (discovery
   hints below), not from the diagram alone. Draw it (Mermaid) and mark inferred parts.
3. **Trace critical paths**: pick the 2-4 most important user journeys and data flows;
   walk each hop for latency budget, failure behavior, state, and trust boundary.
4. **Apply the lenses** (table below): for each, look for evidence of the listed risks
   using the corresponding specialist skill's checklist. Do not duplicate those
   checklists here.
5. **Hunt the cross-cutting issues**: single points of failure, unsupported assumptions,
   unjustified components (every component must trace to a requirement), missing
   operational controls.
6. **Write findings** with the mandatory fields; classify by the rubric.
7. **Self-review** with the finding-quality checklist: delete or downgrade anything
   without evidence; check for duplicates and for generic advice.
8. **Prioritize**: order by severity, then by effort; separate "fix now", "plan", "watch".
9. **Deliver** using `../system-design/assets/templates/review-report.md`.

## Decision framework

### Lenses and where to look

| Lens | Typical evidence sources | Deep-dive skill |
|---|---|---|
| Requirements & capacity | Missing NFR numbers, no load estimate, no growth plan | `requirements-capacity` |
| Scaling & architecture style | Shared state in app tier, sync chains, premature microservices | `architecture-scaling` |
| API & networking | No timeouts, no idempotency, breaking changes, no pagination | `api-networking` |
| Security & identity | Authorization missing on routes, secrets in config, weak hashing | `identity-security` |
| Data model & store choice | Wrong store for the access pattern, missing indexes | `database-selection` |
| Consistency & concurrency | Read-modify-write without locks, replica reads gating writes | `transactions-consistency` |
| Sharding & replication | Sharding without capacity case, no failover plan, lag unmanaged | `sharding-replication` |
| Caching & performance | Cache as source of truth, no stampede protection, N+1 | `caching-performance` |
| Messaging | Dual writes, non-idempotent consumers, no DLQ, unbounded queues | `messaging-streaming` |
| Storage | Blobs in the DB, no multipart, no lifecycle, no restore test | `storage-systems` |
| Deployment | No rollback, destructive migrations, big-bang releases | `deployment-delivery` |
| Reliability | No timeouts/backoff, single zone, untested backups | `reliability-resilience` |
| Observability | No SLOs, symptom alerts missing, high-cardinality labels | `observability` |
| Domain: location | Unbounded geo queries, sharding by id | `geospatial-design` |
| Domain: payments | Retry as correctness, float money, no reconciliation | `payment-systems` |

### Severity rubric

Score impact (what breaks) and likelihood (how soon / how easily).

| Severity | Criteria | Examples |
|---|---|---|
| Critical | Probable or certain data loss, security breach, financial loss or outage of a core journey, with no effective mitigation | Missing authorization check exposing other tenants' data; double-charge path without idempotency; backups never restored and sole copy |
| High | Large impact that is plausible within months, or moderate impact that is certain | Single zone for a 99.99% target; unbounded retries with no budget; replica reads gating writes |
| Medium | Real risk with contained blast radius or an available workaround; or cost/complexity with measurable harm | Missing index on a growing table; no deploy rollback rehearsal |
| Low | Hygiene, clarity, minor risk | Inconsistent naming; missing runbook link |
| Question | Cannot judge without information; state what would settle it | "Is cross-region failover required?" |

Never inflate severity to get attention; never omit a Critical because it is awkward.

## Architecture and implementation guidance

### Discovering architecture from a codebase

Search (adapt to the stack) for: datastores and drivers (connection strings, ORMs),
queues/topics (producers and consumers), outbound HTTP/RPC clients and their timeout and
retry settings, authentication and authorization middleware and per-route checks, secrets
handling (env, config files, repo history), migrations (destructive operations, locks),
background jobs/schedulers, caches and TTLs, feature flags, health checks, deployment
manifests (replicas, resources, zones, autoscaling), IaC (network exposure, IAM),
logging/metrics/tracing setup, and tests around concurrency and failure.
Record `file:line` for each fact used as evidence.

### Finding format (mandatory fields)

```
ID: F-07
Title: Unbounded retries on payment provider calls
Severity: High        Confidence: high
Evidence: src/payments/client.py:88-104 retries on any exception, no max attempts,
          no backoff; callers at api/checkout.py:41 also retry 3x
Impact: During a provider brownout, each checkout generates up to 3 x unbounded calls,
        saturating workers and extending the outage; duplicate charges possible because
        no idempotency key is sent (client.py:92)
Remediation: Cap attempts (3), exponential backoff with jitter, retry at one layer only,
             send idempotency key, add circuit breaker; effort S-M
Verify: fault-injection test: provider returns 503 for 2 minutes; attempts per checkout
        <= 3; no duplicate charge
```

### Finding-quality checklist (run before delivering)

- [ ] Evidence is specific (path, line, config key, diagram element, quoted sentence)
- [ ] Impact is a concrete scenario, not "could be a problem"
- [ ] Remediation is actionable and proportional (smallest effective step first)
- [ ] Severity matches the rubric and the stated requirements
- [ ] Not generic advice; not a missing technology that no requirement demands
- [ ] Not a duplicate of another finding
- [ ] Assumptions are labelled; unknowns are questions
- [ ] Positive findings recorded so good decisions are not undone

### Anti-pattern catalogue (with detection hints)

| Anti-pattern | Detect by | Typical severity |
|---|---|---|
| Distributed monolith | Services deployed together, shared DB schema, long sync call chains | High |
| Shared database between services | Multiple services with write access to the same tables | High |
| Unbounded or layered retries | Retry loops without max/backoff; retries at client and server and gateway | High |
| Missing timeouts | Outbound calls using library defaults (often infinite or very long) | High |
| Cache as source of truth | Data written only to cache; no rebuild path | Critical-High |
| Dual write without outbox | Write DB then publish in separate steps | High |
| Chatty service calls / N+1 | Loops with per-item remote calls | Medium-High |
| Missing idempotency on retried writes | POST/consumer handlers with side effects and at-least-once delivery | High-Critical |
| Single AZ / single instance for critical tier | Manifests with replicas=1 or one zone | High |
| Backups never restored | No restore test evidence | High |
| Secrets in config or repo | Credentials in files, images, history | Critical-High |
| Missing authorization (object level) | Handlers that load by id without owner/tenant check | Critical |
| Destructive migration coupled to deploy | Drop/rename in the same release | High |
| No rollback path | Irreversible data or format change shipped with code | High |
| Over-sharding / premature microservices | Complexity without capacity or team evidence | Medium |
| Alert on causes, none on symptoms | CPU alerts, no SLO alerts | Medium |
| Float money | Binary floats for currency | High |
| Unbounded queues/memory | No limits on queue, cache, pool | Medium-High |
| Hot key / hot partition by design | Monotonic keys, single-tenant dominance | Medium-High |

### What the reviewer must not do

- Recommend a rewrite or a new technology without evidence tied to a requirement.
- Pad the report with generic best practices that the artifacts do not touch.
- Flag "missing Kubernetes/Kafka/microservices" as a defect; flag unmet requirements.
- Present opinions as findings or hide uncertainty behind confident language.
- Review code style; this is an architecture and risk review.

## Failure and edge cases

- Diagram and code disagree: the code wins; report the discrepancy itself as a finding.
- Missing requirements: state inferred ones; weight findings by them; ask for confirmation
  in the Questions section.
- Huge codebase: sample the critical paths, say what share was reviewed, avoid claiming
  completeness.
- Politically sensitive findings: stay factual; evidence and impact only.
- Reviewing without running the system: label conclusions "static review"; propose the
  test that would confirm.
- Findings that conflict between lenses (cache speed vs consistency): present the trade-off
  and recommend per requirement.

## Validation

- Another reader can locate each piece of evidence from your citation alone.
- Each Critical/High finding has a concrete verification step.
- Spot-check: re-derive two findings independently; if you cannot reproduce them, downgrade.
- Coverage table at the end of the report: lenses reviewed, depth (none/skim/deep).

## Expected output

A review report (`../system-design/assets/templates/review-report.md`): verdict,
reconstructed architecture diagram, findings (mandatory fields) ordered by severity,
questions, unjustified-complexity table, positives, and a prioritized remediation plan with
effort estimates and verification steps.

## Sources and confidence

- Book (direct): orchestration as single point of failure (printed p. 38-39), deployment strategy trade-offs (p. 30-31), password and HTTPS simplifications (p. 13-17) — verified against supplied text
- Book (synthesized): review lenses map to the other 16 skills; interview tip (p. 139) — TOC-anchored only
- Modern: severity rubric and anti-pattern catalogue are this library's synthesis — from author knowledge, VERIFY against your organization's risk framework
- Needs workload validation: severity thresholds should be calibrated to the system's SLOs and business impact
