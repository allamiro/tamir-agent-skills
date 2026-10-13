---
name: messaging-streaming
description: Designs asynchronous messaging - queues vs event streams (Kafka fundamentals), workers, delivery guarantees (at-most/at-least/exactly-once), retries, dead-letter queues, deduplication, idempotent consumers, ordering, partitioning, consumer lag, backpressure, transactional outbox, pull vs push. Use for "add a queue", "Kafka or RabbitMQ/SQS", background jobs, event-driven design, duplicate or lost messages, "exactly-once". Use transactions-consistency for DB atomicity, payment-systems for money flows, architecture-scaling for sync-vs-async choices, reliability-resilience for retry policy.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Messaging and streaming

## Purpose and activation

Decide whether asynchronous messaging is needed, which kind, and how to keep the *business
outcome* correct when messages are duplicated, delayed, reordered or lost. A delivery
guarantee describes the transport; correctness of the end-to-end operation is a separate
property you must design.

Activate for background processing, event-driven integration, fan-out, buffering of
spiky load, stream processing, and any report of duplicate/missing/out-of-order events.
Do not add a broker when a direct call, a database table, or a scheduled job suffices.

## Required inputs

Message rate (peak and average), message size, number of producers and consumers, ordering
requirements (per entity? global?), loss and duplication tolerance, processing time per
message, replay needs, retention, and the side effects consumers perform (DB write, email,
payment call). Missing: assume at-least-once with idempotent consumers.

## Workflow

1. **Justify asynchrony**: which of {smooth spikes, isolate a slow/unreliable dependency,
   fan-out to many consumers, durable replayable log, decouple deployments} applies?
   If none, use a direct call.
2. **Choose queue vs log** (matrix below) and a managed service where possible.
3. **Define each message**: name, schema, key (ordering/partition key), idempotency id,
   version, producer, consumers, retention.
4. **Pick the delivery guarantee per flow** and design consumers to be idempotent.
5. **Design the producer side**: how is "state changed" + "message sent" made atomic?
   (transactional outbox; never a bare dual write).
6. **Design retries, dead letters and poison-message handling** (policy table below).
7. **Size it**: partitions/consumers, throughput, lag tolerance, backlog drain time.
8. **Define backpressure and overload behavior**.
9. **Define observability**: lag, age of oldest message, retry and DLQ rates, processing
   latency, duplicate-detected rate.
10. **Document failure scenarios** (`../system-design/assets/templates/failure-analysis.md`).

## Decision framework

### Queue vs event log

| Aspect | Message queue (work queue) | Event log / stream (Kafka-style) |
|---|---|---|
| Model | Message consumed and removed once acknowledged | Append-only partitioned log; consumers track offsets; data retained |
| Fan-out | Needs topic/exchange per consumer group | Many independent consumer groups read the same log |
| Replay | Usually no | Yes, within retention |
| Ordering | Often best effort; per-queue FIFO variants | Per partition |
| Competing consumers | Natural | Parallelism limited by partition count |
| Use when | Task distribution, jobs with per-message retry/delay semantics | Event sourcing, analytics feeds, many subscribers, high throughput, replay |

### Delivery guarantees (Kafka documentation, read 2026-10-14)

| Guarantee | Meaning | How it arises | Consumer requirement |
|---|---|---|---|
| At-most-once | May lose, never redelivers | Commit position before processing, or no producer retries | Accept loss |
| At-least-once | Never lost, may duplicate | Process, then commit position; producer retries | **Idempotent processing** |
| Exactly-once (within the broker) | Each input processed once with outputs written to the broker | Idempotent producer + transactions, offsets committed in the same transaction, consumers with `isolation.level=read_committed` | Applies to read-process-write on Kafka topics |
| Exactly-once to external systems | Not provided by the broker alone | Requires cooperation of the destination: idempotency keys, unique constraints, transactional outbox/inbox | You build it |

Source notes: the idempotent producer deduplicates retries using a producer id and sequence
numbers; Kafka transactions write to multiple partitions atomically and can include the
consumer's offsets; the documentation warns that "exactly-once" claims often do not hold
when consumers or producers can fail, and says exactly-once for other destination systems
generally requires cooperation of those systems.

**Business-operation correctness is separate.** If a handler charges a card, sends an
email, then crashes before committing its offset, the message is redelivered and the
side effect repeats unless the operation is idempotent. The broker's guarantee ends at
the broker boundary.

### Retry policy

| Failure kind | Action |
|---|---|
| Transient (timeout, 5xx, rate limit) | Retry with exponential backoff + jitter, bounded attempts, then DLQ |
| Permanent (validation error, missing referenced data that will never exist) | Do not retry; send to DLQ with reason |
| Poison message (crashes the consumer) | Detect by attempt count; park in DLQ so it does not block the partition |
| Ordering-sensitive stream | Retry in place with a bounded delay or pause the partition; retry topics reorder events |

