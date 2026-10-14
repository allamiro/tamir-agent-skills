---
name: transliteration
description: Transliterates Middle Egyptian hieroglyph sequences into Egyptological transliteration, classifying each sign as uniliteral, biliteral, triliteral, ideogram, phonetic complement or determinative, and flagging every ambiguous or damaged reading with the alternatives. Use for "transliterate these signs", "read this inscription", "what is the phonetic complement here", "why is this sign written twice", "which transliteration convention is this". Use gardiner-sign-lookup for a single sign, text-annotation for a full layout with glosses, and accuracy-review to audit a finished transliteration.
license: Apache-2.0
metadata:
  library: egyptology-skills
  version: "1.0"
---

# Transliteration

## Purpose and activation

Turn a sequence of signs into a transliteration without hiding doubt. Transliteration writes the
consonants of the Egyptian word in Latin letters; it is not translation and not pronunciation.
Activate when the user gives signs (glyphs, Gardiner codes or MdC) and wants the sounds, or asks
how a particular spelling works. Use `gardiner-sign-lookup` for one sign and `text-annotation` when
glosses and translation are wanted.

## Required inputs

The signs in order and direction; the text's date or period if known (Middle Egyptian is the
default); the transliteration convention wanted; and any damage marks. If the signs come from a
photo or OCR, ask for the sign codes or a clear transcription first. Do not read signs off a
low-quality image and present the result as a reading.

## Workflow

1. **Fix the sign sequence.** Normalize every sign to a Gardiner code with `gardiner-sign-lookup`.
   Record reading order: rows, columns, orientation (signs face the start of the line).
2. **Segment into words.** Words end at determinatives, or at a sign that cannot continue a
   spelling. Mark each boundary and why. Where the segmentation is a guess, say so.
3. **Classify each sign in its word**, using the table in `references/sign-roles.md`:
   uniliteral, biliteral, triliteral, ideogram, phonetic complement, determinative, or marker
   (stroke, plural strokes).
4. **Avoid double-counting.** A phonetic complement repeats a consonant of the sign before it, so
   it is not read twice. Example pattern: a biliteral followed by its second consonant as a
   uniliteral writes the biliteral's value once. Check each repeat against the biliteral's value.
5. **Write the transliteration**, in the stated convention (`references/conventions.md`). Use
   brackets only with the meaning given there.
6. **Flag ambiguity at the sign, not the end.** For each doubtful sign list the candidate
   readings, which one you chose and why, and what evidence would settle it.
7. **Separate what is read from what is inferred.** Restored or damaged signs go in a separate
   marked list. A reading that depends on a restoration cannot be called certain.
8. **Hand off.** Pass the segmented, flagged result to `text-annotation` for glosses, or to
   `accuracy-review` for audit.

## Decision framework

| Question | If yes | If no |
|---|---|---|
| Does the sign carry a sound value in this word? | Read it as phonogram | It is an ideogram or determinative: no sound of its own |
| Does a following uniliteral repeat a consonant of the sign before it? | Treat as phonetic complement; do not add the consonant twice | Read both |
| Does the sign end the word and show a category (man, house, movement)? | Determinative: transliterate nothing | Keep reading |
| Could this be ideogram or phonogram? | Give both, choose by whether a determinative or complement follows | |
| Is a stroke (Z1) after the sign? | It marks an ideogram: the word is the thing itself | |

A sign can change role between words, so the table gives values, not rules for each word.

## Implementation guidance

- Sign lists mix three jobs. Gardiner himself says ideographic and phonetic uses "shade off" into
  one another, so a hard split sometimes does not exist; record the doubt.
- Two sign pairs look alike and were confused even by good scribes. The sign list notes this for
  rope and bag signs, and says hieratic caused many assimilations. Do not "correct" the text to
  what Egyptian should have been.
- Old Egyptian kept s and z apart; the Middle Egyptian word for "son" was once *zꜣ*. The list
  prints some values as s (z) for this reason.
- Where a transliteration needs a consonant that is not written, or one that was written but had
  gone silent, the list uses brackets; see `references/conventions.md`.
- Worked examples with each step are in `references/worked-examples.md`.

## Failure and edge cases

- **Homophones.** Many signs share a value; the choice carries meaning (a different word). Keep
  the sign code in the output so no information is lost.
- **Different convention, same text.** Gardiner-era and current spellings differ for some
  letters; convert only if asked, and name the convention.
- **Group writing and Late forms.** Foreign names and Late Egyptian use group writing and different
  conventions; the list is a Middle Egyptian one. Do not apply these values blindly (VERIFY).
- **Damage.** Do not read a half-preserved sign as its most common neighbour.
- **Variant forms** of one sign (Gardiner's starred signs) keep the same value unless the list
  says otherwise.
- **Overconfident gloss.** Do not let a plausible translation pick the reading of an ambiguous
  sign.

## Validation

- Round-trip: re-spell the transliteration with the chosen signs and check each consonant is
  written exactly once.
- Check the values used against the sign table or a sign list, not memory.
- Count: flagged-ambiguous signs, damaged signs, and restored signs, listed separately.
- Falsifier: a published transliteration of the same line that disagrees on a sign you called
  certain.

## Expected output

A table with one row per sign: order, glyph, Gardiner code, role, value, confidence, alternatives.
Then the word-level transliteration with brackets and flags, and a list of every point that needs
expert review. Do not translate here unless asked.

## Sources and confidence

- Gardiner sign-list intro pp. 438-441 (supplied): s/z, bracket convention, ideographic-versus-phonetic overlap, hieratic confusions
- Sign values: from `gardiner-sign-lookup` table, checked against the supplied list
- Current transliteration letters, grammar rules for complements: from author knowledge, VERIFY
- Not covered: Old and Late Egyptian conventions, Demotic, Coptic reconstruction
