# `text-annotation`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Annotate this one-word text, given as Gardiner codes: G39 A1. Use the interlinear layout: word id, signs, transliteration, gloss, grammar, grade and notes, then a literal translation and a review list. No dictionary is supplied, so mark every gloss VERIFY.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 998 | 2,094 |
| Input tokens read across all turns (including cached context) | 30,408 | 148,720 |
| Extra input tokens when the skill is installed | | +118,312 |
| Cost, US dollars at list price | 0.080 | 0.169 |
| Skills invoked in the sample run | none | `text-annotation` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 190 tokens for its name and description, which are in every session where the skill is installed, and about 1,500 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Annotated text: G39 A1 (one word)

Source: sign codes supplied by the user. No object, photo or publication was given.
Convention: Egyptological transliteration (ꜣ, ꞽ/i), with `=` marking suffix pronouns
Draft of: 2026-10-14   Status: **draft, needs expert review**
This is a transcription from Gardiner codes. Printed sign codes cannot show how the signs look on the original, so any reading should be checked against a photo or facsimile.

## Line 1  (grade: C)

| Word | Signs (Gardiner codes) | Transliteration | Gloss | Grammar | Grade | Notes / alternatives |
|---|---|---|---|---|---|---|
| L1.w1 | G39 A1 | sꜣ | "son" (**VERIFY**) | noun, masc. (if A1 is a determinative) | C | G39 (pintail duck) is the biliteral sign sꜣ. A1 (seated man) is most likely the determinative for a man, which makes this a common spelling of sꜣ "son". **Alternative:** A1 could be the 1st person singular suffix, giving sꜣ=i "my son". Without context you can't tell these apart, so the word boundary is uncertain. |

Literal translation: "son" (**VERIFY**). If A1 is the suffix: "my son".
Smoother translation: none. A single word has nothing to smooth.
Damage and restorations: none reported.

## Review list

- **L1.w1, gloss:** "son" is my proposal, not taken from a dictionary. **VERIFY** it against Wb or TLA under sꜣ "Sohn" (son).
- **L1.w1, function of A1 (grade C):** A1 could be a determinative (sꜣ "son") or a suffix pronoun (sꜣ=i "my son"). Context settles it. Look for a following name (as in a filiation formula, "son of X"), a speaker, or a second A1 that would act as the determinative.
- **L1.w1, identity of G39:** check against the original that the bird is the pintail G39 (sꜣ) and not a similar bird such as G38 (gb, goose). G38 would give a different word.
- **L1.w1, no stroke:** the spelling has no Z1 stroke, which is common for "son". It does not change the reading, but check the original in case a stroke or a t (X1) was missed. G39 X1 would point to sꜣt "daughter".
- **Grammar:** "noun, masc." holds only if A1 is the determinative. Remove it if the suffix reading wins.

Run `accuracy-review` before sharing this. Giving me the context the word comes from (the line, object or genre) would let me resolve the grade-C point.
````

## Answer without the skill (excerpt)

````text
# Interlinear annotation: G39 A1

| Field | Value |
|---|---|
| **Word ID** | W1 |
| **Signs** | G39 (pintail duck) + A1 (seated man) |
| **Transliteration** | **sꜣ** (other reading: **sꜣ=i**) |
| **Gloss** | "son" — **VERIFY** |
| **Grammar** | Noun, masculine singular. G39 is the two-consonant sign *sꜣ*. A1 is most likely a determinative ("man, person") with no sound value. |
| **Grade** | **B (probable).** The reading of G39 is secure. Whether A1 is a determinative or a suffix pronoun is not certain. |
| **Notes** | (1) G39 stands for the consonants *s + ꜣ*. Here it has no phonetic complement and no stroke (Z1); "son" is often written G39 + Z1. (2) A1 after a noun is usually the determinative for a male person. A1 can also be the 1st person singular suffix *=i* ("my"). That would give *sꜣ=i* "my son", grade C. One word with nothing around it can't settle this. (3) The determinative rules out the similar-looking *sꜣ* words with other meanings ("back", "protection", "phyle"), which take different determinatives. (4) A feminine *sꜣt* "daughter" would need X1 (*t*) and usually B1 (seated woman). Neither is present, so the word is masculine. |

## Literal translation

**"son"** (other reading: "my son")

## Review list

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
