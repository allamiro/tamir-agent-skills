---
name: database-selection
description: Selects and models a datastore from access patterns, data relationships, query and transaction needs, consistency, scale and operational cost - relational, document, key-value, wide-column, columnar/OLAP, time-series, search, graph, in-memory, ledger and blob. Use for "which database", "SQL vs NoSQL", comparing engines such as PostgreSQL, MySQL, MongoDB, DynamoDB, Cassandra, Redis or Elasticsearch, schema or data-model design, polyglot persistence, or migrating stores. Use transactions-consistency for isolation and concurrency, sharding-replication for scale-out, caching-performance for a cache layer, storage-systems for files/blobs.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Database selection and data modeling

## Purpose and activation

Pick the storage model that fits the *queries and guarantees the system needs*, at a
complexity the team can operate. A datastore is a long-term commitment: the decision is
expensive to reverse, so it is made from written access patterns, not popularity.

Activate when choosing a datastore, designing a schema, or judging a proposed one. Not for
isolation/concurrency details (`transactions-consistency`), partitioning (`sharding-replication`),
or object/file storage (`storage-systems`).

## Required inputs

The entities and their relationships; the **top 10 reads and writes** with frequency and
latency targets; consistency and transaction needs; data volume and growth
(`requirements-capacity`); retention; compliance; team skills; managed-service availability.

## Workflow

1. **Write the access patterns table first** (template: section 2 of
   `../system-design/assets/templates/database-design-review.md`): operation, frequency,
   latency, consistency need, query shape.
2. **Classify the data**: structured with relationships, semi-structured documents, simple
   lookups by key, event/time-ordered measurements, graph traversals, free-text search,
   analytical scans, large binary objects, immutable audit records.
3. **Apply the gate questions** in the decision framework. Eliminate models that fail a
   hard requirement (for example multi-row transactions, ad hoc joins).
4. **Start from the baseline**: a relational database, unless a stated requirement rules it
   out. Name the requirement and the number that rules it out.
5. **Compare 2-3 credible candidates** with
   `../system-design/assets/templates/technology-selection-matrix.md`; score with evidence;
   include operational burden and exit cost.
6. **Model the data** for the chosen store (rules per model in
   [references/models-and-examples.md](references/models-and-examples.md)).
7. **Plan the growth path** (indexes, replicas, partitioning triggers; see
   `sharding-replication`) and **polyglot cost**: each extra datastore needs sync,
   backup, monitoring, expertise, and a consistency story.
8. **Record an ADR** with the revisit trigger.

## Decision framework

### Gate questions (answer each with a requirement ID)

1. Do operations need multi-row/multi-entity atomic transactions or strong constraints?
   → relational (or a store with proven multi-document transactions).
2. Are queries ad hoc, joined, or likely to change? → relational (flexible queries).
3. Are access patterns few, known, and key-based at very high rate or volume? →
   key-value or wide-column may fit.
4. Is the data a hierarchy read as one unit with variable shape? → document.
5. Are relationship traversals of unknown depth the core query? → graph.
6. Is it append-mostly measurements indexed by time with retention/downsampling? →
   time-series.
7. Is the main operation scanning/aggregating many rows by few columns? → columnar/OLAP.
8. Is relevance-ranked text, faceting or fuzzy match needed? → search engine (as a
   derived index, rarely the source of truth).
9. Must latency be sub-millisecond with data fitting memory and loss tolerable or
   persistence configured? → in-memory store (usually as cache; see `caching-performance`).
10. Must records be tamper-evident and immutable? → ledger table design or ledger database.
11. Is it a large unstructured file? → object storage (`storage-systems`), with metadata
    in a database.

### Model comparison

