# `api-networking`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Design the public API for an invoicing product. Compare REST and GraphQL, then cover pagination, idempotency, error format, versioning, and what belongs on the CDN and the load balancer.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 4,898 | 5,435 |
| Input tokens read across all turns (including cached context) | 30,373 | 72,795 |
| Extra input tokens when the skill is installed | | +42,422 |
| Cost, US dollars at list price | 0.157 | 0.238 |
| Skills invoked in the sample run | none | `api-networking` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 190 tokens for its name and description, which are in every session where the skill is installed, and about 3,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Invoicing product: public API design

**What I assumed:** the API is public JSON over HTTPS. The callers are third-party integrators (ERPs, accounting tools, e-commerce platforms), our own web and mobile apps, and webhook receivers. Most traffic is reads. The writes that matter are creating, finalizing and voiding invoices and recording payments, and each of those has real money consequences if it runs twice. The authentication design (API keys, OAuth scopes) is out of scope here.

## 1. REST or GraphQL

| What matters for invoicing | REST | GraphQL |
|---|---|---|
| Third-party integrators (the main audience) | Works with curl, any HTTP client and OpenAPI-generated SDKs | Integrators have to learn the schema and query language; client support is weaker in older ERP stacks |
| Safe retries of money operations | One `Idempotency-Key` per POST, which is simple | One request can carry several mutations, so idempotency has to be handled per mutation, which is awkward |
| Rate limiting and cost control | Count requests per endpoint | Needs query cost and depth analysis; one query can fan out to thousands of line items |
| Authorization | Checked per resource or route | Checked per field, which is easier to get wrong (for example a customer's tax ID reached through a nested field) |
| HTTP caching (for example a public "view invoice" page) | GET responses carry ETags and can be cached | Mostly POST, so it is not cacheable by default |
| Composite dashboard views | Takes several round trips, or needs `expand=` | One round trip that returns exactly the fields asked for |
| Webhooks and events | Event payloads can reuse the same resource shapes | No natural fit (subscriptions do not replace webhooks) |

**Decision: REST for the public API.** If our own dashboard later suffers from too many round trips, add a private GraphQL or backend-for-frontend layer for our apps only, built on the same domain services. For now, `?expand[]=customer&expand[]=lines` covers most over- and under-fetching.

## 2. Resource model (contract outline)

```
POST   /v1/customers                     GET /v1/customers/{id}   PATCH  DELETE
POST   /v1/invoices                      (creates a draft)
GET    /v1/invoices?status=open&customer=cus_123&created[gte]=...
GET    /v1/invoices/{id}
PATCH  /v1/invoices/{id}                 (drafts only; requires If-Match)
POST   /v1/invoices/{id}/lines           DELETE /v1/invoices/{id}/lines/{line_id}
POST   /v1/invoices/{id}/finalize        draft → open (gets a number, becomes immutable)
POST   /v1/invoices/{id}/send
POST   /v1/invoices/{id}/void            open → void
POST   /v1/invoices/{id}/payments        records a payment (full or partial)
POST   /v1/credit_notes                  (corrections to finalized invoices)
GET    /v1/invoices/{id}/pdf             → 302 to a short-lived signed URL
GET    /v1/events                        (backs webhooks and allows replay)
```

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Invoicing Product: Public API Design

## 1. REST vs. GraphQL

| Concern | REST | GraphQL |
|---|---|---|
| **Integrators** (accounting tools, ERPs, scripts) | Works with curl, any language and Zapier-style tools | Needs a client library, and is unfamiliar to many finance teams |
| **Mutations with side effects** (finalize, send, charge) | Map cleanly to `POST /invoices/{id}/finalize` | Possible, but they're RPC in disguise |
| **Idempotency** | `Idempotency-Key` per request is simple | Breaks down when one request batches several mutations |
| **Caching and rate limiting** | Per-endpoint cost, standard HTTP semantics | Needs query-cost analysis and depth limits; everything is `POST /graphql` |
| **Webhooks and events** | Payloads match REST resource shapes | Subscriptions are a poor fit for server-to-server use |
| **Versioning** | Explicit, and can be pinned per account | "Versionless" in practice means deprecating fields indefinitely |
| **Flexible reads** (a dashboard needing invoice + customer + payments) | Needs `expand[]` or several calls | Its strength |
| **Error semantics** | HTTP status codes, which proxies and LBs understand | Always 200 with an `errors[]` array |

**My recommendation: make the public API REST.** Use `expand[]` to cover the flexible-read case. If you want GraphQL, use it as a private backend-for-frontend behind your own dashboard, where you control the queries (persisted queries only). Money-moving APIs gain far more from predictable HTTP semantics than from query flexibility.

## 2. Resource model

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
