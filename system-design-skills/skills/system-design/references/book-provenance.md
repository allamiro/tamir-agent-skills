# Book provenance

Source: ByteByteGo, "System Design: The Big Archive" (May 2022). Page numbers are the book's
printed page numbers.

## How much of the book was actually read

| Region | Status when this library was written |
|---|---|
| Printed pp. 4–44 | Body text was supplied and read. Claims about these pages are marked **verified against supplied text**. The text ended partway through p. 44. |
| Printed pp. 45–159 | Body text was **not available**. Only the table-of-contents titles and page numbers were available. Claims about these pages are marked **TOC-anchored only**: the topic exists at that page, but the book's specific statements, figures and numbers were not read and are not asserted here. |
| Diagrams | None were available as images. No diagram is reproduced; all diagrams in this library are new. |

Nothing in the skills quotes the book. Where a skill says "the book says X", X comes from
pp. 4–44 and is paraphrased. To close the gap, run the upgrade path at the end of this file.

## Evidence tiers

| Tier | Meaning |
|---|---|
| T1 | Directly supported by book text that was read (pp. 4–44) |
| T2 | Synthesized by this library from several sections, or from titles only |
| T3 | Modern extension from an external standard or vendor documentation |
| T4 | Assumption or recommendation that needs workload-specific validation |

External sources marked "fetched 2026-10-14" were read on that date from the vendor or
standards site. Sources marked "from author knowledge, VERIFY" were not fetched.

## Per-skill mapping

| Skill | T1 (book pp. 4–44 read) | T2 (TOC-anchored or synthesized) | T3 (modern extension) | T4 (needs validation) |
|---|---|---|---|---|
| system-design | Orchestration vs choreography (38–39); deployment strategies (30–31); SSO, passwords, HTTPS, API auth (11–17, 35–37) | Workflow draws on scaling (55–57), estimation (157–158), interview tip (139) | — | All capacity numbers |
| requirements-capacity | none | Estimation (157–158); scaling to millions of users (55–57) | Availability arithmetic and Little's law (author knowledge) | Inputs, peak factors, per-node limits |
| architecture-scaling | Orchestration vs choreography trade-offs (38–39) | Scaling a website (55–57); virtualization vs containers (40) | Monolith-first guidance (author knowledge) | Thresholds, autoscaling |
| api-networking | HTTPS walk-through (16–17), used as a baseline to correct | HTTP versions (53); REST/GraphQL/RPC (62); CDN (84); DNS (97); URL walk-through (99) | RFC 9110–9114, 9000, 9111, 9457 (VERIFY) | Timeouts, TTLs |
| identity-security | SSO (11–12); passwords (13–15); HTTPS (16–17); token and HMAC API auth (35–37) | Payment security (138) | OWASP Password Storage Cheat Sheet, RFC 9700, RFC 8446 (fetched) | Hash cost on your hardware, token lifetimes |
| database-selection | Category list (20–21); unique-ID requirements (22–23) | Metrics database choice (126–128); p.133 | none fetched | Query latencies, growth |
| transactions-consistency | Isolation levels and MVCC example (4–5) | Optimistic locking (65); latency vs consistency (67); read replicas (103–106) | PostgreSQL 18 isolation docs; MySQL 8.4 InnoDB docs (fetched) | Contention, staleness bounds |
| sharding-replication | none | Vertical vs horizontal partitioning (82–83); read replicas (103–106) | Failover semantics (VERIFY per engine) | Thresholds, shard counts |
| caching-performance | none | Redis vs Memcached (64); cache miss attack (68); cache strategies (71–73); why Redis is fast (76); Builders' Library caching article named on p. 33 (title only) | Redis persistence and eviction docs; Memcached overview (fetched) | Hit ratio, TTL, sizes |
| messaging-streaming | Google Docs operation queue (28–29); idempotent-API article named on p. 33 | Why Kafka is fast (60); delivery semantics (80); pull vs push (117–118) | Apache Kafka design docs, delivery semantics and transactions (fetched) | Partition counts, retry bounds |
| storage-systems | none | Large-file upload (74–75); erasure coding (87–88); block/file/object (94–95); CDN (84) | AWS S3 consistency model and features (fetched) | Part sizes, tiers, k and m |
| deployment-delivery | Deployment strategies (30–31); Builders' Library reading list (33–34) | Large-scale outage (49–50) | AWS Builders' Library rollback-safety article (fetched) | Stage sizes, bake times |
| reliability-resilience | Reading list items (33–34); orchestration as single point of failure (38–39) | Outage handling (49–50); read replicas (103–106) | Google SRE book cascading failures; AWS timeouts/retries article (fetched) | Timeouts, breaker thresholds, RPO/RTO |
| observability | none | Diagnosing a process (70); pull vs push (117–118); metrics DB and monitoring system (124–130) | Google SRE Workbook alerting on SLOs; Prometheus overview (fetched) | Thresholds, retention, series counts |
| geospatial-design | none | Map rendering (113–114); Google Maps (115–116); quadtree (142–143); nearby restaurants (144–145) | Geohash sizes computed 2026-10-14; S2/H3/PostGIS (VERIFY) | Entry bytes, density, rates |
| payment-systems | Derived vs stored balance and journal as truth (9–10); idempotent-API article named on p. 33 | Money movement (119); reconciliation (122, 131); double charge (136); payment security (138); design a payment system (153–154); SWIFT (77); FX (89) | Stripe idempotency docs; PCI SSC page (fetched) | Provider behavior, settlement timing |
| system-design-review | Orchestration SPOF (38–39); deployment trade-offs (30–31); password/HTTPS simplifications (13–17) | Interview tip (139) | Severity rubric and anti-pattern list are library synthesis | Severity calibration |

## Source-anchor reconciliation

The maintainer's anchor table was compared with the table of contents. Anchors that match a
printed title are listed in the per-skill rows. Anchors with no matching title in the table
of contents (for example database p. 133, storage pp. 91–93, observability pp. 124–125,
127–128, and several second pages of two-page topics) are carried forward unverified.

## Upgrade path when the PDF is available

1. Extract text locally (`pdftotext -layout book.pdf book.txt`); keep it out of version control.
2. Confirm the printed-to-PDF page offset.
3. For each row above marked TOC-anchored, read the cited pages, then change the skill's
   Sources block to "verified against supplied text" only for statements actually checked.
4. Record corrections where the book disagrees with a skill; add modernization entries to
   `modernization-notes.md`.
5. Re-run the library validator and the evaluation scenarios.
