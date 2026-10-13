# Authoring guide for skills in this library

Every skill in `skills/` must follow this contract. `scripts/validate_library.py` enforces the
mechanical parts.

## 1. Frontmatter (Agent Skills spec, agentskills.io/specification)

```yaml
---
name: <must equal directory name; lowercase a-z, 0-9, single hyphens; <=64 chars>
description: <1-1024 chars. Say what the skill does AND when to activate it AND when NOT to (point to the sibling skill). Include trigger keywords a user would actually type.>
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---
```

Do not add other top-level keys. `allowed-tools` and `compatibility` are omitted: skills are
plain instructions and work in any agent that reads `SKILL.md`.

## 2. Body structure (in this order, omit a section only if truly irrelevant)

1. `# Title` and one-paragraph **Purpose and activation**: what it does, when to activate,
   and "Use `<other-skill>` instead when ...".
2. **Required inputs**: minimum facts. Say what to do when missing (ask, or assume and label
   `ASSUMPTION:`). Never block on questions that have a sensible default.
3. **Workflow**: numbered steps an agent can execute. Each step names an artifact it
   produces or a check it performs. No "apply best practices".
4. **Decision framework**: a table, checklist or Mermaid decision tree with the trade-off of
   each branch stated.
5. **Architecture and implementation guidance**: components, data flow, interface contracts,
   storage decisions, constraints.
6. **Failure and edge cases**: concrete failures, concurrency hazards, partial outages, data
   loss, recovery.
7. **Validation**: how to check the recommendation (test, metric, benchmark, source
   inspection, quantitative reasoning). Name the number or observable that would prove the
   recommendation wrong.
8. **Expected output**: the exact deliverable(s) and which template in
   `../system-design/assets/templates/` to use.
9. **Sources and confidence**: at most 12 lines, format in section 4.

Size: `SKILL.md` under 500 lines and about 5,000 tokens (roughly 3,500 words). Push formulas,
long matrices and worked examples into `references/*.md`. Each reference file is linked
directly from `SKILL.md` (one level deep) with a sentence saying when to read it.

## 3. Content rules

- **Simplest viable baseline first.** Every skill must say when NOT to use its pattern and
  what the cheaper alternative is. Do not default to microservices, Kafka, Kubernetes, Redis,
  sharding or a distributed database.
- **Every added component has a documented purpose** tied to a requirement or a measured
  number.
- **Quantify.** Use units. Show the formula, one worked example with stated assumptions, and
  what would change the answer.
- **Distinguish layers.** Delivery guarantee is not business correctness. Replication is not
  backup. A retry is not idempotency. Authentication is not authorization.
- **Original material only.** Do not copy sentences, structures or diagrams from the book.
  Write new explanations and new Mermaid diagrams. Short factual anchors such as "the book
  covers X at printed p. N" are fine.
- **No invented facts.** No made-up benchmarks, RFC numbers, API parameters, vendor limits or
  quotations. If unsure, write `VERIFY:` and say what to check. Illustrative numbers must be
  labelled `illustrative` and must not look like measurements.
- **Vendor-neutral.** Name products as examples ("for example Redis, Memcached"), never as
  requirements.
- **Diagrams**: Mermaid in fenced blocks, one idea per diagram, readable at a glance.
- **Cross-references between skills** use the skill name in backticks, never copied text.
  Shared templates live in `skills/system-design/assets/templates/` and are referenced as
  `../system-design/assets/templates/<file>`.
- Scripts must be standard-library Python 3 or POSIX shell, have `--help`, print clear errors,
  and be invoked in prose as `python3 scripts/<file>.py`.

## 4. Sources and confidence block

Every `SKILL.md` ends with:

```markdown
## Sources and confidence
- Book (direct): <topic> (printed p. N) — verified against supplied text | TOC-anchored only
- Book (synthesized): <guidance combining pages ...>
- Modern: <standard or vendor doc by name> — fetched <date> | from author knowledge, VERIFY
- Needs workload validation: <the numbers or choices that depend on the user's system>
```

Status words are fixed: `verified against supplied text` (only printed pages 4–44 qualify
in the first release), `TOC-anchored only`, `fetched <date>`, `from author knowledge, VERIFY`.
`references/book-provenance.md` aggregates these blocks.

## 5. Evidence tiers (used in provenance and review reports)

| Tier | Meaning |
|---|---|
| T1 | Directly supported by the ByteByteGo book text that was read |
| T2 | Synthesized by this library from several book sections |
| T3 | Modern extension from an external standard or vendor documentation |
| T4 | Assumption or recommendation that needs workload-specific validation |

## 6. Allowed external reference names

Cite only references you are confident exist, by name and identifier, and mark them
`VERIFY` unless fetched: IETF RFC 9110 (HTTP semantics), 9111 (HTTP caching), 9112, 9113
(HTTP/2), 9114 (HTTP/3), 9000 (QUIC), 8446 (TLS 1.3), 6749 (OAuth 2.0), 7636 (PKCE),
7519 (JWT), 9421 (HTTP message signatures), 9457 (problem details), 1034/1035 (DNS);
OWASP Password Storage Cheat Sheet, ASVS, API Security Top 10, Threat Modeling guidance;
NIST SP 800-63B; PostgreSQL "Transaction Isolation" documentation; Apache Kafka
documentation (producer idempotence, transactions, delivery semantics); Redis and Memcached
official documentation; cloud-provider storage documentation; Google "Site Reliability
Engineering" and "The Site Reliability Workbook"; Amazon Builders' Library articles the book
itself names on p. 33. Anything else needs a fetched source.
