# `research-writing-reporting` prompts

Write up computational work so it can be checked and reused, with wording that matches the evidence.

- **Give it:** the audience and venue, the claims, the methods record, the figures, any reviewer
  comments, and the journal's reporting rules
- **Skill file:** [`skills/research-writing-reporting/SKILL.md`](../skills/research-writing-reporting/SKILL.md)
- **References:** [`claim-wording.md`](../skills/research-writing-reporting/references/claim-wording.md) and
  [`reporting-checklist.md`](../skills/research-writing-reporting/references/reporting-checklist.md)
- **Templates:** [`methods-section.md`](../skills/research-writing-reporting/assets/templates/methods-section.md) and
  [`data-availability.md`](../skills/research-writing-reporting/assets/templates/data-availability.md)
- **Audit first with:** [`bioinformatics-review`](bioinformatics-review.md)

## 1. A methods section

> Write the methods section for this analysis from my methods record: <paste>. Use exact versions and parameters, and list anything the record does not give me so I can fill it in.

A good answer: a methods draft built only from the record, with every missing version, parameter or
accession listed as a gap instead of invented.

## 2. Match the wording to the evidence

> Rewrite this sentence so that it matches the evidence: "We identified 120 novel genes." The evidence is open reading frames of at least 100 codons that have no match in the database release we searched.

A good answer: it says "predicted", names the method and the release, and does not call them genes
or novel without independent support.

## 3. Availability statements

> Write the data and code availability statement for reads deposited under <accession> and code at <URL>, version <tag>. The data are controlled-access human data.

A good answer: the repository and accession, the access route and terms, the code location with a
permanent identifier for the version, and what is not shared and why.

## 4. A reviewer on statistics

> A reviewer says our multiple-testing correction is inadequate. Draft a response that includes a new analysis and says what changed.

A good answer: it concedes what is right, reruns the analysis with the stated correction, reports the
result whatever it is, and updates the text and figures.

## 5. An honest figure

> Review this figure description for hidden problems: <paste>. Check axes, n, what the error bars show, and any transformation or cropping.

A good answer: a list of missing or misleading elements, such as an unstated n, an unlabelled
transformation, or an axis that exaggerates a difference.

## 6. A plain-words summary

> Explain our result to a non-specialist in three sentences: the claim, the evidence, and the main caveat.

A good answer: a claim at the right evidence level, one sentence on what supports it, and one caveat
taken from the review findings.

## 7. From journal choice to proofs

> This is my first paper: a differential expression study of a drug response in mouse liver. Which journal should I aim for, who should be an author, and what happens after I submit, including if it is rejected?

A good answer: choose the journal before writing, because its audience decides the emphasis (a methods
journal, a biology journal or a pharmacology journal), and read its instructions for authors. Agree
authorship early by the venue's criteria, with access or sample providers acknowledged rather than listed
as authors. Write the abstract last, and send a cover letter once all co-authors have approved. Answer
reviews point by point; after a rejection, revise on the constructive comments and resubmit to the planned
next journal. At proofs, correct errors only.
