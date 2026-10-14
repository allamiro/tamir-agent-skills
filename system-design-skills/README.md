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

## Which one is for my tool?

| I use | Read | Install | Status |
|---|---|---|---|
| **Claude Code** | [`claude/`](claude/README.md) | `bash scripts/install.sh --claude --project DIR` | Works |
| **OpenAI Codex** | [`openai/`](openai/README.md#codex) | `bash scripts/install.sh --codex --project DIR` | Works |
| **ChatGPT desktop app** | [`openai/`](openai/README.md#chatgpt) | [17 zips](openai/chatgpt/) | Zips built; how the app takes them is not confirmed |
| **OpenAI Skills API** | [`openai/`](openai/README.md#openai-skills-api) | [17 zips](openai/chatgpt/) | Zips built to the documented format and limits |

Claude Code and Codex read the same files from [`skills/`](skills/). Nothing is copied per
platform, so there is one place to fix a skill. The zips for ChatGPT and the API are built from `skills/`.

## What is in this folder

```text
system-design-skills/
├── skills/     the 17 skills (SKILL.md plus references, scripts and templates)
├── claude/     Claude Code: install and use
├── openai/     OpenAI: Codex install, and chatgpt/ with one zip per skill
├── prompts/    ready-to-paste prompts, one per skill
├── scripts/    install.sh, build_chatgpt.py, validate_library.py, check_routing.py
├── evals/      routing cases and end-to-end scenarios
├── docs/       authoring guide
└── assets/     banner
```

## Skills

| Skill | Use it for | Prompt |
|---|---|---|
| [`system-design`](skills/system-design/) | The coordinator. An 11-step workflow for a new architecture | [prompt](prompts/README.md#system-design) |
| [`requirements-capacity`](skills/requirements-capacity/) | Requirements, QPS and storage estimates, availability and latency budgets | [prompt](prompts/README.md#requirements-capacity) |
| [`architecture-scaling`](skills/architecture-scaling/) | Monolith or services, sync or async, scaling ladder, bottlenecks | [prompt](prompts/README.md#architecture-scaling) |
| [`api-networking`](skills/api-networking/) | REST, GraphQL, RPC, HTTP versions, DNS, CDN, load balancing, API contracts | [prompt](prompts/README.md#api-networking) |
| [`identity-security`](skills/identity-security/) | Auth, SSO, tokens, password hashing, TLS, tenant isolation, threat models | [prompt](prompts/README.md#identity-security) |
| [`database-selection`](skills/database-selection/) | Choosing a database from access patterns | [prompt](prompts/README.md#database-selection) |
| [`transactions-consistency`](skills/transactions-consistency/) | Isolation levels, locking, consistency models, sagas, outbox | [prompt](prompts/README.md#transactions-consistency) |
| [`sharding-replication`](skills/sharding-replication/) | Partitioning, replicas, failover, with a capacity case first | [prompt](prompts/README.md#sharding-replication) |
| [`caching-performance`](skills/caching-performance/) | Cache strategies, invalidation, stampedes, Redis vs Memcached | [prompt](prompts/README.md#caching-performance) |
| [`messaging-streaming`](skills/messaging-streaming/) | Queues, Kafka, delivery guarantees, idempotent consumers, retries | [prompt](prompts/README.md#messaging-streaming) |
| [`storage-systems`](skills/storage-systems/) | Block, file and object storage, uploads, erasure coding, tiers | [prompt](prompts/README.md#storage-systems) |
| [`deployment-delivery`](skills/deployment-delivery/) | Rolling, blue-green, canary, safe migrations, rollback | [prompt](prompts/README.md#deployment-delivery) |
| [`reliability-resilience`](skills/reliability-resilience/) | Failure domains, availability math, backoff, breakers, disaster recovery | [prompt](prompts/README.md#reliability-resilience) |
| [`observability`](skills/observability/) | SLOs, burn-rate alerts, metrics, logs, traces, cardinality | [prompt](prompts/README.md#observability) |
| [`geospatial-design`](skills/geospatial-design/) | Geohash, quadtree, nearby search, map tiles, routing | [prompt](prompts/README.md#geospatial-design) |
| [`payment-systems`](skills/payment-systems/) | Initiation, processing, ledger, settlement, idempotency, reconciliation | [prompt](prompts/README.md#payment-systems) |
| [`system-design-review`](skills/system-design-review/) | Evidence-based review with severity-ranked findings | [prompt](prompts/README.md#system-design-review) |

Eleven templates ship with the coordinator: design document, ADR, requirements, capacity
worksheet, technology matrix, database review, failure analysis, security checklist,
observability review, production readiness checklist and review report.

## Install

Run from this folder. Install all 17 skills together, because the specialists share the
coordinator's templates.

```bash
bash scripts/install.sh --claude --project /path/to/your/repo   # Claude Code
bash scripts/install.sh --codex --project /path/to/your/repo    # OpenAI Codex
```

Add `--user` to install for every project on the machine, `--symlink` to link instead of copy,
`--force` to replace, or `--dry-run` to preview. For ChatGPT and the OpenAI Skills API, which take zips,
see [`openai/`](openai/README.md#chatgpt). Details for each tool: [`claude/`](claude/README.md) and
[`openai/`](openai/README.md).

## Try it

| Ask | Skills used |
|---|---|
| "Design a marketplace backend with flash sales and card payments. Give me a design doc and ADRs." | `system-design`, then capacity, scaling, database, consistency, caching, payments, security, reliability |
| "Review `docs/architecture.md` and `services/`. Give me findings with evidence and severity." | `system-design-review`, plus any specialist the findings need |
| "Duplicate emails after consumer restarts. How do I make confirmation idempotent?" | `messaging-streaming`, with `transactions-consistency` |

Every skill has a ready-to-paste prompt in [`prompts/`](prompts/README.md). Fill a template by asking
for it: "write an ADR for this decision" or "run the production readiness checklist".

## Check it

```bash
python3 scripts/validate_library.py         # spec, sections, size, links, templates, navigation, script self-tests
python3 scripts/check_routing.py            # description routing, 43 cases (incl. prompts/)
python3 scripts/build_chatgpt.py --check    # ChatGPT bundle limits
skills-ref validate skills/<name>           # official validator
claude plugin validate skills               # Claude Code's own check of the skill files
```

Last run, 2026-10-14, after the folder restructure: all 17 skills and all 17 ChatGPT bundles pass
`skills-ref`, the library validator reports 0 errors (including the navigation check), routing
passes 43 of 43, both script self-tests pass, the 17 zips are byte-identical to a fresh build, and
markdownlint reports 0 issues, and `claude plugin validate` accepts the skills. The 11 Mermaid diagrams
were parsed earlier the same day; the skills have not changed since. Routing is a word-match check, not a model of how an LLM picks a skill.

Not run yet: the five end-to-end scenarios in [`evals/scenarios.md`](evals/scenarios.md). They need a
live agent and a person to grade them.

## Contribute

See [CONTRIBUTING.md](../CONTRIBUTING.md) and [`docs/authoring-guide.md`](docs/authoring-guide.md).

## License

Apache-2.0

## Citation

ByteByteGo. 2022. *System Design: The Big Archive*. May 2022.
