# `transliteration`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Transliterate this sequence of Gardiner codes: G39 A1. Classify each sign, say which transliteration convention you use, say where the word ends, and flag anything ambiguous.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,320 | 1,756 |
| Input tokens read across all turns (including cached context) | 30,374 | 139,846 |
| Extra input tokens when the skill is installed | | +109,472 |
| Cost, US dollars at list price | 0.086 | 0.170 |
| Skills invoked in the sample run | none | `transliteration` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 210 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**Reading: sꜣ** (older form *zꜣ*). Most likely gloss: "son". That gloss is a proposal from the transliteration notes, not part of the reading.

**Convention.** I use the current Egyptological letters (ꜣ ꞽ ꜥ w b p f … ḏ), as set out in the skill's convention notes. Gardiner-era books print this word as *zꜣ*, because Old Egyptian kept s and z apart (Gardiner, sign-list p. 441). In 2023 a group at the Leiden congress agreed a unified standard. I haven't checked its exact letters, so if you're writing for a publication, follow that publication's stated scheme.

**Sign table**

| # | Gardiner | Sign | Role here | Value | Confidence | Alternatives |
|---|---|---|---|---|---|---|
| 1 | G39 | pintail duck | biliteral (phonogram) | sꜣ | high | older *zꜣ*; may be mixed up with G38, the white-fronted goose, *gb* |
| 2 | A1 | seated man | determinative ("man") | — (no sound) | medium | 1st-person suffix pronoun *=ꞽ* ("my", "I") |

The sign values come from the skill's sign table, checked against the OCR text of Gardiner's sign-list (G39 on p. 471, A1 on p. 442). The diacritics still need checking against the page image.

**Where the word ends.** Most likely after A1: a determinative closes a word, and nothing follows it here. If A1 is read as the suffix pronoun instead, the word *sꜣ* ends after G39 and *=ꞽ* is attached to it.

**Transliteration**
- Preferred: **sꜣ**, with A1 as the determinative.
- Alternative: **sꜣ=ꞽ** ("my son"). Here A1 is the suffix pronoun. Scribes often let one A1 do both jobs, determinative and "my", so a two-sign sequence can't tell the two readings apart.

**Points for expert review**
1. **Determinative or "my" (A1).** This is the main open question. The sentence around these signs would settle it: a possessive, or a name before or after the word.
2. **G39 or G38.** The two ducks look alike, especially in hieratic. Check the signs in the source itself, not just the codes.
3. **Ideogram or phonogram.** G39 is also the ideogram for "son". Without a stroke (Z1) the role is still sꜣ either way, so the reading is unaffected.
4. **"Daughter."** If a *t* (X1) sign followed, the word would be *sꜣt* "daughter", usually with the woman determinative (B1). Make sure no sign has been dropped from the sequence.
5. **Date.** I assumed Middle Egyptian. For an Old Egyptian text, write *zꜣ*.

Nothing was flagged as damaged or restored.
````

## Answer without the skill (excerpt)

````text
# G39 A1 → **sꜣ** "son"

## Sign classification

| Code | Sign | Function here | Value |
|---|---|---|---|
| **G39** | Pintail duck | Phonogram (biliteral) | **sꜣ** |
| **A1** | Seated man | Determinative (male person) | — (not pronounced) |

## Transliteration convention

I use the standard Egyptological (Leiden-style) convention with Unicode **ꜣ** (aleph) and **j** for the reed-leaf yod. The Manuel de Codage (ASCII) equivalent is **zA**. Older works may write *sA* or *s3*.

## Where the word ends

The word ends after **A1**. Determinatives mark the end of a word, so A1 closes **sꜣ** "son". Nothing more is spelled out phonetically.

## Ambiguities to flag

1. **A1 as determinative or as suffix pronoun.** A1 can also write the 1st-person singular suffix **=j** ("my"). Read that way, the group is **sꜣ=j** "my son". Spellings of "son" often use only G39 (sometimes with the stroke Z1), so a following A1 could well be the pronoun. Without more context both readings work: **sꜣ** "son" or **sꜣ=j** "my son". In a sentence, the syntax usually settles it, for example when a possessor is expected or a name follows.
2. **Other words read sꜣ.** The same sound value spells several other words: *sꜣ* "back" (with F-series determinatives), *sꜣ* "protection" (usually V16/V17), and *sꜣ* "phyle". The A1 determinative points clearly to "son" here.
3. **Gender.** "Daughter" would be **sꜣt**, written with t (X1) and the woman determinative B1. With A1 this is masculine.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
