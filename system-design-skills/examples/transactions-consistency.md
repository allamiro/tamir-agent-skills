# `transactions-consistency`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Two customers can buy the last item at the same moment and we oversell. Which isolation level or locking should we use, and how do we test that it works?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,543 | 2,398 |
| Input tokens read across all turns (including cached context) | 40,554 | 73,348 |
| Extra input tokens when the skill is installed | | +32,794 |
| Cost, US dollars at list price | 0.113 | 0.181 |
| Skills invoked in the sample run | none | `transactions-consistency` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 210 tokens for its name and description, which are in every session where the skill is installed, and about 3,800 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
You don't need a stricter isolation level for this. Make the stock check and the decrement **one atomic conditional UPDATE**, and back it with a CHECK constraint. That works correctly at the default Read Committed level in both PostgreSQL and MySQL. You didn't say which database you use, so I've assumed PostgreSQL and noted where MySQL InnoDB differs.

## Why it oversells

The usual code reads the stock and then writes it, with a gap in between:

```
T1: SELECT qty FROM stock WHERE sku='X'   → 1
T2: SELECT qty FROM stock WHERE sku='X'   → 1
T1: UPDATE stock SET qty = 0 ...; INSERT order ...   ✓
T2: UPDATE stock SET qty = 0 ...; INSERT order ...   ✓   ← oversold
```

Both transactions decide based on a value that is already out of date. This is called a *lost update*. Read Committed allows it, and so does MySQL's default Repeatable Read for plain reads.

## The fix, best option first

**1. Atomic conditional decrement (recommended)**

```sql
-- invariant enforced by the DB no matter what code runs
ALTER TABLE stock ADD CONSTRAINT stock_nonneg CHECK (qty >= 0);

BEGIN;
UPDATE stock SET qty = qty - :n
 WHERE sku = :sku AND qty >= :n;
-- rows affected = 0  → ROLLBACK, return "sold out"
INSERT INTO orders (...) VALUES (...);
COMMIT;
```

There's no gap between reading and writing. The second UPDATE waits on the row lock taken by the first. Once the first commits, the second re-checks `qty >= :n` against the new value and matches 0 rows. Always check the affected-row count. The CHECK constraint catches any code path that skips this pattern.

**2. `SELECT ... FOR UPDATE`**, if you need to run logic between reading and writing (for example per-customer limits or bundles):

```sql
BEGIN;
SELECT qty FROM stock WHERE sku = :sku FOR UPDATE;  -- second buyer blocks here
-- if qty < n → ROLLBACK
UPDATE stock SET qty = qty - :n WHERE sku = :sku;
INSERT INTO orders ...;
COMMIT;
```

Keep this transaction short. Never call a payment provider or any other network service while holding the lock. If one order can contain several SKUs, lock them in a fixed order (sorted by SKU) to avoid deadlocks, and retry when a deadlock happens.

**3. Serializable isolation**: this also works. In PostgreSQL, one of the two transactions fails with SQLSTATE `40001`, and you must retry the whole transaction, with a cap on retries and some random delay between them. It's more expensive and only safe if every transaction can be retried. In MySQL, Serializable mostly adds blocking. Use it when the rule spans several rows, such as "total reserved across warehouses ≤ capacity". For a single stock counter, option 1 is simpler.

**Not enough on its own:** "it's ACID", PostgreSQL's Repeatable Read without retry handling (it aborts the second updater and you have to catch that), or checking stock against a read replica or cache. A replica can be behind, so it must never decide whether a write goes ahead.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
The cause is almost certainly a check-then-act race. Two requests both read `stock = 1`, both pass the "in stock?" check, and both write. Raising the isolation level is usually not the best fix. Make the decrement itself conditional and atomic instead.

## Fix: conditional atomic update (recommended)

```sql
UPDATE inventory
SET    qty = qty - 1
WHERE  product_id = $1 AND qty >= 1;
-- rows affected = 1 → you got it; 0 → sold out
```

Do this in the same transaction as the order insert. If no row was updated, roll back and show "sold out." This works at the default READ COMMITTED level in both Postgres and MySQL. The `UPDATE` takes a row lock, so the second transaction waits for the first. It then re-checks `qty >= 1` against the committed value and matches 0 rows. There's nothing to retry, no deadlock between the two buyers, and the lock is held only briefly.

Also add a database-level backstop so a code path you missed can't oversell:

```sql
ALTER TABLE inventory ADD CONSTRAINT qty_nonneg CHECK (qty >= 0);
```

## Alternatives, and when to use them

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
