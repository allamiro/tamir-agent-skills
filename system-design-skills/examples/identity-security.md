# `identity-security`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> We are building a multi-tenant B2B SaaS where each customer brings its own single sign-on. Design authentication, authorization and tenant isolation, and give me a threat model.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 7,484 | 7,084 |
| Input tokens read across all turns (including cached context) | 30,369 | 72,891 |
| Extra input tokens when the skill is installed | | +42,523 |
| Cost, US dollars at list price | 0.209 | 0.271 |
| Skills invoked in the sample run | none | `identity-security` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 190 tokens for its name and description, which are in every session where the skill is installed, and about 3,300 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Multi-tenant B2B SaaS where each customer brings its own SSO: authentication, authorization, tenant isolation and threat model

**Assumptions** (tell me if any are wrong): web app plus a public API; customers' business data includes personal data (PII); shared infrastructure by default with an option to give large customers their own; customers connect Okta, Entra ID, Google Workspace or similar over OIDC or SAML; you run on a managed cloud with a key management service (KMS) and Postgres.

**The rule that matters most:** the tenant is always decided by *your* configuration (which SSO connection was used, or the verified domain). It is never decided by anything the customer's identity provider asserts or the request supplies.

---

## 1. Authentication

### 1.1 Working out the tenant before login
- **Primary:** a tenant-specific login URL (`acme.yourapp.com` or `/login/acme`). This selects exactly one SSO connection.
- **Secondary:** email-domain discovery ("enter your work email"). Only use domains the tenant has **proven it owns with a DNS TXT record**. Refuse public email domains (gmail.com, outlook.com), and don't let two tenants claim the same domain.
- Show the same discovery response whether or not a domain is known, so attackers can't enumerate which companies are customers.

### 1.2 SSO connections (one or more per tenant)
Store each connection as `{connection_id, tenant_id, protocol, issuer, client_id, encrypted client secret or IdP signing certificate, redirect/ACS URL, allowed domains, attribute mapping, status}`.

**OIDC (preferred):**
- Use the authorization code flow with PKCE, plus `state` and `nonce`. Redirect URIs must match exactly.
- Check the ID token's `iss` and `aud` against **this connection's** expected values, plus `exp`, `iat` and `nonce`. Accept only an allow-listed signing algorithm (RS256/ES256, never `none` or HS256 with a public key). Fetch signing keys from the IdP's key set (JWKS), cache them, and re-fetch when an unknown key ID appears.
- **Defend against IdP mix-up attacks**, which matter here because you have many IdPs. Give each connection its own redirect URI (`/sso/callback/{connection_id}`) and check the RFC 9207 `iss` response parameter. That way a response from IdP B can never be processed as if it came from connection A.

**SAML (needed for enterprise deals):**
- Use a mature, maintained library and never parse XML signatures yourself. Signature-wrapping attacks are the classic SAML failure.
- Require a signed assertion and verify it against the connection's pinned certificate.
- Validate `Audience`, `Recipient`/`Destination`, `NotBefore` and `NotOnOrAfter` (with a small, explicit clock-skew leeway), and `InResponseTo` for logins your app started.
- Cache assertion IDs until they expire so a replayed assertion is rejected.
- Decide on IdP-initiated login on purpose. If you allow it, it has no `InResponseTo`, so keep it off by default or tighten the replay checks.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Multi-tenant B2B SaaS with per-tenant SSO: authentication, authorization, isolation and threat model

## 0. Core rules

1. **A user's identity is `(tenant_id, idp_issuer, subject)`. Never match on email alone.** Each tenant controls its own IdP, so each tenant can make that IdP claim any email address. The most damaging failure in this kind of system is merging accounts across tenants by email.
2. **Tenant context comes only from the authenticated session.** Never take it from a URL, header or request body. If the request names a tenant, check that it equals the session's tenant and reject it if not.
3. **Tenant isolation is enforced at more than one layer:** the application, the database (row-level security), storage IAM, and encryption keys. A bug in one layer should not leak data.
4. **A tenant's IdP configuration is security-critical.** Changing it can take over every account in that tenant, so it needs the same protection as a root credential.

---

## 1. Authentication

### 1.1 Tenant discovery (home realm discovery)
- The main entry point is a tenant subdomain (`acme.app.com`) or an org slug. Email-domain discovery is a convenience on top of that.
- **Verify domains** with a DNS TXT challenge before a tenant can use a domain for discovery or to enforce SSO. A domain can be verified by only one tenant. Re-check it periodically and alert when it lapses.
- Never let an unverified domain route logins to a tenant's IdP.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
