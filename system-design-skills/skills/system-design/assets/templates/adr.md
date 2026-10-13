# ADR-<number>: <decision title as a verb phrase, e.g. "Use a single PostgreSQL primary with read replicas">

- Status: proposed | accepted | superseded by ADR-<n> | rejected
- Date: <YYYY-MM-DD>
- Deciders: <names or roles>
- Requirements driven by: <requirement IDs from the requirements doc, e.g. N2, N4>

## Context

What forces make a decision necessary now? Include the measured or estimated numbers that
matter (QPS, data size, failure rate) and constraints (team, budget, compliance).

## Decision

One paragraph in the active voice: "We will ...". Include scope and what is explicitly not
decided.

## Options considered

| Option | Advantages | Disadvantages | Operational cost | Fails when |
|---|---|---|---|---|
| A: <chosen> | | | | |
| B: <simplest baseline> | | | | |
| C: <more scalable alternative> | | | | |

Always include the simplest baseline, even when it is rejected, and say why it fails the
numbers.

## Consequences

- Positive:
- Negative / debt accepted:
- New failure modes introduced:
- Reversibility: how hard to undo (one-way door / two-way door) and the exit path.

## Validation and revisit triggers

- Experiment or measurement that confirms the assumption: <test, expected result>
- Revisit when: <metric crosses threshold, requirement changes, date>

## Example (filled)

ADR-004: Use a relational primary with read replicas for the order store.
Context: 185 peak writes/s, 3.5k reads/s, orders need multi-row transactions (N4).
Decision: PostgreSQL primary, two asynchronous replicas, reads of own recent orders go to the primary.
Rejected: sharded store (no capacity need, loses cross-order transactions); document store (needs joins on order lines).
Revisit when: sustained primary CPU > 60% after index tuning, or storage > 70% of volume.
