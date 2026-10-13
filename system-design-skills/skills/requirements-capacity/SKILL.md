---
name: requirements-capacity
description: Turns a system idea into testable functional and non-functional requirements and a quantified workload - users, QPS and peak load, read/write ratio, storage growth, bandwidth, availability and downtime budget, latency budgets - using back-of-the-envelope formulas with units and sensitivity analysis. Use for capacity planning, "how many servers/how much storage", SLO targets, or when a design lacks numbers. Use architecture-scaling to act on the bottleneck it finds, observability for SLO measurement, and system-design for the full workflow.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Requirements and capacity estimation

## Purpose and activation

Produce the numbers every later decision depends on. Activate when requirements are vague,
when someone asks "will this scale", or at step 2-3 of `system-design`. Do not use it to
pick technologies (`database-selection`, `architecture-scaling`) or to design monitoring
(`observability`).

## Required inputs

Minimum: what users do, how many users, how often, how big the data is, how long it is kept.
If any is missing, assume, label `ASSUMPTION:`, and give a range (low / expected / high)
instead of one number. Ask a question only if the answer moves a result by more than 5×.

## Workflow

1. **List actors and use cases.** Fill `../system-design/assets/templates/requirements.md`
   sections 1-2. Each functional requirement is "actor can verb object" with an acceptance check.
2. **Write non-functional requirements with numbers** (section 3 of the same template):
   availability, latency percentile, durability, consistency, security, scale, recovery
   (RPO/RTO), cost. A quality with no number is a question, not a requirement.
3. **Define the workload shape**: daily active users (DAU), actions per user per day,
   peak-to-average factor, read:write ratio, object sizes, retention, growth horizon.
4. **Compute** with `python3 scripts/capacity.py --help`, or by hand using the formulas in
   [references/estimation-reference.md](references/estimation-reference.md). Fill
   `../system-design/assets/templates/capacity-worksheet.md`.
5. **Convert targets into budgets**: availability → downtime minutes; latency target →
   per-hop budget; storage → cost and backup time.
6. **Run sensitivity analysis**: scale each input ×2 and ×10 (the script's `--sensitivity`).
   Report which input dominates peak QPS and which dominates storage, and which assumption
   the design must survive being wrong by ×10.
7. **Find the first bottleneck**: compare peak figures to *measured* per-node limits. If a
   limit is unmeasured write `UNMEASURED` and put a load test in the plan. Hand the result
   to `architecture-scaling`.
8. **State scaling triggers**: metric + threshold + action (for example "primary CPU > 60%
   sustained for 1 h → add read replica or tune queries").

## Decision framework

| Question | Rule |
|---|---|
| Average or peak? | Provision for peak (average × peak factor); cost for average |
| Which peak factor? | Use observed traffic if any; otherwise state 2-5× as an assumption and test 10× in sensitivity. Event-driven systems (sales, launches) need explicit spike inputs |
| Mean or percentile latency? | Percentiles. Means hide tails; a request that fans out to n parallel calls is as slow as the slowest, so tail probability grows with n |
| Is precision needed? | No. One significant digit is enough to choose between architectures; need more only to size a purchase |
| Estimate or measure? | Estimate to decide the design; measure to size the deployment |

Availability budget (30-day window = 43,200 min; computed, not quoted):

| Target | Budget / 30 days | Budget / year |
|---|---|---|
| 99% | 432 min | 87.6 h |
| 99.9% | 43.2 min | 8.76 h |
| 99.95% | 21.6 min | 4.38 h |
| 99.99% | 4.32 min | 52.6 min |
| 99.999% | 0.43 min | 5.26 min |

Serial dependencies multiply availability (0.999 × 0.999 = 0.998). Parallel redundancy
gives 1 − (1 − a)^n only if failures are independent; shared deployments, configs and
regions make them correlated, so treat the formula as an upper bound.

## Architecture and implementation guidance

- Record every estimate as: formula, inputs with units, source tag, result, uncertainty.
- Keep read and write paths separate: they scale and fail differently.
- Fan-out systems (feeds, notifications): multiply writes by followers, then check storage
  and the *peak* of the fan-out burst, not the average.
- Bandwidth: bits vs bytes (×8); include replication traffic and backups.
- Connections: concurrent connections ≈ QPS × average request duration (Little's law);
  compare with pool and file-descriptor limits.
- Hardware numbers (disk IOPS, network, core counts) come from vendor specs or your own
  benchmark; do not reuse "latency numbers" from memory without checking.

## Failure and edge cases

- Seasonal or event spikes ignored by an annual average.
- Hot keys/tenants: a uniform-load estimate hides a single partition receiving 50% of traffic.
- Growth compounding: apply growth to DAU, not to storage alone; storage grows with
  cumulative data.
- Retries and thundering herds multiply load during incidents (a 3-layer × 3-try stack is
  up to 27 attempts); include an incident-load row.
- Dependency quotas (third-party rate limits, cloud API limits) cap the system below your math.
- Units: MB vs MiB, bits vs bytes, per-day vs per-second.

## Validation

- Re-derive one figure by a different route (for example peak QPS from concurrent users ÷
  think time) and reconcile within 2×.
- Compare with production metrics or a comparable system if they exist.
- `python3 scripts/capacity.py --selftest` confirms the calculator against a hand-computed
  example.
- Proof test: a load test at 1.5× expected peak with p99 inside budget. Falsifier: any
  per-node limit below the requirement.

## Expected output

A filled requirements table, a capacity worksheet (inputs, derived load, storage,
bandwidth, provisioning check, sensitivity, latency budget), and a bottleneck and scaling
trigger list. Worked example: [references/estimation-reference.md](references/estimation-reference.md).

## Sources and confidence

- Book (direct): none verified in the supplied text (estimation section printed p. 157-158 and scaling p. 55-57) — TOC-anchored only
- Book (synthesized): workload-first, assumptions-labelled workflow
- Modern: Little's law and availability arithmetic are standard queueing and probability results — from author knowledge, VERIFY wording if cited externally
- Needs workload validation: every input value, peak factor, per-node limits
