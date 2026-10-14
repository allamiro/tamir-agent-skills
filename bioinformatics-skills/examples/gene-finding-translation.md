# `gene-finding-translation`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Translate ATGAAATAG in frame 1 under the standard genetic code and tell me what each symbol in the answer means.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 196 | 401 |
| Input tokens read across all turns (including cached context) | 30,351 | 35,639 |
| Extra input tokens when the skill is installed | | +5,288 |
| Cost, US dollars at list price | 0.063 | 0.110 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 230 tokens for its name and description, which are in every session where the skill is installed, and about 2,200 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**Translation: `MK*`**

| Codon | Symbol | Meaning |
|---|---|---|
| ATG | **M** | Methionine (Met). ATG is also the usual start codon. |
| AAA | **K** | Lysine (Lys). The one-letter code is K because L is already used for leucine. |
| TAG | **\*** | Stop codon, called "amber". It is not an amino acid. It marks where translation ends. |

Frame 1 means the codons are read starting from the first base, with no offset. The encoded peptide is the dipeptide **Met-Lys**. The `*` is a marker for the stop, not part of the protein. Some tools drop it or stop at it, so they would show just `MK`.

Because the sequence runs from a start codon to an in-frame stop, it is technically a complete open reading frame. At only 2 codons it is far too short to be a real gene.
````

## Answer without the skill (excerpt)

````text
**Translation:** `ATG AAA TAG` → **`MK*`**

| Codon | Symbol | Meaning |
|---|---|---|
| ATG | **M** | Methionine (Met). ATG is also the standard start codon. |
| AAA | **K** | Lysine (Lys). |
| TAG | **\*** | Stop codon. It ends translation and does not add an amino acid. TAG is called the "amber" stop codon. |

So the sequence codes for a two-residue peptide, Met-Lys, followed by a stop.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
