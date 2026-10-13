# API contract checklist

Complete for every public or cross-team API. Each unchecked item is a design gap.

## 1. Resource and operation model

- [ ] Resources are nouns with stable identifiers (opaque, not sequential if enumeration matters)
- [ ] Each operation lists: method/verb, path or RPC name, request schema, response schema, success codes
- [ ] Safe (read-only) vs idempotent vs non-idempotent classification written down
- [ ] Bulk operations: maximum batch size, partial-failure semantics (all-or-nothing vs per-item results)
- [ ] Long-running operations return `202` plus a status resource; status has terminal states and expiry

## 2. Idempotency

- [ ] Unsafe operations accept an `Idempotency-Key` (client-generated, unique per logical operation)
- [ ] Server stores key → (request fingerprint, response) for a stated retention (for example 24 h)
- [ ] Concurrent same-key requests: second waits or receives `409` in-progress
- [ ] Same key with different payload is rejected
- [ ] Natural idempotency preferred where possible (PUT with client-chosen id)

## 3. Errors

- [ ] One error envelope for the whole API: code, message, details, correlation id
- [ ] Error codes are stable strings documented as part of the contract
- [ ] 400 vs 401 vs 403 vs 404 vs 409 vs 422 vs 429 vs 5xx chosen consistently
- [ ] `Retry-After` on 429/503; retryable vs non-retryable explicit
- [ ] No stack traces, SQL, internal hostnames in responses

## 4. Timeouts, limits and quotas

- [ ] Documented server timeout and recommended client timeout
- [ ] Request body size, array length, page size, query depth/cost limits
- [ ] Rate limit scope (per key, per user, per IP, per tenant), algorithm, headers returned
- [ ] Concurrency limits for expensive endpoints

## 5. Pagination, filtering and sorting

- [ ] Cursor-based for large/mutating collections; cursor is opaque and expires or is stable
- [ ] Default and maximum page size
- [ ] Sort keys are indexed and have a unique tiebreaker
- [ ] Filters are an allow-list; unknown parameters rejected or ignored by documented rule

## 6. Compatibility and versioning

| Change | Compatible? | Notes |
|---|---|---|
| Add optional response field | Yes | Clients must ignore unknown fields |
| Add optional request field/parameter | Yes | Default must preserve old behavior |
| Add new endpoint | Yes | |
| Add new enum value | Risky | Clients with exhaustive switches break; document "unknown enum" handling |
| Add required request field | No | Breaking |
| Remove or rename field/endpoint | No | Breaking |
| Change type, units or semantics | No | Breaking even if the schema looks the same |
| Tighten validation | Risky | Can reject previously valid requests |
| Change default sort or page size | Risky | |

- [ ] Versioning mechanism chosen (path, header, or additive-only evolution with sunset policy)
- [ ] Deprecation process: announce, add `Deprecation`/`Sunset` information, measure usage, remove after a stated period
- [ ] Contract tests run on every change; schema diff gates the pipeline

## 7. Security touchpoints (details in `identity-security`)

- [ ] Authentication scheme stated per endpoint; authorization checked per object
- [ ] TLS required; HSTS for browsers
- [ ] CORS policy explicit; CSRF considered for cookie auth
- [ ] Sensitive fields excluded from logs

## 8. Observability hooks

- [ ] Correlation id accepted/propagated/returned
- [ ] Per-endpoint latency, error rate and rate-limit metrics
- [ ] Deprecated-endpoint usage counter

## 9. Example (fragment)

```
POST /v1/orders
Idempotency-Key: 7c1f...         # required
Body: { "items": [ { "sku": "A1", "qty": 2 } ], "currency": "USD" }
201 Created  Location: /v1/orders/ord_91   -> order resource
409 Conflict  { "code": "idempotency_in_progress", ... }
422 Unprocessable { "code": "out_of_stock", "details": [ { "sku": "A1" } ] }
429 Too Many Requests  Retry-After: 2
```
