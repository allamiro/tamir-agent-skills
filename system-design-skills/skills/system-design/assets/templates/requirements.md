# Functional and Non-Functional Requirements

Use at workflow step 2. Every row must be testable. Label anything you inferred as
`ASSUMPTION` and give the default you used. Unknowns that would change the architecture go
in "Open questions" with the decision they block.

## 1. System boundary

- In scope: <what this system owns>
- Out of scope: <what neighbours own>
- Actors: <end users, admins, other systems>
- External dependencies: <identity provider, payment processor, email provider, ...>

## 2. Functional requirements

| ID | Requirement (actor can <verb> <object>) | Priority (must/should/could) | Acceptance check |
|---|---|---|---|
| F1 | A shopper can place an order for items in stock | must | Order accepted once; stock decremented once; confirmation visible within 2 s |
| F2 | | | |

## 3. Non-functional requirements (each needs a number or a stated "unknown")

| ID | Quality | Target | Measured how | Source (stated / ASSUMPTION) |
|---|---|---|---|---|
| N1 | Availability of checkout | 99.9% monthly (43.2 min budget) | success ratio of checkout requests | ASSUMPTION |
| N2 | Latency, read path | p99 < 300 ms at peak | server-side histogram | stated |
| N3 | Durability of orders | no acknowledged order lost | restore drill result | stated |
| N4 | Consistency | stock never oversold; browse may be stale up to 30 s | oversell counter = 0 | ASSUMPTION |
| N5 | Security / compliance | PII encrypted at rest; audit log of admin actions | checklist | stated |
| N6 | Scale | peak 2,000 req/s, 5M users, 3-year growth 5x | see capacity worksheet | ASSUMPTION |
| N7 | Operability | on-call of 4 engineers; deploys daily; RPO 5 min, RTO 1 h | drill | ASSUMPTION |
| N8 | Cost ceiling | <budget>/month | billing | |

## 4. Constraints

Team size and skills, existing platforms, regulatory regions, deadlines, budget, vendor limits.

## 5. Workload shape (feeds the capacity worksheet)

Users, requests per user per day, peak-to-average factor, read:write ratio, object sizes,
retention. Traffic spikes: events, launches, batch jobs.

## 6. Open questions

| Question | Why it matters | Default if unanswered |
|---|---|---|
| Is overselling ever acceptable (backorders)? | Decides strict inventory locking vs eventual reconciliation | Not acceptable |
