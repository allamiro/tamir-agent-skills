# Security Architecture Checklist

Mark each item `Y` (met, with evidence), `N` (gap → finding), or `N/A` (with reason).
Evidence is a file, config, diagram element, or test. Standards named here are starting
points; confirm current versions before relying on parameters.

## 1. Assets and trust boundaries

| Asset (data/function) | Classification | Where stored | Who may access | Boundary crossed |
|---|---|---|---|---|

Threat model (STRIDE per boundary): Spoofing, Tampering, Repudiation, Information
disclosure, Denial of service, Elevation of privilege. Record top threats, mitigation, owner.

| Threat | Boundary | STRIDE | Likelihood | Impact | Mitigation | Status |
|---|---|---|---|---|---|---|

## 2. Authentication

- [ ] Standard protocol for user login (for example OpenID Connect with authorization code + PKCE), not bespoke tokens
- [ ] Tokens validated for issuer, audience, expiry, signature algorithm allow-list
- [ ] Passwords hashed with Argon2id (or scrypt/bcrypt/PBKDF2 per current guidance), never fast hashes; per-user salt via the library
- [ ] Rate limiting and lockout/slowdown for credential stuffing; breached-password screening; MFA offered
- [ ] Service-to-service identity (mTLS or signed short-lived tokens), no shared static secrets
- [ ] Session/token lifetime, revocation and refresh rotation defined

## 3. Authorization

- [ ] Every endpoint enforces authorization server-side; default deny
- [ ] Object-level checks (the caller owns this record), not just role checks
- [ ] Tenant isolation mechanism named (row-level, schema, database, account) and tested with cross-tenant attempts
- [ ] Admin/support access is audited and time-limited

## 4. Data protection

- [ ] TLS everywhere externally (TLS 1.3 preferred, 1.2 minimum) and internally across trust boundaries
- [ ] Encryption at rest with managed keys; key rotation and access policy
- [ ] Secrets in a secret manager, not in code, images, or env files in repos
- [ ] PII inventory, retention limits, deletion path, masking in logs
- [ ] Backups encrypted and access controlled

## 5. API and request security

- [ ] Input validation and output encoding; parameterized queries
- [ ] Rate limits and quotas per identity; request size limits; timeouts
- [ ] CORS, CSRF (for cookie auth), security headers
- [ ] Request signing (HMAC-SHA-256+) includes method, path, body hash, timestamp and nonce; constant-time comparison; replay window
- [ ] Webhook receivers verify signatures and tolerate duplicates

## 6. Supply chain and runtime

- [ ] Dependency and image scanning in CI; pinned versions
- [ ] Least-privilege cloud roles; network segmentation; no public data stores
- [ ] Patch cadence defined

## 7. Detection and response

- [ ] Security-relevant events logged (auth, authz failures, admin actions) with tamper-resistant storage
- [ ] Alerts on anomalous access; incident runbook; contact path
- [ ] Audit log retention meets compliance

## 8. Result

Critical/High gaps: ______  Accepted risks (owner, expiry): ______
