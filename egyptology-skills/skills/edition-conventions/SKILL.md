---
name: edition-conventions
description: Applies the editorial conventions of published editions of Egyptian texts, covering the Leiden-style marking of lacunae, restorations, emendations and uncertain signs, a declared key, the apparatus and notes, base witness and variants, evidence for a restoration, dating statements, and the transliteration standard agreed at Leiden in 2023. Use for "mark the damaged signs", "how do I show a restoration", "format this as an edition", "what do the brackets mean here", "which transliteration standard should I use", "restored from a parallel", "add an apparatus". Use transliteration for the sound reading, text-annotation for the interlinear layout, accuracy-review to audit a finished text, and egyptology-literature to find the parallels and editions.
license: Apache-2.0
metadata:
  library: egyptology-skills
  version: "1.0"
---

# Edition conventions

## Purpose and activation

An edition has to show four things apart: what is on the object, what is damaged, what the editor
supplies, and what the editor removes. Editorial marks do that, but the marks differ between
publications. This skill applies one declared key consistently, records the evidence behind each
restoration, and checks the mechanics. Activate when text is being prepared for a reader beyond the
person who made it. It produces a draft for an Egyptologist, never a published edition.

## Required inputs

The text (signs or transliteration); what is damaged or restored and why (a parallel, grammar, context,
space); the publication, series or journal to follow and its key; the transliteration scheme it requires;
whether a facsimile or photograph exists; and any other copies of the text.

## Workflow

1. **Choose the key.** If the target publication has one, use it exactly. If not, declare a key at the top
   (`python3 scripts/sigla.py key FILE` drafts one from what the text uses) and keep to it. Do not mix keys.
2. **Give every sign or word a status:** clear; preserved but doubtful; damaged but legible; traces only;
   lost; restored by the editor; supplied by the editor; erased in antiquity; superfluous; omitted by the
   scribe. `references/sigla.md` lists the classical marks for each.
3. **Record the evidence for each restoration:** a parallel (cite it), a grammatical need, the space available
   (state the number of signs only if it was measured on the object or a scaled image), or context.
4. **Mark the text** and run `python3 scripts/sigla.py check FILE` (add `--per-line` if each line must balance).
5. **Write the notes** (`assets/templates/apparatus.md`): one entry per doubtful reading, restoration or
   emendation, giving the lemma, the reading adopted, the alternatives, the evidence and its source.
6. **Handle witnesses.** If there is more than one copy, name the base witness, give the others sigla, and record
   variants in the notes. Keep the original inscription apart from later copies.
7. **State the transliteration scheme** used (see the notice on the 2023 standard below).
8. **Date with care.** Give a range, the criteria (orthography, palaeography, grammar, context) and the
   chronology used, because chronologies differ.
9. **Keep the translation separate** from the edition line, with supplied words marked in the way the key says.
10. **Hand off** to `accuracy-review` before the text is shared.

## Decision framework

| Evidence for a restoration | Present it as |
|---|---|
| A parallel with the same wording, cited | Restoration in the text, parallel in the note |
| Grammar or the formula demands a word but offers several | Gap marked, candidates in the note |
| Only an impression of what "should" be there | Leave the gap; do not restore |
| Traces visible on the object | Doubtful reading with a note, not a restoration |

| Question | Rule |
|---|---|
| Which key? | The publication's. If none, declare one and stay with it |
| Can brackets carry a second meaning? | No. One mark, one meaning, per key |
| Round brackets | Often words added for sense in a translation or an expansion; confirm in the key |
| Transliteration scheme | The one the publication or project requires, named in the edition |

## Implementation guidance

- The classical Leiden system was agreed at Leiden in 1931 for Greek and Latin texts, and the marks it fixes are
  the starting point here; Egyptological publications adapt them, so treat the table in `references/sigla.md`
  as a draft key, not as a statement about any given edition.
- Never complete a broken formula from memory without marking it as a restoration and naming the parallel.
  A formula that "feels familiar" is a lead, not evidence.
- Keep the edition, the apparatus and the translation in three visible layers.
- Keep Unicode brackets consistent and check that the font shows them; plain text can use `[[ ]]` for erasure.
- Declare the scheme, because transliteration conventions differ between projects and eras.

## Notice on transliteration standards

A page from the Netherlands Institute for the Near East (read 2026-10-14) reports that a workshop of
fifteen Egyptologists met on 8 August 2023 at the 13th International Congress of Egyptologists in Leiden,
produced a unified transliteration standard for the uniliteral signs, and that members of the International
Association of Egyptologists voted to accept it. The page lists no specific characters and names open
questions about diacritics (brackets and dots), capital letters and final weak radicals, with a working group
to continue. This collection's `transliteration` skill uses a conventional character set from author
knowledge. Which characters the new standard prescribes was not read: VERIFY from the standard itself, and
follow the scheme the target publication states.

## Failure and edge cases

- **A mark with the wrong meaning for the publication,** such as angle brackets used for a different purpose.
- **A restoration presented as a reading.**
- **A gap length counted from a drawing** or from memory.
- **Silent change of brackets** between the edition line and the translation.
- **Mixed glyph styles** for the same mark.
- **A restored formula taken from memory** without naming a parallel.
- **A transliteration scheme mixed within one text.**
- **A date given as a single year** with no criteria.
- **A key that is never printed,** so the reader cannot decode the marks.

## Validation

- `python3 scripts/sigla.py --selftest` passes, and `check` reports no errors on the marked text.
- Every restoration has a note with evidence, and every note's lemma appears in the text.
- The key is printed with the text and matches the marks used.
- Falsifier: a bracket the key does not define, or a restoration whose cited parallel does not contain the restored words.

## Expected output

The marked-up text; the key; the notes; a statement of the base witness and variants; the dating statement with
its criteria; the transliteration scheme; and a list of points for a specialist to check.

## Sources and confidence

- Classical Leiden marks, origin in 1931 and the remark that uses vary between fields: a Wikipedia page on the
  Leiden Conventions, read 2026-10-14; it does not discuss Egyptology
- Egyptological variants of the marks, apparatus layout and dating practice: from author knowledge, VERIFY
  against a current edition and the journal's guide
- The 2023 standard: the Netherlands Institute for the Near East page read 2026-10-14; the standard itself was not read
- Not covered: hieratic or Demotic editorial practice, digital markup such as TEI, or publication layout
