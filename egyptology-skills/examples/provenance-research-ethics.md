# `provenance-research-ethics`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> An object was excavated in 1895 with a field register entry, sold in 1921 with a catalogue lot number, and given to a museum in 1982 by the collector's heirs, with only an oral account for that last step. Build the record, run the checker and tell me what can and cannot be said.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 3,521 | 3,408 |
| Input tokens read across all turns (including cached context) | 138,573 | 190,389 |
| Extra input tokens when the skill is installed | | +51,815 |
| Cost, US dollars at list price | 0.179 | 0.253 |
| Skills invoked in the sample run | none | `provenance-research-ethics` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 2,400 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I built the record and ran the checker. The checker's own self-test passes (27 checks). The record has **4 flags**, and nothing contradicts itself: there are no out-of-order dates and no undated events.

Record file: `scratchpad/record.json` (excavation 1895 → sale 1921 → gift 1982). You didn't give me names, the site, the museum, the object number or the citations, so those are labelled placeholders. I also had to **assume the excavator was the 1921 seller**, because you didn't say who sold it. Please confirm that.

## Checker flags and what each one means

| Flag | Response |
|---|---|
| **undocumented-event**: the 1982 gift rests on an oral account | It's the weakest step. Ask the museum for its accession register entry, deed of gift or donor correspondence for 1982. Any of these would turn it into a documented step. Until then, write down who gave the oral account and when. |
| **broken-chain**: the collector → the heirs | Nothing records how the object passed from the collector to the heirs: no date of death, will or estate inventory. Probate records or the deed of gift could close this. |
| **gap, 1895–1921 (26 years)** | It's unclear where the object was between excavation and sale. Did it go through a division of finds, an export permit, or stay with the excavator? **No export from Egypt is recorded at all.** |
| **gap, 1921–1982 (61 years)** | The object was with the collector and then the heirs for 61 years, and nothing documents it. Look for exhibitions, publications, insurance lists or letters. |

The checker also noted that the object was documented in 1895, before both 1970 (UNESCO) and 1973 (the Archaeological Institute of America's publication rule). An earlier date only shows when the object was first documented. **It does not show that the object left Egypt lawfully.**

## What can be said

- **Excavated in 1895, recorded in the field register (entry no. __).** You can call this "documented" once someone has seen the entry. If you only know of it from another source, call it **"reported"**.
- **Sold in 1921 as lot __ of [sale catalogue].** The same rule applies: "documented" if the catalogue has been checked, otherwise "reported".
- **The object was documented before 1970 and 1973.** That's relevant to a journal rule that accepts earlier documentation, such as the Archaeological Institute of America's. Confirm the exact policy of your journal.

## What can only be said with qualification

- **"Said by the collector's heirs to have been given to [museum] in 1982."** Call this **"reported"** or **"claimed"**, not documented. The museum's own records could upgrade it quickly.
- **That the 1921 seller was the excavator.** I assumed this; nothing you gave me supports it.

## What cannot be said

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
The working directory was empty, so there was no checker to run. I wrote a record and a small checker myself (`provenance_record.json` and `check_provenance.py`) and ran it. It found **6 blocking issues**, so the chain of ownership does not hold up as it stands. The checker's rules are my own, based on standard provenance practice. If your institution has its own checker or standard, run that one instead.

## What can be said

- **1895:** The object was excavated. The field register entry documents this, as long as the object can be shown to be the one described in the entry (by its description, a number on the object, or its measurements).
- **1921:** The object was offered at a sale, as a numbered lot in the catalogue.

## What cannot be said, or not yet

1. **That the object legally left the excavation.** A field register records the find. It does not record who was allowed to keep it, or whether it was exported legally.
2. **How it got from the excavation to the 1921 sale.** There are 26 years with no recorded owner. The checker can't connect the excavator to whoever sent it to the sale.
3. **That the collector bought it in 1921.** A catalogue shows the object was put up for sale. It doesn't show that it sold or who bought it. That needs a marked-up catalogue, the auction house's sale records, or an invoice.
4. **That the collector held it from 1921 until death, and the heirs inherited it.** There are 61 years with no record. Nothing documents the collector's death or the estate passing to the heirs.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
