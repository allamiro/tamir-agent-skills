# System Design Skills

Seventeen modular [Agent Skills](https://agentskills.io/specification) that help a coding
agent make defensible architecture decisions: estimate load, choose components, analyze
failures, and review existing designs. The skills are original guidance informed by
ByteByteGo's *System Design: The Big Archive* (May 2022) and modernized against standards
and vendor documentation where the book is introductory. The book itself is not included.

> **Provenance in one sentence:** the source PDF was not available when this library was
> written; only the table of contents and the text of printed pages 4-44 were read, so
> claims about later pages are marked "TOC-anchored only" and the rest rests on vendor and
> standards documentation fetched on 2026-10-14 or marked `VERIFY`. Details:
> `skills/system-design/references/book-provenance.md` and `modernization-notes.md`.

## Skills

| Skill | Use it for |
|---|---|
| `system-design` | Coordinator: 11-step workflow for a new architecture; routes to only the specialists needed |
| `requirements-capacity` | Requirements, QPS/storage/bandwidth estimates, availability and latency budgets, sensitivity analysis |
| `architecture-scaling` | Monolith vs services, sync vs async, orchestration vs choreography, scaling ladder, bottleneck hunting |
| `api-networking` | REST/GraphQL/RPC, HTTP versions, DNS, CDN, load balancing, API contracts, timeouts |
| `identity-security` | AuthN/AuthZ, SSO (OIDC), tokens, request signing, password hashing, TLS, tenant isolation, threat modeling |
| `database-selection` | Choosing relational/document/key-value/wide-column/time-series/search/graph from access patterns |
| `transactions-consistency` | Isolation levels, anomalies, locking, consistency models, sagas, outbox |
| `sharding-replication` | Partitioning, replicas, failover, rebalancing, with a capacity case required before sharding |
| `caching-performance` | Cache strategies, invalidation, stampede/penetration/hot keys, Redis vs Memcached |
| `messaging-streaming` | Queues vs logs, Kafka basics, delivery guarantees, idempotent consumers, retries, backpressure |
| `storage-systems` | Block/file/object storage, multipart uploads, replication vs erasure coding, tiers |
| `deployment-delivery` | Rolling/blue-green/canary, expand-contract migrations, rollback safety |
| `reliability-resilience` | Failure domains, availability math, retries/jitter, breakers, load shedding, DR |
| `observability` | SLIs/SLOs, burn-rate alerts, metrics/logs/traces, cardinality, pull vs push |
| `geospatial-design` | Geohash/quadtree, proximity search, map tiles, routing; single machine vs distributed |
| `payment-systems` | Initiation vs processing vs ledger vs settlement, idempotency, reconciliation |
| `system-design-review` | Evidence-based review of designs and codebases with severity-ranked findings |

Eleven reusable templates ship in `skills/system-design/assets/templates/`: system design
document, ADR, requirements, capacity worksheet, technology selection matrix, database design
review, failure analysis, security architecture checklist, observability and reliability
review, production readiness checklist, and architecture review report.

## How agents discover and activate skills

Each skill is a folder with a `SKILL.md`. Agents read only the `name` and `description` of
every installed skill at startup and load the full body when a request matches. The
descriptions say what the skill does, when to use it, and which sibling to use instead. Deeper
material sits in `references/` and loads on demand. You can also name a skill explicitly in
your prompt.

## Install

Install **all skills together**: the specialist skills point at the shared templates in
`../system-design/assets/templates/`.

```bash
# Claude Code, one project / all your projects
bash scripts/install.sh --claude --project /path/to/your/repo
bash scripts/install.sh --claude --user

# Codex and other agents that read .agents/skills
bash scripts/install.sh --agents --project /path/to/your/repo

# Keep a live link to this checkout instead of copying
bash scripts/install.sh --claude --project . --symlink
```

`--force` replaces existing copies; `--dry-run` previews.

| Tool | Where skills are read from | Verification |
|---|---|---|
| Claude Code | `.claude/skills/` (project) or `~/.claude/skills/` (user) | Installer tested against a scratch project; skills pass `skills-ref` |
| Codex | `$CWD/.agents/skills` and each parent up to the repo root, `$HOME/.agents/skills`, `/etc/codex/skills`; symlinked skill folders are followed | Paths per OpenAI's Codex skills documentation, read 2026-10-14 |

## ChatGPT

ChatGPT and the OpenAI API take a skill as a **zip with one top-level folder containing
exactly one `SKILL.md`**. That rule rules out sibling references, so this collection builds a
self-contained bundle per skill: the templates a skill needs are copied into its own
`assets/templates/`, links are rewritten, and an optional `agents/openai.yaml` display
metadata file is added. Ready-to-upload zips are in [`chatgpt/`](chatgpt/):

```bash
python3 scripts/build_chatgpt.py            # rebuild chatgpt/*.zip (deterministic)
python3 scripts/build_chatgpt.py --check    # verify limits without writing
```

What was verified (OpenAI developer docs, "Skills" guide, read 2026-10-14): single top-level
folder, exactly one `SKILL.md` (case-insensitive), at most 500 files per skill, zip up to
50 MB, 25 MB per file. The build script enforces all of these, and every bundle also passes
`skills-ref validate` after extraction. In ChatGPT, skills are chosen with `@`; Codex uses
`$skill-name` or `/skills`.

What was **not** verified: the exact upload menu in the ChatGPT app. OpenAI's help article
for it was not retrievable from this environment (HTTP 403), and secondary guides describe
Plugins, then Skills, then Create, then Upload from your computer. Menus differ by plan,
workspace admins can restrict uploads, and uploaded skills are scanned before use, so follow
the in-product flow. The specialist skills mention each other by name; for the best results
upload the coordinator `system-design` bundle together with the specialists you need.

## Use it

Ask for outcomes, not skill names:

1. **A complete design**: "Design the backend for a marketplace with 2M monthly users, flash
   sales, and card payments. Team of 6 on a major cloud. Produce a design doc and ADRs."
   Expected: `system-design`, then `requirements-capacity`, `architecture-scaling`,
   `database-selection`, `transactions-consistency`, `caching-performance`, `payment-systems`,
   `identity-security`, `reliability-resilience`. Not `geospatial-design`.
2. **An architecture review**: "Review the architecture in `docs/architecture.md` and the code
   under `services/`. Give me findings with evidence, severity, impact and remediation."
   Expected: `system-design-review`, consulting specialists only for the risks it finds.
3. **A focused question**: "We see duplicate emails after consumer restarts on our queue. How
   do we make order confirmation idempotent?" Expected: `messaging-streaming`, with
   `transactions-consistency` for the dedupe table. The coordinator is not needed.

Fill templates by asking the agent to "use the capacity worksheet", "write an ADR for this
decision", or "run the production readiness checklist".

## Validate

```bash
python3 scripts/validate_library.py         # spec rules, sections, size, links, templates, script self-tests
python3 scripts/check_routing.py --verbose  # lexical smoke test of skill descriptions (26 cases)
python3 scripts/build_chatgpt.py --check    # OpenAI bundle limits and link integrity
skills-ref validate skills/<name>           # official Agent Skills validator, per skill
python3 skills/requirements-capacity/scripts/capacity.py --selftest
python3 skills/observability/scripts/slo_budget.py --selftest
```

Status when last run (2026-10-14): `skills-ref` valid for all 17 skills and all 17 extracted
ChatGPT bundles; library validator 0 errors; routing 26/26; both script self-tests pass; all
11 Mermaid diagrams parse with the Mermaid parser; Markdown lint clean under the project
configuration. The routing test is a lexical proxy, not a model of an LLM router.

**Not yet done:** end-to-end behavioral runs of the five scenarios in
[`evals/scenarios.md`](evals/scenarios.md) (e-commerce, metrics platform, collaborative editor,
multi-tenant security, architecture review) plus negative tests. They need a live agent and
a human grader; record results in `evals/results-template.md`.

## Contribute

See the repository's [CONTRIBUTING.md](../CONTRIBUTING.md) and
[`docs/authoring-guide.md`](docs/authoring-guide.md).

## License

Apache-2.0. The source book is not included and must not be committed (`source/` is
git-ignored).
