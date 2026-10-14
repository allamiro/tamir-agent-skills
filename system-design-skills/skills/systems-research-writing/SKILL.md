---
name: systems-research-writing
description: Plans, drafts and reviews systems research papers, theses, proposals and technical reports, covering claim-first structure, the contribution list, related work, the evaluation write-up, limitations and threats to validity, artifact and reproducibility statements, authorship and AI-use disclosure, reviewing someone else's paper, and rebuttals. Use for "outline my systems paper", "write the evaluation section", "review this paper for a conference", "respond to the reviewers", "what are the threats to validity", "prepare an artifact", "turn this internal report into a paper", "is my contribution clear". Use performance-evaluation-methodology to design the experiments, systems-literature-reading for related work, system-design-review to critique an architecture rather than a paper, and system-design for new architectures.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Systems research writing

## Purpose and activation

A systems paper stands or falls on whether each claim is backed by evidence a reviewer can check.
This skill structures that link, helps write each section, and does the reverse job when the user
is the reviewer. Activate when the user is writing for a conference, journal, thesis, grant or technical
report, or reviewing or answering a review. For an architecture or design document that will not
be published, use `system-design`; to critique an existing architecture, use `system-design-review`.

## Required inputs

The audience and venue (call for papers, page limit, double-blind or not); the work itself (system,
design, results); the claims the authors want to make; the experiments and their data; related work
the authors already know; for a review, the manuscript and the venue's review form; for a rebuttal, the
reviews and the word limit.

## Workflow

Writing:

1. **Write the claim in one sentence,** then at most three contributions, each falsifiable. Fill the
   matrix in `assets/templates/claims-evidence.md`: contribution, the experiment or argument that
   supports it, the figure or table, and the limit of the claim.
2. **State the problem and the insight.** Why do existing approaches fail, shown with a measurement or
   a precise argument, and what is the one idea that changes it.
3. **Outline** (adapt to the call): abstract; introduction with problem, insight, contributions and
   headline results; background or motivation; design; implementation; evaluation; related work;
   limitations and discussion; conclusion.
4. **Write the evaluation as questions:** each experiment answers a stated question, with setup,
   workload, baselines, metric, runs and variance, an ablation, a sensitivity study, overheads and
   failures. Take the plan from `performance-evaluation-methodology`.
5. **Write related work as a comparison** along the axes that matter (assumptions, guarantees, cost),
   not as a list. Find and check the sources with `systems-literature-reading`, including its citation checker.
6. **Write limitations and threats to validity** in three groups: internal (could something else explain
   the result), external (does it generalise), and construct (does the metric measure what is claimed).
7. **Prepare the artifact:** code, configuration, scripts, raw data, environment description and a
   one-command run, placed in a permanent public repository if the venue awards an "available" badge.
8. **Record contributions and tool use:** who did what (the CRediT roles are a standard vocabulary) and
   any generative-AI use, following the venue's policy.

Reviewing:

9. **Summarise the paper's claims in your own words** before judging; if you cannot, say what is unclear.
10. **Judge** significance, novelty, soundness, evaluation and clarity; list major concerns first, each
    with the page or figure and what would resolve it; then minor points and questions for the authors.
11. **Give a recommendation with your confidence,** and say which parts you are not expert in
    (`assets/templates/review-and-response.md`).

Responding:

12. **Answer each point,** grouped by reviewer concern: agree and change, clarify, disagree with evidence,
    or cannot address (say why). Do not introduce claims the paper does not support.

## Decision framework

| Reviewer concern | Typical response | Do not |
|---|---|---|
| Missing baseline | Run it, or explain why it is not comparable, with evidence | Dismiss it |
| Weak evaluation | Add the experiment and show the number | Promise results you have not seen |
| Novelty unclear | Compare against the closest prior work on the axes that differ | Attack the reviewer |
| Claim too strong | Narrow the claim in the text | Defend wording with adjectives |
| Misunderstanding | Point to the section and fix the clarity problem | Blame the reader |

| Venue artifact badge | What it generally requires | Check |
|---|---|---|
| Artifacts available | A permanent public archive, not only a personal or code-hosting page | The venue's rule |
| Artifacts evaluated | A reviewer ran it and found it functional or reusable | The criteria in the call |
| Results reproduced or replicated | Another team (or setup) obtained the results | The badging version; the two terms swapped meaning between ACM versions 1.0 and 1.1 |

## Architecture and implementation guidance

- Put the claim and the number it rests on in the abstract and the introduction; every number there must
  appear, with its setup, in the evaluation.
- Replace adjectives with measurements ("faster" becomes "1.4 times the throughput at p99 200 ms, 5 runs").
- Say what the system cannot do and where the design assumptions break.
- Use one name per concept and define it once.
- Report negative and surprising results that bear on the claim.
- Reviewing: a confidential manuscript is not yours to paste into external tools, so check the venue's
  reviewer policy first: VERIFY.
- Check every reference with `systems-literature-reading` before submission.

## Failure and edge cases

- **Contributions that are components, not claims** ("we built a scheduler").
- **An evaluation that answers a different question** from the introduction's.
- **A weak or untuned baseline** used to make the new system look good.
- **Related work that is a list,** or that omits the closest competitor.
- **Silent scope growth in a rebuttal,** adding experiments that change what the paper claims.
- **Self-plagiarism or recycled text** across papers without disclosure.
- **Invented or unchecked references.**
- **Undisclosed AI assistance** where the venue requires disclosure.
- **A review that judges the paper the reviewer would have written.**

## Validation

- Every contribution maps to at least one experiment or argument, and every figure is cited in the text.
- Each number in the abstract can be found in a table, with its setup.
- Every reference passes `systems-literature-reading`'s checker, or is marked as unverified.
- A reader outside the sub-area can state the claim after the introduction.
- Falsifier: a reviewer's major concern that the manuscript did not mention as a limitation.

## Expected output

An outline with the claims-evidence matrix; drafted sections with placeholders for missing numbers;
a limitations and threats list; an artifact checklist; or, for review and rebuttal, a structured
review or a point-by-point response with the changes made.

## Sources and confidence

- Book (direct): none; this skill extends the library to research work and is not taken from the book
- Book (synthesized): none
- Modern: Levin and Redell (1983, reprinted 1988) and Smith, *The Task of the Referee* (IEEE Computer, 1990), records fetched from Crossref 2026-10-14, content from author knowledge, VERIFY; ACM Artifact Review and Badging pages read in part 2026-10-14 (version 1.1 swaps the meanings of "reproduced" and "replicated", and "available" needs a permanent public archive); 14 CRediT roles from CASRAI pages 2026-10-14; the ACM authorship policy page says generative AI tools cannot be authors and use must be disclosed, while one conference page read the same day says otherwise, so read the venue's current policy
- Needs workload validation: the venue's call, page limit, review form, badge rules and AI policy decide the details; not covered are formal proofs, statistics (`performance-evaluation-methodology`) and venues outside ACM
