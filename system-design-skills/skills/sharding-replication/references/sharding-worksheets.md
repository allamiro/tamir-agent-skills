# Sharding and replication worksheets

Illustrative numbers only. Replace with measurements.

## 1. Do we need to shard? (worksheet)

| Item | Measured value | Ceiling | Utilization | Verdict |
|---|---|---|---|---|
| Peak write QPS on primary | 1,800/s | 2,400/s (load-tested) | 75% | tight |
| Primary write IO | 70% of volume limit | 100% | 70% | tight |
| Data size | 4 TB | 16 TB volume limit | 25% | fine |
| Working set vs RAM | 180 GB vs 256 GB | - | 70% | OK |
| Replica lag p99 | 0.4 s | 5 s tolerance | 8% | fine |
| Restore time | 3 h | 4 h RTO | 75% | tight |

Reading it: writes and IO are the limit, storage is not. Next: reduce write amplification
(drop unused indexes, batch), move the audit/event table to its own store (functional
split), then re-measure. If write utilization still exceeds the threshold at projected
12-month load (say ×2), horizontal sharding of the hot tables is justified. If instead the
data were 14 TB of 16 TB with comfortable writes, archival and partitioned tables come first.

Growth projection: utilization(t) = utilization(now) × growth^(t / period). Time to
ceiling = period × ln(1 / utilization) / ln(growth). Example: 75% now, ×1.5 per 6 months →
ln(1/0.75)/ln(1.5) = 0.71 periods ≈ 4.3 months. This is the deadline for the work.

## 2. Hash-slot sketch (fixed slots)

```
slot = hash(shard_key) mod 1024          # 1024 logical partitions
slot_map: slot → shard (stored in the directory service)
add a shard: reassign ~1024/(N+1) slots from existing shards, copy those slots, flip map
```

Moving one slot is a bounded copy; with plain `hash mod N` changing N would remap most keys.

## 3. Shard-key scorecard (template)

| Candidate | Cardinality | Load skew (top key % of traffic) | Single-shard % of top queries | Mutable? | Verdict |
|---|---|---|---|---|---|
| tenant_id | 20k | 8% | 95% | no | candidate; isolate the large tenant |
| user_id | 5M | 0.01% | 70% (orders by user ok; admin queries scatter) | no | good for user-centric access |
| created_at | - | 100% on newest shard | - | no | reject (write hotspot) |

## 4. Failover runbook skeleton

1. Alert fires: primary unreachable from ≥ 2 observers for T seconds.
2. Confirm: check from another vantage point; read replication positions.
3. Fence old primary (revoke its network/storage access or power it off).
4. Choose the replica with the highest applied position; record the gap (lost writes).
5. Promote; verify it accepts writes and is not read-only.
6. Repoint traffic (proxy update, discovery, DNS); drain old connections.
7. Verify with a synthetic write and read from the app path.
8. Attach other replicas to the new primary; rebuild the old node from a clean copy.
9. Reconcile lost writes if recoverable from the old primary's log or application logs.
10. Post-incident review; measure actual RPO/RTO against targets.

## 5. Replica read routing rules

| Read | Route | Reason |
|---|---|---|
| Right after the user's own write | Primary (or replica caught up to write position) | read-your-writes |
| Dashboards, reports | Replica | lag acceptable |
| Checks gating a write (uniqueness, balance) | Primary | stale value would break invariant |
| Search suggestions, feeds | Replica / cache | staleness acceptable |

## 6. Monitoring list

Replication lag (seconds and bytes), replica state, failover count, per-shard QPS and
storage, hottest keys, connection counts, long transactions, backup age, restore test age.
