---
name: sharding-replication
description: Designs data partitioning (vertical and horizontal sharding, range, hash, consistent hashing, lookup tables), primary-replica replication, read replicas, request routing, hotspot prevention, replication lag handling, failover, recovery and rebalancing - and requires proof of capacity exhaustion before recommending sharding. Use for "do we need to shard", "pick a shard key", "add read replicas", "failover plan", "resharding", "split brain". Use transactions-consistency for read-after-write semantics, database-selection for store choice, reliability-resilience for DR strategy.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Sharding and replication

## Purpose and activation

Decide whether to replicate, partition, both, or neither - and make the failure behavior
explicit. Sharding is the most expensive scaling step for stateful data: it permanently
complicates queries, transactions, operations and rebalancing. **Do not recommend it
without a capacity justification.** Replication is cheaper but has its own correctness
issues (lag, failover loss).

Activate for read/write scaling of stateful stores, availability of the data tier, and
partition-key design. Not for store choice (`database-selection`) or cache design
(`caching-performance`).

## Required inputs

Measured or projected peak read QPS, write QPS, data size and growth, working-set size vs
memory, current primary utilization (CPU, IO, connections, replication lag), query shapes
(single-key, range, cross-entity), availability and recovery targets (RPO/RTO). Missing
numbers: get them from `requirements-capacity`; if still unknown mark `UNMEASURED` and
recommend the non-sharded path.

## Workflow

1. **Identify the limit being hit**: write throughput, storage size, read throughput,
   working set larger than memory, availability, or operational (backup/restore/migration
   time). Different limits have different cures.
2. **Run the exhaustion checklist** (below). Sharding is justified only when the single
   limit remains after the cheaper rungs.
3. **Choose replication first** if the limit is reads or availability: topology, sync mode,
   lag tolerance per read path (`transactions-consistency`).
4. **If partitioning is justified**: choose functional (vertical) split first when
   domains are independent; horizontal sharding only for one large, homogeneous table set.
5. **Select the shard key** using the evaluation table; prove distribution and query
   locality with real data.
6. **Design routing**: where the shard map lives, how clients/proxies find the shard,
   how the map changes.
7. **Design failover**: detection, promotion, fencing, client redirection, data-loss window,
   rehearsal.
8. **Plan rebalancing/resharding** before the first shard exists.
9. **Write the ADR** with measured triggers and the exit path.

## Decision framework

### Exhaustion checklist (all should be "done or ruled out" before horizontal sharding)

| Rung | Evidence required |
|---|---|
| Indexes and query plans reviewed | Top 10 queries by total time have good plans |
| Schema/data hygiene: archival, partition tables, TTL deletion | Hot data fits memory; old data off the primary |
| Connection pooling | Connections not the limiter |
| Caching of hot reads | Hit ratio measured; backing-store load acceptable |
| Read replicas | Reads offloaded where lag is tolerable |
| Vertical scale | Largest practical instance size evaluated; cost compared |
| Batching/async writes | Write amplification reduced; queue for spiky writes |
| Functional split (separate databases per domain) | Independent domains moved apart |

