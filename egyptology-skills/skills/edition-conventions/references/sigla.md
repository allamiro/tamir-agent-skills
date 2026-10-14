# Sigla: a draft key

The first two columns come from a page on the Leiden Conventions read on 2026-10-14. That page describes
the system as agreed for epigraphic and papyrological texts in 1931 and says uses vary between fields. The
Egyptological column is from author knowledge: VERIFY against the publication you follow. If the
publication has a key, its key wins.

| Meaning | Classical Leiden mark | Egyptological practice | Draft advice |
|---|---|---|---|
| Missing text restored by the editor | `[abc]` | Square brackets for restored or lost text are widely used | Add the evidence in a note |
| Missing text, not restored, extent known | `[...]` with a dot per sign | Often a number of dots or a count | Count signs only from the object or a scaled image |
| Missing text, not restored, extent unknown | `[ ... ]` or half-open bracket | Often `[...]` | Say "extent unknown" in the key |
| Omitted by the scribe, supplied by the editor | `⟨abc⟩` | Angle brackets are used for this in many editions | Put the reason in a note |
| Superfluous or wrongly written text | `{abc}` | Curly brackets | Keep the removed signs visible |
| Erased in antiquity | `⟦abc⟧` | Double square brackets, `[[abc]]` in plain text | Say whether the erasure is legible |
| Abbreviation expanded | `a(bc)` | Round brackets for supplied letters are one use | Round brackets also often mark added words in translation, so the key must say which |
| Unclear or damaged letters | dot under the letter | Half brackets `⸢ ⸣` or `⌈ ⌉` for damaged but legible signs | Do not mix the two glyph styles |
| Doubtful expansion or reading | question mark inside the mark | Question mark after the sign or word | State the convention in the key |

`python3 scripts/sigla.py check FILE` checks that the brackets above are balanced, properly nested, not empty
and not nested inside the same kind. It treats `[[` and `]]` as an erasure mark. It cannot tell whether a
mark is used correctly for its meaning.
