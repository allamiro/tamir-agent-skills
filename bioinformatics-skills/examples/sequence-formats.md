# `sequence-formats`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Parse this FASTA file and check the format: how many sequences, the length range, repeated names, empty entries, and whether each looks like DNA, RNA or protein: >seq1 first
> ACGTACGTAC
> >seq2
> ACGTACGTACGTACGTACGTACGT
> >seq1 again
> MKVLEF
> >empty
> . Say where that guess is uncertain.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,480 | 1,500 |
| Input tokens read across all turns (including cached context) | 30,434 | 35,725 |
| Extra input tokens when the skill is installed | | +5,291 |
| Cost, US dollars at list price | 0.090 | 0.132 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 210 tokens for its name and description, which are in every session where the skill is installed, and about 2,100 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
## FASTA check

**Records:** 4 headers, but only 3 contain sequence.

| # | ID | Full header | Length | Likely type |
|---|----|-------------|-------:|-------------|
| 1 | `seq1` | `seq1 first` | 10 | DNA |
| 2 | `seq2` | `seq2` | 24 | DNA |
| 3 | `seq1` | `seq1 again` | 6 | Protein |
| 4 | `empty` | `empty` | 0 | Can't tell (no sequence) |

**Length range:** 0–24 across all records, or 6–24 if you leave out the empty one.

### Problems
1. **Repeated name: `seq1` appears twice.** The two full headers are different ("first" and "again"). But most tools use only the first word as the ID, including Biopython's `SeqIO.to_dict`, samtools faidx and BLAST databases. Those tools will either stop with an error or quietly keep only one of the two. Give each record a unique ID.
2. **Empty entry: `>empty`** has no sequence lines. Some parsers skip it, some keep a 0-length record, and indexers like `samtools faidx` may complain. Either remove it or add its sequence.
3. **DNA and protein in the same file.** The format allows it, but nearly every downstream tool expects one type per file (BLAST, aligners, translation). Split it into a nucleotide file and a protein file.
4. **The trailing "."** after `>empty` looks like the end of your sentence, so I didn't count it as data. If it really is in the file, then `empty` has a 1-character sequence made of a gap/unknown symbol, which isn't a real sequence either.

### How sure is each type guess?
- **seq1 (DNA), the least certain.** It uses only A, C, G and T, and has no U, so DNA is the usual call. But those four letters are also valid amino acids (Ala, Cys, Gly, Thr). With only 10 characters, the letters alone can't prove it isn't a short peptide. It is DNA by convention and likelihood, not by proof.
- **seq2 (DNA), fairly confident.** Same caveat as seq1, but 24 characters using only A/C/G/T would be very unusual for a protein. It isn't RNA, since there's no U, unless someone wrote RNA using T.
- **seq3 (protein), confident.** E, L and F are not nucleotide letters, not even in the IUPAC ambiguity codes. M, K and V are ambiguity codes, but E, L and F settle it. It starts with M, as many proteins do, but at 6 residues it's a peptide or fragment, not a full protein.
- **empty: no call possible.**
````

## Answer without the skill (excerpt)

````text
## FASTA check

**4 records**, of which **3 have sequence data** and **1 is empty**.

| # | Header | ID (first word) | Length | Looks like | Confidence |
|---|---|---|---|---|---|
| 1 | `>seq1 first` | seq1 | 10 | DNA | Medium |
| 2 | `>seq2` | seq2 | 24 | DNA | Medium–high |
| 3 | `>seq1 again` | seq1 | 6 | Protein | High for type, low for meaning |
| 4 | `>empty` | empty | 0 | — | Can't tell |

**Length range:** 6–24 if you only count records with sequence data, or 0–24 if you count the empty one.

### Problems with the format

1. **Repeated name: `seq1`.** The two full header lines are different (`seq1 first` and `seq1 again`), but most tools (Biopython, samtools faidx, BLAST makeblastdb) use only the first word as the ID. They'll see two records called `seq1`, and will either give an error or quietly overwrite one with the other.
2. **Empty record: `>empty`** has a header but no sequence. Many parsers accept this, but indexing and alignment tools often reject it or skip it.
3. **Mixed sequence types.** The file has both DNA and protein in it. Most tools expect only one type per file, so this will probably cause errors further down the line.
4. **The trailing `.`**: I've read it as the full stop at the end of your sentence, not as part of the file. If it really is the sequence line under `>empty`, then that record is length 1, and `.` is a gap character from alignment formats, not a residue. That would still mean there's no real sequence there.

### Where the type guesses are uncertain

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
