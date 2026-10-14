---
name: egyptology-literature
description: Finds, reads, appraises and cites Egyptological scholarship, covering the main reference tools (the Wörterbuch and the Thesaurus Linguae Aegyptiae, the Topographical Bibliography, the Online Egyptological Bibliography, the Lexikon der Ägyptologie, Gardiner's grammar), how to tell an edition from a translation, commentary or handbook, how old an interpretation is, and how to cite without inventing references. Use for "find literature on this text", "where is this monument published", "how do I cite this", "is this translation still current", "check these references", "read this article for me", "which dictionary lists this word". Use accuracy-review to audit readings, text-annotation to prepare a text, edition-conventions for editorial marks, and provenance-research-ethics for object histories.
license: Apache-2.0
metadata:
  library: egyptology-skills
  version: "1.0"
---

# Egyptological literature

## Purpose and activation

Egyptological references are long, abbreviated and in several languages, which makes an invented
one easy to write and hard to spot. This skill finds the right kind of source for a question, reads
it for the specific claim, records how the source was known, and cites it so a specialist can find it.
Activate when a statement needs a reference, when the user asks where something is published, or when
a reference list must be checked. It does not translate texts (`text-annotation`) and does not decide
whether a reading is right (`accuracy-review`).

## Required inputs

The target (sign, word, grammar point, text, monument or object, site, period or topic); what the user
already has (a reference, a museum number, a photo, a quotation); what the answer will be used for; the
languages the user reads; and which databases the user can open (some are subscription services).

## Workflow

1. **Classify the target** and choose the tool from `references/reference-tools.md`.
2. **Search under every form of the name.** Egyptological names, titles and transliterations have
   several conventional spellings, and the literature is in English, German and French. Record each
   variant searched.
3. **Prefer the edition.** For a text or object, the publication with the facsimile or photograph and
   the transliteration comes before a translation, a handbook or a popular account.
4. **Check the age and standing of the source.** Note the publication date, whether a newer edition or
   a correction exists, whether reviews dispute it, and whether the reading it gives is the current one.
5. **Read for the claim.** Take the specific reading, meaning, date or attribution, and note whether the
   author states it as certain or as restored or probable.
6. **Record how you know each source** as `read` (opened and read), `seen` (a secondary source cites it) or
   `recalled` (from memory, so unverified). Give a page, plate, line or entry number only if you saw it.
7. **Cite** in the style the target journal or institution requires, using
   `assets/templates/citation-record.md` for the details. Run `python3 scripts/citecheck.py LIST --online`
   on references with a DOI; check books, monographs and database entries by hand.
8. **Report** the answer, the sources table with their marks, what could not be reached, and what the user
   must look up (for example in a subscription database).

## Decision framework

| You want | First stop | Then |
|---|---|---|
| A sign value or sign form | The sign list in Gardiner's grammar (`gardiner-sign-lookup`) | The grammar section it points to |
| What a word means and where it occurs | The Wörterbuch and the Thesaurus Linguae Aegyptiae | A specialised dictionary for the period or genre: VERIFY |
| Where a monument, relief, statue or painting is published | The Topographical Bibliography, by site | The cited edition |
| What has been written recently on a topic | The Online Egyptological Bibliography | The articles it lists |
| Background on a topic or person | The Lexikon der Ägyptologie | The bibliography it ends with |
| A text edition | The edition for that text, found through the above | Reviews of the edition |

| Source type | Weight | Check |
|---|---|---|
| Edition with facsimile or photograph | High for the readings shown | Collation quality, date, reviews |
| Translation without edition | Medium | Which edition it translates |
| Commentary or monograph | High for argument, varies | Date, whether it is contested |
| Handbook or encyclopedia entry | Lead only | The sources it cites |
| Database record | Depends on the record | Its own source note and date |
| Web page without a named source | Low | Find the primary publication |
| Your recollection | None | Look it up |

## Implementation guidance

- A `recalled` reference is a lead. State it as "reported in the literature, to be checked", never as a citation.
- Quote a transliteration exactly as printed, with its diacritics, and name the scheme the source uses
  (`edition-conventions`).
- Databases move and change; give the date accessed and the entry identifier.
- Keep a list of what you could not open, so the user knows where the answer is thin.
- Citation form varies by journal, so a neutral record is kept first and formatted last.

## Failure and edge cases

- **An invented reference** with a plausible journal, volume and pages. Treat every `recalled` reference as unverified.
- **Citing a translation as if it were the edition.**
- **An old reading presented as current,** or a disputed reading presented as settled.
- **Searching under one spelling** and concluding nothing exists.
- **Citing a database as authority** for a reading it only reports.
- **Missing non-English literature.**
- **Page numbers recalled from memory.**
- **Treating a museum label or catalogue entry as a scholarly publication.**
- **No access to the paywalled source.** Say so and mark the claim `seen`.

## Validation

- Every reference carries a `read`, `seen` or `recalled` mark, and no `recalled` reference is presented as a citation.
- `python3 scripts/citecheck.py --selftest` passes, and `--online` returns no `DOI-NOT-FOUND` or `MISMATCH` on the list.
  A pass means the record matches the line; it does not mean the article says what is cited.
- Each claim can be traced to a page, plate or entry that someone saw.
- Falsifier: a reference that a librarian cannot find, or a quotation that is not on the page cited.

## Expected output

A short answer; a sources table (reference, type, mark, what it supports, date); a list of what could not
be reached; the search variants used; and a formatted bibliography only after the checks above.

## Sources and confidence

- Reference tools: the Thesaurus Linguae Aegyptiae (a joint project of the Berlin-Brandenburg and Saxon
  academies, free online), the Topographical Bibliography (Griffith Institute, Oxford; volumes 1 to 7 by
  location and volume 8 for objects of unknown provenance) and the Online Egyptological Bibliography
  (successor to the Annual Egyptological Bibliography, subscription) were checked through search results on
  2026-10-14; the sites themselves were not opened
- Wörterbuch der ägyptischen Sprache: sources disagree on the number of volumes and the dates of the reference volumes, so give no
  volume counts without checking: VERIFY
- Lexikon der Ägyptologie and journal conventions: from author knowledge, VERIFY
- Gardiner's grammar: see the collection README for the edition used
- Not covered: reading hieratic or Demotic, dating methods, or the legal status of objects
