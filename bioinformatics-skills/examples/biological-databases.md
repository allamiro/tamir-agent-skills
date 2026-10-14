# `biological-databases`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> What kind of identifier is NM_000546.6, and what does the .6 at the end mean? What should I record alongside it?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,056 | 1,469 |
| Input tokens read across all turns (including cached context) | 30,352 | 111,730 |
| Extra input tokens when the skill is installed | | +81,378 |
| Cost, US dollars at list price | 0.080 | 0.166 |
| Skills invoked in the sample run | none | `biological-databases` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 240 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
## What NM_000546.6 is

It's an **NCBI RefSeq accession.versioned identifier**.

- **`NM_`**: the underscore marks it as RefSeq, not GenBank/INSDC. GenBank accessions have no underscore, e.g. `AB123456`. `NM_` means a **curated mRNA (transcript) record**. Other prefixes you'll see: `NR_` is curated non-coding RNA, `NP_` is curated protein, `NC_` is a chromosome or complete genomic molecule, `NG_` is a genomic region, and `XM_`/`XR_`/`XP_` are *predicted* model records. Treat the X records as leads, not curated evidence.
- **`000546`**: the stable accession. This one is the human **TP53** transcript. NM_000546.6 is, to my knowledge, the MANE Select transcript for TP53, which pairs it with Ensembl ENST00000269305. Check that against the current MANE release before relying on it.
- **`.6`**: the **sequence version**. It goes up each time the sequence of the record changes. So `.6` is the sixth version of this sequence, and `NM_000546.5` is a different sequence. Changes to annotation alone, such as notes or references, don't bump the version.

What this means in practice: **a bare `NM_000546` doesn't pin a sequence.** Variant descriptions depend on the exact transcript version. For example, in HGVS `NM_000546.6:c.215C>G`, the `c.` numbering can shift between versions if the UTR or exons change. Two people using the same accession but different versions can get different coordinates without any error being raised.

## What to record alongside it

Use separate columns, and store everything as text so a spreadsheet can't reformat it:

| Field | Example |
|---|---|
| Accession | `NM_000546` |
| Version | `6` (or keep the full `NM_000546.6` as well) |
| Source database | NCBI RefSeq |
| Entity type | mRNA transcript (and say what you actually meant: gene, transcript or protein) |
| Organism | *Homo sapiens* (taxid 9606) |
| Gene | Stable ID **NCBI Gene 7157 / HGNC:11998**. Keep the symbol "TP53" only as a label, not as a key |
| Genome build, if mapping to coordinates | GRCh38 (plus the annotation release, e.g. RefSeq annotation release / MANE version) |
| Retrieval date and method | e.g. 2026-10-14, Entrez efetch script |
| Checksum of the downloaded sequence | MD5/SHA-256 of the FASTA |
| Linked records, if used | Protein `NP_000537.x` and the matching Ensembl `ENST…` with its version, plus where each mapping came from |

The test is whether someone else can follow your record and retrieve exactly the same sequence. If they can't, something is missing. Usually it's the version or the build.

I ran the skill's identifier checker on it, and it classified the string as RefSeq NM_ curated mRNA, version 6. The checker labels its RefSeq prefix rules as "unverified". The prefix meanings above are standard NCBI conventions, but NCBI's accession-prefix documentation is the authority if you need to cite it.
````

## Answer without the skill (excerpt)

````text
**NM_000546.6 is an NCBI RefSeq accession for a curated mRNA transcript.** This one is the human *TP53* transcript, which encodes p53.

## What each part means

| Part | Meaning |
|---|---|
| `NM_` | RefSeq prefix for a **curated, protein-coding mRNA**. Related prefixes: `NR_` is curated non-coding RNA, `XM_`/`XR_` are computationally predicted models, `NP_` is curated protein, `NC_` is a complete genomic molecule such as a chromosome, and `NG_` is a genomic region (RefSeqGene). |
| `000546` | The stable accession number. It identifies the record and never changes. |
| `.6` | The **sequence version**. It goes up by one each time the nucleotide sequence itself changes, for example when UTRs are extended or an error is corrected. `.6` means this is the sixth sequence of the record. Changes to annotation alone, such as notes or features, do not change the version. |

The version matters because **different versions can have different sequences, so the same position can mean different things**. A variant such as `NM_000546.6:c.743G>A` is only unambiguous with the version. Coordinates from `.5` may not map to `.6`, especially in the UTRs. For this reason HGVS nomenclature requires a versioned reference sequence. NM_000546.6 is also the **MANE Select** transcript for *TP53*, matched to Ensembl `ENST00000269305`. You can check whether a newer version exists on the NCBI Nucleotide record.

## What to record alongside it

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
