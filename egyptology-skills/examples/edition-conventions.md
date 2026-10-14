# `edition-conventions`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Check the brackets in this line and tell me what is wrong: `htp-dj-nsw [Wsjr {nb} ddw (dj=f prt-xrw]`. Then draft the key the line would need.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,835 | 3,018 |
| Input tokens read across all turns (including cached context) | 30,383 | 175,825 |
| Extra input tokens when the skill is installed | | +145,443 |
| Cost, US dollars at list price | 0.096 | 0.203 |
| Skills invoked in the sample run | none | `edition-conventions` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 270 tokens for its name and description, which are in every session where the skill is installed, and about 2,300 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
The line has one structural error and two problems with what the brackets mean.

## What's wrong

**1. The brackets cross, so the line is malformed.** The round bracket opened before `dj=f` is never closed. The square bracket closes over it instead:

```
htp-dj-nsw [Wsjr {nb} ddw (dj=f prt-xrw]
           ^                ^           ^
           [ opens          ( opens     ] closes while ( is still open
```

A bracket checker gives: `ERROR line 1, col 40: ] closes [ opened at 1:12, but ( from 1:27 is still open (crossing)`. You need to close the `(` before the `]`, or remove it.

**2. Superfluous text sits inside a restoration.** `{ }` usually means signs that are on the object but that the editor removes as a scribal error. `[ ]` means text that is lost and that the editor restores. If `nb` is inside a restored passage, it isn't on the object, so the scribe can't have written it in error. Either:
- the signs `Wsjr … ddw` are actually preserved, so the `[ ]` is wrong or should start later; or
- `nb` is lost, in which case `{ }` is wrong. Also, *Wsjr nb Ḏdw* ("Osiris, lord of Busiris") is a normal epithet in this formula, so check why `nb` would be removed at all.

**3. Round brackets have no clear meaning here.** In an edition line, `( )` usually marks an expanded abbreviation. In a translation it marks words added for sense. `(dj=f prt-xrw` matches neither use. If the aim is to mark *dj=f prt-xrw* as damaged but legible, use half brackets `⸢ ⸣`. If it is restored, it already sits inside `[ ]`, so `( )` isn't needed.

**A smaller point:** the transliteration is in ASCII/MdC-style shorthand (`htp` for ḥtp, `ddw` for Ḏdw, `xrw` for ḫrw), and capitals are only partly used (`Wsjr` has one, `ddw` doesn't). Pick one scheme, name it, and use it throughout.

## A corrected line (one possible reading)

This assumes the passage from Osiris onward is lost and restored from a parallel, and that `nb` is restored too:

```
ḥtp-dj-nsw [Wsjr nb Ḏdw dj=f prt-ḫrw]
```

If instead *dj=f prt-ḫrw* is preserved but damaged:

```
ḥtp-dj-nsw [Wsjr nb Ḏdw] ⸢dj=f prt-ḫrw⸣
```

Which one is right depends on what is actually on the object. I can't tell that from the line alone.

## Draft key

Use your publication's key instead if it has one.

| Mark | Meaning in this edition |
|---|---|
| `[abc]` | Lost text restored by the editor; the evidence (parallel, formula, space) is given in a note |
| `[…]` | Lost text not restored, extent unknown; where measured on the object or a scaled image, one dot per sign |
| `⸢abc⸣` | Damaged but legible signs |
| `⟨abc⟩` | Omitted by the scribe, supplied by the editor |
| `{abc}` | Written on the object but superfluous; the editor removes it (shown, not deleted) |
| `⟦abc⟧` | Erased in antiquity |
| `( )` | Edition line: expansion of an abbreviation only. Translation: words added for sense |
| `?` | After a sign or word: doubtful reading |
| Scheme | Transliteration: [name the scheme, e.g. the publication's required one or the 2023 Leiden uniliteral standard, VERIFY] |

## Still needed before the line is shared

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
## What's wrong with the brackets

`htp-dj-nsw [Wsjr {nb} ddw (dj=f prt-xrw]`

1. **The `(` is never closed.** There is no matching `)` anywhere on the line.
2. **The brackets overlap.** `(` opens inside `[ … ]`, and then `]` closes before any `)`. In Leiden-style notation, sigla must nest cleanly, like `[ … ( … ) … ]` or `[ … ] ( … )`. They can't interleave, like `[ … ( … ] … )`.
3. **`{nb}` is balanced, but it's worth checking.** Braces normally mark something the scribe wrote that the editor deletes. *nb Ḏdw* ("lord of Busiris") is a standard epithet of Osiris, so marking *nb* as superfluous is unusual. Keep the braces only if the scribe really wrote something extra, such as a dittography. If *nb* was actually left out by the scribe, use `⟨nb⟩`. If it's lost, put it inside `[ ]`.

### Not brackets, but worth fixing at the same time
If this is Manuel de Codage–style transliteration, the case is wrong in two places:
- `htp` should be `Htp` (ḥtp). Lowercase `h` is plain h.
- `ddw` should be `Ddw` (Ḏdw, Busiris). Lowercase `d` is plain d.

### Possible corrected readings
The right fix depends on what the `(` was meant to cover:

- If the restored text ends after the toponym and *dj=f* is an editorial addition:
  `Htp-dj-nsw [Wsjr {nb} Ddw] (dj=f) prt-xrw`
- If the whole formula after *Htp-dj-nsw* is restored and *dj=f* is supplied within it:
  `Htp-dj-nsw [Wsjr {nb} Ddw (dj=f) prt-xrw]`

## Draft key

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
