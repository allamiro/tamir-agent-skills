# Coordinates

## The two conventions

| Name | First base is | An interval is | Example: the first 100 bases |
|---|---|---|---|
| 0-based, half-open | 0 | start included, end excluded: [start, end) | start 0, end 100 |
| 1-based, closed | 1 | start and end both included: [start, end] | start 1, end 100 |

Length is end minus start for half-open and end minus start plus one for closed. The two describe
the same bases: `seq[start:end]` with half-open coordinates equals `seq[start-1:end]` with closed
ones.

## Formats

| Format | Convention | Basis |
|---|---|---|
| BED | 0-based, half-open | UCSC format FAQ, read 2026-10-14: first base is 0, chromEnd not included |
| GFF3 | 1-based, start <= end | GFF3 specification, read 2026-10-14 |
| SAM POS | 1-based, 0 means unmapped | SAM specification, read 2026-10-14 |
| VCF POS | 1-based | general knowledge, VERIFY |
| BAM | 0-based internally, shown 1-based by tools | general knowledge, VERIFY |
| Python and most programming languages | 0-based, half-open slices | language rule |

## Conversion

| From | To | Formula |
|---|---|---|
| BED (s, e) | 1-based closed | (s + 1, e) |
| 1-based closed (s, e) | BED | (s - 1, e) |

A zero-length BED interval (an insertion point, start equal to end) has no 1-based closed form;
the conversion function refuses it rather than inventing one.

## Typical off-by-one patterns

| Symptom | Likely cause |
|---|---|
| Every feature shifted by one base | A 0-based and a 1-based file mixed |
| Feature one base too long or short | End treated as included in one tool and excluded in another |
| First base of a chromosome missing | A start of 0 passed to a 1-based tool |
| Slice returns the wrong length | Closed coordinates used as a Python slice |
| Reverse-strand coordinates wrong | Position counted from the wrong end of the reverse complement |

For a feature on the reverse strand, the coordinates in GFF3 and BED still run along the forward
strand, start less than end; only the direction of reading flips. `genecode.py` follows the same
rule for ORFs.

## Habits

- Name the convention in the variable (`start_0`, `end_excl`, `pos_1`).
- Convert once, at the file boundary.
- Test with a sequence where every base is different, so a shift of one shows at once.
- Check the genome build as well: coordinates from one build do not apply to another.
