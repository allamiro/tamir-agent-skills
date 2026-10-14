# `sequence-formats` prompts

Read, check and convert FASTA, FASTQ, GFF3, BED and SAM data, and settle which coordinate system
each file uses before touching a position.

- **Give it:** the file or a sample of it, the format you think it is, where it came from, and the
  genome build
- **Skill file:** [`skills/sequence-formats/SKILL.md`](../skills/sequence-formats/SKILL.md)
- **References:** [`formats.md`](../skills/sequence-formats/references/formats.md) and
  [`coordinates.md`](../skills/sequence-formats/references/coordinates.md)
- **After it:** [`gene-finding-translation`](gene-finding-translation.md) for what the sequence encodes

## 1. Summarise a FASTA file

> Parse this FASTA file and check the format: how many sequences, the length range, repeated names, empty entries, and whether each looks like DNA, RNA or protein: <paste or give the path>. Say where that guess is uncertain.

A good answer: the counts, any duplicate or empty records by name, and a note that a short string
of A, C, G and T could also be protein.

## 2. A FASTQ file that parses to the wrong count

> My FASTQ parser reports the wrong number of reads. One record's quality line starts with @, like this: <paste the record>. What is going wrong and how should the file be read?

A good answer: the parser is treating a quality line as a header; read strict four-line blocks
and never scan for @, because @ is a valid quality character (Q 31).

## 3. Convert between BED and GFF

> Convert the BED interval 2 to 5 to GFF3 coordinates, and the GFF3 interval 3 to 5 back to BED. Show that both select the same bases of ACGTACGTAC.

A good answer: BED 2-5 is GFF3 3-5, and both give GTA; the formula is start plus one going to
GFF3 and start minus one coming back, with the end unchanged.

## 4. Read quality characters

> In a Phred+33 FASTQ file, what do the quality characters I, 5 and ! mean? Give Q and the probability that the base call is wrong for each.

A good answer: I is Q40 (0.0001), 5 is Q20 (0.01), and ! is Q0 (probability 1).

## 5. Check a GFF3 file

> Check this GFF3 file and list every line with a problem, with the line number and the rule it breaks: <paste>. Also check the first line.

A good answer: line-level problems such as start greater than end, an invalid strand, or a CDS
without a phase, and a note if the file lacks the ##gff-version 3 line.

## 6. DNA or protein

> Is the string ACGT DNA or protein? And what about MKV*? Tell me what else I would need to decide.

A good answer: both strings are valid in more than one alphabet (every letter of ACGT is also an
amino acid code, and M, K and V are valid nucleotide ambiguity codes), so the answer needs
context such as the source, the length and the file's own metadata.
