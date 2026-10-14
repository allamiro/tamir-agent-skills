# System Design Skills for OpenAI

OpenAI has two tools that matter here, and each takes the skills in a different form.

| Tool | Takes | Status for this collection | Where to read |
|---|---|---|---|
| **Codex** (CLI and IDE) | The `SKILL.md` folders in [`../skills/`](../skills/) | Works | [Codex](#codex) |
| **ChatGPT** | One zip per skill, in [`chatgpt/`](chatgpt/) | Zips built and size-checked | [ChatGPT](#chatgpt) |

## Codex

Codex reads the standard `SKILL.md` folders from `.agents/skills`. There is no separate OpenAI copy.

Run from the `system-design-skills/` folder:

```bash
bash scripts/install.sh --codex --project /path/to/your/project   # this project only
bash scripts/install.sh --codex --user                            # every project on this machine
```

`--codex` and `--agents` do the same thing. Install all 17 skills together, because the
specialists share the coordinator's templates. `--symlink`, `--force` and `--dry-run` work as they
do for Claude Code.

Codex looks for skills in `.agents/skills` in the repo and in each parent folder up to the repo
root, in `~/.agents/skills`, and in `/etc/codex/skills` (OpenAI Codex documentation, read
2026-10-14). Tool versions change, so confirm in your tool's docs.

## ChatGPT

ChatGPT takes a zip with one top-level folder and exactly one `SKILL.md`. A skill that points at a
sibling's templates would break that rule, so [`chatgpt/`](chatgpt/) holds one self-contained zip
per skill with its templates copied in.

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

Checked against OpenAI's developer docs (read 2026-10-14): single top-level folder, one `SKILL.md`,
500 files, 50 MB zip, 25 MB per file. The upload menu inside the ChatGPT app is unconfirmed,
because OpenAI's help page was not reachable (HTTP 403). Follow the in-product flow.

### Rebuild the zips

Only needed after you change a skill. The zips are built deterministically, so an unchanged skill
gives a byte-identical file.

```bash
python3 scripts/build_chatgpt.py            # rebuild openai/chatgpt/*.zip
python3 scripts/build_chatgpt.py --check    # verify limits only
```

Ready-to-paste prompts, one per skill, are in [`../prompts/`](../prompts/README.md).
