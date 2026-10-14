---
name: accuracy-review
description: Audits Egyptological output for confident errors, checking that every sign reading, transliteration, gloss and translation has a source, a grade and a stated convention, and that uncertain readings are marked rather than smoothed over. Use for "check this transliteration", "review this annotation", "is this reading right", "audit my sign table", "what needs a citation". Use transliteration or text-annotation to produce the work and this skill to challenge it; use gardiner-sign-lookup to check one sign.
license: Apache-2.0
metadata:
  library: egyptology-skills
  version: "1.0"
---

# Accuracy review

## Purpose and activation

The biggest risk in this field is a wrong answer that sounds sure. This skill reviews finished
work, whether from an agent or a person, and returns findings ranked by how much they could
mislead. Activate before sharing, teaching with, or publishing any reading. It does not replace
an Egyptologist; it finds the places where one must look.

## Required inputs

The work to review (signs, transliteration, glosses, translation), the convention used, the sources
the author claims, and the intended use (class handout, database, publication). Ask for sign codes
if the review input is only a picture.

## Workflow

1. **List every claim.** Break the work into atomic claims: this sign has this value, this segment
   is one word, this word means this, this clause translates this way.
2. **Trace each claim to a source.** Source types, strongest first: primary publication or
   photograph; dictionary entry; sign list; grammar; the author's memory. A claim with only the
   last has no source.
3. **Re-derive the sign layer yourself** with `gardiner-sign-lookup` and `transliteration`, not
   from the author's table. Compare.
4. **Check consistency.** Same word glossed the same way; same convention throughout; brackets
   used with their stated meaning; no consonant counted twice.
5. **Look for smoothing.** Compare the translation with the word table; flag words that have no
   row, rows that have no word, and glosses chosen to make the sentence read well.
6. **Check calibration.** For each grade, ask what evidence supports it. Flag grades that rest on
   plausibility alone.
7. **Rank findings** using the severity scale below, each with evidence, impact and a fix.
8. **State what was not checked** (no photograph, no dictionary, no access to the original).

## Decision framework

| Severity | Meaning | Example |
|---|---|---|
| Critical | A wrong reading presented as certain, or an invented source | A sign value that disagrees with the sign list and no flag |
| Major | Unsourced claim that others will build on, or inconsistent convention | The same word glossed two ways |
| Minor | Presentation, missing page numbers, unlabelled convention | |
| Note | A choice a specialist may take differently | A smoother or more literal rendering |

## Implementation guidance

- The checklist is in `references/checklist.md`; use it for the claim-by-claim pass.
- Check values against the page image of a sign list, not OCR text: OCR corrupts diacritics.
- A claim stated "from memory" is a finding, even if correct, until a source is added.
- For a sign table, sample at random rather than reading from the top; errors cluster by
  section and by the person who typed them.

## Failure and edge cases

- Reviewing only what is flagged: the unflagged claims are where confident errors live.
- Anchoring on the author's reading; derive your own first.
- Treating a source's printed value as perfect: sign lists differ by edition and period.
- Accepting an LLM's own self-assessment of its confidence.
- Reviewing a translation that is plausible but unsupported by the words.
- Period mismatch: a Middle Egyptian value applied to a Late text.

## Validation

- Re-run the review on a sample with known errors (plant three wrong values) and confirm they are
  found.
- Report counts: claims checked, claims sourced, findings by severity, claims unverifiable.
- Falsifier: an error found after the review in a claim marked checked.

## Expected output

A review report: scope and what was not checked; counts; findings ranked by severity, each with
claim, evidence, impact and fix; a list of claims needing a specialist; and an overall statement
("safe for classroom use with the listed corrections", "not ready to publish").

## Sources and confidence

- Method (claim tracing, severity, calibration): own design; same shape as `system-design-review` in the sibling collection
- Gardiner sign-list pp. 438-441 (supplied) on the limits of the list, confusions in hieratic, and not "correcting" the Egyptians
- Source ranking: from author knowledge, adjust to the user's field norms
