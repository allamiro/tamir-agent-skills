# `transliteration` prompts

Read a sequence of signs as consonants in Latin letters. Transliteration is not translation and not
pronunciation. The skill classifies every sign and marks the doubt at the sign where it arises.

- **Give it:** signs in reading order (Gardiner codes, MdC or Unicode), the direction, the period
  (Middle Egyptian is the default) and the convention you want
- **Skill file:** [`skills/transliteration/SKILL.md`](../skills/transliteration/SKILL.md)
- **Before it:** [`gardiner-sign-lookup`](gardiner-sign-lookup.md) for a single sign
- **After it:** [`text-annotation`](text-annotation.md) for glosses and translation

## 1. A word with a determinative

> Transliterate this sequence of Gardiner codes: G39 A1. Classify each sign, say which transliteration convention you use, say where the word ends, and flag anything ambiguous.

A good answer: G39 is the biliteral sꜣ (the table also gives the older zꜣ), A1 is a determinative
with no sound, and the word ends at the determinative.

## 2. An ideogram marked by a stroke

> Transliterate O1 Z1. Is this the ideogram for "house" or a spelling of pr with no determinative? Show both and say what would settle it.

A good answer: pr either way, with a flag. O1 is also a determinative for buildings, Z1 marks an
ideogram, and with no determinative after it the reading rests on the stroke, so look for a
parallel.

## 3. A sign standing alone

> N5 stands alone. Is it the ideogram rꜥ or a determinative for time? Give both readings, choose by context, and mark it uncertain if the context is thin.

A good answer: both readings listed, a choice tied to what comes before the sign, and
`uncertain` if there is nothing to go on.

## 4. Your own line

> Transliterate this line: <Gardiner codes in reading order>. Direction: <left to right, right to left, or columns>. Period: Middle Egyptian. Convention: <the one you want>. Segment it into words and say why each boundary is where it is. Classify each sign, mark phonetic complements so no consonant is counted twice, and flag each doubtful sign with its alternatives. List damaged or restored signs separately. Do not translate.

A good answer: one row per sign (order, code, role, value, confidence, alternatives), then the
word-level transliteration, then a list of every point that needs an Egyptologist.

## 5. Which convention is this

> Which transliteration convention does this use: <paste a transliteration>? Do not convert it. Tell me which letters differ between the Gardiner-era spelling and current practice, and mark anything you say from memory VERIFY.

A good answer: it names the convention, leaves your text as it is, and labels what it cannot
source.

## 6. A photo

> Here is a photo of an inscription: <attach the image>. Transliterate it.

A good answer: it asks for the sign codes or a clear transcription first. It does not read signs
off a low-quality image and present the result as a reading.
