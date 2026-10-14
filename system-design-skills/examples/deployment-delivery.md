# `deployment-delivery`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> We need to rename a database column on a live service with zero downtime and a safe rollback. Plan the release, including a canary and the rollback triggers.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 3,244 | 3,471 |
| Input tokens read across all turns (including cached context) | 30,352 | 72,843 |
| Extra input tokens when the skill is installed | | +42,492 |
| Cost, US dollars at list price | 0.124 | 0.199 |
| Skills invoked in the sample run | none | `deployment-delivery` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 210 tokens for its name and description, which are in every session where the skill is installed, and about 3,400 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Zero-downtime column rename: release plan

You didn't name the engine, table or service, so this plan assumes PostgreSQL or MySQL 8, a horizontally scaled stateless service, and a rename of `users.fullname` → `users.display_name`. Swap in your real names. The thresholds below are starting values to adjust to your traffic.

## 1. Why you can't just run `RENAME COLUMN`

During any rollout, old and new pods run at the same time against the same database. If you run `ALTER TABLE ... RENAME COLUMN`, every pod still on the old code fails at once with "column does not exist". Rolling back the code then fails too, because the old column name is gone. So the rename has to be split into steps where each step is safe to deploy and safe to reverse on its own (expand → migrate → contract). Schema changes ship separately from code deploys.

**Inventory every reader and writer of the column before you start.** Include the service code and ORM mappings, raw SQL, views, stored procedures and triggers, ETL/analytics jobs, change-data-capture/replication pipelines, search indexers, cached objects that serialise the field name, API responses that expose it, and backups/restore scripts. If you miss one, it breaks at the contract step.

## 2. Release steps

| # | Change | Type | State afterwards | How to roll back |
|---|---|---|---|---|
| 0 | Reconciliation query and dashboards in place; snapshot plan agreed | prep | — | — |
| 1 | **Expand:** `ADD COLUMN display_name` as nullable with no default | schema | New column exists; nothing uses it | `DROP COLUMN display_name` (harmless) |
| 2 | **Dual-write:** app writes both columns and still **reads `fullname`** | code, canary | New rows land in both columns | Redeploy previous build; the new column just goes stale |
| 3 | **Backfill:** `UPDATE ... SET display_name = fullname WHERE display_name IS NULL` in throttled batches | data job | Every row populated | Stop the job; it's idempotent, so rerun later |
| 4 | **Verify:** reconciliation query (`WHERE display_name IS DISTINCT FROM fullname`) returns 0 and stays at 0 | gate | — | — |
| 5 | **Switch reads:** app reads `display_name` and keeps writing both | code, canary (+ optional flag) | New column is the source of truth | Redeploy step 2's build (or flip the flag). Safe, because `fullname` is still being written |
| 6 | Migrate the other consumers (ETL, views, CDC, APIs) to `display_name` | code/config | Nothing reads `fullname` | Revert each consumer on its own |
| 7 | **Stop writing old:** app writes only `display_name` | code, canary | `fullname` goes stale | See the warning below |
| 8 | **Bake** for a full business cycle, including batch and month-end jobs | wait | — | — |
| 9 | **Contract:** snapshot, then `DROP COLUMN fullname` | schema | Done | **Point of no return.** The only way back is restoring from the snapshot |

**Warning about step 7:** after it ships, rolling back to step 2 or 5 code means reading a stale `fullname`. You have two options:
- **(a) Recommended:** keep dual-writing until step 9. It's the simplest and keeps rollback free.
- **(b)** Add a temporary DB trigger that copies `display_name` → `fullname`, so older builds stay correct.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Zero-downtime column rename: release plan

I've assumed a relational database (Postgres in the examples), several app instances behind a load balancer, and rolling or canary deploys. Throughout, `old_col` is the current name and `new_col` is the target.

## Approach: add a new column and remove the old one later

Don't use `ALTER TABLE ... RENAME COLUMN` on a live service. During a rolling deploy, old and new app versions run at the same time, and whichever version expects the other name breaks. Instead, run the rename as a series of releases. Each release works with the previous one, and each can be rolled back by itself.

| Phase | Change | Readers use | Writers write | Rollback |
|---|---|---|---|---|
| 0 | Prep | `old` | `old` | n/a |
| 1 | Add `new_col` (nullable, no default rewrite) | `old` | `old` | Drop `new_col` |
| 2 | App dual-writes `old` + `new` | `old` | both | Redeploy previous app |
| 3 | Backfill `new_col` in batches + verify | `old` | both | Stop the job; data is untouched |
| 4 | App reads `new`, still dual-writes (**canary**) | `new` | both | Flip flag / redeploy; `old` is still correct |
| 5 | Stop writing `old` | `new` | `new` | Redeploy Phase 4 + re-backfill `old` |
| 6 | Drop `old_col` (days or weeks later) | `new` | `new` | Restore from backup only. This is the one step you can't undo. |

Each phase is its own deploy. Don't move to the next phase until the current one has run in production for at least a full traffic cycle (usually 24 hours, including peak).

## Phase details

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
