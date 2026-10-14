# `hieroglyph-app-builder` prompts

Design and build software that stores, searches, shows and exchanges hieroglyphic text. The hard
parts are modelling uncertainty, rendering and exchange formats, so the prompts ask for those first.

- **Give it:** who uses the app, what they do in it, your data sources and their licences, your
  platforms, and the scale
- **Skill file:** [`skills/hieroglyph-app-builder/SKILL.md`](../skills/hieroglyph-app-builder/SKILL.md)
- **References it uses:** [`data-model.md`](../skills/hieroglyph-app-builder/references/data-model.md)
  and [`rendering.md`](../skills/hieroglyph-app-builder/references/rendering.md)
- **Sign facts come from:** [`gardiner-sign-lookup`](gardiner-sign-lookup.md) ·
  **Data checks come from:** [`accuracy-review`](accuracy-review.md)

## 1. A whole small app

> Design a small web app where students look up a hieroglyph by Gardiner code or by sound and see its Unicode character, readings and sources. Give me the data model, the rendering plan with fallbacks, and tests. Before we ship, check the licences of the data and fonts I plan to use: <list them>.

A good answer: the smallest app that does the job, a design note with user and task, data model,
encoding, rendering, search, licences and tests, and no scanned or OCR text of a book you may not
redistribute.

## 2. Rendering on the web

> How do I render hieroglyphs on the web? Cover font choice, joiners and quadrat layout, line direction, and what the page shows when a font lacks a sign. Show the fallback that prints the Gardiner code instead of an empty box.

A good answer: a font test with a sample set before a choice is made, direction stored as data on
the line, and a visible code wherever a glyph is missing.

## 3. Modelling a corpus

> Model a corpus of inscriptions with text, line, word, sign, reading and attestation. Put a source and a confidence on every reading. Key signs by Gardiner code and keep the Unicode character as a derived field. Give me the schema and the reason for each key choice.

A good answer: signs keyed by code string, not code point; a role per reading; provenance on every
datum; low-confidence data styled differently from verified data.

## 4. Search by sound

> Add search by sound. Students type plain ASCII, so plan a mapping from typed letters to transliteration letters, and make sure ꜣ, ꞽ and ꜥ are not collapsed into one letter. Keep the mapping table in one place and write tests for it.

A good answer: one mapping table, deliberate normalisation, and tests that fail if two distinct
letters start returning each other's words.

## 5. MdC import and export

> Add MdC import and export. Write round-trip tests (MdC to model to MdC), say what the model holds that MdC cannot carry, such as confidence and damage, and design a sidecar file for it.

A good answer: round-trip tests on a set of strings, a list of what is lost on export, and a
sidecar format that carries it.
