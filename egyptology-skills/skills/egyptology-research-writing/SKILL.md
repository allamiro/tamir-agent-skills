---
name: egyptology-research-writing
description: Plans, drafts and revises Egyptological articles, text publications, theses and conference papers, covering journal choice, authorship and acknowledgements, the title and an introduction ending in a question, presenting a text or object (provenance, description, images and permissions, epigraphic method, conventions), keeping reading apart from interpretation, discussion against earlier editions, the abstract, cover letter, reviewer responses, rejection, and checking proofs with hieroglyphs and diacritics. Use for "help me write up this stela for publication", "outline my article", "which journal should I send this to", "write the abstract", "respond to the reviewer who disputes my reading", "my article was rejected", "check my proofs". Use egyptology-literature for references, edition-conventions for editorial marks, accuracy-review to audit readings, and provenance-research-ethics for object histories and image permissions.
license: Apache-2.0
metadata:
  library: egyptology-skills
  version: "1.0"
---

# Egyptological research writing

## Purpose and activation

An Egyptological publication has to let a specialist check every reading against the source, see which
parts are certain and which restored, and follow the argument from the evidence to the interpretation.
It also has to get through submission, review and proofs, where hieroglyphs and diacritics are easily
corrupted. This skill covers both the content and the craft. Activate when the user is writing, revising,
submitting or defending an article, a text publication, a thesis chapter or a conference paper.

## Required inputs

The source (text, object or corpus) with its museum number or findspot, images and their permissions;
the reading (transliteration, translation, commentary) and its conventions; the question and the main
finding; earlier publications of the source and the parallels; the target journal or series and its
instructions; the authors and contributors; and, for revisions, the reviews and the editor's letter.

## Workflow

1. **Decide the journal and audience** before drafting, and read its instructions for authors
   (`references/manuscript-craft.md` for the sequence from decision to proofs). Philological, archaeological,
   museum and general-humanities journals want different emphases.
2. **Agree authorship and acknowledgements:** who read and collated the text, who took the photographs, who
   gave access (usually an acknowledgement, not authorship), and who approves the final version.
3. **Write the claim ledger:** each claim about a reading, date, attribution or meaning, the evidence (sign
   forms, parallels, palaeography, context) and how certain it is. The certainty words follow `accuracy-review`.
4. **Present the source** with `assets/templates/text-publication-outline.md`: provenance and current location
   (`provenance-research-ethics`), physical description, images with permissions, the epigraphic method, and the
   transliteration and editorial conventions declared once (`edition-conventions`).
5. **Keep reading apart from interpretation:** transliteration and translation first, with restorations and
   doubts marked; commentary second; wider interpretation in the discussion.
6. **Discuss against earlier work:** where your reading agrees with or differs from earlier editions, why,
   and what a better source (a collation, a new photograph) would settle.
7. **Check every reference** with `egyptology-literature`, including plate and page numbers, then write the
   **abstract** last and a **title** that states the finding.
8. **Submit** with a cover letter, and after review answer point by point with `assets/templates/review-response.md`.
9. **Check proofs** for hieroglyphs, diacritics, line numbers and plate references against your own copy.

## Decision framework

| Situation | Choice |
|---|---|
| New text never published | A text publication: full presentation, transliteration, translation, commentary |
| New reading of a published text | Article focused on the passage, with the evidence for the new reading and the old one stated fairly |
| Object history or collection study | Museum or collection-history venue; provenance record from `provenance-research-ethics` |
| Broad interpretive argument | General or thematic journal; keep the philological detail in notes or an appendix |
| Images not cleared for publication | Do not submit until permission is in writing; describe and use a drawing if allowed |
| Reviewer disputes a reading | Answer with the sign-level evidence and parallels, concede where the evidence is weaker, mark the reading as uncertain if needed |

| Certainty of a claim | Wording |
|---|---|
| Signs clear and reading standard | State it |
| Signs damaged, restoration from parallels | "Restored after ...", marked with the declared brackets |
| Reading possible but not compelling | "Perhaps", with the alternative |
| Date or attribution from style alone | "On stylistic grounds, probably ..." |

## Failure and edge cases

- **Readings presented without the evidence a specialist needs to check them** (no image, no facsimile, no sign-level note).
- **Interpretation mixed into the translation.**
- **Earlier editions ignored or misrepresented,** including those in German or French.
- **Conventions changed silently** between transliteration systems or bracket keys.
- **Images used without permission,** or with a credit line the museum did not approve.
- **Authorship decided at submission,** or a contributor who never saw the final text.
- **Proofs approved without checking the hieroglyphs and diacritics.**
- **A recalled reference** with a guessed page number.

## Validation

- Every reading claim maps to a ledger row with its evidence and certainty, and the wording matches it.
- The conventions (transliteration scheme, bracket key) are declared once and used consistently.
- Every image has a written permission and the required credit.
- Every reference passes `egyptology-literature`'s checks or is marked for a librarian.
- Falsifier: a reviewer or reader who, from the published images, reads a sign differently and the
  article gave no grounds for the reading chosen.

## Expected output

The journal choice and outline; the claim ledger; drafted sections (presentation of the source,
transliteration and translation with marks, commentary, discussion, abstract, title); a permissions list;
a cover letter; and for revisions a point-by-point response.

## Sources and confidence

- Baker, "How to write your first paper", *Obstetrics, Gynaecology and Reproductive Medicine* 22(3):81–82,
  2012, doi:10.1016/j.ogrm.2011.12.003 (supplied text; record checked on Crossref 2026-10-15; © Elsevier, so
  paraphrased only): journal choice first, authorship early, section jobs, abstract last, cover letter,
  responses, rejection, proofs
- The structure of a text publication and the Egyptological adaptations: author knowledge, VERIFY against
  the target journal's instructions and recent text publications in it
- Not covered: book contracts, catalogue-raisonné formats, or copyright law beyond asking for permission
