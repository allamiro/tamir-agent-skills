# `hieroglyph-app-builder`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Design a small web app where students look up a hieroglyph by Gardiner code or by sound and see its Unicode character, readings and sources. Give me the data model, the rendering plan with fallbacks, and tests. Before we ship, check the licences of the data and fonts I plan to use: a Unicode hieroglyph web font and my own list of 86 signs checked against Gardiner's sign list.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 7,176 | 5,995 |
| Input tokens read across all turns (including cached context) | 61,201 | 151,564 |
| Extra input tokens when the skill is installed | | +90,362 |
| Cost, US dollars at list price | 0.212 | 0.258 |
| Skills invoked in the sample run | none | `hieroglyph-app-builder` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 220 tokens for its name and description, which are in every session where the skill is installed, and about 1,700 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I couldn't finish the licence check. You didn't say which web font you're using, and there's no sign list in the working directory. The licence section below covers what I can say now and what I need from you. The design and tests are complete.

## 1. Scope

The app is a static site built from one checked JSON file of 86 signs. It needs no server or database: search runs in the browser over a small index. Unicode text and a web font cover display. If you later add whole inscriptions, you can add text, line and word tables; don't build them now.

## 2. Data model

```jsonc
// signs.json, the single source of truth, built and checked in CI
{
  "meta": {
    "version": "1.0.0",
    "translit_convention": "Allen / MdC-ASCII search form",   // state it once, follow it everywhere
    "licence": "CC BY 4.0 (your text and selection)",
    "compiled_by": "…", "checked_against": "Gardiner, Egyptian Grammar, 3rd ed. 1957, Sign-list"
  },
  "signs": [
    {
      "code": "D21",                       // primary key, the Gardiner code as a string
      "section": "D",                      // "D" = parts of the human body
      "unicode_name": "EGYPTIAN HIEROGLYPH D021",  // stored; the character is computed from it at build time
      "label": "mouth",                    // your own words, not copied from Gardiner
      "variants_of": null,                 // e.g. "A1" for A1A-type variants
      "readings": [
        {
          "role": "uniliteral",            // uniliteral|biliteral|triliteral|ideogram|determinative|marker
          "value": "r",                    // Unicode transliteration
          "search": "r",                   // ASCII/MdC form, generated from one shared mapping table
          "source": { "work": "Gardiner 1957", "loc": "Sign-list D21" },
          "status": "verified",            // verified | VERIFY. Records without a status are rejected
          "checked_by": "…", "checked_on": "2026-10-01"
        }
      ]
    }
  ]
}
```

Rules:

- **Codes are the keys, not code points.** Unicode keeps adding signs: Unicode 16 added Egyptian Hieroglyphs Extended‑A (U+13460–U+143FF). The build looks up each character from `unicode_name`, so you never type a code point by hand.
- **Every reading has a role, a source and a status.** Show readings with status `VERIFY` in a different style and label them "unchecked".
- **Sound search uses one mapping table.** It is case-sensitive, as in MdC:

  | Typed | Matches | Typed | Matches |
  |---|---|---|---|
  | `A` | ꜣ | `x` | ḫ |
  | `i` / `j` | ꞽ / j | `X` | ẖ |
  | `a` | ꜥ | `S` | š |
  | `H` | ḥ | `T` | ṯ |
  | `h` | h | `D` | ḏ |
  | `q` / `k` | q / k (kept distinct) | `s` / `z` | s / z |

  `h` and `H` are different letters. A search that folds ꜣ, ꞽ and ꜥ together returns wrong signs. Add an optional "loose" mode that ignores diacritics, rank exact matches first, and label the loose ones.
- **Code input** is normalised: `d21`, `D 21` and `D021` all become `D21`. `Aa1` keeps its case.

## 3. Rendering plan with fallbacks

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
The working directory is empty and you didn't name the font, so **I couldn't check the actual licences**. I haven't seen your font file or your 86-sign list. Section 4 gives what I know about the likely candidates and what to check before you ship. Send me the font's name or its licence file and your list, and I'll check them for real.

---

## 1. Data model

86 signs is a small dataset. Keep it as JSON in the repo, check it with a schema in CI, and build a static site from it. You don't need a database.

```ts
// Shown as "A1", "Aa15", "NL1", "A14a". Unicode writes the same signs as A001, AA015, NL001, A014A.
type GardinerCode = string;

interface Source {
  id: string;                 // "gardiner1957", "allen2014", "unikemet16"
  citation: string;           // full bibliographic reference
  locator?: string;           // a page or section, e.g. "p. 442"
  licence?: string;           // only needed when we copy data from it (e.g. "Unicode-3.0")
}

type ReadingKind =
  | "uniliteral" | "biliteral" | "triliteral"   // phonograms
  | "logogram" | "determinative" | "phonetic-complement";

interface Reading {
  kind: ReadingKind;
  translitMdC?: string;       // the sound as typed in MdC (case matters: "H" is ḥ, "h" is h). Empty for determinatives
  translit: string;           // the scholarly spelling shown to students: "ḥ", "mn", "nfr"
  meaning?: string;           // for logograms and determinatives, e.g. "man, person"
  sourceIds: string[];        // must name at least one source
  note?: string;
}

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
