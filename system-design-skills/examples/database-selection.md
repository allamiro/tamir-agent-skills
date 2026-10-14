# `database-selection`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Pick a database for an order system with 185 writes per second, multi-row transactions, ad hoc reports and three years of growth. Compare PostgreSQL, MongoDB and DynamoDB.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,650 | 3,476 |
| Input tokens read across all turns (including cached context) | 30,380 | 72,626 |
| Extra input tokens when the skill is installed | | +42,246 |
| Cost, US dollars at list price | 0.093 | 0.197 |
| Skills invoked in the sample run | none | `database-selection` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 230 tokens for its name and description, which are in every session where the skill is installed, and about 3,100 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Recommendation: PostgreSQL

**Use PostgreSQL on a managed service** (RDS, Aurora, Cloud SQL or Azure Flexible Server). It is the only one of the three that fully meets both hard requirements, multi-row transactions and ad hoc reports. 185 writes/s is a light load for a single PostgreSQL primary.

## Sizing (assumptions are marked; check them)

| Quantity | Calculation | Result |
|---|---|---|
| Writes per day | 185 × 86,400 | ~16 M |
| New rows over 3 years | assume 70% are inserts: 130/s × 94.6 M s | ~12 B rows |
| Storage over 3 years | assume ~1 KB per row including indexes | **~12 TB** if 185/s is the steady average; **~4 TB** if 185/s is the peak and the average is a third of that |
| Write load | a modest PostgreSQL node handles thousands of simple OLTP writes/s | **under 10% of one node's capacity** |

Writes are not your bottleneck. **Data volume and reporting over a growing history are.** That decides the design.

## Gate questions

| Gate | Requirement | PostgreSQL | MongoDB | DynamoDB |
|---|---|---|---|---|
| Multi-row atomic transactions | Order, order lines, inventory and payment written together | ✅ Native ACID, any number of rows and tables | ⚠️ Multi-document transactions work (replica sets since 4.0, sharded since 4.2), but cost more and have time limits (60 s by default). Embedding lines in the order document avoids most of them, but not for inventory | ⚠️ `TransactWriteItems`: up to 100 items and 4 MB, at 2× write cost. No interactive transactions (you can't read, decide, then write inside one) |
| Ad hoc reports | Questions you don't know yet | ✅ SQL, joins, window functions, CTEs | ⚠️ Aggregation pipeline and `$lookup` work, but joins are clumsy and slow at scale | ❌ **Fails.** Only key and index queries. Anything ad hoc needs Scan, or an export to S3 plus Athena or a warehouse |
| Constraints | No orphan lines, unique order numbers, no negative stock | ✅ FK, UNIQUE and CHECK enforced by the database | ⚠️ Unique indexes and schema validation, no FKs | ❌ Done in app code or with condition expressions |
| 185 writes/s | | ✅ Trivial | ✅ Trivial | ✅ Trivial |
| 3-year growth | 4–12 TB | ✅ With partitioning and archiving (see growth path) | ✅ Shards horizontally | ✅ No storage ceiling |
| Ops burden (managed) | | Low–medium | Low–medium (Atlas) | Lowest |
| Exit cost | | Low: standard SQL | Medium: its query language is proprietary | High: the data model is shaped for one vendor's API |

**Result:**
- **DynamoDB is eliminated** by the ad hoc reporting requirement. Its strengths (unlimited scale, no servers to run) solve a write volume you don't have.
- **MongoDB is viable but second-best.** It wins only if orders really are self-contained documents with highly variable shape. Order systems are relational: customers, products, inventory, payments, shipments. PostgreSQL's `jsonb` covers the variable fields anyway.

## Data model sketch (PostgreSQL)

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Recommendation: PostgreSQL

Your four requirements point to a relational database. Multi-row transactions and ad hoc reports are what PostgreSQL is built for. 185 writes per second is a small load for any of the three, so throughput doesn't decide this. Query flexibility and data growth do.

## Sizing check

- 185 writes/s ≈ **16M writes/day** ≈ **17.5B writes over 3 years**, if that rate is sustained around the clock.
- Many of those writes are probably updates (status changes, payments), not new rows. Assume about 30% are inserts of roughly 1 KB each, including indexes. That gives **~5–6 TB in 3 years**.
- A single PostgreSQL primary handles this well: one well-sized instance or managed service (RDS/Aurora, Cloud SQL, AlloyDB), with partitioning by month.
- Peak load needs checking too. If 185/s is the average and peaks run 5–10x higher, a single PostgreSQL primary still handles about 2,000 writes/s comfortably.

## Comparison

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
