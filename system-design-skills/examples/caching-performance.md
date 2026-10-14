# `caching-performance`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Our product page makes 10,000 reads per second against a database that handles 3,000. Design the cache, handle stampedes and invalidation, and show what happens if Redis goes down.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 4,559 | 5,334 |
| Input tokens read across all turns (including cached context) | 30,367 | 73,143 |
| Extra input tokens when the skill is installed | | +42,776 |
| Cost, US dollars at list price | 0.151 | 0.238 |
| Skills invoked in the sample run | none | `caching-performance` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 200 tokens for its name and description, which are in every session where the skill is installed, and about 3,500 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Product page cache design: 10k reads/s against a database that handles 3k

**Main point:** the cache isn't a speed-up here. The site can't run without it. Without a cache, the database gets 10,000 reads/s, which is 3.3× what it can handle. So the design has to answer two questions:
1. How high must the hit ratio be?
2. What keeps the database alive when Redis is gone?

## 1. The numbers

Database load = (1 − h) × 10,000/s, where h is the hit ratio. The latency column assumes a 1 ms cache read and a 20 ms database read; replace these with your measured p50s.

| Hit ratio (h) | Database reads/s | vs. 3,000 capacity | Average latency |
|---|---|---|---|
| 0 (Redis down, no protection) | 10,000 | **333%, database falls over** | 20 ms, then timeouts |
| 0.50 | 5,000 | 167%, overloaded | 10.5 ms |
| 0.70 | 3,000 | 100%, no headroom | 6.7 ms |
| 0.80 | 2,000 | 67% | 4.8 ms |
| **0.95 (target)** | **500** | **17%** | **1.95 ms** |

- **h = 0.70 is the break-even point.** Below that, the database is overloaded even with the cache up.
- **Target h ≥ 0.95.** Product traffic is usually heavily skewed toward a few products, so this is realistic. Confirm it by replaying production access logs against a simulated cache.

**Do this first:** profile the product query. If it's an N+1 or is missing an index, fixing that raises the 3,000 ceiling. Every point you gain there shrinks the Redis-down problem in section 5.

## 2. Architecture: two tiers, cache-aside

```
request → L1 in-process cache (per app instance, ~10k hot products, TTL 10s)
        → L2 Redis (all products, TTL 5 min ±15% jitter)
        → DB, behind a concurrency limiter (cap ≈ 2,500 QPS total)
```

- **Split the data by how quickly it goes stale.**
  - Product details (title, images, description) can be up to 5 minutes stale.
  - Price and stock can't be. Give them their own key with a 10–30 s TTL, or don't cache them and read them at checkout.
  - This assumes the business accepts these windows. Confirm them.
- **L1 (in-process) is required, not optional.** It does two jobs: it absorbs hot keys before they reach a single Redis shard, and it's the only cache left when Redis fails (section 5).
- **CDN:** if the page is the same for every anonymous user, edge caching it with `stale-while-revalidate` removes most of the 10k/s before it reaches your servers. Do it if you can.
- **Keys:** `product:v3:{id}:{locale}` and `price:{id}:{region}`. Include everything that changes the value. Bump `v3` when the serialization format changes.
- **Strategy:** cache-aside with delete-on-write.
  - Not write-back: you can't afford to lose writes.
  - Not write-through: it would cache the long tail of products nobody views.

## 3. Stampede protection

Picture a hot product's key expiring while it gets 2,000 req/s. Without protection, all of those requests miss at the same moment and hit the database together. Four layers stop that:

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Product page cache design: 10k reads/s against a 3k reads/s database

## 1. The numbers

| | Value |
|---|---|
| Incoming reads | 10,000/s |
| Database capacity | 3,000/s (plan for about 70% of that, roughly 2,100/s) |
| Minimum hit rate to survive | 70%, which leaves no margin |
| **Target hit rate** | **≥ 97%** (about 300/s reaches the DB, about 10% of its capacity) |

The cache isn't an optimization here. Without it the database falls over. So the design must answer one question: **what keeps DB load under 3k/s when a cache layer fails or goes cold?**

## 2. Architecture: three tiers

```
Client ─▶ CDN / edge (optional, tier 0) ─▶ App pods
                                             │
                                  ┌──────────┴──────────┐
                                  │ L1: in-process LRU   │  ~5–10k hottest products, TTL 30s
                                  └──────────┬──────────┘
                                             │ miss
                                  ┌──────────┴──────────┐
                                  │ L2: Redis (HA)       │  all products, TTL 10 min ± jitter
                                  └──────────┬──────────┘
                                             │ miss (coalesced, rate-limited)
                                  ┌──────────┴──────────┐
                                  │ DB (≤ 2,100 r/s cap) │
                                  └─────────────────────┘
```

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
