# `gardiner-sign-lookup`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> What is Gardiner sign G17? Give me the Unicode character and code point, the section, every role it has with its value and Gardiner page, and the status your table gives that row.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 944 | 684 |
| Input tokens read across all turns (including cached context) | 91,802 | 101,256 |
| Extra input tokens when the skill is installed | | +9,454 |
| Cost, US dollars at list price | 0.095 | 0.122 |
| Skills invoked in the sample run | none | `gardiner-sign-lookup` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 180 tokens for its name and description, which are in every session where the skill is installed, and about 1,700 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**G17, the owl**

| Field | Value |
|---|---|
| Glyph | 𓅓 |
| Code point | U+13153 |
| Section | G (Birds) |
| Role | uniliteral |
| Value | **m** |
| Gardiner page | p. 469 (*Egyptian Grammar*, 3rd ed., sign list) |

**Status:** "checked against the supplied Gardiner list (OCR text); diacritics and modern spelling from author knowledge, VERIFY against the page image"

The curated table gives G17 only one role, the uniliteral *m*. It lists no ideogram or determinative use. The table is small, though, so that doesn't prove G17 has no other uses. To check for any, look at Gardiner p. 469 directly.

For *m* the diacritics don't matter, since the letter has none. The VERIFY note still applies: the value was checked only against OCR text, not against the printed page image.
````

## Answer without the skill (excerpt)

````text
I couldn't find a table to check against. The working directory is empty, there are no project files that mention G17, and I have no saved memory from earlier work. So I can't tell you the status your table gives this row, and I can't confirm page numbers from your source.

Here is what I know about G17 from general knowledge:

- **Sign:** an owl (*Bubo ascalaphus*, the Pharaoh eagle-owl).
- **Unicode:** 𓅓, code point **U+13153** (EGYPTIAN HIEROGLYPH G017).
- **Section:** G, Birds.
- **Roles:**
  - **Phonogram, uniliteral *m*.** This is its main use. For example, it writes the preposition *m* ("in, with, from") and appears in many words with *m*.
  - It is also used as part of composite signs such as G18 (two owls, *mm*) and G20 (owl with forearm, *m* + *ı͗*). Those are separate sign numbers, though, not other roles of G17.
- **Gardiner page:** G17 is in the Birds section of the sign list in *Egyptian Grammar* (3rd ed.), around pp. 467–469. I can't confirm the exact page from memory.
- **Status:** I can't give one because I don't have your table.

If you send me the table (a file path, CSV or pasted rows), I'll give you the exact row, including its roles, page references and status.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
