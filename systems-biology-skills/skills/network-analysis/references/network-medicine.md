# Network and systems medicine, and provenance

## Network medicine in brief

The working hypothesis is that a disease reflects the perturbation of a module of interacting
molecules rather than a single gene, so genes linked to the same disease tend to sit close together in the
interaction network. Uses: proposing new disease genes from the neighbourhood of known ones, explaining
comorbidity through shared modules, and choosing drug targets or repurposing candidates by network
proximity. Each use inherits the interactome's incompleteness and study bias.

## Systems medicine

Systems medicine combines clinical, molecular and patient data with mechanistic and statistical models
across scales from molecular reactions (seconds) to disease progression (years). The workbook's
introduction, drawing on Apweiler et al. 2018, stresses that focused clinical questions allow models that
are context-specific yet predictive, and that data integration depends on knowing where each datum came
from.

## Provenance fields to record (after W3C PROV)

W3C PROV models provenance with entities (data), activities (what produced or changed them) and agents
(who or what was responsible). For a network, record at least:

| Field | Example |
|---|---|
| Entity | edge list file, with checksum |
| Derived from | database name, release, download date, query |
| Activity | filtering script and version, parameters (score cut-off, organism) |
| Agent | person or pipeline that ran it |
| Evidence per edge | experimental method, publication identifier, confidence score |

Source: the workbook names W3C PROV (<https://www.w3.org/TR/prov-overview/>) as helpful but rarely used in
biomedicine; the field mapping above is author knowledge, VERIFY against the PROV specification.
