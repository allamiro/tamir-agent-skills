# Evaluation scenarios

Each scenario gives the prompt, the skills that should activate, the reasoning an expert
answer must contain, evidence of quality (checkable in the output), and common failure
conditions. Grade by reading the agent's final output against these lists. Run every
scenario with and without the library installed to see what the skills add.

Status of this suite: scenarios are authored. The description-routing smoke test
(`scripts/check_routing.py`) was executed. **Behavioral runs of the scenarios with a live
agent have not been executed.** Record results in `evals/results-template.md`.

## Scenario A: high-traffic e-commerce platform

**Prompt**: "Design the backend for an online store. 3 million monthly active users, a
flash sale every Friday that spikes traffic about 10x for 30 minutes, thousands of SKUs
with limited stock. We have 8 engineers and run on a major cloud."

**Expected activation**: `system-design` (coordinator) → `requirements-capacity`,
`architecture-scaling`, `database-selection`, `transactions-consistency`,
`caching-performance`, `reliability-resilience`; `payment-systems` and `identity-security`
for checkout and accounts; `messaging-streaming` for order fulfilment events.
Not expected: `geospatial-design`, `storage-systems` beyond product images, full `sharding-replication`.

**Required reasoning**

- Converts MAU to DAU and peak QPS with stated assumptions; models the flash-sale spike
  separately (10x of what baseline), including write rate on hot SKUs.
- Baseline: modular monolith or few services, one relational database, CDN for static
  content, cache for product reads. States the number at which the baseline fails.
- Identifies scaling bottleneck candidates (database writes on inventory rows, checkout
  path, payment provider rate limits) before adding components.
- Inventory concurrency: atomic conditional decrement or reservation with expiry; no
  read-modify-write in application code; explains oversell risk and the test.
- Flash sale handling: queueing/waiting room or rate limiting, load shedding, precomputed
  cached catalog, idempotent order placement.
- Payment as a separate state machine with idempotency (not "retry until success").
- Failure analysis: payment timeout with unknown outcome, duplicate submit, cache loss at
  peak (backing store survives h = 0 or sheds), provider outage.
- Operations: SLOs for browse and checkout, rollout strategy for sale-day code freeze.

**Evidence of quality**: a capacity table with units; a Mermaid diagram; an ADR or
alternatives table showing why sharding/microservices/Kafka were rejected or deferred; a
named concurrency mechanism for inventory; a validation plan with a load test at 1.5x
the spike.

**Common failures**: jumps to microservices+Kafka+Kubernetes without numbers; ignores the
spike; uses a cache as the inventory source of truth; says "use eventual consistency"
for stock; retries payments without keys; omits the cache-failure case.

## Scenario B: distributed metrics platform

**Prompt**: "Design an internal metrics platform for 20,000 hosts and 400 services:
ingest, store, query dashboards, and alert. Metrics at 15-second resolution, keep 13
months."

**Expected activation**: `system-design` → `requirements-capacity`, `observability`,
`database-selection` (time-series), `messaging-streaming` (ingestion buffering),
`sharding-replication`, `storage-systems` (long-term/downsampled data),
`reliability-resilience` (monitoring the monitor).
Not expected: `payment-systems`, `geospatial-design`.

**Required reasoning**

- Estimates active series and samples/s from hosts x metrics x labels; shows the
  cardinality formula and warns about unbounded labels; sets a series budget per team.
- Pull vs push with trade-offs; service discovery for pull; gateway/collector for
  short-lived jobs.
- Ingestion path with buffering, backpressure and per-tenant limits; write-ahead durability.
- Storage tiers: raw short retention, downsampled rollups for 13 months, compression;
  uses measured bytes per sample, not a guess.
- Query path: caching, limits on expensive queries; sharding by tenant/metric hash with
  the failover story.
- Alerting: evaluation engine HA, deduplication, routing; SLO burn-rate alerts; dead-man's
  switch; the monitor must be more reliable than the monitored.
- Retention vs cost; delete/compaction; multi-region if needed.

**Evidence of quality**: a worked cardinality example; storage sizing arithmetic; a
retention/downsampling table; the alert design includes windows and burn rates; a
failure table including ingestion overload and storage node loss.

**Common failures**: treats metrics like logs; no cardinality control; picks a
transactional database for time series without justification; alerts on causes (CPU) only;
no plan for monitoring the monitoring system; ignores query-time cost.

## Scenario C: real-time collaborative editor

**Prompt**: "Design a collaborative document editor: up to 50 people editing the same
document, edits visible in under a second, offline edits sync when reconnecting, full
version history."

**Expected activation**: `system-design` → `requirements-capacity`, `api-networking`
(WebSocket, connection management), `transactions-consistency` (conflict resolution,
ordering), `database-selection`, `messaging-streaming` (operation log), `storage-systems`
(snapshots/attachments), `reliability-resilience`, `identity-security` (sharing, permissions).
Not expected: `payment-systems`, `geospatial-design`.

**Required reasoning**

- Chooses a convergence approach (operational transformation, CRDT, or differential
  synchronization) with the trade-off stated (central server ordering vs merge
  complexity vs metadata growth) and a justification for the team's size.
- Document as an append-only operation log plus periodic snapshots; per-document
  ordering by routing a document to one sequencer/owner; scaling by document sharding.
- Presence and cursors separate from durable edits (ephemeral).
- Disconnection: client buffers operations, reconnect with last known revision, rebase or
  merge; conflict handling for long offline periods; idempotent operation ids.
- Persistence: ack after durable append; recovery by replaying log from snapshot.
- WebSocket scaling: sticky routing to the document owner, reconnect storms, load balancer
  timeouts.
