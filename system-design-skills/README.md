<p align="center">
  <img src="assets/banner.svg" alt="System Design Skills: design, scale, secure and review software systems" width="100%">
</p>

<p align="center">
  <img alt="17 skills" src="https://img.shields.io/badge/skills-17-6c64eb?style=flat-square&labelColor=0d2438">
  <img alt="11 templates" src="https://img.shields.io/badge/templates-11-096efb?style=flat-square&labelColor=0d2438">
  <img alt="skills-ref valid" src="https://img.shields.io/badge/skills--ref-valid-9cc464?style=flat-square&labelColor=0d2438">
  <img alt="License Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-fb6373?style=flat-square&labelColor=0d2438">
</p>

Seventeen skills that help a coding agent make sound architecture decisions: estimate load,
pick components, find failure modes, and review existing designs. A coordinator skill runs the
workflow and calls only the specialists a problem needs.

## Skills

| Skill | Use it for |
|---|---|
| `system-design` | The coordinator. An 11-step workflow for a new architecture |
| `requirements-capacity` | Requirements, QPS and storage estimates, availability and latency budgets |
| `architecture-scaling` | Monolith or services, sync or async, scaling ladder, bottlenecks |
| `api-networking` | REST, GraphQL, RPC, HTTP versions, DNS, CDN, load balancing, API contracts |
| `identity-security` | Auth, SSO, tokens, password hashing, TLS, tenant isolation, threat models |
| `database-selection` | Choosing a database from access patterns |
| `transactions-consistency` | Isolation levels, locking, consistency models, sagas, outbox |
| `sharding-replication` | Partitioning, replicas, failover, with a capacity case first |
| `caching-performance` | Cache strategies, invalidation, stampedes, Redis vs Memcached |
| `messaging-streaming` | Queues, Kafka, delivery guarantees, idempotent consumers, retries |
| `storage-systems` | Block, file and object storage, uploads, erasure coding, tiers |
| `deployment-delivery` | Rolling, blue-green, canary, safe migrations, rollback |
| `reliability-resilience` | Failure domains, availability math, backoff, breakers, disaster recovery |
| `observability` | SLOs, burn-rate alerts, metrics, logs, traces, cardinality |
| `geospatial-design` | Geohash, quadtree, nearby search, map tiles, routing |
| `payment-systems` | Initiation, processing, ledger, settlement, idempotency, reconciliation |
| `system-design-review` | Evidence-based review with severity-ranked findings |

Eleven templates ship with the coordinator: design document, ADR, requirements, capacity
worksheet, technology matrix, database review, failure analysis, security checklist,
observability review, production readiness checklist and review report.

## Install

Install all skills together, because the specialists share the coordinator's templates.

```bash
bash scripts/install.sh --claude --project /path/to/your/repo   # Claude Code
bash scripts/install.sh --agents --project /path/to/your/repo   # Codex and .agents/skills readers
bash scripts/install.sh --claude --user                         # every project on this machine
```

Add `--symlink` to link instead of copy, `--force` to replace, `--dry-run` to preview.

| Tool | Reads skills from |
|---|---|
| Claude Code | `.claude/skills/` or `~/.claude/skills/` |
| Codex | `.agents/skills/` in the repo and each parent up to the repo root, `~/.agents/skills/`, `/etc/codex/skills/` (OpenAI Codex docs, read 2026-10-14) |

## ChatGPT

ChatGPT takes a zip with one top-level folder and exactly one `SKILL.md`. A skill that points at a
sibling's templates would break that rule, so `chatgpt/` holds one self-contained zip per skill with
its templates copied in.

```bash
python3 scripts/build_chatgpt.py            # rebuild chatgpt/*.zip
python3 scripts/build_chatgpt.py --check    # verify limits only
```

Checked against OpenAI's developer docs (read 2026-10-14): single top-level folder, one
`SKILL.md`, 500 files, 50 MB zip, 25 MB per file. The upload menu inside the ChatGPT app is
unconfirmed, because OpenAI's help page was not reachable (HTTP 403). Follow the in-product flow.
Upload `system-design.zip` plus the specialists you want.

## Try it

| Ask | Skills used |
|---|---|
| "Design a marketplace backend with flash sales and card payments. Give me a design doc and ADRs." | `system-design`, then capacity, scaling, database, consistency, caching, payments, security, reliability |
| "Review `docs/architecture.md` and `services/`. Give me findings with evidence and severity." | `system-design-review`, plus any specialist the findings need |
| "Duplicate emails after consumer restarts. How do I make confirmation idempotent?" | `messaging-streaming`, with `transactions-consistency` |

Fill a template by asking for it: "write an ADR for this decision" or "run the production
readiness checklist".

## Check it

```bash
python3 scripts/validate_library.py         # spec, sections, size, links, templates, script self-tests
python3 scripts/check_routing.py            # description routing, 26 cases
python3 scripts/build_chatgpt.py --check    # ChatGPT bundle limits
skills-ref validate skills/<name>           # official validator
```

Last run, 2026-10-14: all 17 skills and all 17 ChatGPT bundles pass `skills-ref`, the library
validator reports 0 errors, routing passes 26 of 26, both script self-tests pass, and all 11 Mermaid
diagrams parse. Routing is a word-match check, not a model of how an LLM picks a skill.

Not run yet: the five end-to-end scenarios in [`evals/scenarios.md`](evals/scenarios.md). They need a
live agent and a person to grade them.

## About the source

The skills draw on ByteByteGo's *System Design: The Big Archive* (May 2022), which is not included.
Only the table of contents and the text of pages 4 to 44 were read. Claims about later pages are
marked "TOC-anchored only", and modern guidance comes from official docs fetched on 2026-10-14 or is
marked `VERIFY`. See `skills/system-design/references/book-provenance.md` and
`modernization-notes.md`.

## Contribute

See [CONTRIBUTING.md](../CONTRIBUTING.md) and [`docs/authoring-guide.md`](docs/authoring-guide.md).

## License

Apache-2.0
