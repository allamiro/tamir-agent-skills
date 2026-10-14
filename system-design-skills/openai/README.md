# System Design Skills for OpenAI

OpenAI has more than one place that takes skills, and they do not take them the same way. What each
accepts below is as the OpenAI documentation states it (read 2026-10-14); anything the documentation
does not say is marked as unconfirmed.

| Tool | How skills get in | Status for this collection | Read |
|---|---|---|---|
| **Codex** (CLI and IDE extension) | Folders of `SKILL.md` files in `.agents/skills` | Works | [Codex](#codex) |
| **ChatGPT desktop app** | Standalone skills show in a Skills sidebar and are picked with `@` | 17 zips built; how the app takes a skill is not confirmed | [ChatGPT](#chatgpt) |
| **OpenAI Skills API** | A zip with one top-level folder | 17 zips built and checked against the documented limits | [OpenAI Skills API](#openai-skills-api) |

## Codex

Codex reads the standard `SKILL.md` folders. There is no separate OpenAI copy of the skills.

Run from the `system-design-skills/` folder:

```bash
bash scripts/install.sh --codex --project /path/to/your/project   # this project only
bash scripts/install.sh --codex --user                            # every project on this machine
```

`--codex` and `--agents` do the same thing. Install all 17 skills together, because the specialists share the coordinator's templates.
`--symlink`, `--force` and `--dry-run` work as they do for Claude Code.

Codex scans `.agents/skills` in every directory from the working directory up to the repository root,
`$HOME/.agents/skills` for your user, and `/etc/codex/skills` for an administrator, and it follows
symlinked skill folders. To use a skill, describe the task and Codex picks one from the description,
or run `/skills` or type `$` and the skill name to choose one yourself. (Codex skills documentation
at learn.chatgpt.com, read 2026-10-14.)

Ready-to-paste prompts, one file per skill, are in [`../prompts/`](../prompts/README.md).

## ChatGPT

The ChatGPT documentation says standalone skills are available in the ChatGPT desktop app as well
as in Codex, that in ChatGPT you type `@` and pick the skill, and that the desktop app has a Skills
sidebar. It describes the optional `agents/openai.yaml` file as display and invocation settings for
the desktop app, and every zip here includes one. For wider distribution it recommends packaging
skills as a plugin, which this collection does not do.

What the documentation read does **not** describe is uploading a zip as a standalone skill in the
ChatGPT chat app, and it does not say where the desktop app looks for skills. So how you add these
skills to the desktop app is unconfirmed. Two things to try, neither verified here: install the skill
folders as for Codex (the documentation lists the desktop app next to Codex but does not say they
read the same folders), or use a zip upload if your ChatGPT version offers one. Follow the in-product
flow.

## OpenAI Skills API

The OpenAI skills guide (read 2026-10-14) says you can upload a directory, or a `.zip` that contains
a single top-level folder; a bundle may hold exactly one `SKILL.md`; the zip may be at most 50 MB;
there may be at most 500 files per skill version; and an uncompressed file may be at most 25 MB. The
zips in [`chatgpt/`](chatgpt/) meet all of these, one zip per skill:

Start with `system-design.zip`, the coordinator, then add the specialists you need.

| Zip | Skill |
|---|---|
| [`system-design.zip`](chatgpt/system-design.zip) | The coordinator: an 11-step workflow for a new architecture |
| [`requirements-capacity.zip`](chatgpt/requirements-capacity.zip) | Requirements, QPS and storage estimates, availability and latency budgets |
| [`architecture-scaling.zip`](chatgpt/architecture-scaling.zip) | Monolith or services, sync or async, scaling ladder, bottlenecks |
| [`api-networking.zip`](chatgpt/api-networking.zip) | REST, GraphQL, RPC, HTTP versions, DNS, CDN, load balancing |
| [`identity-security.zip`](chatgpt/identity-security.zip) | Auth, SSO, tokens, TLS, tenant isolation, threat models |
| [`database-selection.zip`](chatgpt/database-selection.zip) | Choosing a database from access patterns |
| [`transactions-consistency.zip`](chatgpt/transactions-consistency.zip) | Isolation levels, locking, consistency models, sagas, outbox |
| [`sharding-replication.zip`](chatgpt/sharding-replication.zip) | Partitioning, replicas, failover |
| [`caching-performance.zip`](chatgpt/caching-performance.zip) | Cache strategies, invalidation, stampedes |
| [`messaging-streaming.zip`](chatgpt/messaging-streaming.zip) | Queues, Kafka, delivery guarantees, idempotent consumers |
| [`storage-systems.zip`](chatgpt/storage-systems.zip) | Block, file and object storage, uploads, erasure coding |
| [`deployment-delivery.zip`](chatgpt/deployment-delivery.zip) | Rolling, blue-green, canary, safe migrations, rollback |
| [`reliability-resilience.zip`](chatgpt/reliability-resilience.zip) | Failure domains, availability math, backoff, breakers |
| [`observability.zip`](chatgpt/observability.zip) | SLOs, burn-rate alerts, metrics, logs, traces |
| [`geospatial-design.zip`](chatgpt/geospatial-design.zip) | Geohash, quadtree, nearby search, map tiles |
| [`payment-systems.zip`](chatgpt/payment-systems.zip) | Payment flow, ledger, settlement, idempotency, reconciliation |
| [`system-design-review.zip`](chatgpt/system-design-review.zip) | Evidence-based review with severity-ranked findings |

### Rebuild the zips

Only needed after you change a skill. The zips are built deterministically.
The builder also copies the shared templates into each specialist's bundle, because a bundle cannot reach a sibling skill.

```bash
python3 scripts/build_chatgpt.py            # rebuild openai/chatgpt/*.zip
python3 scripts/build_chatgpt.py --check    # verify limits
```
