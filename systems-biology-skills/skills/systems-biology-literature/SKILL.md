---
name: systems-biology-literature
description: Finds, reads, appraises and cites systems biology literature and models, covering search strategy across PubMed, Europe PMC, Google Scholar and preprint servers, finding published models in BioModels and parameters in databases such as BRENDA and SABIO-RK, reading a modelling paper critically (question, formalism, assumptions, parameter sources, validation), tracking which claims rest on which source, and checking references so none are invented. Use for "find papers on modelling this pathway", "is there a published model of this", "where can I get kinetic parameters", "summarise this modelling paper", "check my reference list", "read this paper and tell me if the model is any good", "related work for my model". Use model-review for a full audit of a model, modeling-paper-writing to write related work, and systems-biology-programming to reuse a model file.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Systems biology literature

## Purpose and activation

Modelling papers combine biology, mathematics and code, so reading one means checking all three, and
reusing one means finding its model file and the provenance of every parameter. References in this field
are easy to invent plausibly; every citation must be traceable. Activate when the user searches for
papers, models or parameters, reads a modelling paper, or needs a reference list checked.

## Required inputs

The topic (pathway, organism, cell type, formalism); what the literature is for (background, parameters,
a model to reuse, related work, a review); the date range; and any references already in hand.

## Workflow

1. **Search systematically:** write the query (synonyms for the pathway, organism, and the formalism words:
   "kinetic model", "ODE", "constraint-based", "Boolean"), run it in at least two databases, and record the
   date and counts. Include preprints, labelled as not peer reviewed.
2. **Search model repositories:** BioModels (curated and non-curated), the Physiome model repository for
   CellML, and the paper's supplementary files or code repository.
3. **Search parameter databases** (BRENDA, SABIO-RK) and record the organism, pH, temperature and assay of each
   value; parameters measured in vitro may not hold in vivo.
4. **Read each paper with the checklist** in `references/reading-checklist.md`: question, formalism,
   assumptions, parameter sources, fitting, validation on independent data, code and model availability.
5. **Record each source** with `assets/templates/source-record.md`, marking it read (opened and read), seen
   (cited by another source) or recalled (from memory, unverified). Never cite a recalled source.
6. **Check the reference list** with `python3 scripts/citecheck.py REFS.txt --online`; a DOI that does not
   resolve is the strongest sign of an invented reference. Check books and theses by hand.
7. **Synthesise** by question, not by paper: which models agree, where they differ, and why (different
   assumptions, data, or organisms).

## Decision framework

| Need | First stop | Check |
|---|---|---|
| Background on a pathway | Recent reviews | Their primary sources for key claims |
| An existing model | BioModels, the paper's supplement | Does the file reproduce the paper's figures? |
| Kinetic parameters | BRENDA, SABIO-RK, primary enzymology papers | Organism, conditions, assay |
| Genome-scale metabolic model | BiGG, BioModels, the authors' repository: VERIFY | MEMOTE report, version |
| Methods for an analysis | The method's original paper and a recent benchmark | Whether the benchmark matches your setting |
| Teaching material | Open textbooks such as the Sauter and Albrecht workbook | Licence for reuse |

| Source type | Weight |
|---|---|
| Peer-reviewed paper with model file that reproduces | High |
| Peer-reviewed paper, no model file | Medium: equations may contain typos |
| Preprint | Medium-low until reviewed; label it |
| Review | Lead to primary sources |
| Database value without its primary reference | Low |
| Recollection | None until looked up |

## Failure and edge cases

- **An invented reference** with a plausible journal and year.
- **Parameters copied from a model** that copied them from another model, with the original lost.
- **Equations in a paper that differ from the model file.**
- **A curated BioModels entry taken as validated biology;** curation checks reproduction of results, not truth.
- **Preprints cited as established.**
- **Searching only one database** or only English titles.

## Validation

- `python3 scripts/citecheck.py --selftest` passes, and `--online` shows no DOI-NOT-FOUND on the list.
  A pass shows the record matches; it does not show the paper says what is cited.
- Every parameter has a primary source with organism and conditions.
- Every reused model reproduces at least one figure of its paper.
- Falsifier: a librarian cannot find a cited reference, or the cited page does not contain the claim.

## Expected output

The search record (queries, databases, dates, counts); a sources table with read, seen or recalled marks;
models and parameters found with provenance; a synthesis by question; and the checked reference list.

## Sources and confidence

- Repository and database names: author knowledge, VERIFY current access and scope; BioModels:
  Malik-Sheriff et al., doi:10.1093/nar/gkz1055 (record checked on Crossref 2026-10-15)
- The reference checker is shared with the other collections in this repository
- Sauter and Albrecht 2023, doi:10.11647/OBP.0291: further reading recommended in the workbook (Barabási et al.,
  network medicine; Apweiler et al., systems medicine) (supplied text)
