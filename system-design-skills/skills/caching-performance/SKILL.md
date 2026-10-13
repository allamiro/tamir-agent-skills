---
name: caching-performance
description: Designs caching and performance improvements - cache-aside, read-through, write-through, write-back, TTL and invalidation, stampede, penetration (cache miss attacks), avalanche, hot keys, Redis vs Memcached, eviction, durability risks and memory sizing - plus measure-first performance triage. Use for "add a cache", "cache invalidation", "Redis or Memcached", "database too slow", "hot key", "thundering herd", p99 latency work. Use transactions-consistency for stale-read correctness, api-networking for CDN/HTTP caching headers, sharding-replication for replicas.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Caching and performance

## Purpose and activation

Reduce latency and backing-store load with a cache **only when measurement shows a
repeatable read hot spot**, and design what happens when the cache is stale, cold, or
gone. A cache is a derived copy of data that creates a consistency problem; it must earn
its place.

Activate for read-heavy paths, slow queries, expensive computations, hot keys, and
cache incidents. Not for CDN/HTTP header design in depth (`api-networking`) or replica
topology (`sharding-replication`).

## Required inputs

The operation to speed up with current latency (p50/p95/p99) and request rate; read:write
ratio; how often the same data is read (repeat rate, key distribution); staleness the
business tolerates (seconds, minutes, never); data size per entry; backing-store capacity.

## Workflow

1. **Measure first**: profile the path (query time, serialization, network, N+1 queries,
   missing index). Many "cache needs" are an index or a query fix; do that first.
2. **Prove cacheability**: repeat rate high, results identical for many callers (or
   keyable), staleness tolerable. Estimate hit ratio from the key distribution.
3. **Compute the benefit**: effective latency = h × t_cache + (1 − h) × t_miss;
   backing-store load = (1 − h) × request rate. Do it for h = 0.5, 0.8, 0.95 and for h = 0
   (cache failure) - [references/cache-design-reference.md](references/cache-design-reference.md).
4. **Choose placement**: in-process, shared distributed cache, CDN/edge, or database-side.
5. **Choose the strategy** with the matrix below.
6. **Define keys, TTLs and invalidation**, including the race between update and
   invalidate.
7. **Plan protection** against stampede, penetration, avalanche and hot keys.
8. **Size memory and pick eviction**; decide persistence (usually none for a pure cache).
9. **Define failure behavior**: cache down, cold start, slow cache; the backing store
   must survive the h = 0 load, or the system needs shedding.
10. **Instrument and validate** (below).

## Decision framework

### Strategy

| Strategy | Read path | Write path | Strengths | Risks |
|---|---|---|---|---|
| Cache-aside (lazy) | App checks cache, on miss reads DB and fills | App writes DB, then deletes (or updates) cache entry | Simple, cache holds only requested data, tolerates cache loss | Stale until invalidated; miss storms; race on invalidate |
| Read-through | Cache layer loads from DB on miss | App writes DB (plus invalidation) | Callers don't know the DB | Needs loader support; same staleness issues |
| Write-through | Reads hit cache | Write goes to cache and DB synchronously | Cache consistent with DB after success; read-heavy data warm | Higher write latency; caches data never read |
| Write-back (write-behind) | Reads hit cache | Write to cache, flushed to DB later | Very fast writes, batching | **Data loss if cache dies before flush**; ordering and failure handling complex |
| Refresh-ahead | Entry refreshed before expiry | n/a | Avoids miss latency for hot keys | Wasted refreshes for cold keys |

Default: cache-aside with TTL and delete-on-write. Use write-back only for data you can
afford to lose or reconstruct, with a durable queue/log behind it.

### Placement

| Where | Pros | Cons |
|---|---|---|
| In-process | Fastest, no network | Per-instance copies diverge, memory per instance, cold on deploy |
| Distributed cache (Redis, Memcached as examples) | Shared, large, centralized invalidation | Network hop, extra component to operate, becomes a dependency |
| CDN / edge | Closest to users | Invalidation/purge delay, personalization limits |

### Redis vs Memcached (facts fetched 2026-10-14 from official docs)

| Aspect | Redis | Memcached |
|---|---|---|
| Data model | Rich types (strings, hashes, sets, sorted sets, streams, etc. - VERIFY list for your version) | Simple key-value of opaque data; clients serialize |
| Persistence | Optional RDB snapshots and/or AOF; with AOF `everysec` you can lose about one second of writes; snapshots alone can lose minutes; "no persistence" is an option and common for caches | Docs reviewed describe a cache; persistence features exist as options but were not covered in the pages read - VERIFY |
| Replication | Supported | None among servers ("no replication" per its docs); distribution is client-side hashing |
| Eviction | `maxmemory` + policy (`allkeys-lru` suggested as a good default when a hot subset dominates; also LFU, random, TTL-based, `noeviction`); LRU is approximated by sampling | LRU by default, items also expire by TTL |
| Memory accounting | Replication/AOF buffers are not counted against `maxmemory`; leave headroom | Slab-based memory (VERIFY) |
| Choose when | Need data structures, atomic ops, persistence, replication, pub/sub, locks/counters | Plain, high-volume key-value caching with simple operations and client-side scaling |

