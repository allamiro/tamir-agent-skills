# `gardiner-sign-lookup` prompts

Look up one sign by code, character, MdC string or sound. The skill reads readings only from the
checked table of 86 rows and says so when a sign is not in it.

- **Give it:** a Gardiner code, a Unicode hieroglyph, an MdC string, or a sound value
- **Skill file:** [`skills/gardiner-sign-lookup/SKILL.md`](../skills/gardiner-sign-lookup/SKILL.md)
- **Next skill:** [`transliteration`](transliteration.md) to read a whole word

## 1. One sign by code

> What is Gardiner sign G17? Give me the Unicode character and code point, the section, every role it has with its value and Gardiner page, and the status your table gives that row.

A good answer: 𓅓, U+13153, section Birds, uniliteral m, Gardiner p. 469, with the row's status
quoted.

## 2. Which sign writes a sound

> Which signs in your table read nfr? Tell me how many rows the table has, and do not treat a missing sign as proof that no other sign has this value.

A good answer: F35 (heart with windpipe), triliteral nfr, Gardiner p. 465. It says the table is
small, so absence proves nothing.

## 3. MdC string to Unicode

> Convert this MdC string to Unicode and list any token you could not read: G17-D21:N35

A good answer: Unicode text for the three signs, with the stacked pair joined, and a note that
stacking is only a layout hint for the renderer.

## 4. A sign that is not in the table

> Look up Gardiner sign A14. If it is not in your table, tell me what you can still say from Unicode and the section, and mark any value you offer VERIFY.

A good answer: the glyph, its code point and the section (Man and his occupations), then a plain
statement that there is no curated reading. It does not fill the gap from memory.

## 5. A sign with more than one job

> Is D2 only the ideogram for "face"? List every role D2 can have, and tell me what I would need to see in a text to choose between them.

A good answer: both roles, the ideogram for "face" and the biliteral ḥr, and a hand-off to
`transliteration` to choose from context.

## 6. A picture and no code

> I can see a bird standing on a stand, but I do not know the code. Narrow it down by section and ask me for the code. Do not guess one.

A good answer: it points to the Birds section and asks you to find the code in a sign list,
instead of naming a sign.
