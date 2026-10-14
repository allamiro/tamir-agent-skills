# `sharding-replication`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Our PostgreSQL primary is at 75% write IO and growing 50% every six months. Do we need to shard? If so, which shard key, and what is the failover plan?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,926 | 3,164 |
| Input tokens read across all turns (including cached context) | 30,365 | 72,840 |
| Extra input tokens when the skill is installed | | +42,475 |
| Cost, US dollars at list price | 0.118 | 0.193 |
| Skills invoked in the sample run | none | `sharding-replication` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 210 tokens for its name and description, which are in every session where the skill is installed, and about 3,400 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
## Short answer

**Probably yes, eventually. Not as your next step.** Your growth rate makes sharding (or at least partitioning your data across databases) very likely within 1–2 years. But you're already close to the limit, and sharding safely takes 6–12 months. You need cheaper fixes now to buy that time, and you should start the sharding design in parallel.

## The math

Write IO grows 1.5× every 6 months, which is about 2.25× per year and about 11× over 3 years.

| Threshold | Time from now (75%, growing 1.5× per 6 months) |
|---|---|
| 85% (where latency usually starts to degrade) | **~1.8 months** |
| 90% | ~2.7 months |
| 100% (saturated) | **~4.3 months** |

How much time vertical scaling buys, measured as months until you're back at 75%:

| Write IO headroom added | Time bought |
|---|---|
| 2× (e.g. double provisioned IOPS) | ~10 months |
| 4× | ~20 months |
| 8× | ~31 months |

**Conclusion:** vertical scaling and tuning only buy time. At 2.25× per year, a single primary runs out unless growth slows. That makes this a "plan it now" problem, not a "maybe someday" one.

## Do these first (the next 0–3 months)

These are listed roughly by write-IO payoff:

1. **Find what is generating the IO.** Use `pg_stat_statements` (sort by `shared_blks_written`/`wal_bytes`), `pg_stat_wal`, and `pg_stat_bgwriter`/`pg_stat_checkpointer`. Split it into WAL, checkpoint and vacuum IO.
2. **Reduce write amplification:**
   - Drop unused indexes (`pg_stat_user_indexes.idx_scan = 0`). Every index multiplies the cost of each write.
   - Get more HOT updates: lower `fillfactor` on tables with heavy updates, and avoid indexing columns that change often.
   - Raise `max_wal_size` and `checkpoint_timeout` so you get fewer full-page writes. Consider `wal_compression = lz4`.
   - Tune autovacuum, and fix bloat on the hottest tables.
3. **Remove write traffic that doesn't need to be there:**
   - Move cold data out with archival or TTL. Partition time-series tables so you can drop partitions instead of running `DELETE`.
   - Batch small writes.
   - Move counters and event logs to a queue or a separate store.
4. **Raise the IO ceiling**, e.g. more provisioned IOPS or NVMe storage. This is usually the cheapest single lever.
5. **Split by function:** if independent domains share the primary (audit logs, events, sessions, analytics), move the biggest writers into their own database. This often removes 30–60% of write IO without the complexity of sharding.

Read replicas won't help here, because they add no write capacity.

**Re-check after this phase.** Recompute the date you hit 85% from the new baseline. If it's more than about 18 months out, you can postpone sharding. If not, go ahead with the plan below.

## Shard key

I can't pick one without your schema and top queries. This is how to decide:

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
**Short answer:** Yes, you probably need to shard eventually, but it can't happen fast enough to fix your near-term problem. You have roughly 1–4 months of headroom. Sharding takes 6–12 months to do safely. So you need to do two things at once: buy time on the current primary now, and start designing shards now.

## 1. The timeline math

At 50% growth every six months, write IO multiplies by about 1.5× each half-year.

| When | Write IO (relative to today's capacity) |
|---|---|
| Now | 75% |
| ~1 month | ~80–85%. Latency usually starts degrading here (checkpoint spikes, replication lag). |
| ~4.3 months | 100% |
| 12 months | ~170% |
| 3 years | ~850% (11×) |

No single box absorbs 11×. Unless growth flattens, this ends in horizontal scaling. Getting 2× headroom buys about 10 months, and 4× buys about 20 months. That's runway, not a fix.

## 2. Buy time now (weeks, not months)

Most Postgres write IO is amplification rather than the logical writes themselves, so first measure what the IO actually is. Check `pg_stat_wal`, `pg_stat_bgwriter` or `pg_stat_checkpointer`, and `pg_stat_statements` sorted by `wal_bytes`. Then:

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