The book's Redis-vs-Memcached comparison (p. 64) is TOC-anchored only. Neither choice is
mandatory; a managed cache service or in-process cache may fit better.

## Architecture and implementation guidance

- **Keys**: `service:entity:id:version-or-locale`; include everything that changes the
  value (tenant, locale, permission scope) or you leak data across users. Namespace by
  deployment version if the value format changes.
- **TTL**: set on every entry. Add random jitter (for example ±10-20% of TTL) so
  entries created together do not expire together (avalanche).
- **Invalidation order**: the safe default is *write DB, then delete cache key*. Race:
  reader misses, reads old value from DB, writer updates DB and deletes key, reader then
  fills the cache with the old value. Mitigations: short TTL as backstop, versioned values
  with compare-before-set, delayed second delete, or lease/lock on fill.
- **Stampede (thundering herd)**: many requests miss the same hot key at once and hit the
  DB. Use single-flight (one loader per key, others wait), a short lock/lease, serving
  stale-while-revalidate, probabilistic early refresh, or request coalescing.
- **Penetration (cache miss attack)**: requests for keys that never exist bypass the cache.
  Mitigate with negative caching (short TTL for "not found"), input validation, a Bloom
  filter or set of valid ids in front of the DB, rate limiting.
- **Avalanche**: mass expiry or cache restart sends everything to the DB: jittered TTLs,
  warm-up, multi-layer caches, load shedding, circuit breaker.
- **Hot keys**: one key receives disproportionate traffic and saturates one cache node.
  Use local in-process replication of the hot value, key suffix sharding (`key#0..k`),
  or a read replica per hot key.
- **Large values**: avoid caching huge objects (network and memory); cache IDs or
  fragments instead.
- **Memory sizing**: entries × (value + key + overhead per entry) ÷ target fill ratio; set
  `maxmemory` below physical RAM leaving room for buffers and fragmentation; choose an
  eviction policy matching the access pattern; watch eviction rate.
- **Multi-tenant fairness**: per-tenant quotas or key prefixes with monitoring.
- Performance triage beyond caches (profile → fix queries → batch → connection pools →
  async) is in [references/cache-design-reference.md](references/cache-design-reference.md).

## Failure and edge cases

- Cache down or slow: callers need a timeout (a few ms, not seconds), then fall back to
  the DB with protection; otherwise the cache becomes a single point of failure.
- Cold start after deploy or flush: DB takes the full load; test it.
- Stale data served after update (race) or after partial failure of invalidation.
- Write-back loss: acknowledged writes disappear when the cache node dies or evicts.
- Eviction of important keys by a noisy workload; memory fragmentation.
- Serialization format changes breaking readers of old entries.
- Authorization bypass: cached response served to a user who should not see it.
- Cache as source of truth: data written only to the cache is lost on eviction/restart.
- Clock/TTL surprises: client-set TTL vs server time.
- Hit ratio looks good but misses are the expensive keys (measure by cost, not count).

## Validation

- Baseline vs with-cache p50/p95/p99 and DB QPS in a load test with a realistic key
  distribution (not uniform random).
- Chaos checks: flush the cache during load; kill a cache node; add 100 ms latency to the
  cache; confirm the system degrades within SLO or sheds load.
- Metrics: hit ratio, miss latency, evictions, memory used vs limit, expired keys,
  connection errors, per-key hotness, backing-store QPS. Alert on hit-ratio drop and
  eviction surge.
- Staleness test: update a record and measure how long readers see the old value.
- Falsifier: backing-store load at h = 0 exceeds its tested capacity, or measured hit ratio
  is below the assumed value that justified the cache.

## Expected output

A measurement of the problem, benefit calculation (h sensitivity incl. h = 0), strategy and
placement choice, key/TTL/invalidation design with the race analysis, protection list,
sizing, failure behavior, metrics and alerts, and an ADR.

## Sources and confidence

- Book (direct): none verified in the supplied text (Redis vs Memcached p. 64, cache miss attack p. 68, cache strategies p. 71-73, why Redis is fast p. 76) — TOC-anchored only
- Book (synthesized): Amazon Builders' Library "Caching challenges and strategies" is named in the supplied reading list (p. 33) — verified as a title only; not read
- Modern: Redis persistence docs and eviction docs — fetched 2026-10-14; Memcached site overview — fetched 2026-10-14 (partial); stampede, avalanche and race mitigations — from author knowledge, VERIFY
- Needs workload validation: hit ratio, TTLs, sizes, key skew, tolerance for staleness
