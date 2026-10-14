# SAM and BAM guide

Source: SAM specification (hts-specs), read 2026-10-14. SAM is text, BAM its compressed binary form,
CRAM a reference-based compressed form.

## Mandatory fields

QNAME, FLAG, RNAME, POS, MAPQ, CIGAR, RNEXT, PNEXT, TLEN, SEQ, QUAL, in that order. POS is 1-based;
0 means unmapped. QUAL is the ASCII value of the Phred quality plus 33.

## FLAG bits

| Bit | Hex | Meaning |
|---|---|---|
| 1 | 0x1 | template having multiple segments in sequencing |
| 2 | 0x2 | each segment properly aligned according to the aligner |
| 4 | 0x4 | segment unmapped |
| 8 | 0x8 | next segment in the template unmapped |
| 16 | 0x10 | SEQ being reverse complemented |
| 32 | 0x20 | SEQ of the next segment in the template being reverse complemented |
| 64 | 0x40 | the first segment in the template |
| 128 | 0x80 | the last segment in the template |
| 256 | 0x100 | secondary alignment |
| 512 | 0x200 | not passing filters, such as platform or vendor quality controls |
| 1024 | 0x400 | PCR or optical duplicate |
| 2048 | 0x800 | supplementary alignment |

The FLAG is the sum of the bits that apply. The specification states that bit 0x4 is the only
reliable place to tell whether a read is unmapped.

Common values for paired reads: 99 is 1 + 2 + 32 + 64 (first in pair, forward, mate reverse); 147
is 1 + 2 + 16 + 128 (second in pair, reverse, mate forward); 83 is 1 + 2 + 16 + 64; 163 is 1 + 2 +
32 + 128. `ngs.py flags` decodes any value.

## CIGAR operations

| Op | Description | Consumes query | Consumes reference |
|---|---|---|---|
| M | alignment match (a sequence match or mismatch) | yes | yes |
| I | insertion to the reference | yes | no |
| D | deletion from the reference | no | yes |
| N | skipped region from the reference | no | yes |
| S | soft clipping (clipped bases are present in SEQ) | yes | no |
| H | hard clipping (clipped bases are not present in SEQ) | no | no |
| P | padding (silent deletion from padded reference) | no | no |
| = | sequence match | yes | yes |
| X | sequence mismatch | yes | yes |

- Read bases accounted for = sum of M, I, S, = and X lengths.
- Reference span = sum of M, D, N, = and X lengths.
- The last reference base of the alignment is POS plus the reference span minus 1.
- `5S10M3D10M2S` at POS 100: 27 read bases, spans 23 reference bases, ends at 122.

## MAPQ

A Phred-scaled estimate that the mapping position is wrong. Low values mean the read maps equally
well in several places. The scale and the meaning of special values differ between aligners (VERIFY).

## Coordinates

SAM POS is 1-based. BAM stores 0-based internally and tools usually show 1-based. See
`sequence-formats` for the full coordinate table.
