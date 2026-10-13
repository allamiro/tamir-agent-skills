# Database Design Review

Use when choosing or reviewing a schema/datastore. Fill every table; a blank cell is a
finding. Examples are illustrative.

## 1. Scope

Datastore(s) and version: ______  Owner: ______  Review date: ______

## 2. Access patterns (write these first; the schema serves them)

| # | Operation | Frequency (peak/s) | Latency target | Consistency need | Query shape | Index that serves it |
|---|---|---|---|---|---|---|
| A1 | Fetch order by id | 2,000 | p99 20 ms | read-your-writes | PK lookup | PK |
| A2 | List a user's last 20 orders | 500 | p99 50 ms | may lag 5 s | user_id, created_at desc | (user_id, created_at desc) |
| A3 | Decrement stock | 150 | p99 30 ms | no oversell | UPDATE ... WHERE qty >= n | PK |

## 3. Model

| Entity | Key | Cardinality now / in 3 years | Relationships | Mutable? | Retention / archival |
|---|---|---|---|---|---|

Checks: normalization level chosen on purpose; denormalized copies list their refresh
mechanism; no unbounded arrays or rows; ids are not guessable if exposed (authorization is
still required); money in integer minor units; timestamps in UTC with a time-zone policy.

## 4. Integrity and concurrency

| Invariant | Enforced by (constraint, transaction, app code) | Concurrent-writer scenario | Isolation / locking used | Tested? |
|---|---|---|---|---|
| Stock never negative | CHECK + conditional UPDATE | two buyers, last unit | single atomic statement | yes |

## 5. Performance and capacity

Rows × row size = ______; index size = ______; working set vs memory = ______;
write amplification and hot rows = ______; the three slowest queries with plans (EXPLAIN)
attached = ______.

## 6. Scale path

Vertical headroom left: ______. Read replicas useful? Which reads tolerate lag? ______.
Sharding needed? Only with measured exhaustion of the above; shard key candidate and its
skew risk = ______.

## 7. Operations

Backup type and frequency, last restore test date and duration, PITR window, replication
lag alert, migration process (expand/contract), connection pool limits, failover test date.

## 8. Security

Encryption at rest/in transit, least-privilege roles, row/tenant isolation mechanism, PII
columns and masking, audit logging, secrets rotation.

## 9. Verdict

Blocking issues / should-fix / accepted risks, each with owner and date.