Triggers are ratios against *your measured* ceilings (for example "sustained write
IO > 70% of the volume's provisioned limit at peak after tuning"), not universal numbers.

### Replication topologies

| Mode | Guarantee | Cost / risk |
|---|---|---|
| Asynchronous primary→replicas | Primary commits without waiting; replicas lag | Failover can lose the last acknowledged writes (RPO > 0); stale reads |
| Semi-synchronous / quorum | Commit waits for at least one/majority replica | Higher write latency; availability depends on replicas; RPO near 0 |
| Multi-primary / multi-region active-active | Local writes everywhere | Conflict resolution required; usually the hardest option |

Read replicas help read-heavy workloads only; they do not raise write capacity and
multiply storage. Each replica adds a lag signal to monitor.

### Partitioning strategies

| Strategy | How | Good for | Problems |
|---|---|---|---|
| Vertical (functional) | Split tables/columns by domain or hot/cold | Independent domains; wide rows | Cross-domain joins/transactions break |
| Range | Contiguous key ranges per shard | Range scans, time data | Hotspots (all new writes to last range); needs splitting |
| Hash (modulo) | hash(key) mod N | Even distribution | Changing N moves most keys |
| Consistent hashing / hash slots | Keys map to a ring or fixed slot count; shards own slots | Adding shards moves a small fraction | Virtual nodes, skew from hot keys remain |
| Directory / lookup | Table maps key → shard | Flexible placement, tenant moves | Directory is a critical, cached dependency |
| Geographic | Region decides shard | Data residency, latency | Cross-region users, uneven regions |

### Shard key evaluation

| Criterion | Question | Pass condition |
|---|---|---|
| Cardinality | Enough distinct values? | Many more distinct keys than shards |
| Distribution | Is load even (by request, not by row count)? | Top key below a stated percent of traffic |
| Locality | Do the common queries hit one shard? | Top queries single-shard; cross-shard ones rare and tolerable |
| Immutability | Does the key change? | Never or rarely (moves are expensive) |
| Growth | Does one entity outgrow a shard? | Largest tenant/entity fits comfortably |
| Monotonic | Does the key increase over time? | Avoid for range partitioning of writes |

Typical candidates: tenant id, user id, composite (tenant, hash). Bad: timestamp, country
alone, status.

## Architecture and implementation guidance

- **Routing**: a shard map (service or config) maps key → shard; clients cache it with
  versioning; a routing proxy hides it from callers. Map changes are staged: dual-read,
  then switch.
- **Cross-shard operations**: avoid by design; otherwise scatter-gather for reads (latency
  = slowest shard) and sagas (`transactions-consistency`) for writes. Global uniqueness
  and global secondary indexes need their own service or derived index.
- **IDs**: generate globally unique ids that do not depend on one counter (time-ordered
  ids as in the book's unique-ID requirements, p. 22-23); embedding shard id in the key
  enables routing.
- **Hotspots**: salting a hot key, splitting a hot tenant onto a dedicated shard, adding
  a cache in front, or write-buffering counters. Detect with per-shard metrics.
- **Failover (primary-replica)**:
  1. Detect failure with multiple signals and a timeout longer than transient blips.
  2. Pick the most up-to-date replica (highest replicated position).
  3. **Fence** the old primary (block writes/kill network access) before promoting, to
     prevent split brain.
  4. Promote, repoint clients (DNS with short TTL, proxy, or service discovery).
  5. Rebuild the old primary as a replica after discarding or reconciling divergent writes.
  Record the data-loss window for the topology used; test with a game day.
- **Rebalancing**: use many more logical partitions than machines (fixed slots) so moving a
  partition is a copy, not a re-hash. Throttle moves; verify checksums; keep double-write
  or change capture until cutover; keep the ability to roll back.
- **Backup is not replication**: replicas copy mistakes (a bad `DELETE`, corruption) within
  seconds. Keep independent backups with point-in-time recovery and test restores
  (`reliability-resilience`).
- Details, a sizing worked example and a failover runbook skeleton:
  [references/sharding-worksheets.md](references/sharding-worksheets.md).

## Failure and edge cases

- Replica lag causing stale reads or lost uniqueness checks; replica promoted behind.
- Split brain after network partition; fencing absent.
- Hot shard from celebrity entity or sequential keys.
- Resharding under load; double-write divergence; partial migration leaving orphan data.
- Cross-shard transaction failing midway.
- Shard map cache stale after a move: requests hit the wrong shard (return redirect or retry via router).
- Schema migrations across N shards partially applied.
- Large shard backup/restore times exceeding RTO.
- Uneven shard growth leading to one shard out of capacity first.

## Validation

- Show the capacity argument: measured ceiling, projected growth, date or load at which the
  current design fails, and which exhaustion rungs were applied.
- Load-test with a production-like key distribution; plot per-shard load (max/avg ratio).
- Failover drill: kill the primary under write load; measure detection time, promotion
  time, writes lost, client error rate, and recovery to full redundancy.
- Resharding rehearsal on a copy; verify row counts and checksums.
- Falsifier: after the proposed change, the original bottleneck metric is still above its
  threshold, or the max/avg shard load ratio is high enough to erase the gain.

## Expected output

Capacity justification (limit, evidence, rungs tried), replication/partitioning design with
Mermaid diagram, shard key evaluation, routing design, failover runbook, rebalancing plan,
monitoring list (replication lag, per-shard load, failover events), and an ADR.

## Sources and confidence

- Book (direct): none verified in the supplied text (vertical vs horizontal partitioning p. 82-83; read replica pattern p. 103-106) — TOC-anchored only
- Book (synthesized): exhaustion-first approach combines scaling (p. 55-57) and partitioning topics
- Modern: replication and failover semantics are engine-specific — from author knowledge, VERIFY against your database's documentation
- Needs workload validation: every threshold, replica lag tolerance, shard count, key distribution
