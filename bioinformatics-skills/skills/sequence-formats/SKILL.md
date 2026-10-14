---
name: sequence-formats
description: Reads, checks and converts the common bioinformatics file formats (FASTA, FASTQ with Phred+33 qualities, GFF3, BED, SAM) and settles coordinate conventions, the 0-based versus 1-based mix-ups behind most silent errors. Use for "parse this FASTA", "why does my FASTQ fail", "is this GFF3 valid", "convert BED to GFF coordinates", "what do these quality characters mean", "off-by-one error in my annotation", "is this DNA or protein". Use gene-finding-translation for what the sequence encodes, sequence-alignment to compare sequences, and reproducible-research-code to record which file version was used.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Sequence formats

## Purpose and activation

Get data in and out of files without changing it by accident. Most pipeline errors that do no
visible harm are format errors: a coordinate shifted by one, a quality offset misread, a header
split in the wrong place. Activate when the user opens, writes, validates or converts a sequence,
read or annotation file, or reports a position that is "off by one".

## Required inputs

The file or a sample of it; the format the user believes it is; the source (sequencer, database,
tool) and version; the reference genome build the coordinates refer to; and what the next step
will do with it.

## Workflow

1. **Identify the format** from its structure, not its extension. `>` starts FASTA; four-line
   blocks starting `@` are FASTQ; nine tab-separated columns after `##gff-version 3` are GFF3.
2. **Parse strictly.** `python3 scripts/seqformats.py fasta FILE`, `fastq FILE`, or `gff3 FILE`
   reports counts, lengths, duplicate identifiers, empty records and line-level problems.
3. **Check the alphabet.** The letters of any DNA string are also valid protein letters, so a short
   string can be both. `possible_alphabets()` returns every alphabet that fits; `alphabet_call()` gives
   the best guess with a confidence (certain, likely or ambiguous, the last for fitting both and under
   20 characters); the report lists the records whose alphabet is ambiguous.
4. **Fix the coordinate system** before touching a position. See `references/coordinates.md`.
   Convert with `python3 scripts/seqformats.py coords bed2gff START END` or `gff2bed`.
5. **Decode FASTQ qualities.** Quality Q is the ASCII code minus 33, and the probability the base
   is wrong is 10 to the power of minus Q/10. Mean Q is not a mean error rate.
6. **Record what was read:** format, version, build, checksum, and any records that were dropped.
   Hand the record to `reproducible-research-code`.
7. **Fail loudly.** A truncated file, a length mismatch or a missing header is an error, not a
   record to skip.

## Decision framework

| Question | Answer |
|---|---|
| FASTQ record count looks wrong | Parse by 4-line blocks; a quality line can begin with `@`, so never scan for `@` |
| Quality characters include `!` or low codes | Phred+33; a file with only high codes may use an older offset (VERIFY) |
| Positions disagree by one between tools | One is 0-based half-open (BED), the other 1-based (GFF3, SAM) |
| Same gene, two coordinate lists | Same genome build? Check the build first |
| Short string classified as DNA | It may be protein; check `possible_alphabets()` |
| GFF3 CDS rows fail | CDS requires a phase of 0, 1 or 2 |
| Windows line endings | Handled; do not strip characters by hand |

Format details and the coordinate table are in `references/formats.md` and
`references/coordinates.md`.

## Implementation guidance

- The parsers read the whole file; for large files, stream with your own loop over
  `parse_fastq()` on chunks of four lines.
- Treat identifiers as the text up to the first whitespace; the rest of the header is a free-text
  description.
- Never convert coordinates by adding or subtracting 1 inline. Use the two conversion functions,
  which are tested against round trips and against real slices.
- Keep one canonical coordinate system inside your own code, convert at the file boundary, and name
  it in variable names and comments.
- Keep ambiguity codes (N, R, Y and the rest of IUPAC) as they are; do not delete or randomise them.

## Failure and edge cases

- **Off by one at scale.** One shifted start moves every feature in the file.
- **Multi-line FASTQ,** which this parser does not support; it reports the line count problem.
- **Duplicate identifiers,** which silently overwrite each other in a dictionary.
- **Lower case** carrying soft-masking information that `.upper()` destroys.
- **Mixed builds** between the sequence file and the annotation file.
- **Header characters** such as `|`, spaces and `:` that other tools parse differently.
- **A truncated download** whose last record is partial.
- **Empty read** (length 0): legal in FASTQ, easy to drop by accident.
- **Quality offset guessed wrongly,** making every base look excellent or terrible.

## Validation

- `python3 scripts/seqformats.py --selftest` must pass: a quality line beginning with `@` still
  parses as two records; BED 0-100 converts to GFF 1-100 and back; `seq[2:5]` from BED coordinates
  and `seq[s-1:e]` from the converted GFF coordinates give the same bases.
- Count records and total bases before and after any conversion; they must match.
- Falsifier: convert an interval both ways and slice a known sequence; the bases must be identical.

## Expected output

The detected format and version, record counts, lengths, problems found with line numbers, the
coordinate system in force, and any conversion applied with the formula used.

## Sources and confidence

- GFF3 specification (The Sequence Ontology), read 2026-10-14: nine tab-separated columns;
  1-based coordinates; start less than or equal to end; strand `+ - . ?`; phase 0, 1 or 2 and
  required for CDS; `##gff-version 3` first; `;`, `=` and tab escaped in column 9
- SAM specification (hts-specs), read 2026-10-14: POS is 1-based, 0 for unmapped; eleven mandatory
  fields; FLAG bits 0x1, 0x4, 0x10; QUAL is ASCII of base quality plus 33
- UCSC format FAQ, read 2026-10-14: BED chromStart is 0-based and chromEnd is not included; the first
  100 bases are chromStart 0, chromEnd 100
- The GFF3 text does not say "inclusive"; treating GFF3 intervals as closed follows from
  one-base features having start equal to end. VERIFY the zero-length case in the specification
- FASTA and FASTQ conventions, the older Phred+64 encodings, VCF and BAM coordinates, IUPAC letters:
  general knowledge, VERIFY against the specifications
- The source text leaves out practical programming and database handling, so none of this comes
  from it
- Not covered: BAM and CRAM binary layout, VCF parsing, compressed formats, paired-end handling
