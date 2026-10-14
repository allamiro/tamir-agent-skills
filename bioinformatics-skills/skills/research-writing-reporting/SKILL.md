---
name: research-writing-reporting
description: Writes up bioinformatics research so it can be checked and reused, covering methods sections, figure and table practice, claim wording matched to the evidence, data and code availability statements, citing software and databases, preprints, journal choice, authorship, cover letters, reviewer responses, rejection and proofs, and reporting checklists. Use for "write my methods section", "how should I phrase this result", "data availability statement", "respond to a reviewer comment on the statistics", "what must I report for a sequencing study", "make this figure honest", "summarise this analysis for a non-specialist", "which journal should I submit to", "my paper was rejected". Use bioinformatics-review to audit the work first, reproducible-research-code for the methods record, and biological-databases for citing data.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Research writing and reporting

## Purpose and activation

Turn a finished analysis into text, figures and statements that say exactly what was done and
exactly as much as the evidence supports. Writing is where an analysis gets overclaimed, and where a
missing version or a vague phrase makes a result unrepeatable. Activate when the user is writing,
revising or answering reviewers about computational work, or summarising it for others.

## Required inputs

The audience and venue (journal, report, grant, lab meeting, non-specialists); the claims the work
rests on; the methods record (data with versions, software with versions, parameters, seeds,
statistics); the figures and tables; reviewer comments, if any; and the journal's reporting rules.

## Workflow

1. **Choose the journal and settle authorship first.** The journal decides the audience and emphasis; read
   its instructions for authors, agree who is an author and who is acknowledged, and plan the next journal in
   case of rejection (`references/manuscript-craft.md` takes a paper from that decision to the proofs).
2. **Build a claims ledger.** One row per claim: the sentence, the figure or table it rests on, the
   script that produced it, the data, and the evidence level. A claim without a row is not ready to
   be written.
3. **Write the methods from the record,** not from memory: data sources with accessions and versions,
   reference build, software with versions and parameters, the statistical tests and the correction
   for many tests, exclusions and why (`assets/templates/methods-section.md`).
4. **Match the wording to the evidence** with the ladder in `references/claim-wording.md`. A candidate
   gene is not a gene, a correlation is not an interaction, and a significant difference is not a
   large one.
5. **Make the figures honest:** label axes with units, show individual points when the sample is
   small, show uncertainty, state n and what it counts, and say what any transformation or
   clipping did.
6. **Write the availability statements:** where the data are, under what access terms, where the
   code is, which version, and a permanent identifier for a snapshot (`assets/templates/data-availability.md`).
7. **Cite what was used:** the datasets by accession and version, the software by name and version,
   the databases by release, and the methods papers.
8. **State limits** in the discussion, from the review findings, not in a generic closing line.
9. **Write the abstract last** in the journal's format, and send a short cover letter once every co-author
   has approved the final version.
10. **Answer reviewers** by conceding what is right, rerunning what is in doubt, and showing the new
   result, not by restating the original text. After a rejection, revise on the constructive points and
   resubmit elsewhere.
11. **Check the text against the ledger** one last time, and again at the proofs, where only corrections are allowed.

## Decision framework

| Situation | Choice |
|---|---|
| Result passes only before correction | Report it as exploratory, with the correction stated |
| Evidence is a prediction | Say "predicted", name the method, and give its confidence |
| Effect is statistically significant but small | Give the effect size and say whether it matters |
| A reviewer asks for a new analysis | Run it, report the result whatever it is, and say what changed |
| Data cannot be shared | Say why, state the access route, and share code and summary statistics if allowed |
| Software has no paper | Cite the repository, version and date |
| Non-specialist audience | State the claim, the evidence and the main caveat in plain words |
| Someone only provided samples, access or routine help | Acknowledgement, unless they meet the venue's authorship criteria |
| Paper rejected | Revise on the constructive comments, agree the next journal with co-authors, resubmit |

## Implementation guidance

- Keep one source of truth for numbers: figures and tables come from scripts, and the text quotes them.
- Give exact versions and parameters, even for defaults; defaults change.
- Report the number of tests, the number of samples per group and any that were excluded.
- Put the genome build and annotation release in the methods, not only in a supplement.
- `references/reporting-checklist.md` lists what to report by type of study.

## Failure and edge cases

- **Methods that cannot be rerun:** no versions, no parameters, "standard settings".
- **Wording stronger than the evidence:** "shows", "proves", "identifies" for a candidate or a correlation.
- **Uncorrected multiple testing** hidden in a supplementary table.
- **Figures that hide n,** or axes cropped to exaggerate a difference.
- **"Data available on request"** as the only statement.
- **Software and databases not cited,** or cited without versions.
- **A reviewer's point answered rhetorically,** not with an analysis.
- **Numbers in the text that differ from the figure** because they came from different runs.
- **Supplementary results that contradict the main claim,** left unmentioned.
- **Authorship settled at submission,** or a co-author who never saw the final version.

## Validation

- Every sentence of result in the draft maps to a row of the claims ledger.
- The methods section lists every input with a version, and every tool with a version.
- A colleague can rerun the main analysis from the methods and availability statements alone.
- Falsifier: a number in the text that does not match a regenerated figure.

## Expected output

The claims ledger, the methods section, the results wording at the right evidence level, figure
notes, the availability statements, the citation list, and for reviews a point-by-point response.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed., ch. 1.2 (supplied text): in biology the usual
  scientific routine of assigning numbers and manipulating them by public rules is often confounded,
  which is why the origin of every number needs reporting
- Reporting practice, wording ladder, checklists, journal expectations: general practice from author
  knowledge, VERIFY against the target venue's instructions and any reporting guideline for your
  study type
- Baker, "How to write your first paper", *Obstetrics, Gynaecology and Reproductive Medicine* 22(3):81–82,
  2012, doi:10.1016/j.ogrm.2011.12.003 (supplied text, paraphrased; record checked on Crossref 2026-10-15):
  journal first, authorship early, the job of each section, abstract last, cover letter, responses,
  rejection and proofs
- Not covered: grant writing, patents, authorship disputes and publication ethics in detail
