# Technology Selection Matrix

Use at workflow steps 5–6 for any "which X" choice (database, queue, cache, load balancer,
storage). Decide on requirements, not popularity.

## 1. Decision and hard requirements (gate)

Decision to make: <e.g. datastore for order history>
Hard requirements (a failing candidate is eliminated, not scored):

| ID | Hard requirement | Source |
|---|---|---|
| H1 | Multi-row ACID transactions | N4 |
| H2 | Runs on our managed platform | constraint |

## 2. Candidates

Always include: the simplest option the team already operates (baseline), the best-fit
specialist, and one in-between. Write why each candidate is credible.

## 3. Weighted scoring (only for candidates that pass the gate)

Weights sum to 100. Score 0–5 with a one-line justification and evidence link. Evidence is a
benchmark on your workload, vendor documentation, or "judgement". Judgement scores are
capped at 3.

| Criterion | Weight | Baseline | Candidate B | Candidate C | Evidence |
|---|---|---|---|---|---|
| Fit to top access patterns | 25 | 4 | 5 | 3 | query list |
| Consistency / transaction model | 15 | 5 | 2 | 4 | docs |
| Scalability at 10× load | 15 | 3 | 5 | 4 | capacity worksheet |
| Operational burden (on-call, upgrades, backups) | 20 | 5 | 2 | 3 | team survey |
| Team skill / hiring | 10 | 5 | 2 | 3 | |
| Cost at projected scale | 10 | 4 | 3 | 3 | |
| Lock-in / exit cost | 5 | 4 | 2 | 3 | |
| **Weighted total** | 100 | | | | |

## 4. Sensitivity

Change the two heaviest weights by ±10 points. Does the ranking change? If yes, the choice
depends on a value judgement; escalate it to the decider instead of hiding it.

## 5. Recommendation

Pick, runner-up, and the condition under which the runner-up wins. Record in an ADR.

## 6. Proof plan

Smallest spike that could falsify the choice (workload, dataset size, pass/fail number).
