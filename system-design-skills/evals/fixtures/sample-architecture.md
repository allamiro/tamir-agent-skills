# Sample architecture for Scenario E (review exercise)

"ShopNow" runs an online store. Expected load: about 50 requests per second at peak,
roughly 300 orders per day. Availability target: "always up". Team: 5 engineers.

## Components

- **Gateway** (Node.js, 1 instance) terminates TLS and forwards to services. Rate limiting: none.
- **Catalog service**, **Cart service**, **Order service**, **Payment service**,
  **Notification service**: each a separate deployment on Kubernetes (single node pool in one
  availability zone). All five services use the same PostgreSQL instance (one primary, no
  replica) and may read and write each other's tables.
- **Cart service** stores carts only in Redis (no persistence configured, no replica).
- **Order service** writes the order row, then publishes `order.created` to Kafka (3 brokers,
  one zone). If publishing fails, it logs an error and returns success to the user.
- **Notification service** consumes `order.created` and sends emails, committing the offset
  after the email is sent. Messages are processed by 4 consumer instances; there is no
  deduplication.
- **Payment service** calls an external provider with `requests.post(url, data)` (no timeout)
  inside a `while True` retry loop with no sleep, until a 200 is returned. No idempotency key
  is sent.
- **Admin API** (`/admin/*`) checks that a user is logged in; any logged-in user can call it.
  Database passwords and the payment API key are in `config.yaml` committed to the repo.
- **Deployment**: pipeline builds and deploys all services at once on merge to `main`.
  Schema migrations run automatically at container start, including `DROP COLUMN` for
  removed fields. No rollback procedure is documented.
- **Backups**: nightly database dump to a bucket in the same zone. Restore has never been
  attempted.
- **Monitoring**: CPU and memory alerts on hosts only; logs are plain text on pod disks.
  No SLOs, no tracing.
- **Passwords**: stored as `sha256(password + salt)`; salt is a single constant stored in
  config.

## Stated requirements

1. Customers must never be charged twice.
2. Order confirmation emails should be sent once per order.
3. The store should survive a single server failure without downtime.
4. Cart contents should not be lost when a server restarts.
