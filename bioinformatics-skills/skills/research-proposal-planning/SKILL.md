---
name: research-proposal-planning
description: Turns a bioinformatics idea into a research plan, covering the question and whether it is exploratory or confirmatory, aims with success criteria, feasibility and risk, data sources and access, a data management plan with the FAIR principles and funder requirements, a schedule with critical path and buffer, roles and authorship credit, and a proposal or thesis outline. Use for "help me write a research proposal", "turn this idea into aims", "write a data management plan", "plan my thesis chapters", "is this project feasible in 6 months", "who should be an author", "what could go wrong with this project", "check my data management plan". Use experimental-design for sample size and layout, bioinformatics-workflow for the analysis plan, data-governance-ethics for consent and privacy, and research-writing-reporting for the paper.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Research proposal planning

## Purpose and activation

A project fails at the plan more often than at the code: the question is vague, the data are not
accessible, the schedule ignores the slow steps, or credit is never discussed. This skill turns an idea
into a plan that someone else can judge, with aims that can fail, a data plan, a schedule and a risk list.
Activate when the user is starting a project, a thesis, a grant or a collaboration, or has a draft plan to
check. It does not do the analysis (`bioinformatics-workflow`) or the sample-size calculation
(`experimental-design`).

## Required inputs

The idea in a few sentences; who it is for (thesis committee, funder, supervisor, team); the time, people,
compute and money available; the data the user has or hopes to get; known constraints (consent, access
agreements, funder rules); and any draft text.

## Workflow

1. **Write the question** in one sentence, and say whether the work is exploratory (generating hypotheses) or
   confirmatory (testing a stated one). For a confirmatory question, state the prediction and what result would
   change the plan.
2. **Check novelty and prior work** with `literature-search-appraisal`; note what already exists and the closest competitor.
3. **Check feasibility:** is the data obtainable (accession, access agreement, collection), is there enough
   of it (`experimental-design`), are the skills and compute available?
4. **Write two or three aims,** each with a measurable output, a success criterion, a method, the main risk and a
   fallback. Order them so a failed aim does not strand the rest.
5. **Plan the data:** sources and access route (`data-governance-ethics`), expected volume, storage and compute,
   formats and metadata, repository and timelines. Draft the data management plan (notes in `references/data-plan.md`) and check it:
   `python3 scripts/dmpcheck.py PLAN.md` (the `fair` profile gives a FAIR check).
6. **Build the schedule** as a list of tasks with durations and dependencies:
   `python3 scripts/schedule.py PLAN.csv --deadline WEEKS`. Read the critical path and the effect of a buffer.
7. **List risks** with likelihood, effect, early warning and response, and set decision gates where the plan
   can stop or change.
8. **Agree roles and credit early:** who does what, who is first author on what, and how contributions will be
   recorded (the CRediT roles are a standard vocabulary). Write down the authorship criteria the venue uses.
9. **Outline the document** for its audience (`assets/templates/proposal-outline.md`).
10. **Red-team the plan:** what would make the result uninterpretable (`bioinformatics-review`), and what is the
    cheapest experiment that would show the idea is wrong.

## Decision framework

| Project type | Emphasis | Typical risk |
|---|---|---|
| Reanalysis of public data | Data quality and metadata, batch structure | The data do not answer the question |
| New data generation | Design, samples, cost, lead times | Sample failure, delays, batch confounding |
| Method development | Benchmark design (`method-benchmarking`) | Overfit to the development data |
| Tool or pipeline build | Users, maintenance, tests | Scope creep, no adopters |
| Benchmark or review | Search or design protocol, neutrality | Bias in selection |

| Data plan item | Question |
|---|---|
| Access | Open, controlled or restricted, and who approves? How long does approval take? |
| Identifiers | Which accession and version, so the data can be found again? |
| Sharing | Which repository, what is shared, when, under which licence? |
| Preservation | How long, and who is responsible? |

## Implementation guidance

- Make each aim's success criterion testable by someone other than the author.
- The data management plan elements reported by university guides for the NIH Data Management and Sharing
  policy (effective for applications received on or after 25 January 2023) are data type; tools, software and code;
  standards; preservation, access and timelines; access, distribution or reuse considerations; and oversight.
  Check the funder's current template, because the checker only looks for keywords.
- The FAIR Guiding Principles (Wilkinson et al., Scientific Data 2016) group data practices as findable,
  accessible, interoperable and reusable.
- Estimate task durations from past work, add the slow steps (approval, sequencing queues, reruns), and keep a buffer.
  The default 30 percent in `scripts/schedule.py` is an illustration.
- Keep a changes log so the plan can be audited against what happened.

## Failure and edge cases

- **An aim that depends on a dataset not yet released** or an approval not yet granted.
- **Vague success criteria,** so nothing can fail.
- **Exploratory work presented as confirmatory** after the fact.
- **The slow steps missing from the schedule:** data cleaning, identifier mapping, approvals, reruns.
- **A data plan copied from a template** that names no repository, volume or timeline.
- **Compute and storage costs left out.**
- **Authorship and credit left until the paper is written.**
- **A plan with no stop conditions.**
- **Ethical and consent limits found late** (`data-governance-ethics`).

## Validation

- `python3 scripts/dmpcheck.py --selftest` and `python3 scripts/schedule.py --selftest` pass; the plan itself passes
  `dmpcheck.py` with no missing element and the schedule fits with its buffer.
- A colleague outside the project can state the question, each aim and its success criterion after one read.
- Every aim has a fallback and every risk an early warning.
- Falsifier: a project that stalled on a dataset, approval or tool that the plan did not list as a risk.

## Expected output

A plan: question and type, aims with criteria and fallbacks, data plan, schedule with critical path and buffer,
risk list with gates, roles and credit, and an outline for the target document, with the checker output attached.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: nothing in the supplied text covers project planning;
  this skill extends the collection to research work
- NIH data management plan elements and the 25 January 2023 start: university guides found in search results,
  2026-10-14; the NIH notice itself was not read: VERIFY. FAIR principles: Wilkinson et al., record checked on Crossref
  2026-10-14; the paper was not read. CRediT roles listed on CASRAI pages, 2026-10-14
- Aim structure, risk list and schedule method: own design, with critical-path arithmetic checked by self-test
- Not covered: budgets, grant-specific page limits, ethics board submissions, or the ICMJE authorship criteria (VERIFY)