| Model | Fits | Trade-offs and limits |
|---|---|---|
| Relational | Related entities, constraints, transactions, ad hoc queries | Scaling writes beyond one primary needs partitioning work; schema changes need migration discipline |
| Document | Self-contained aggregates, flexible fields | Cross-document joins/transactions weaker or costly; duplicated data drifts |
| Key-value | Lookups by key, sessions, counters | No secondary queries unless designed in; value-only model |
| Wide-column | Massive write volume, predictable key-range queries | Query-driven table design; limited ad hoc querying and joins |
| Columnar / OLAP | Analytics scans and aggregates | Poor for point updates; separate from transactional path (ETL/ELT) |
| Time-series | Metrics, IoT, sensor data | Cardinality explosion if tags are unbounded; delete/update semantics narrow |
| Search | Full text, ranking, facets | Eventually consistent derived index; reindex cost; not a system of record |
| Graph | Deep or variable relationship queries | Bulk analytics and sharding harder; smaller ecosystem |
| In-memory | Latency-critical small datasets | Memory cost; durability depends on configuration |
| Immutable ledger | Audit trails, financial history | Corrections by appending; storage growth |

Rule of thumb, stated as a default, not a law: **choose a relational database unless a
requirement you can quote rules it out.** Mainstream relational systems handle JSON
columns, full-text search, and moderate scale; adopting a second store should clear a
higher bar than "might be faster".

### Polyglot persistence check

Before adding a store: What is the source of truth? How does the copy get updated (CDC,
outbox, dual write)? What is the maximum staleness? What happens when the copy is lost or
wrong - can it be rebuilt? Who is on call for it?

## Architecture and implementation guidance

- Access patterns drive indexes: each hot query has an index that supports its filter and
  sort order; verify with query plans, not intuition.
- Primary keys: choose stable, non-reusable ids. Sequential ids leak volume and serialize
  inserts at one index edge; random UUIDs fragment B-tree indexes; time-ordered ids (as
  the book's unique-ID requirements suggest - roughly sortable, 64-bit, scalable) balance
  both. Pick by insert rate and exposure.
- Constraints belong in the database (unique, foreign key, check) even if the app also
  validates; they are the last line against concurrent writers.
- Store money as integer minor units or exact decimals, never binary floating point.
- Time: store UTC instants; keep the user time zone separately when it matters.
- Soft delete vs hard delete decided against retention law and index bloat.
- Multi-tenant: tenant id in keys and indexes; enforce at the data layer.
- Plan schema evolution (expand/contract; see `deployment-delivery`).
- Managed vs self-hosted: managed services reduce operations burden; check backup/restore
  semantics, failover behavior and limits in the provider's documentation.

## Failure and edge cases

- Choosing a store for projected scale that never arrives: operational cost paid early.
- Choosing for flexibility, then re-creating joins and constraints in application code.
- Hot partitions in key-based stores from skewed keys (celebrity user, current timestamp).
- Unbounded growth: no retention plan for time-series/logs; indexes larger than memory.
- Dual writes between stores diverge on partial failure; use outbox/CDC and reconciliation.
- Search or cache treated as source of truth, then lost or stale.
- Migration lock-in: proprietary query language or data model with no export path.
- Large rows/blobs in the database inflating backups and replication.

## Validation

- Run the top queries on a realistic dataset (volume, skew) and record p50/p99 and plan.
- Load test the top write pattern at 1.5× peak, including index maintenance.
- Backup, restore, and failover drill on the candidate; record time to recover.
- Exit test: export a table and re-import it elsewhere; estimate migration time.
- Falsifier: any gate question answered "yes" that the chosen model cannot satisfy.

## Expected output

Access-pattern table, gate-question answers, candidate comparison (matrix with evidence),
chosen model with data model sketch (tables/collections, keys, indexes), growth path with
triggers, polyglot justification if more than one store, ADR, and a
`database-design-review.md`. Worked comparison:
[references/models-and-examples.md](references/models-and-examples.md).

## Sources and confidence

- Book (direct): database categories list - relational, columnar, key-value, in-memory, wide column, time series, immutable ledger, geospatial, graph, document, text search, blob (printed p. 20-21); ID requirements (p. 22-23) — verified against supplied text
- Book (synthesized): metrics database choice (p. 126-128, 133) — TOC-anchored only
- Modern: none beyond author knowledge of mainstream engines — from author knowledge, VERIFY vendor-specific limits before quoting
- Needs workload validation: query latencies, index sizes, write rates, growth
