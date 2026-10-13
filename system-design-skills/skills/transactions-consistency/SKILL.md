---
name: transactions-consistency
description: Analyzes and designs transaction isolation, concurrency control, optimistic vs pessimistic locking, consistency models, replication lag, read-after-write guarantees, atomicity and distributed correctness (sagas, outbox, two-phase commit limits) with engine-specific behavior for PostgreSQL and MySQL InnoDB. Use for race conditions, double spends, overselling, lost updates, write skew, stale reads from replicas, "which isolation level", or multi-service consistency. Use sharding-replication for replica topology, messaging-streaming for delivery semantics, payment-systems for money flows.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Transactions, concurrency and consistency

## Purpose and activation

Make concurrent and distributed operations *correct*: find which anomaly can corrupt
which invariant, then choose the cheapest mechanism that prevents it, and prove it with a
test. Activate when two actors can touch the same data, when reads come from replicas,
or when one business operation spans several stores or services.

## Required inputs

The invariants that must never break ("stock >= 0", "one active subscription per user",
"balance never negative"); the code path or SQL that reads then writes; database engine and
version, current isolation level and where reads go (primary or replica); whether the
operation spans services. Missing: assume PostgreSQL-like behavior and say so.

## Workflow

1. **List invariants** and, for each, the operations that can violate it.
2. **Trace the concurrent interleavings**: for each pair of operations touching the same
   data, write the read/write sequence and look for the anomalies in the table below.
3. **Choose the mechanism** per invariant using the decision framework: constraint, atomic
   statement, optimistic version check, row lock, higher isolation with retry, or
   a distributed pattern.
4. **Decide read consistency per read**: which reads must see own writes, which tolerate lag
   (state a staleness bound), which must be linearizable.
5. **For cross-service work**: pick saga, outbox, or avoid distribution by moving data
   ownership; never rely on distributed atomic commit across heterogeneous systems unless a
   transaction coordinator is proven in your stack.
6. **Define retry behavior**: serialization failures and deadlocks are expected; retry the
   whole transaction, bounded, with jitter, and keep operations idempotent.
7. **Write the concurrency test** for each invariant (see Validation).

## Decision framework

### Anomalies (what can go wrong)

| Anomaly | Meaning | Example |
|---|---|---|
| Dirty read | Read another transaction's uncommitted data | Report shows an order later rolled back |
| Non-repeatable read | Same row read twice, different value | Balance changes mid-transaction |
| Phantom | Same predicate query returns different row set | Count of reservations changes |
| Lost update | Two read-modify-write cycles overwrite each other | Two clerks both set stock = 9 from 10 |
| Write skew | Two transactions each read overlapping data and write disjoint rows, breaking a joint invariant | Two doctors both go off-call, leaving none |

### Isolation levels by engine (verified against vendor docs, fetched 2026-10-14)

The book (printed p. 4-5) lists the four standard names and says serializable means
transactions behave as if executed in sequence. Names are standard; guarantees differ by
engine. Check your engine and version.

| Level | PostgreSQL (docs, v18) | MySQL InnoDB (8.4 manual) |
|---|---|---|
| Read Uncommitted | Behaves as Read Committed; dirty reads never occur | Dirty reads possible |
| Read Committed | No dirty read; non-repeatable reads, phantoms and serialization anomalies possible; each statement sees a fresh snapshot | Each consistent read uses its own snapshot; no gap locks (phantoms possible) |
| Repeatable Read | Snapshot isolation: no phantoms (stronger than the standard), but serialization anomalies such as write skew possible; concurrent update of the same row aborts with `could not serialize access due to concurrent update` and must be retried | **Default.** Snapshot from the first read; locking reads and updates use next-key/gap locks depending on the index and condition; mixing locking and non-locking reads in one transaction sees different states |
| Serializable | Serializable Snapshot Isolation; may abort with SQLSTATE 40001 ("serialization failure"); application must retry | Plain `SELECT` becomes `SELECT ... FOR SHARE` when autocommit is off; more blocking |

