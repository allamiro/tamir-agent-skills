# Ledger and reconciliation reference

Illustrative schema and examples. Adapt names, constraints and accounting rules with your
finance team; this is design guidance, not accounting advice.

## 1. Double-entry ledger schema

```sql
CREATE TABLE account (
  id         bigint PRIMARY KEY,
  owner_type text NOT NULL,          -- customer | merchant | platform | provider_clearing | fees
  owner_id   text,
  currency   char(3) NOT NULL,
  kind       text NOT NULL           -- asset | liability | revenue | expense
);

CREATE TABLE ledger_txn (
  id           uuid PRIMARY KEY,
  business_ref text NOT NULL,        -- e.g. payment id + step
  entry_type   text NOT NULL,        -- charge | capture | refund | fee | payout ...
  created_at   timestamptz NOT NULL DEFAULT now(),
  UNIQUE (business_ref, entry_type)  -- posts at most once per payment step (idempotency)
);

CREATE TABLE ledger_entry (
  id        bigserial PRIMARY KEY,
  txn_id    uuid NOT NULL REFERENCES ledger_txn(id),
  account_id bigint NOT NULL REFERENCES account(id),
  direction char(1) NOT NULL CHECK (direction IN ('D','C')),
  amount    bigint NOT NULL CHECK (amount > 0),   -- minor units
  currency  char(3) NOT NULL
);
-- Invariant (enforced by a deferred constraint, trigger or application check, and verified by job):
-- for every txn_id: SUM(amount WHERE D) = SUM(amount WHERE C), single currency per txn.
-- No UPDATE or DELETE on ledger_txn/ledger_entry (revoke privileges; corrections are new txns).
```

## 2. Example postings (amounts in cents)

Customer pays $50.00 for a merchant; the PSP fee of $1.75 is charged to the merchant.

| Step | Debit | Credit | Amount |
|---|---|---|---|
| Capture confirmed | Provider clearing (asset) | Merchant payable (liability) | 5000 |
| Fee assessed (merchant bears it) | Merchant payable | Provider clearing | 175 |
| Settlement received (net) | Bank (asset) | Provider clearing | 4825 |
| Payout to merchant | Merchant payable | Bank | 4825 |

If the platform bears the fee instead, debit a fee-expense account in the fee step and the
merchant payable stays 5000. Check: provider clearing nets to zero after settlement
(5000 − 175 − 4825 = 0) and merchant payable nets to zero after payout (5000 − 175 − 4825 = 0). A non-zero
balance after the expected settlement date is a reconciliation alert.
Refund of $20.00 later: Debit merchant payable 2000 / Credit provider clearing 2000 (then
the cash movement when the provider returns funds to the customer). The original entries
are untouched.

## 3. Balance derivation

- Derived: `SELECT SUM(CASE direction WHEN 'C' THEN amount ELSE -amount END) ...` per
  account (sign convention depends on account kind).
- Cached: maintain `account_balance` updated in the same transaction as the entries, with
  a nightly job recomputing from entries and alerting on difference.
- Concurrency: if you enforce "balance must not go negative", use a locked row or
  conditional update per account (`transactions-consistency`).

## 4. Reconciliation design

Sources: (A) internal ledger/payment records, (B) provider transaction reports (per
charge/refund/fee), (C) provider settlement/payout reports, (D) bank statements.
Checks: A↔B per transaction (existence, amount, currency, status); B↔C fees and net
amounts per settlement batch; C↔D payout totals per date.

| Mismatch class | Example | Typical resolution |
|---|---|---|
| Missing internally | Provider shows a charge we never recorded (crash after charge) | Create the payment/ledger entries from provider data; notify |
| Missing at provider | We recorded a charge the provider never made | Mark failed; reverse ledger entries; investigate |
| Amount differs | Partial capture, FX, fee rounding | Post an adjusting entry with reason, or fix input |
| Status differs | We say captured, provider says refunded/disputed | Update state, post reversing entries |
| Duplicate | Two charges for one order | Refund one; root-cause idempotency gap |
| Timing | Settles next business day | Hold in "expected" until the window passes |

Process: ingest files idempotently (store file hash); normalize; match by provider reference
then by amount/date heuristics; produce a report with counts and amounts; auto-resolve safe
classes; assign the rest; track aging and resolution time; alert on unmatched amount above a
threshold or any growth.

## 5. Recovery job (stale payments)

```
every minute:
  for p in payments where state in (PROCESSING, UNKNOWN) and updated_at < now() - T:
      status = provider.query(p.provider_reference or p.idempotency_key)
      apply transition if status is definitive
      else escalate after N attempts
```

Query by the provider reference if you have it; otherwise by your idempotency key or
metadata. Never create a new charge from the recovery job.

## 6. Currency handling

- Store `amount_minor` (integer) and `currency` (ISO 4217). Know each currency's minor-unit
  exponent (not always 2).
- Round once, at defined points, with a documented mode; keep the unrounded rate used.
- FX: record base/quote currencies, rate, rate source, timestamp, and who bears the spread;
  settle in the currency the provider settles in; revalue only per accounting policy.

## 7. Webhook handler checklist

- [ ] Verify signature on the raw body (constant-time compare), reject old timestamps
- [ ] Persist event id before processing; skip duplicates
- [ ] Acknowledge quickly; process asynchronously
- [ ] Tolerate out-of-order events (apply by state machine rules, ignore stale)
- [ ] Unknown object → retry later (event may precede your commit)
- [ ] Alert on repeated failures; support replay from the provider's event log
