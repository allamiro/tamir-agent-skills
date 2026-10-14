# `geospatial-design`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Design nearby-restaurant search for 50 million places and 20,000 queries per second. Geohash or quadtree? Does the index fit on one machine?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,727 | 3,208 |
| Input tokens read across all turns (including cached context) | 30,361 | 73,270 |
| Extra input tokens when the skill is installed | | +42,909 |
| Cost, US dollars at list price | 0.114 | 0.197 |
| Skills invoked in the sample run | none | `geospatial-design` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 220 tokens for its name and description, which are in every session where the skill is installed, and about 3,600 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**Short answer:** use a geohash. Yes, the index fits on one machine with room to spare. You still want several replicas, for availability and to serve users in different regions, not because of memory or CPU. Don't shard.

## 1. Workload

- **Data:** 50M restaurants. They are static points of interest that change rarely, maybe tens to hundreds of edits per second worldwide. A few seconds of delay before an edit shows up in search is fine.
- **Query:** "Restaurants within radius r of (lat, lon)", plus filters such as cuisine or open now, sorted by distance or score, paginated. r ranges from about 0.5 to 20 km.
- **Load:** 20k QPS average. I assume a peak of about 2× that, so 40k QPS.

## 2. Does it fit on one machine?

| Item | Per entry | × 50M |
|---|---|---|
| Index only: 64-bit geohash or cell ID, 64-bit place ID, lat/lon as two float32 | ~24–40 B | **1.2–2 GB** |
| Plus the fields needed to filter and rank (category, rating, hours bitmap, price) | ~100–150 B | **5–7.5 GB** |
| Full records (names, addresses, photo URLs) | ~1 KB | ~50 GB. Keep these in the database or a cache, not in the index |

The index plus the filter fields comes to under 10 GB, which fits easily in a 64 GB server.

**CPU check.** These per-query costs are my estimates, so benchmark them:

- A query does about 9 cell range scans over a sorted array, then exact haversine distance checks on a few hundred candidates.
- That should take roughly 50–200 µs of CPU, so about 5–20k QPS per core.
- A 16-core box should therefore handle 80k+ QPS in theory, which covers the 40k peak by itself.

**Deployment.** Every node holds the full index, so no query ever has to fan out to several shards.

- Run 3–4 replicas per region, in 2–3 regions, for failover and lower latency. Each node then runs at a small fraction of its capacity.
- Shard by geography only if a measurement shows one of these:
  - the index exceeds RAM with headroom,
  - replicas plus caching can't keep up with QPS, or
  - write volume exceeds what one writer can handle.

  None of these is close at this scale.

## 3. Geohash or quadtree?

| | Geohash (or an S2 cell ID) | Quadtree |
|---|---|---|
| Storage | A sorted `uint64` array in memory, or an indexed column in any database | A custom in-memory tree |
| Updates | Insert or delete one key | Nodes need splitting and merging; usually rebuilt periodically |
| Startup | Load a sorted snapshot in seconds | Build the tree from 50M points, which takes minutes per replica |
| Uneven density | Fixed cell size, so a downtown cell can hold thousands of places | Adapts naturally: dense areas split into smaller cells |
| Sharding later | By prefix, which is trivial | Harder |
| "k nearest" queries | Widen the search ring until k results are found | Natural fit |

**Recommendation: geohash, or S2 if you want more uniform cells.**

- The data is static, so the quadtree's main strength, adapting to density, matters less than geohash's simplicity.
- The same key works in Postgres, in an in-memory array and as a shard key.

The density problem is real, but you can fix it in the query instead of the data structure:

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Nearby-restaurant search: 50M places at 20k QPS

**Short answers:** Use geohash (or S2 cells, which work the same way). The index easily fits on one machine. You still need several machines, but they hold full copies of the index (replicas) for throughput and availability. You don't need to split the data across machines.

## 1. Back-of-envelope sizing

**Search index.** The index only stores what's needed to find places, not their details.

| Field | Bytes |
|---|---|
| place_id | 8 |
| lat, lon (float32 ×2, about 1 m precision) | 8 |
| geohash (as a 64-bit integer) | 8 |
| Small ranking fields (category, rating, price, open-hours bitmap) | ~8 |
| **Total** | **~32 B** |

- 50M × 32 B ≈ **1.6 GB**.
- With 2–3× overhead for data structures and allocator, that's about **3–5 GB in RAM**. A standard 64 GB server holds this many times over.

**Place details** (name, address, photos, menu link): about 1–2 KB × 50M ≈ **50–100 GB**. These go in a separate key-value store or cache, looked up by ID after search finds the top results.

**Throughput.** One query looks up about 9 grid cells, checks a few hundred candidates and sorts them. That costs about 10–50 µs of CPU. One 16-core machine can serve **50k–100k+ QPS** from memory.

20k QPS fits on one machine in theory. In practice, run **4–6 replicas per region** at about 30% load. That leaves headroom for:
- A machine failing
- Deploys
- Traffic spikes, like Friday at 7pm

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
