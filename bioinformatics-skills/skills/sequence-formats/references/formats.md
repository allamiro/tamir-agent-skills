# Formats

## FASTA

```text
>identifier optional description
ACGTACGTAC
GTAC
```

- A line starting with `>` begins a record. The identifier is the text up to the first
  whitespace; the rest is a description.
- Sequence lines may be wrapped at any width; join them. Blank lines are ignored by the parser.
- Alphabet is DNA, RNA or protein; the file does not say which. See `possible_alphabets()`.
- Gap characters (`-`) and stop symbols (`*`) can appear in alignments and protein files.

## FASTQ (strict 4-line records)

```text
@read1 optional description
ACGT
+
IIII
```

1. `@` and the identifier.
2. The bases.
3. `+`, optionally repeating the identifier.
4. One quality character per base.

Quality Q is the ASCII code minus 33 (SAM specification, QUAL, read 2026-10-14; Phred+33). The
probability of a wrong base call is 10 to the power of -Q/10:

| Character | ASCII | Q | Error probability |
|---|---|---|---|
| `!` | 33 | 0 | 1 |
| `+` | 43 | 10 | 0.1 |
| `5` | 53 | 20 | 0.01 |
| `?` | 63 | 30 | 0.001 |
| `I` | 73 | 40 | 0.0001 |

A quality line can start with `@` (Q 31), so a FASTQ file must be read in blocks of four lines.
Older Illumina files used a different offset (Phred+64); VERIFY the offset from the instrument
documentation when the lowest code seen is far above `!`.

## GFF3

Nine tab-separated columns: seqid, source, type, start, end, score, strand, phase, attributes.
The file starts with `##gff-version 3`. Attributes are `tag=value` pairs separated by `;`, with
`;`, `=` and tab escaped (GFF3 specification, read 2026-10-14). Phase (0, 1 or 2) is required for
CDS features and is `.` otherwise.

## BED

Tab-separated: chrom, chromStart, chromEnd, and optional columns (name, score, strand and more).
0-based, half-open (UCSC format FAQ, read 2026-10-14).

## SAM

Eleven mandatory tab-separated fields: QNAME, FLAG, RNAME, POS, MAPQ, CIGAR, RNEXT, PNEXT, TLEN,
SEQ, QUAL (SAM specification, read 2026-10-14). FLAG is a set of bits: 0x1 template has multiple
segments, 0x4 segment unmapped, 0x10 SEQ is reverse complemented. The specification says bit 0x4
is the only reliable place to tell whether a read is unmapped. This collection does not parse SAM.

## What the parser here does not do

Multi-line FASTQ, compressed input, paired-end linking, SAM/BAM/CRAM, VCF, GenBank and EMBL flat
files, and any validation of GFF3 feature hierarchies (parent and child relations).