- Permissions checked per operation; audit/version history; limits on document and
  operation size.

**Evidence of quality**: sequence diagram of two concurrent edits and a reconnect; a
statement of what happens to the same character edited by two people; snapshot/compaction
policy; a test plan with simulated latency/reorder/disconnect and convergence assertion.

**Common failures**: last-write-wins on the whole document; no ordering story; ignoring
offline; storing only the latest text; one global lock; claiming CRDT/OT is trivial.

## Scenario D: secure multi-tenant application

**Prompt**: "Design the architecture for a B2B SaaS where each customer company has
many users, some customers need single sign-on with their own identity provider, and a
customer's data must never be visible to another customer. Provide a public API."

**Expected activation**: `system-design` → `identity-security` (primary),
`api-networking`, `database-selection`, `transactions-consistency` (tenant-scoped
uniqueness), `observability` (audit), `reliability-resilience`, `deployment-delivery`
(tenant-aware migrations).
Not expected: `geospatial-design`, `payment-systems` (unless billing is asked).

**Required reasoning**

- Identity boundaries: tenant → organization → user; federation via OpenID Connect/SAML
  per tenant; authentication separate from authorization.
- Authorization model (RBAC/ABAC/ReBAC) with object-level and tenant checks enforced in
  the data layer; default deny.
- Tenant isolation choice (shared tables with enforced tenant filter / schema / database)
  justified against sensitivity, tenant count and noisy neighbors; cross-tenant tests.
- API security: tokens with audience/scope, short lifetimes, rate limits per tenant,
  idempotency, input validation, no IDOR; API keys hashed at rest if used.
- Data protection: encryption in transit (TLS 1.3 preferred) and at rest, per-tenant keys
  if required, secrets management, backups per tenant restore.
- Auditability: append-only audit log of security events and admin/support access.
- Threat model (STRIDE) on the trust boundaries; support impersonation controls.
- Password handling if local accounts exist: Argon2id, MFA.

**Evidence of quality**: tenant isolation diagram; a table of threats with mitigations;
authorization enforcement point described; at least one automated cross-tenant test;
audit log schema; mentions of rate limiting and abuse.

**Common failures**: role check without tenant check; tenant id taken from the request;
JWT claims trusted blindly; shared admin database credentials; no audit; fast-hash
password storage; HMAC without replay protection.

## Scenario E: architecture review

**Prompt**: "Review this architecture and tell me what's wrong." with the sample in
`evals/fixtures/sample-architecture.md`.

**Expected activation**: `system-design-review` (primary); may consult
`reliability-resilience`, `messaging-streaming`, `transactions-consistency`,
`identity-security`, `caching-performance`, `observability`, `deployment-delivery`.
Not expected: `system-design` creating a new design from scratch.

**Required reasoning (planted issues in the fixture)**

1. Shared database between "microservices" (distributed monolith).
2. Order service writes DB then publishes to the queue (dual write, no outbox).
3. Consumer is not idempotent but the queue is at-least-once.
4. Redis is the only copy of cart data (cache as source of truth).
5. No timeouts and unbounded retries on the payment provider call.
6. Single availability zone; one database instance; backups never restored.
7. Admin endpoints check login but not role; secrets in a config file in the repo.
8. Kafka and Kubernetes for a workload of 50 requests per second (unjustified complexity).
9. No SLOs; only CPU alerts.
10. Destructive migration coupled with the deploy; no rollback path.
11. Passwords stored as a fast hash with one constant salt kept in config.

**Evidence of quality**: every finding has ID, evidence (quote or file reference from the
fixture), severity per the rubric, impact scenario and a concrete remediation; unsupported
claims are labelled questions; unjustified complexity is tied to missing requirements;
positives are listed; the prioritized plan orders Critical/High first.

**Common failures**: generic advice not tied to the fixture; missing severities;
recommending a rewrite; flagging absent technology as a defect; fewer than 7 of the 11
planted issues found; inventing details not in the fixture.

## Negative tests (skills that must NOT activate)

| ID | Prompt | Must not activate | Why |
|---|---|---|---|
| N1 | "Fix this off-by-one error in my Python loop." | Any system-design skill | Code bug, no architecture question |
| N2 | "Write a CSS grid layout for a pricing page." | Any system-design skill | UI styling |
| N3 | "What does the HTTP 404 status code mean?" | `system-design`, `reliability-resilience` | Trivial fact; at most `api-networking` |
| N4 | "Should I add an index to this slow query?" | `system-design`, `sharding-replication`, `messaging-streaming` | Narrow DB tuning; at most `database-selection`/`caching-performance` |
| N5 | "How should I hash passwords?" | `system-design`, `payment-systems`, `geospatial-design` | Specialist question: `identity-security` only |
| N6 | "Design a nearby-driver search." | `payment-systems`, `identity-security` as primary | Specialist: `geospatial-design` (+ `system-design` optional for full design) |
| N7 | "Summarize this meeting transcript." | Any | Not engineering design |
| N8 | "Choose a color palette for our brand." | Any | Not engineering design |

Also verify: for a full design request, the coordinator loads only the specialists its
decision table triggers (Scenario D does not load `geospatial-design`; Scenario B does not
load `payment-systems`). Count activated skills; more than 8 for a single scenario is a
red flag.

## Grading sheet (per scenario)

| Criterion | Pass? | Notes |
|---|---|---|
| Correct skills activated, none extra | | |
| Numbers with units and assumptions | | |
| Simplest baseline stated; additions justified | | |
| Required reasoning items (list above) covered | | |
| Failure modes and recovery explicit | | |
| Validation plan with falsifiable numbers | | |
| No invented facts/benchmarks | | |
