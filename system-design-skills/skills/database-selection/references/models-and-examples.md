# Data models per store type and a worked comparison

## 1. Modeling rules by store type

### Relational

- Normalize to the point where each fact is stored once; denormalize deliberately for a
  measured read path and document how copies are refreshed.
- One table per entity; junction tables for many-to-many; foreign keys with indexes on the
  referencing column.
- Index for the access-pattern list: composite index column order = equality filters first,
  then range/sort column. Partial indexes for sparse conditions.
- Keep hot and cold data apart if rows are wide (separate large text/JSON into a side table).

### Document

- Embed what is read together and changes together; reference what is shared or unbounded.
- Cap array sizes; an unbounded embedded list becomes a hot, ever-growing document.
- Plan for the cross-document invariant (uniqueness, balance) - use a store feature or a
  single-document design that makes the invariant local.

### Key-value / wide-column

- Design the key from the query. Partition key chooses the machine; clustering/sort key
  chooses order within it. A key that concentrates traffic (a date, a single tenant) is a
  hot partition.
- One table per query shape is normal; denormalized writes replace joins.
- Secondary indexes, if offered, have their own consistency and cost; check the vendor docs.

### Time-series

- Series identity = metric name + label set. Number of series = product of distinct label
  values. High-cardinality labels (user id, request id) multiply cost; keep them out of labels.
- Define retention tiers and downsampling up front (raw 7-30 days, rollups for longer).

### Search

- Treat as a derived index fed from the source of truth through an outbox/CDC pipeline;
  design full reindex from source; expect seconds of lag.

### Graph

- Model entities as nodes and relationships as typed edges; verify the traversal depth and
  fan-out against supernodes (accounts with millions of edges).

### Ledger / append-only

- Entries are immutable; corrections are new reversing entries; balances are derived or
  cached with reconciliation (see `payment-systems`).

## 2. Worked comparison (illustrative): order management for a mid-size shop

Requirements: 185 peak writes/s, 3.5k reads/s, 13 TB over 3 years including replicas, order
placement must decrement stock atomically, customers list their orders, support runs ad hoc
reports. Team of 6, one on-call rotation, no prior experience with distributed databases.

Access patterns (excerpt):

| # | Operation | Rate | Needs |
|---|---|---|---|
| A1 | Place order (insert order + lines, decrement stock) | 150/s | atomic multi-row transaction, no oversell |
| A2 | Get order by id | 2,000/s | PK lookup |
| A3 | List a customer's orders | 500/s | index on (customer, created_at desc) |
| A4 | Support report: orders by SKU and date range | rare, ad hoc | joins and aggregates |

Candidates and fit:

| Criterion | Relational (PostgreSQL-like) | Document store | Wide-column store |
|---|---|---|---|
| A1 atomic multi-row | Native transaction | Needs multi-document transactions or a single-document design that mixes stock with orders (bad) | Not natively; needs application-level protocol |
| A3 index | Secondary index | Secondary index | Separate table per query |
| A4 ad hoc | SQL | Aggregation pipeline, less flexible | Not suited |
| Ops burden for this team | Low (managed offering, known) | Medium | High |
| Write ceiling | Single primary handles this rate comfortably if measured | Higher | Highest |
| Verdict | Choose | Reject: A1/A4 cost | Reject: no need for its ceiling |

Why the rejected options lose is stated in numbers: required write rate (185/s) is far
below the designed ceiling of the specialist options, so their strength buys nothing,
while their weaker transactions and querying cost real functionality. The revisit trigger
is recorded: primary CPU sustained above 60% after index/query tuning, or storage above 70%
of provisioned volume. (These numbers are an example of the form of a trigger, not
recommendations.)

## 3. Migration and exit-cost checklist

- [ ] Data export in an open format exists and was tested
- [ ] Query language/features used are portable or isolated behind a repository layer
- [ ] Dual-run plan (shadow reads/writes) possible
- [ ] Backup and restore tested on current volume; time recorded
- [ ] Cutover rollback defined
