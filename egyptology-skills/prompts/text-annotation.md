# `text-annotation` prompts

Lay a short text out line by line: signs, transliteration, gloss, grammar, a confidence grade per
word, a translation, and a list of points for an expert. The output is a draft, never a finished
translation.

- **Give it:** the signs (Gardiner codes, MdC or Unicode), the line breaks and direction, the date
  or genre if you know it, and any dictionary you trust
- **Skill file:** [`skills/text-annotation/SKILL.md`](../skills/text-annotation/SKILL.md)
- **Template it fills:** [`interlinear.md`](../skills/text-annotation/assets/templates/interlinear.md)
- **Grades A to D:** [`confidence-scale.md`](../skills/text-annotation/references/confidence-scale.md)
- **Before it:** [`transliteration`](transliteration.md) · **After it:** [`accuracy-review`](accuracy-review.md)

## 1. A first annotation

> Annotate this one-word text, given as Gardiner codes: G39 A1. Use the interlinear layout: word id, signs, transliteration, gloss, grammar, grade and notes, then a literal translation and a review list. No dictionary is supplied, so mark every gloss VERIFY.

A good answer: one table row with the codes kept in it, a gloss marked VERIFY, a grade for the
word, and a review list that includes that gloss.

## 2. With your own dictionary

> Annotate <Gardiner codes> using only this glossary: <paste the entries>. Cite the entry for each gloss. If a word is not in the glossary, leave the gloss as VERIFY and do not fill it from memory.

A good answer: grade A only where the sign values are certain and the word is in your glossary;
every other word carries a lower grade or VERIFY.

## 3. A damaged sign

> Annotate this line: <Gardiner codes>, where the third sign is damaged. Show the restoration separately, give that word grade D, and put it in the review list. Do not read the damaged sign as its most common neighbour.

A good answer: the restoration sits in its own marked list, the word is graded D, and the line's
grade is D because a line takes the grade of its weakest word.

## 4. Regrade by the evidence

> Regrade every word in this annotation on the A to D scale, by the evidence and not by how natural the translation sounds. Give each line's grade as its weakest word, not an average. <paste the annotation>

A good answer: each grade is justified by what supports it, and any grade resting on plausibility
alone is lowered.

## 5. Before it goes in a handout

> This will go in a class handout. Annotate <Gardiner codes>, then hand the result to accuracy-review and show me its findings separately from the annotation.

A good answer: the annotation first, then a ranked list of findings with a statement on whether it
is ready for classroom use.
