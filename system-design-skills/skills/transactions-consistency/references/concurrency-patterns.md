# Concurrency patterns, SQL sketches and a test harness

SQL is illustrative and PostgreSQL-flavored. Check syntax and semantics on your engine.

## 1. Atomic conditional update (inventory)

```sql
UPDATE stock SET qty = qty - :n WHERE sku = :sku AND qty >= :n;
-- rows affected = 1 → reserved; 0 → insufficient stock (do not retry blindly)
```

Why it works: the check and decrement happen in one statement under the row lock. The broken
variant reads qty in application code, checks, then writes - two buyers both pass the check.

## 2. Optimistic locking

```sql
UPDATE profile
   SET display_name = :name, version = version + 1
 WHERE id = :id AND version = :seen_version;
-- 0 rows → someone else changed it: return 409/412, client reloads and reapplies
```

Exposure to clients: return the version as an `ETag`; require `If-Match` on updates.
Use when conflicts are rare. When conflicts are frequent, retries waste work: switch to a
queue per key (serialize on the key) or a pessimistic lock.

## 3. Pessimistic lock

```sql
BEGIN;
SELECT balance FROM account WHERE id = :id FOR UPDATE;  -- lock order: lowest id first
UPDATE account SET balance = balance - :amt WHERE id = :id;
COMMIT;
```

For two accounts always lock in a fixed order (for example ascending id) to prevent deadlock.
Keep the transaction to a few statements; no network calls inside.

## 4. Write skew and a fix

Invariant: at least one doctor on call. Two transactions each check "count >= 2" then
remove themselves; under snapshot isolation both succeed.
Fixes, cheapest first:

1. Lock a shared parent row (for example the shift row) with `FOR UPDATE` in both transactions.
2. Materialize the conflict: both update a `shift.on_call_count` row (their writes now conflict).
3. Run those transactions as Serializable and retry on 40001 (PostgreSQL) - verify behavior
   for your engine.

## 5. Retry wrapper (pseudo-code)

```
for attempt in 1..max_attempts:
    try:
        return run_transaction()
    except SerializationFailure or Deadlock:
        sleep(random(0, base * 2**attempt))   # jittered backoff
raise
```

The unit retried is the *whole* transaction including reads. The function must not have
external side effects, or those must be idempotent.

## 6. Outbox

```sql
BEGIN;
INSERT INTO orders ...;
INSERT INTO outbox(id, topic, payload, created_at) VALUES (:uuid, 'order.created', :json, now());
COMMIT;
-- relay: SELECT ... FROM outbox WHERE sent_at IS NULL ORDER BY id LIMIT 100 FOR UPDATE SKIP LOCKED;
-- publish; UPDATE outbox SET sent_at = now() WHERE id IN (...)
```

Relay can publish twice (crash after publish, before mark): consumers must dedupe on `id`.

## 7. Saga skeleton (order → payment → shipment)

| Step | Local transaction | Compensation | On timeout |
|---|---|---|---|
| 1 | Create order (PENDING) | Cancel order | Cancel after T |
| 2 | Reserve stock | Release stock | Release |
| 3 | Authorize payment | Void authorization | Query provider, then void |
| 4 | Create shipment | Cancel shipment | Alert operator |

Each step records state; a recovery job resumes or compensates sagas stuck beyond a
timeout. Compensations are idempotent and may need manual escalation when they fail.

## 8. Read-your-writes with replicas (options)

1. Route the session's reads to the primary for N seconds after a write.
2. Record the write's log position/version; read from a replica only when it has reached it.
3. Read the specific entity from the primary after the write, others from replicas.

Measure replica lag and alert when it exceeds the staleness bound.

## 9. Concurrency test harness (sketch)

```python
# Stock must never go negative when 50 workers each try to buy 1 of 10 units.
import threading
def worker(barrier, results):
    barrier.wait()                       # start at the same moment
    results.append(try_purchase(sku="A1", qty=1))   # calls the real code path
barrier = threading.Barrier(50); results = []
ts = [threading.Thread(target=worker, args=(barrier, results)) for _ in range(50)]
[t.start() for t in ts]; [t.join() for t in ts]
assert sum(r.ok for r in results) == 10 and stock_qty("A1") == 0
```

Run it against the same engine/isolation level as production, repeat many times, and also
run a mutated version of the code (remove the `qty >= n` condition) to see the test fail.

## 10. Consistency review prompts

- Where can two requests for the same user/entity run at once?
- Is there any read followed by a dependent write outside a single statement or lock?
- Does any decision use data from a replica, a cache, or a search index?
- What is the maximum acceptable staleness for each, and how is it monitored?
- If the process dies after step N of M, what does the data look like and who repairs it?
