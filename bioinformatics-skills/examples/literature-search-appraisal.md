# `literature-search-appraisal`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Check this reference list for citations that might be invented or wrong, mark each one read, seen or recalled, and tell me what the checker proves and what it does not: (1) Gardiner, A. H. Egyptian Grammar. Oxford, 1957. (2) Nobody, N. 2019. A new result. J Imaginary Biol 5:1-9. doi:10.1000/imaginary.2019.1

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,581 | 2,553 |
| Input tokens read across all turns (including cached context) | 92,665 | 167,171 |
| Extra input tokens when the skill is installed | | +74,506 |
| Cost, US dollars at list price | 0.111 | 0.216 |
| Skills invoked in the sample run | none | `literature-search-appraisal` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 2,500 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I ran the skill's checker (`citecheck.py`). Its self-test passes (28 checks), and then I checked your list against Crossref.

## Results

| # | Reference | Checker result | Mark | Verdict |
|---|---|---|---|---|
| 1 | Gardiner, A. H. *Egyptian Grammar*. Oxford, 1957. | `NO-DOI`: it can't be checked against Crossref | **recalled** | Almost certainly real. This is the well-known grammar of Middle Egyptian. 1957 is the 3rd revised edition; the first came out in 1927. The publisher is usually given as Griffith Institute / Oxford University Press. I know this from memory only. I haven't read it or looked up a record for it today, so check a library catalogue (WorldCat, or the Bodleian) and add the edition: "3rd ed., rev." |
| 2 | Nobody, N. 2019. A new result. *J Imaginary Biol* 5:1–9. doi:10.1000/imaginary.2019.1 | `DOI-NOT-FOUND`: Crossref has no record of this DOI | **none of the three** | Treat it as invented. Crossref has no record of the DOI. The prefix `10.1000` is the example prefix used in the DOI Handbook, not a real publisher. I don't know of any journal called *J Imaginary Biol*, and the author and title are placeholders. I can't honestly mark it read, seen or recalled, because nobody has any evidence it exists. Remove it, or replace it with the real source behind the claim. |

## What the checker proves
- **When it passes:** a DOI on the line resolves in Crossref, and the record's metadata (title, year, authors) matches what you wrote. That catches typos, a wrong year, or a DOI pasted onto the wrong paper (`MISMATCH`).
- **When it reports `DOI-NOT-FOUND`:** Crossref has no record of that DOI. That's strong evidence of a typo or an invented reference. It isn't absolute proof, because a few DOIs are registered with other agencies such as DataCite.

## What it does not prove
- **It can't check books or other items without a DOI.** For entry 1, `NO-DOI` is neither a pass nor a fail; it just means it was never checked.
- **A pass doesn't mean the paper says what you cite it for.** Only reading it (the `read` mark) shows that.
- **It doesn't check retractions or corrections,** or whether a reviewed version replaced a preprint.
- **It doesn't check that you picked the right source** or the right edition. For example, it can't tell you whether you mean the 1957 or the 1927 edition of Gardiner.
- **The read/seen/recalled marks are your declaration of how you know each source.** The checker can't verify them. My "recalled" for Gardiner means I know it from memory and I haven't confirmed it today.

**Next steps:** look up Gardiner in a library catalogue (after that you can mark it **seen**), and remove or replace reference 2.
````

## Answer without the skill (excerpt)

````text
I couldn't check either reference against a live source. I tried to resolve the DOI and search Crossref, but the network lookup needed your approval and wasn't run, and the working directory is empty. So the marks below come from my memory or from reading the citation text, not from opening any record.

| # | Citation | Mark | Verdict |
|---|---|---|---|
| 1 | Gardiner, A. H. *Egyptian Grammar.* Oxford, 1957. | **Recalled** | **Probably real and correct.** Sir Alan H. Gardiner's *Egyptian Grammar: Being an Introduction to the Study of Hieroglyphs* is the standard work. The 3rd revised edition was published in 1957 (Oxford: Griffith Institute / Oxford University Press). The 1st edition was 1927. The citation is incomplete: it leaves out the subtitle, the edition and the publisher. I haven't checked it against a catalogue. |
| 2 | Nobody, N. 2019. A new result. *J Imaginary Biol* 5:1-9. doi:10.1000/imaginary.2019.1 | **Seen** (only the text you gave) | **Almost certainly made up.** Several signs point that way: the author is "Nobody, N.", the title is "A new result", and the journal is called *Imaginary Biol*. Also, `10.1000` is the DOI Foundation's example prefix, used in documentation, not by real publishers. I didn't try to resolve the DOI, so the "made up" call rests on these signs, not on a failed lookup. |

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