Always attach an attempt counter and original timestamp; alert on DLQ growth; provide a
replay tool for the DLQ after fixing the cause.

## Architecture and implementation guidance

- **Idempotent consumer pattern**: derive a stable id for each message (`event_id` or a
  business key such as `payment_id + step`). Inside the same local transaction as the
  side effect, insert the id into a `processed_messages` table with a unique constraint;
  on conflict, skip. Where the side effect is an external call, pass the id as an
  idempotency key to that system.
- **Transactional outbox** (producer side): in one DB transaction write the business row
  and an outbox row; a relay publishes unsent rows and marks them sent (publish may
  repeat - consumers dedupe). Alternative: change-data-capture from the database log.
  Details in `transactions-consistency`.
- **Partition key** = the entity whose events must stay ordered (account id, order id).
  Ordering holds per partition only; cross-key ordering is not provided. Hot keys cap the
  throughput of one partition.
- **Parallelism**: consumers in a group ≤ partitions. Choose partition count with headroom
  for growth (changing it later alters key→partition mapping). Drain time = backlog ÷
  (consumer rate − arrival rate); if consume ≤ arrival the backlog never drains.
- **Backpressure**: bound queue length or age; consumers pull at their own pace (pull
  models self-limit; push models need credits/flow control); producers get rejected or
  throttled when limits are exceeded; shed or degrade low-priority work. Pull vs push
  collection is also a topic on printed p. 117 (TOC-anchored).
- **Schema evolution**: versioned schemas (additive changes, defaults), a registry or
  contract tests; consumers ignore unknown fields.
- **Replication/durability** (Kafka-style): with acks from all in-sync replicas and a
  minimum in-sync-replica setting, a committed message survives as long as one in-sync
  replica survives; raising the minimum improves durability but reduces write
  availability (per Kafka docs, read 2026-10-14).
- **Retention vs replay**: set retention longer than the longest plausible consumer outage
  plus recovery time; compaction keeps the latest value per key for state-like topics.
- **Why a log is fast** (printed p. 60, TOC-anchored): sequential disk access and OS page
  cache reuse are described in the Kafka design docs - quoted here only as a pointer.
- Worked patterns and sizing: [references/messaging-patterns.md](references/messaging-patterns.md).

## Failure and edge cases

- Duplicate delivery (consumer crash after side effect, rebalance, producer retry).
- Lost messages (acks=0/1, unreplicated broker failure, consumer commits before processing).
- Reordering (retries, multiple partitions, parallel handlers on one key).
- Poison messages blocking a partition.
- Consumer rebalance storms and long processing exceeding poll/session timeouts.
- Backlog growth and retention expiry before consumers catch up (data loss by age).
- Dual-write gaps: DB committed but publish failed, or publish succeeded but DB rolled back.
- Large messages and slow consumers causing head-of-line blocking.
- Schema break by an unannounced producer change.
- Transactional processing aborted: consumer must reset its position and reprocess.
- Time-based logic (TTL, delays) affected by clock skew.

## Validation

- Chaos tests: kill consumers mid-processing; restart brokers; inject duplicates; delay
  acknowledgements; confirm final state equals the single-delivery outcome.
- Property test: replay the same message set twice and in shuffled order per key where
  allowed; assert idempotent results.
- Load test: arrival rate at 1.5× peak; observe lag and drain time.
- Metrics: consumer lag and age, retry rate, DLQ depth, duplicate-skipped rate, rebalance
  count, produce/consume latency.
- Falsifier: any discrepancy between expected and actual business totals after a failure drill.

## Expected output

Justification for asynchrony; queue/log choice; message catalog (key, schema, guarantee);
producer atomicity design (outbox); idempotent consumer design; retry/DLQ policy; sizing
(partitions, consumers, drain time); backpressure plan; Mermaid flow; failure table; ADR.

## Sources and confidence

- Book (direct): Google Docs operation queue between WebSocket and operation servers (printed p. 28-29); recommended Builders' Library reading "Making retries safe with idempotent APIs" (p. 33, title only) — verified against supplied text
- Book (synthesized): why Kafka is fast (p. 60), delivery semantics (p. 80), pull vs push (p. 117-118) — TOC-anchored only
- Modern: Apache Kafka documentation "Message Delivery Semantics", "Using Transactions", replication/ISR sections (from the project's docs source, apache/kafka trunk docs/design/design.md) — fetched 2026-10-14; outbox/inbox patterns — from author knowledge, VERIFY
- Needs workload validation: partition counts, retention, retry bounds, drain times
