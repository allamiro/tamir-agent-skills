# Data plan notes

## NIH-style elements (draft)

Per university guides found in search results on 2026-10-14; the funder's own notice was not read, so
check the current template. The checker `dmpcheck.py` looks for each element by keyword.

| Element | What to say |
|---|---|
| Data type | Kinds of data, estimated volume, which will be preserved and shared |
| Related tools, software and code | Software needed to access or interpret the data; where the code is released |
| Standards | Formats and metadata standards |
| Data preservation, access and timelines | Repository, persistent identifier, how long, when shared |
| Access, distribution or reuse considerations | Consent, privacy, licences, embargoes |
| Oversight | Who monitors compliance |

## FAIR groups

The four FAIR groups (findable, accessible, interoperable, reusable) are from the FAIR Guiding Principles
paper (record checked on Crossref 2026-10-14; the paper was not read). The checker's `fair` profile looks for
signs of each group. It is a prompt to think, not a measure of FAIRness.

## Typical sizes to ask about

Ask for the number of samples, the data type and the format, then compute storage from those. Do not quote a
size from memory; use the facility's or the repository's figures.

## Schedule file

```text
task,weeks,after
data access,6,
quality control,2,data access
alignment,3,quality control
statistics,4,alignment
writing,5,statistics
```

Run `python3 scripts/schedule.py PLAN.csv --deadline 24` to see the critical path and whether the plan fits
with a buffer.
