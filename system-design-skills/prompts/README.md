# Prompts

One ready-to-paste prompt per skill. Swap in your own numbers, stack and constraints: the more
specific the prompt, the more specific the answer. Each prompt names the skill that should lead,
and `scripts/check_routing.py` checks that its wording matches that skill's description.

You never need to type a skill name. Describe the problem and the agent picks the skill.

## Which tool are these for

All of them. A prompt is plain text, so the same wording works in every tool that has the skills:
Claude Code ([`claude/`](../claude/README.md)), Codex and ChatGPT ([`openai/`](../openai/README.md)).
In ChatGPT, upload the zips first.

## Start here

### `system-design`

> Design the backend for a food-delivery app: 500,000 orders a day across 3 cities, a team of 8, and AWS. Give me a design doc with a diagram, a capacity table and ADRs for the hard decisions.

[Open the skill](../skills/system-design/SKILL.md)

## Numbers and shape

### `requirements-capacity`

> We expect 2 million daily users making 40 requests each, with a 4x evening peak and 5% writes. How many requests per second and how much storage per year do we need, and which availability target is realistic?

[Open the skill](../skills/requirements-capacity/SKILL.md)

### `architecture-scaling`

> Our monolith slows down at 1,200 requests per second. Should we split it into microservices, scale up, or do something else? Find the bottleneck before recommending anything.

[Open the skill](../skills/architecture-scaling/SKILL.md)

### `api-networking`

> Design the public API for an invoicing product. Compare REST and GraphQL, then cover pagination, idempotency, error format, versioning, and what belongs on the CDN and the load balancer.

[Open the skill](../skills/api-networking/SKILL.md)

### `identity-security`

> We are building a multi-tenant B2B SaaS where each customer brings its own single sign-on. Design authentication, authorization and tenant isolation, and give me a threat model.

[Open the skill](../skills/identity-security/SKILL.md)

## Data

### `database-selection`

> Pick a database for an order system with 185 writes per second, multi-row transactions, ad hoc reports and three years of growth. Compare PostgreSQL, MongoDB and DynamoDB.

[Open the skill](../skills/database-selection/SKILL.md)

### `transactions-consistency`

> Two customers can buy the last item at the same moment and we oversell. Which isolation level or locking should we use, and how do we test that it works?

[Open the skill](../skills/transactions-consistency/SKILL.md)

### `sharding-replication`

> Our PostgreSQL primary is at 75% write IO and growing 50% every six months. Do we need to shard? If so, which shard key, and what is the failover plan?

[Open the skill](../skills/sharding-replication/SKILL.md)

### `caching-performance`

> Our product page makes 10,000 reads per second against a database that handles 3,000. Design the cache, handle stampedes and invalidation, and show what happens if Redis goes down.

[Open the skill](../skills/caching-performance/SKILL.md)

### `storage-systems`

> Users upload videos up to 20 GB. Design the uploads, metadata, storage tiers and lifecycle rules, and compare replication with erasure coding on cost.

[Open the skill](../skills/storage-systems/SKILL.md)

## Flow and delivery

### `messaging-streaming`

> Order confirmation emails go out twice after consumers restart. Design the queue, retries, dead letters and idempotent consumers so each email is sent once.

[Open the skill](../skills/messaging-streaming/SKILL.md)

### `deployment-delivery`

> We need to rename a database column on a live service with zero downtime and a safe rollback. Plan the release, including a canary and the rollback triggers.

[Open the skill](../skills/deployment-delivery/SKILL.md)

### `reliability-resilience`

> A slow payment provider keeps taking checkout down through retry storms. Add timeouts, backoff, circuit breakers and a degradation plan for a 99.95% availability target.

[Open the skill](../skills/reliability-resilience/SKILL.md)

### `observability`

> Define SLOs and alerts for checkout so we stop getting paged on CPU. Include burn-rate alerts and a check for metric cardinality.

[Open the skill](../skills/observability/SKILL.md)

## Specialist domains

### `geospatial-design`

> Design nearby-restaurant search for 50 million places and 20,000 queries per second. Geohash or quadtree? Does the index fit on one machine?

[Open the skill](../skills/geospatial-design/SKILL.md)

### `payment-systems`

> Design card payments with a payment provider, a ledger and daily reconciliation. How do we avoid double charges when requests time out?

[Open the skill](../skills/payment-systems/SKILL.md)

## Review

### `system-design-review`

> Review the architecture in docs/architecture.md and the code under services/. Give me findings with evidence, severity, impact and a fix for each one.

[Open the skill](../skills/system-design-review/SKILL.md)
