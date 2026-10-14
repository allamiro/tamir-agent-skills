---
name: gardiner-sign-lookup
description: Looks up Egyptian hieroglyphs by Gardiner sign code (D21, G43, Aa1), by Unicode character, by a Manuel de Codage (MdC) code string, or by a transliterated sound, and reports section, Unicode code point, role (uniliteral, biliteral, triliteral, ideogram, determinative) and a sourced reading. Use for "what is sign G17", "which sign is nfr", "convert this MdC string to Unicode", "is this a determinative". Use transliteration to read a whole word or sign sequence, and text-annotation for a full inscription layout.
license: Apache-2.0
metadata:
  library: egyptology-skills
  version: "1.0"
---

# Gardiner sign lookup

## Purpose and activation

Answer one question reliably: what is this sign, what code does it have, what can it do in a
word, and how sure are we. Activate when the user names a Gardiner code, pastes a hieroglyph or
MdC string, or asks which sign writes a sound. Use `transliteration` when the task is to read a
sequence of signs as words, and `text-annotation` for a line-by-line layout.

## Required inputs

One of: a Gardiner code (`D21`, `d 21`, `Aa1`), a Unicode hieroglyph, an MdC code string
(`G17-D21:N35`), or a sound value (`nfr`). If the user only describes a picture ("a bird on a
stand"), narrow it by section (see `references/sections.md`) and ask for the code rather than
guessing.

## Workflow

1. **Normalize the code.** Run `python3 scripts/signs.py <code>` (or `--char`, `--mdc`,
   `--value`). The script maps code and character in both directions using Unicode names, so
   the code-to-glyph link does not depend on memory.
2. **Report the glyph facts**: code, character, code point, section, and whether the code is in
   Gardiner's printed list (the script flags codes that exist only in the wider Unicode set).
3. **Report readings from the curated table only.** `references/common-signs.json` holds 86 rows,
   each with a role, a value, a page in Gardiner's list and a status. Quote the status.
4. **If the sign is not in the table, say so.** Give the section and Unicode data, then name
   where to look it up (a sign list or dictionary) and mark any value you offer `VERIFY`. Do not
   fill the gap from memory without that label.
5. **Separate roles.** A sign is not one thing. Report every role it has (for example D2 is the
   ideogram for "face" and the biliteral ḥr; O1 is pr and a determinative for buildings).
6. **For an MdC string**, return the Unicode text with joiners and list any token the script
   could not read. Stacking is only a hint to the renderer; see `hieroglyph-app-builder`.
7. **For a sound value**, return every curated sign with that value and say the table is small:
   absence is not evidence that no sign has the value.

## Decision framework

| Situation | Do this |
|---|---|
| Code in the curated table | Report role, value, page and status |
| Code valid in Unicode, not in the table | Report glyph and section; value unknown, `VERIFY` |
| Starred code (`A14*`) or letter suffix (`A14A`) | Explain these are variants; the Unicode letter suffix may not equal Gardiner's variant |
| Several readings | List all roles; if used in a text, hand over to `transliteration` to choose from context |
| Code outside every section | Report invalid; there is no section J |

## Implementation guidance

- Gardiner has 26 sections: A to Z without J, plus `Aa`. `references/sections.md` names them.
- The Unicode name of a code is `EGYPTIAN HIEROGLYPH` + section letters + three digits +
  optional letter (`D021`, `AA001`). `signs.py` builds and reverses that.
- MdC uses Gardiner codes: `-` separates signs, `:` stacks one above the other, `*` places side
  by side. Other MdC features (ligatures, scaling, shading, text switches) are not handled;
  the script reports them as unsupported tokens. MdC details come from author knowledge: VERIFY
  against the JSesh or MdC documentation before building on them.
- Needs Python 3 with `unicodedata`. Older Python versions have older Unicode data; the joiner
  characters are Unicode 15, but the script writes them by code point so it works anyway.

## Failure and edge cases

- Reading a printed OCR text: diacritics and hieroglyph pictures are often corrupted. Check a
  value against the page image before calling it verified.
- Gardiner's transliteration differs from current spelling in places (for example ḳ for q);
  say which convention a value uses. See `transliteration`.
- A glyph that renders as a box means the font lacks it; the lookup is still valid.
- Variant forms: a sign Gardiner draws one way may be drawn differently on the monument; the
  code identifies the type, not the exact picture.

## Validation

- `python3 scripts/signs.py --selftest` checks code normalization, both mapping directions,
  the section gaps, and that every curated code has a Unicode character.
- Spot-check three curated values against the page image of the sign list before trusting a
  new batch of rows. A wrong reading in this table is the failure that matters.

## Expected output

A short record per sign: code, glyph, code point, section, roles with values and pages, status,
and a note for anything unverified.

## Sources and confidence

- Gardiner, *Egyptian Grammar*, 3rd ed. (1957), sign-list pp. 438-548: values and pages in the table checked against the supplied OCR text, 2026; diacritics unreliable in OCR
- Code-to-glyph mapping: Unicode character names (Egyptian Hieroglyphs block), computed by the script
- Modern transliteration spellings, MdC syntax, Unicode joiner behaviour: from author knowledge, VERIFY
- Not covered: signs outside the 86-row table; Ptolemaic and Old Egyptian values; non-Gardiner sign sets
