# `payment-systems`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Design card payments with a payment provider, a ledger and daily reconciliation. How do we avoid double charges when requests time out?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 3,404 | 3,404 |
| Input tokens read across all turns (including cached context) | 30,353 | 73,755 |
| Extra input tokens when the skill is installed | | +43,402 |
| Cost, US dollars at list price | 0.128 | 0.205 |
| Skills invoked in the sample run | none | `payment-systems` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 230 tokens for its name and description, which are in every session where the skill is installed, and about 4,300 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Card payments design: PSP, ledger, daily reconciliation

**Assumptions** (change these if yours differ): one third-party PSP (Stripe-like) using hosted card fields, so no card numbers ever reach us. Separate authorize and capture steps, confirmation by webhook, a single currency stored as integer minor units, and the PSP's daily settlement report plus a bank statement.

## 1. Four stages, each with an owner

| Stage | Owner | Source of truth |
|---|---|---|
| Intent (order, amount, currency, idempotency key) | Payment service | `payment_intents` table |
| External processing (auth/capture) | PSP, mirrored by us | PSP API and webhooks |
| Accounting record | Ledger module | `ledger_entries` (append-only, double-entry) |
| Settlement (money actually reaches us) | PSP and bank | Settlement report and bank statement |

Components:
- **Payment API**: owns intents and the state machine.
- **PSP adapter**: keeps PSP-specific details in one place.
- **Webhook receiver**: checks the signature, stores the event and queues it.
- **Ledger poster**: consumes outbox events.
- **Recovery job**: resolves payments stuck in PROCESSING or UNKNOWN.
- **Daily reconciliation job**: compares our records with the PSP and the bank.

## 2. State machine

```
CREATED → PROCESSING → AUTHORIZED → CAPTURED → SETTLED
                │                      │          └→ CHARGEBACK
                ├→ FAILED (definitive decline)    └→ REFUNDED / PARTIALLY_REFUNDED
                └→ UNKNOWN (timeout / 5xx / crash)
                      ├→ AUTHORIZED (query or webhook confirms)
                      └→ FAILED (query confirms no charge)
```

- Transitions only move forward and are checked. A compare-and-set does this: `UPDATE … SET state=$new WHERE id=$id AND state=$expected`.
- Every transition records the time, the actor and the PSP reference.
- **UNKNOWN is a real state. The only exits from it are a status query or a webhook, never a new charge.**

## 3. Avoiding double charges on timeout

Retries only handle temporary errors. A single charge is guaranteed by these layers working together:

**Layer 1: client → our API**
- The UI disables the button after the first click.
- The client generates an `Idempotency-Key` once per checkout attempt and reuses it on every retry.
- We store `(key, request_hash, status, response)` with a unique constraint on the key:
  - Same key and same payload: return the stored response.
  - Same key and different payload: 422.
  - Same key while the first request is still running: 409, or wait.

**Layer 2: our API → PSP**
- The key sent to the PSP is derived from our own ID, e.g. `pay_123:auth` or `pay_123:capture`. It is not random per attempt.
- This way a retry after a crash or a new deploy still sends the same key, and the PSP returns the original result instead of charging again.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Card payments: provider, ledger and daily reconciliation

## Core rule

**A timeout tells you nothing about whether the charge happened.** Treat a timeout as "unknown", never as "failed". Find out what happened using the same identity you used to create the charge. Never retry with a new one.

## Components

```
Client ──► Payments API ──► Payments DB (payment intents + state machine)
                │                   │
                │                   ├─► Outbox ──► Ledger (double-entry, append-only)
                ▼                   │
        Provider Adapter ◄──────────┤
          │        ▲                │
          ▼        │ webhooks       │
       Provider ───┘                │
          │                         │
          └─ daily settlement file ─► Reconciliation job ──► exceptions queue
```

- **Payments API:** takes requests, enforces idempotency and owns the payment state machine.
- **Provider adapter:** the only code that talks to the provider. It maps provider statuses to your states.
- **Ledger:** append-only double-entry journal. It records only facts the provider has confirmed, never intentions.
- **Outbox:** state changes and the matching ledger events are written in the same DB transaction, then delivered. This means you never charge without a ledger entry, or the reverse.
- **Reconciliation:** compares the ledger against the provider's records and the bank every day.

## State machine

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
