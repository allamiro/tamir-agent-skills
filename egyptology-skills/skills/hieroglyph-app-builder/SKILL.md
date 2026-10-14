---
name: hieroglyph-app-builder
description: Designs and builds software that stores, searches, displays and exchanges Egyptian hieroglyphic text, covering the data model (sign, reading, attestation, text, line, word), Unicode and fonts, joiners and quadrat layout, right-to-left and column direction, search by Gardiner code or sound, MdC and JSesh import and export, and accessibility. Use for "build a sign database", "make a hieroglyph search app", "how do I render hieroglyphs on the web", "model a corpus of inscriptions", "import MdC". Use gardiner-sign-lookup for answering a single sign question and accuracy-review to check data quality.
license: Apache-2.0
metadata:
  library: egyptology-skills
  version: "1.0"
---

# Hieroglyph app builder

## Purpose and activation

Build a tool researchers can trust: a sign database, a corpus search, an annotation editor, or a
teaching app. The hard parts are modelling uncertainty, rendering, and exchange formats, not
screens. Activate for any software task involving hieroglyphs. Use `gardiner-sign-lookup` for
the sign facts the app will hold and `accuracy-review` to design its data checks.

## Required inputs

Who uses it (specialists, students, public); what they do (look up, search a corpus, annotate,
publish); data sources and their licences; platforms; offline needs; scale (hundreds or millions
of signs). If the licence of a source is unknown, treat it as restricted and ask.

## Workflow

1. **Name the main task** and pick the smallest app that does it: a static sign table, a search
   page over a file, a database-backed editor. Do not start with a full corpus platform.
2. **Model the data** with `references/data-model.md`: signs, readings, texts, lines, words and
   attestations, with a source and a confidence on every reading.
3. **Choose encodings.** Store the Gardiner code as the key and the Unicode character as a derived
   field; keep MdC as an import/export format. Handle variants and starred signs explicitly.
4. **Plan rendering** with `references/rendering.md`: font choice, joiners, quadrat layout,
   direction, and fallbacks when a font lacks a sign.
5. **Design search**: by code, by sound (transliteration), by category, by determinative; plan
   normalisation of transliteration letters so users can type them.
6. **Design import and export**: MdC strings, Unicode text, JSON, and CSV; round-trip tests.
7. **Record provenance** on every datum: where a value came from, which edition, who checked it.
8. **Plan accuracy checks** with `accuracy-review`: unit tests for the sign table, and a review
   workflow for new readings.
9. **Check licences** before shipping data or fonts. Do not ship scanned or OCR text of a book you
   have no right to redistribute; ship your own descriptions and Unicode data.

## Decision framework

| Need | Choose | Why |
|---|---|---|
| Show a few signs on a page | Unicode text plus a hieroglyph web font | No server |
| Complex quadrat layout, publication quality | An existing layout tool or JSesh export | Layout is hard; do not reinvent it |
| Search by sound or code | A small relational or JSON index | Simple, testable |
| Large corpus with annotations | Database with a normalized sign table and word table | Joins by sign code |
| Public access | Static site generated from a verified data file | Fewer moving parts |

## Implementation guidance

- Key signs by Gardiner code string (`D21`), not by code point; code points shift as Unicode adds
  characters and variants.
- Store a role per reading: uniliteral, biliteral, triliteral, ideogram, determinative, marker.
- Keep transliteration as Unicode text plus an ASCII search form (for example `ꜣ` also typed as
  `A`); the mapping table lives in one place.
- Direction: hieroglyphic writing runs in rows or columns, left to right or right to left; signs
  face the beginning of the line. Treat direction as data on the line, not a global setting.
- Joiner and layout controls exist in current Unicode; font support varies. Test fonts with a
  sample set before choosing one (`references/rendering.md`).
- Accessibility: provide the transliteration and a text alternative next to every glyph image, and
  do not rely on a font being installed.

## Failure and edge cases

- A font missing a sign shows a box and silently loses data. Detect it and show the Gardiner code.
- Round-tripping through MdC drops information the model holds (confidence, damage). Export
  with a sidecar file.
- Copy-pasted OCR from a printed sign list corrupts diacritics and glyph pictures.
- Search that treats ꜣ, ꞽ and ꜥ as the same letter returns wrong words; normalise on purpose.
- Mixing data from sources with different transliteration conventions.
- Presenting low-confidence data in the same style as verified data.

## Validation

- Unit tests: every sign code resolves to one Unicode character; no duplicate keys; the
  sign table's readings carry a source.
- Round-trip test: MdC to model to MdC on a set of strings.
- Render test on the target browsers with the chosen font.
- Reviewer test: show a specialist ten random records; count the ones they dispute.

## Expected output

A short design note: user and task, data model, encoding choices, rendering plan, search and
exchange design, licences, and a test plan; then the code or schema asked for.

## Sources and confidence

- Gardiner sign-list pp. 438-441 (supplied) on the limits of printed type and the need for facsimile
- Unicode code-point mapping: Unicode names via `gardiner-sign-lookup/scripts/signs.py`
- MdC syntax, JSesh behaviour, font support, joiner behaviour: from author knowledge, VERIFY against their documentation
- Not covered: OCR of hieroglyph images, handwriting recognition, hieratic
