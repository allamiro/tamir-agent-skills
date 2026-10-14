# `edition-conventions` prompts

Apply the editorial conventions of a published edition: mark lacunae, restorations and doubtful signs with a
declared key, record the evidence for each restoration, and check that the brackets are well formed. The
skill produces a draft for an Egyptologist, not a published edition.

- **Give it:** the text, what is damaged and why, the publication or journal to follow and its key, and the
  transliteration scheme it requires
- **Skill file:** [`skills/edition-conventions/SKILL.md`](../skills/edition-conventions/SKILL.md)
- **Draft key it uses:** [`sigla.md`](../skills/edition-conventions/references/sigla.md)
- **Template it fills:** [`apparatus.md`](../skills/edition-conventions/assets/templates/apparatus.md)
- **Sound reading first:** [`transliteration`](transliteration.md) · **Layout after:** [`text-annotation`](text-annotation.md) · **Audit with:** [`accuracy-review`](accuracy-review.md)

## 1. Check the brackets

> Check the brackets in this line and tell me what is wrong: `htp-dj-nsw [Wsjr {nb} ddw (dj=f prt-xrw]`. Then draft the key the line would need.

A good answer: it finds that the square bracket and the round bracket cross, with the position, and drafts a
key marked as a draft to be checked against the publication. It may also question the curly-bracket mark
inside the restored stretch, which is a point about meaning, not about balance, and the curly brackets
themselves balance.

## 2. Make an edition line

> Set out this damaged line as an edition line with a key and notes, and tell me which restorations you would not make: <paste the line and what survives>

A good answer: the key printed first, one note per restoration with its evidence, gaps left open where only
an impression of the wording exists, and no formula completed from memory.

## 3. Which transliteration standard

> Which transliteration standard should I use for a new article, and what do you know about the 2023 Leiden standard?

A good answer: use the scheme the target publication states; the 2023 standard came from a workshop at the
13th International Congress of Egyptologists in Leiden and was accepted by members of the International
Association of Egyptologists, but the answer says it has not read which characters it prescribes.

## 4. Read a publication's key

> This publication's translation uses round, square and angle brackets and half brackets. Here is its key: <paste>. Rewrite my draft line in that key without importing marks from elsewhere.

A good answer: it uses only the marks the key defines, asks about any mark that the key leaves open, and
does not swap in the classical Leiden meanings.

## 5. A dating statement

> Write a dating statement for this inscription from the following criteria: <paste orthography, grammar, palaeography and context>. Say what chronology you are using.

A good answer: a range rather than one year, the criteria listed as evidence, the chronology named
because chronologies differ, and uncertainty stated.

## 6. Witnesses and variants

> This text survives on a stela and in two later copies. Show me how to set out the base witness, the sigla for the other copies and the variants.

A good answer: the original inscription kept apart from later copies, a named base witness, sigla for the
others, variants recorded in the notes, and no variant resolved without a stated reason.
