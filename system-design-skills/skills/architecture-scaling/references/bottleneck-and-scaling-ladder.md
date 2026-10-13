# Bottleneck hunting and the scaling ladder

## 1. Bottleneck procedure (run at current peak or in a load test)

Use the USE method per resource: Utilization, Saturation, Errors. Tool names are examples.

| Resource | Signals of saturation | Typical diagnostic | Typical fix |
|---|---|---|---|
| CPU | run queue > cores, high user time, latency rises with load | profiler, flame graph, `top`-style tools | optimize hot path, cache, add instances |
| Memory | swapping, OOM kills, GC pauses, evictions | heap profile, GC logs, cgroup metrics | fix leaks, tune pools, bigger instance |
| Disk IO | high await/queue depth, IOPS at provisioned limit | `iostat`-style tools | indexes, batching, faster volume, cache |
| Network | bandwidth near limit, retransmits, connection exhaustion | interface counters, packet drops | CDN, compression, keep-alive, pooling |
| Locks/contention | low CPU yet high latency, many threads waiting | thread dumps, lock wait views | shorten critical sections, shard counters, optimistic concurrency |
| Database | slow queries, connection pool wait, replication lag | slow query log, query plans, pool metrics | indexes, query rewrite, replicas, cache |
| Downstream/third party | timeouts, rate-limit responses | dependency latency histograms | timeouts, caching, async, quota increase |
| Queue/consumers | rising depth or lag | consumer lag, age of oldest message | more consumers, faster handler, partitions |

Procedure:

1. Define the symptom as a number (p99 = 2.4 s at 3,000 req/s; target 300 ms).
2. Check utilization of each row; the first resource at ≥ 70-80% of its *measured*
   limit, or showing saturation, is the suspect.
3. Make one change; re-measure. If the symptom moves, the hypothesis was right.
4. Record the evidence; do not scale a component that is not the bottleneck.

## 2. The scaling ladder

Climb one rung at a time; each rung lists the trigger that justifies it.

| Rung | Change | Trigger | Cost / new failure modes |
|---|---|---|---|
| 0 | Single node, single DB | Default | Single point of failure |
| 1 | Profile and fix (indexes, N+1 queries, payload size) | Any measured slowness | Engineering time only |
| 2 | Separate app and DB hosts; managed DB with backups | Resource contention | Network hop |
| 3 | Redundant stateless app tier behind a load balancer | Availability target or CPU saturation | Session externalization, deploy complexity |
| 4 | Cache hot reads (`caching-performance`) | Read-heavy, DB read saturation | Staleness, invalidation, cold-start load |
| 5 | CDN for static/cacheable content (`api-networking`) | Egress/latency for static assets | Cache invalidation, cost |
| 6 | Vertical scale of the database | Primary CPU/memory/IO saturated, headroom on larger sizes | Ceiling, downtime on resize |
| 7 | Read replicas | Read saturation with tolerance for lag | Replication lag, read-your-writes handling |
| 8 | Async offload (queues, workers) | Slow or spiky work off the request path | Eventual consistency, idempotency |
| 9 | Partition data (functional split, then sharding) | Write or storage limit reached after rungs 1-8 (`sharding-replication`) | Cross-partition queries, rebalancing |
| 10 | Split into services | Team/deploy independence or divergent scaling needs | Distributed failure modes, contracts |
| 11 | Multi-region | Latency to users, regional failure tolerance, data residency | Consistency and cost, failover complexity |

Skipping rungs requires a written reason (for example data residency forces rung 11).

## 3. Worked example (illustrative)

Symptom: checkout p99 is 1.8 s at 600 req/s; target 400 ms. App CPU 25%, database CPU 85%,
slow-query log shows a 1.2 s query without a usable index.

- Wrong move: add 10 app instances (rung 3) - the database is the bottleneck, load on it
  would rise.
- Right move: rung 1 (add index, rewrite query), re-measure; then rung 4 if reads still
  dominate. Result recorded: DB CPU 85% → 40%, p99 → 300 ms (hypothetical numbers for
  illustration).

## 4. Stateless tier checklist

- No request-affinity requirement; any instance can serve any request.
- Config via environment; secrets from a manager.
- Idempotent startup and graceful shutdown; readiness distinct from liveness.
- Connection pools sized: instances × pool size ≤ DB limit × 0.8.
- Local caches tolerate being cold and being inconsistent across instances.

## 5. Microservice readiness check (all should be yes before splitting)

1. Boundary follows a business capability with its own data.
2. The team can deploy it independently today (CI/CD).
3. Tracing, metrics and logs exist across the call path.
4. A contract-testing or versioning approach exists.
5. Cross-service transactions have designed compensation.
6. On-call ownership is defined.
