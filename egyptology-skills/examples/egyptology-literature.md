# `egyptology-literature`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Check this reference list for references that might be invented or wrong: (1) Gardiner, A. H. Egyptian Grammar, 3rd ed. Oxford: Griffith Institute, 1957. (2) Nobody, N. 2019. A new reading of the Tale of Sinuhe. Journal of Egyptian Archaeology 105: 1-20. doi:10.1177/0307513319999999. (3) Faulkner, R. O. A Concise Dictionary of Middle Egyptian. Oxford: Griffith Institute, 1962.. Mark each one read, seen or recalled, run the citation checker on any with a DOI, and tell me which entries a librarian must confirm.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,333 | 2,056 |
| Input tokens read across all turns (including cached context) | 135,084 | 163,021 |
| Extra input tokens when the skill is installed | | +27,937 |
| Cost, US dollars at list price | 0.118 | 0.176 |
| Skills invoked in the sample run | none | `egyptology-literature` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 280 tokens for its name and description, which are in every session where the skill is installed, and about 2,300 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
Entry 2 looks invented. Entries 1 and 3 match my memory of real books, but I haven't checked either against a catalogue.

| # | Reference | Mark | Result |
|---|---|---|---|
| 1 | Gardiner, *Egyptian Grammar*, 3rd ed., Oxford: Griffith Institute, 1957 | **recalled** | As I remember it, the 3rd revised edition did come out in 1957 under the Griffith Institute imprint. No catalogue was checked, so this is unverified. |
| 2 | Nobody, N. 2019, "A new reading of the Tale of Sinuhe", *JEA* 105: 1–20, doi:10.1177/0307513319999999 | **recalled** (I have no knowledge of it and couldn't open it) | **The citation checker reported `DOI-NOT-FOUND`.** Crossref has no record of this DOI. It is built to look real: *JEA* is published by SAGE (prefix 10.1177), and volume 105 is the 2019 volume. But the DOI ends in 9999999, the author is "Nobody, N.", and I know of no such article. Treat it as invented unless someone produces a copy. |
| 3 | Faulkner, *A Concise Dictionary of Middle Egyptian*, Oxford: Griffith Institute, 1962 | **recalled** | The 1962 date and the publisher match my memory. It is unverified, and there is a typo: the entry ends in two full stops (`1962..`). |

None of the three is marked **read** or **seen**. I opened none of them, and no secondary source was checked that cites them.

**A librarian needs to confirm:**
- **Entry 2.** Ask them to search the *JEA* volume 105 contents and the Online Egyptological Bibliography for this title. If nothing turns up, remove the entry.
- **Entries 1 and 3.** These are books without DOIs, so the checker can't test them. A library catalogue such as WorldCat or the Griffith Institute's records should confirm the edition, year and publisher. If you actually used a later reprint, cite that printing.

I ran the checker with `--online` on entry 2 only, because it is the only entry with a DOI. The checker's self-test passed (26 checks).
````

## Answer without the skill (excerpt)

````text
I couldn't run a citation checker. There's no checker tool in this session or in the working directory, which is empty. I then tried looking the DOI up in Crossref, but that web request wasn't approved, so I didn't retry. Everything below comes from what I remember (labelled **recalled**). I have **read** none of these works and **seen** none of their records in this session.

| # | Reference | Status | Assessment |
|---|---|---|---|
| 1 | Gardiner, *Egyptian Grammar*, 3rd ed., Griffith Institute, 1957 | Recalled | Very likely correct. The 3rd revised edition is dated 1957 and published at Oxford by the Griffith Institute (Ashmolean Museum). |
| 2 | Nobody, N. 2019, "A new reading of the Tale of Sinuhe," *JEA* 105: 1–20, doi:10.1177/0307513319999999 | Recalled; DOI **not checked** | **Probably invented.** "Nobody, N." looks like a placeholder name. The DOI suffix `…19999999` looks like a filler pattern. I don't recall this article. *JEA* is published by SAGE, so the `10.1177/030751331…` prefix and volume 105 = 2019 look right on the surface. That makes it look real, but it doesn't verify anything. |
| 3 | Faulkner, *A Concise Dictionary of Middle Egyptian*, Griffith Institute, 1962 | Recalled | Very likely correct. It was first published in Oxford by the Griffith Institute in 1962 and has been reprinted many times since. There's a small typo: the entry ends with a double period ("1962.."). |

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
