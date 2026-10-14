---
name: text-annotation
description: Produces a line-by-line annotated layout of a short Egyptian text, with glyphs or sign codes, transliteration, word-by-word gloss, translation and a confidence grade per word, and a list of points for expert review. Use for "annotate this inscription", "make an interlinear of this line", "give me glyphs, transliteration and translation in a table", "prepare a text for publication or teaching". Use transliteration for the sound reading alone, gardiner-sign-lookup for single signs, and accuracy-review to audit a finished annotation.
license: Apache-2.0
metadata:
  library: egyptology-skills
  version: "1.0"
---

# Text annotation

## Purpose and activation

Lay a text out so a reader can see exactly what is certain and what is not, one line at a time.
The output is a draft for a person who knows the language, never a finished translation.
Activate when the user wants an interlinear layout, a teaching handout, or a first pass at a
short text. Use `transliteration` first if the sound reading is still open.

## Required inputs

The signs (Gardiner codes, MdC or Unicode), line breaks and reading direction, the date or
genre if known, and any dictionary or glossary the user trusts. If no dictionary is supplied,
glosses are proposals marked `VERIFY`. A photo alone is not enough; ask for a sign transcription.

## Workflow

1. **Establish the lines.** One row group per line or column, in reading order, with the original
   line number and any damage marks.
2. **Transliterate** each line with `transliteration`, keeping its sign-level flags.
3. **Segment into words** and give each word an id (`L1.w3`). Keep the sign codes with the word.
4. **Gloss each word** with a source: the user's dictionary, or `VERIFY` when it is your proposal.
   Give one gloss, not a list, and put alternatives in the notes column.
5. **Add grammar only where certain.** Part of speech and form (for example "noun, masc.") are
   given only if the segmentation is clear; otherwise leave blank. Do not invent forms.
6. **Translate each line** after the word table, as a separate column. Show the literal
   rendering and, if useful, a smoother one, clearly labelled.
7. **Grade confidence per word** with `references/confidence-scale.md`. The line's grade is its
   weakest word, not an average.
8. **List review points** at the end: every grade C or D word, every `VERIFY` gloss, and every
   place where the translation needs a word you could not identify.
9. **Hand off to `accuracy-review`** if the text will be shared or published.

## Decision framework

| Situation | Handling |
|---|---|
| Sign values certain, word in the user's dictionary | Grade A, cite the entry |
| Sign values certain, word identified from context only | Grade B |
| Sign or segmentation ambiguous | Grade C, show alternatives |
| Damaged or restored sign | Grade D, show the restoration separately |
| Proper name | Give the transliteration, label it a name, gloss only if the name is transparent and sourced |
| Formula known to the user | Mark it; do not "complete" a broken formula from memory without a flag |

## Implementation guidance

- Use the template in `assets/templates/interlinear.md`: one table per line, columns for word id,
  signs, transliteration, gloss, grammar, grade, notes. Keep a separate translation row.
- Keep the sign codes in every row so a reader can check the reading without the original image.
- Write each translation sentence so it can be traced to the words that make it.
- Publish-ready text needs facsimile or photographs. Gardiner himself notes that printed
  hieroglyphs cannot capture the variety of the originals; say that the layout is a transcription.

## Failure and edge cases

- A fluent translation hiding an unknown word. Show a gap marker rather than a smooth guess.
- Gloss drift: the same word glossed two ways in one text without a note.
- Line breaks that split a word, or words that run across a column.
- Honorific transposition and ligatures that change the written order.
- A text the user thinks is Middle Egyptian that is Old or Late: the sign values may differ.
- Confidence inflation: the gloss is plausible, so the grade drifts upward. Grade the evidence.

## Validation

- Every row has a source or `VERIFY` for its gloss.
- Every grade C or D word appears in the review list.
- Re-read the translation against the word table: each translated word maps to a row.
- Falsifier: a specialist reader finds a grade-A word wrong.

## Expected output

A document with a header (text id, source, convention, date of draft, "draft: needs expert
review"), one table per line using `assets/templates/interlinear.md`, a translation per line, and
the review list.

## Sources and confidence

- Layout conventions (interlinear lines, confidence grades): own design; adjust to the user's journal style
- Reading and sign values: via `transliteration` and `gardiner-sign-lookup` tables
- Grammar and lexicon: not supplied by this skill; need a dictionary and grammar from the user
- Gardiner sign-list pp. 438-441 (supplied) on the limits of printed hieroglyphs
