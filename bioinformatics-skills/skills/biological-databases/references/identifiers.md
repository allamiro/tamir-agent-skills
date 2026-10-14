# Identifiers

The status column says whether the pattern was checked against the database's own documentation
(read 2026-10-14) or is from general knowledge.

| Identifier | Pattern | Example | Status |
|---|---|---|---|
| INSDC nucleotide (GenBank, ENA, DDBJ) | 1 letter + 5 digits; 2 letters + 6 digits; 2 letters + 8 digits | U12345, AB123456 | Verified (NCBI) |
| INSDC protein | 3 letters + 5 digits; 3 letters + 7 digits | AAA12345 | Verified (NCBI) |
| RefSeq | 2 letters, an underscore in the third position, digits | NM_000546 | The underscore rule is verified; the prefix meanings are not |
| Ensembl | ENS + species prefix (none for human) + feature letter + 11 digits | ENSG00000141510, ENSMUSG00000000001 | The layout is verified; the feature letters are not |
| UniProtKB accession | 6 or 10 characters in a fixed pattern | P12345, A0A022YWF9 | Not verified |
| PDB entry | 4 characters, a digit first | 1ABC | Not verified |
| SRA / ENA run, experiment, sample, study | SRR, SRX, SRS, SRP (or ERR, DRR and so on) + digits | SRR1234567 | Not verified |
| GEO series, sample, platform | GSE, GSM, GPL + digits | GSE12345 | Not verified |

## Version suffix

NCBI records and Ensembl identifiers carry a version after a dot (NM_000546.6, ENSG00000141510.18).
The same accession with a different version can be a different sequence or annotation. Store the
accession and the version separately and always record the version.

## Prefix meanings (unverified)

| RefSeq prefix | Meaning |
|---|---|
| `NC_` | chromosome or complete genomic molecule |
| `NG_` | genomic region |
| `NT_`, `NW_` | contig, supercontig |
| `NM_` / `NR_` | curated mRNA / curated non-coding RNA |
| `NP_` | curated protein |
| `XM_`, `XR_`, `XP_` | predicted mRNA, non-coding RNA, protein |
| `WP_` | non-redundant protein |

| Ensembl feature letter | Meaning |
|---|---|
| G | gene |
| T | transcript |
| P | protein |
| E | exon |

## A string can fit more than one database

| String | Fits |
|---|---|
| P12345 | UniProt accession, and the GenBank 1-letter-5-digit nucleotide layout |
| SRR1234567 | SRA run, and the GenBank 3-letter-7-digit protein layout |
| GSE12345 | GEO series, and the GenBank 3-letter-5-digit protein layout |

A bare identifier does not tell you which database issued it. Keep the source next to it.