Consequence: "set it to Serializable" is a valid strategy only if every transaction can be
retried safely and the throughput cost is acceptable; "it's ACID" does not tell you which
anomalies exist. MVCC snapshots (the book's p. 5 example) explain why readers do not block
writers; they do not by themselves prevent lost update or write skew.

### Mechanism selection

| Situation | Prefer | Why / caveat |
|---|---|---|
| Invariant expressible as a constraint (unique, check, FK) | Database constraint | Enforced regardless of isolation level; handle violation errors |
| Single counter/stock change | One atomic statement: `UPDATE ... SET qty = qty - n WHERE id = ? AND qty >= n`; check rows affected | No read-modify-write gap |
| Read-modify-write of an entity edited by humans or low contention | Optimistic locking: `version` column, `UPDATE ... WHERE id=? AND version=?`; zero rows → conflict, reload and retry | No lock held across think time; retries under contention |
| High contention on few rows, short critical section | Pessimistic: `SELECT ... FOR UPDATE` in a short transaction, consistent lock order | Deadlocks possible; lock duration kills throughput |
| Joint invariants over multiple rows (write skew) | Serializable with retry, or lock a parent row, or materialize the conflict (a row both transactions must update) | Test it; do not assume |
| Uniqueness across partitions | Single owner of the key space, or unique index per partition on a routing key | Cross-shard uniqueness is not free |
| Several services must agree | Saga with compensation, outbox for reliable events | Eventual consistency; compensations must be idempotent and may themselves fail |

### Consistency models for reads

| Model | Guarantee | Typical use / cost |
|---|---|---|
| Linearizable | Behaves like one copy; reads see the latest completed write | Locks, leader elections, balances; needs quorum/leader reads, higher latency |
| Read-your-writes | A client sees its own writes | Profile edits; route to primary or use session/LSN tokens |
| Monotonic reads | Never see older data after newer | Avoid time going backward across replicas; pin session to a replica |
| Causal | Effects follow causes | Comment threads; vector/version metadata |
| Eventual | Replicas converge if writes stop; **no stated time bound** | Feeds, counters; define the acceptable lag in seconds and alert on it |

The book (p. 65-67, TOC-anchored) frames a latency-vs-consistency trade-off: stronger
guarantees cost round trips; choose per read path, not globally.

## Architecture and implementation guidance

- **Keep transactions short** and free of network calls to other systems; a slow external
  call inside a transaction holds locks and connections.
- **Replica reads**: asynchronous replication lags. After a write, route that user's next
  reads to the primary for a window (or wait for the replica to reach the write's log
  position). Never use a lagging replica for a check that gates a write.
- **Optimistic version example**:
  `UPDATE doc SET body=:b, version=version+1 WHERE id=:id AND version=:v` and treat
  0 rows as conflict returned to the caller (HTTP 409 / ETag precondition 412).
- **Outbox**: write the business row and an outbox row in one local transaction; a relay
  publishes outbox rows and marks them sent; consumers deduplicate (`messaging-streaming`).
  This closes the dual-write gap (DB committed, message lost, or the reverse).
- **Saga**: sequence of local transactions with compensating actions; define each step's
  state, timeout, compensation, and what the user sees while pending. Orchestrated or
  choreographed (`architecture-scaling`).
- **Two-phase commit** blocks on coordinator failure and ties availability to the slowest
  participant; avoid across independent services; acceptable inside one database engine.
- **Idempotency keys** protect retried requests; a unique constraint on (key) makes the
  second attempt a no-op.
- Deadlocks: acquire locks in a consistent order; retry the transaction on deadlock error.
- Details, SQL patterns, and a concurrency test harness sketch:
  [references/concurrency-patterns.md](references/concurrency-patterns.md).

## Failure and edge cases

- Crash between commit and acknowledgement: client retries; the operation must be
  idempotent or detectable (the client cannot know whether it committed).
- Failover with async replication loses acknowledged writes beyond the replica's log
  position (RPO > 0); synchronous or quorum replication trades latency for lower loss.
- Split brain: two nodes accept writes; requires fencing/leader leases.
- Clock-based ordering across machines is unsafe without bounded-skew guarantees; prefer
  logical versions.
- Long transactions pin old row versions (table bloat) and increase conflict aborts.
- Retry storms on serialization failure under contention; cap retries, add jitter.
- Cache invalidation races: a stale value written back after an invalidation (see
  `caching-performance`).
- "Exactly once" claims: delivery semantics do not imply that the business effect happened
  once (see `messaging-streaming`).

## Validation

- For each invariant write a test that runs the competing operations concurrently
  (threads/processes, barrier to start together, N iterations) against a real instance of
  the same engine and isolation level; assert the invariant at the end. A test that
  passes with one thread proves nothing.
- Deliberately weaken (lower isolation, remove the constraint) and confirm the test fails:
  a test that cannot fail does not protect you.
- Inject: kill the app between commit and response; delay replicas; force deadlocks.
- Metrics: serialization-failure rate, deadlock count, replica lag, lock wait time,
  retry counts.
- Falsifier: invariant violation count > 0 in the concurrent test or in production audit queries.

## Expected output

Per-invariant table (invariant, violating interleaving, anomaly, mechanism, isolation and
retry policy, test), read-consistency table per read path with staleness bound, distributed
pattern selection (saga/outbox) with sequence diagram if multi-service, and tests to add.

## Sources and confidence

- Book (direct): isolation level names, MVCC and Repeatable Read read-view example (printed p. 4-5) — verified against supplied text
- Book (synthesized): optimistic locking (p. 65), latency vs consistency (p. 67), read replicas (p. 103-106) — TOC-anchored only
- Modern: PostgreSQL 18 "Transaction Isolation" documentation — fetched 2026-10-14; MySQL 8.4 manual "Transaction Isolation Levels" — fetched 2026-10-14; consistency-model definitions and saga/outbox patterns — from author knowledge, VERIFY
- Needs workload validation: contention level, retry rate, acceptable staleness bounds
