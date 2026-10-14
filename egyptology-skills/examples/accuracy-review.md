# `accuracy-review`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Review this transliteration and gloss for confident errors: Transliteration: G39 A1 = sꜣ 'son'. I am certain this is right. Source: from memory. Convention: Gardiner-era spelling.. State the convention, trace each claim to a source, and give me findings ranked critical, major, minor or note, each with evidence, impact and a fix. Say what you could not check.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,562 | 3,548 |
| Input tokens read across all turns (including cached context) | 30,437 | 151,742 |
| Extra input tokens when the skill is installed | | +121,305 |
| Cost, US dollars at list price | 0.111 | 0.213 |
| Skills invoked in the sample run | none | `accuracy-review` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 180 tokens for its name and description, which are in every session where the skill is installed, and about 1,400 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Accuracy review: G39 A1 = sꜣ 'son'

**Verdict:** The reading is very probably right, but it isn't ready to share as "certain." It has no source, its convention label is vague, and the sign group has a second reading you haven't ruled out. Fine for a class handout once the fixes below are made. Not ready to publish.

## Convention

- **What you stated:** "Gardiner-era spelling." That names a period, not a convention.
- **What I applied:** the Gardiner sign list for sign codes and values, and the modern Egyptological transliteration for spelling. In that system, aleph is written ꜣ (U+A723), and the first-person suffix is written =j (older books write it =i). The period is assumed to be Middle Egyptian, because no text or date was given.

## Claims and where each one comes from

| # | Claim | Source found | Status |
|---|---|---|---|
| 1 | G39 is the pintail duck, a biliteral sign read sꜣ | Bundled sign data: Gardiner, *Egyptian Grammar* 3rd ed., p. 471, "Ideogram for sꜣ 'son'". It was checked against OCR text, not the page image. | Supported, needs a check against the page image |
| 2 | A1 (seated man) is the determinative here | Bundled data: Gardiner p. 442, "Determinative for man; as an ideogram it writes 'I, me'" | Supported, but A1 has a second role (see F2) |
| 3 | G39 + A1 is one word, sꜣ | Your memory only | Unsourced |
| 4 | It means 'son' | Your memory only | Unsourced (no dictionary entry cited) |
| 5 | The reading is "certain" | Your own confidence | Not evidence |

I worked out the readings myself from the sign data rather than from your table, and the values match.

## Findings

### Major

**F1. The reading has no source but is labelled "certain."**
- **Evidence:** Claims 3 to 5 rest only on memory. Under this review method, a claim from memory counts as a finding even if it is correct.
- **Impact:** Anyone who reuses it inherits the certainty with nothing behind it. This would be critical if the reading were wrong. My own derivation agrees with it, which is why it is ranked major.
- **Fix:**
  - Cite the sign list (Gardiner, *Eg. Gr.*³, p. 471 for G39 and p. 442 for A1, checked against the page image).
  - Cite a dictionary entry for sꜣ 'son': the Wörterbuch / Thesaurus Linguae Aegyptiae (TLA) lemma, or Faulkner's *Concise Dictionary*. I'm not giving page numbers for these from memory, so look them up.
  - Grade the reading by that evidence instead of calling it "certain."

**F2. A second reading is possible: sꜣ=j 'my son'.**
- **Evidence:** A1 also writes the first-person singular suffix pronoun when the speaker is male. After a noun, G39 A1 can be read sꜣ=j 'my son'. The plain determinative is omitted or does double duty here.
- **Impact:** The gloss could be missing a pronoun. Out of context, that changes what is being said.
- **Fix:** Give the context: the surrounding text, who is speaking, and whether this sits in a filiation formula or in speech. If no context is available, record both readings: "sꜣ 'son' (A1 as determinative); alternatively sꜣ=j 'my son'."

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Review: G39 A1 = sꜣ "son"

**Verdict:** I found no critical errors. The reading is standard and almost certainly correct. The main problem is how the claim is supported: it says "certain" but the only source is memory. There are also a few gaps in how the convention is stated.

## Convention used for this review
- **Sign codes:** Gardiner's Sign List (*Egyptian Grammar*, 3rd ed., 1957), the same codes the Manuel de Codage (MdC) uses. G39 is the pintail duck and A1 is the seated man.
- **Transliteration:** the Egyptological alef. Gardiner printed it as ȝ. The modern Unicode character is ꜣ (U+A723). These are different typographic forms of the same value.
- **Gloss:** standard English lexical gloss.

## Where each claim comes from
| Claim | Your source | Where it should be traceable | Did I check it? |
|---|---|---|---|
| G39 = sꜣ (biliteral) | Memory | Gardiner, *Egyptian Grammar*, Sign List, G39 | No. This is from my own knowledge; I had no access to the text. |
| G39 + A1 spells sꜣ "son" | Memory | Gardiner Sign List G39 (sꜣ "son"); Faulkner, *Concise Dictionary*, s.v. sꜣ; Wb IV 408 | No. Same as above. |
| A1 is the determinative | Implied | Gardiner Sign List A1 (determinative for man and male roles) | No. Same as above. |

## Findings

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
