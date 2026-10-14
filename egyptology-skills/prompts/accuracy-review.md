# `accuracy-review` prompts

Audit a reading, an annotation or a sign table for confident errors. The skill traces every claim
to a source, re-derives the sign layer itself, and ranks findings by how much they could mislead.
It does not replace an Egyptologist; it shows where one must look.

- **Give it:** the work to review, the convention used, the sources the author claims, and the
  intended use (handout, database, publication)
- **Skill file:** [`skills/accuracy-review/SKILL.md`](../skills/accuracy-review/SKILL.md)
- **Checklist it follows:** [`checklist.md`](../skills/accuracy-review/references/checklist.md)
- **Review work made by:** [`transliteration`](transliteration.md) or
  [`text-annotation`](text-annotation.md) · **Check one sign with:**
  [`gardiner-sign-lookup`](gardiner-sign-lookup.md)

## 1. Review a reading

> Review this transliteration and gloss for confident errors: <paste>. State the convention, trace each claim to a source, and give me findings ranked critical, major, minor or note, each with evidence, impact and a fix. Say what you could not check.

A good answer: counts of claims checked and sourced, ranked findings, and a plain list of what was
not checked, such as no photograph or no dictionary.

## 2. Audit a sign table

> Audit this sign table: <paste or give the path>. Sample rows at random instead of reading from the top, re-derive each sampled value with the lookup, and report claims checked, claims sourced, findings by severity and claims you could not verify.

A good answer: a random sample, values re-derived and not copied from the table, and a note that a
claim made from memory is a finding until a source is added.

## 3. Find the smoothing

> Compare my translation with my word table. Flag words that have no row, rows that have no word, and glosses that look chosen to make the sentence read well. <paste both>

A good answer: each translated word maps to a row, and any gap is shown as a gap, not as a
smoother guess.

## 4. Check the grades

> Check every grade in this annotation. For each one, say what evidence supports it, and flag any grade that rests on plausibility alone. Do not accept the confidence the annotation claims for itself. <paste>

A good answer: grades tied to evidence, and a note where a plausible gloss has pushed a grade up.

## 5. Is it safe to use

> Is this safe for a class handout? Give me an overall statement, the corrections it needs, and the list of claims that need a specialist before anyone relies on them. <paste>

A good answer: a verdict in the report's own terms, for example safe for classroom use with the
listed corrections, or not ready to publish.

## 6. Test the reviewer

> I planted three wrong sign values in this annotation and I am not telling you where. Review it as you would any other, and report every finding with its evidence. <paste>

A good answer: all three planted errors appear among the findings, each with the source it
contradicts. If one is missed, do not trust the "no findings" it gave elsewhere. Plant the errors
yourself so the agent cannot know where they are.
