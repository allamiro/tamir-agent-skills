# Architecture Review Report: <system / proposal / repository>

Reviewer: ______  Date: ______  Scope and artifacts reviewed: ______
Not reviewed (and why): ______

## 1. Verdict

One paragraph: is the design fit for its stated requirements? Number of findings by
severity: Critical: 0, High: 0, Medium: 0, Low: 0, Questions: 0

## 2. Reconstructed architecture

*Mermaid diagram of what actually exists (from code/config/diagrams), not what the
document claims. Mark inferred parts as inferred.*

## 3. Severity rubric

| Severity | Criteria |
|---|---|
| Critical | Likely or certain data loss, security breach, or outage of a core journey, with no mitigation in place |
| High | Plausible within a year and large impact, or certain and moderate impact |
| Medium | Real risk or cost, contained blast radius or workaround exists |
| Low | Hygiene or clarity; fix opportunistically |

## 4. Findings

Every finding needs evidence. If there is no evidence it goes under "Questions".

### F-01: <short title>

- **Severity:** High    **Confidence:** high | medium | low
- **Evidence:** `path/file.py:123` | config key | diagram element | document sentence quoted briefly
- **Why it matters (potential impact):** concrete scenario with numbers where possible
- **Remediation:** specific change; smallest effective step first; effort S/M/L
- **How to verify the fix:** test or metric

*(repeat)*

## 5. Questions needing answers

| Q | Why it matters | Who can answer |
|---|---|---|

## 6. Unjustified complexity

| Component | Requirement it serves (or none) | Simpler alternative | Saving |
|---|---|---|---|

## 7. What is good

Decisions worth keeping, so they are not accidentally removed.

## 8. Prioritized plan

1. This week:  2. This quarter:  3. Watch list (with trigger metrics):
