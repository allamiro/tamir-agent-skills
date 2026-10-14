---
name: bioinformatics-review
description: Audits a finished bioinformatics analysis, pipeline, paper section or claim for errors that look fine, including missing null models, uncorrected multiple testing, leakage, batch confounding, pseudoreplication, genome-build or coordinate mix-ups, circular annotation, overclaiming from candidates, and results that cannot be rerun. Returns severity-ranked findings with evidence and a fix. Use for "review my analysis", "is this result trustworthy", "check this pipeline", "what is wrong with this figure", "can I publish this", "audit these methods". Use bioinformatics-workflow to plan before the work, reproducible-research-code to fix what the review finds, and the specialist skill for the step in question.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Bioinformatics review

## Purpose and activation

The worst error in this field is a clean-looking result that is wrong. This skill reviews finished
work, whether from a person or an agent, and returns findings ranked by how much they could
mislead. Activate before sharing, submitting, depositing or building on a result. It does not
replace the person who collected the data; it finds the places where they must look.

## Required inputs

The claim in one sentence; the methods or code; the data description and provenance; the figures or
tables the claim rests on; what the result will be used for; and what checks the author says were done.

## Workflow

1. **State the claim** as written, then as a falsifiable statement. If it cannot be falsified, that
   is the first finding.
2. **Trace each supporting number** to a script, input and parameter set. A number without a source
   in the record is unverified, even if correct.
3. **Check the null.** What does "no effect" look like here, and was it generated or only assumed?
4. **Count the tests.** Find every comparison made, including those not shown, and check the correction.
5. **Check the data layer:** accession and version, genome build, coordinate convention,
   identifiers, file format, and units (`sequence-formats`).
6. **Check the design:** replicates, batch, pairing, leakage between training and test data,
   pseudoreplication (`omics-data-analysis`).
7. **Rerun a piece.** Re-derive one or two numbers with an independent route, using the scripts in
   the specialist skills where they apply. Do not rely on the author's own table.
8. **Check the language.** Candidate is not gene; correlation is not interaction; similar is not
   homologous; significant is not large.
9. **Rank findings** with the scale below, each with evidence, impact and a fix
   (`assets/templates/review-report.md`).
10. **State what was not checked,** and which claims need an expert in the data type.

## Decision framework

| Severity | Meaning | Example |
|---|---|---|
| Critical | The conclusion is probably wrong, or a source is invented | Batch perfectly aligned with condition; test data used in training |
| Major | The conclusion may be wrong, or others will build on an unsupported number | No multiple-testing correction across thousands of tests |
| Minor | Reproducibility or clarity | Package versions missing; seeds not recorded |
| Note | A choice another analyst may make differently | Normalisation method |

The checklist for the claim-by-claim pass is in `references/checklist.md`.

## Implementation guidance

- Review the code and data as well as the text; the text describes intent, the code is what ran.
- Prefer a check that can fail: shuffle the labels and rerun, plant a known effect and see if it is
  found, convert a coordinate both ways.
- Quote the line, file or table cell behind each finding. A finding without evidence is an opinion.
- A claim stated "from memory" or "as is well known" is a finding until a source is added.
- Keep a count: claims checked, claims traced to a source, findings by severity, claims unverifiable.

## Failure and edge cases

- **Reviewing only what is flagged,** when the unflagged numbers are where the confident errors live.
- **Anchoring on the author's analysis** instead of re-deriving a piece independently.
- **Accepting a database annotation as truth.** Entries carry their sources' errors, and the
  source text lists database reliability as a topic in its comparison chapter.
- **Treating a tool's default as a justified choice.**
- **Missing the negative controls:** a method that finds the same thing in shuffled data.
- **Mistaking a long method list for rigour.**
- **Accepting a model's or a tool's own confidence** as evidence of correctness.
- **Review of a figure only,** without the data behind it.

## Validation

- Plant three known errors in a copy of an analysis (a shifted coordinate, a dropped correction, a
  swapped label) and confirm the review finds them. Plant them yourself so the reviewer does not know where.
- Report the counts so a reader can see how much was checked.
- Falsifier: an error found after the review in a claim marked checked.

## Expected output

A review report: scope and what was not checked; counts; findings ranked by severity, each with
claim, evidence, impact and fix; a list of claims needing a specialist; and an overall statement
such as "usable for hypothesis generation with the listed corrections" or "not ready to publish".

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed., ch. 1.2 (supplied text): the physical-science
  routine of assigning numbers and then manipulating them by public rules is often confounded in
  the biological sciences; ch. 13.4.1 (section title only): database reliability
- Review method (claim tracing, severity scale, planted-error validation): own design, with the
  same shape as `accuracy-review` in the sibling Egyptology collection and `system-design-review`
  in the System Design collection
- Checklist items: general practice from author knowledge, VERIFY against the standards of the
  user's field and journal
- Not covered: ethics and consent review, clinical validation, statistical power calculation
