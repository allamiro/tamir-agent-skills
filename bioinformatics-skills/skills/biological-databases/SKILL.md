---
name: biological-databases
description: Finds, identifies, cites and versions biological data and records, including reading accession numbers and which database they belong to, accession versus version, mapping identifiers between databases, pinning releases and genome builds, judging the reliability of annotations, licences, and where to deposit your own data. Use for "which database has this", "what kind of ID is NM_000546.6", "map these gene IDs", "how do I cite this dataset", "which genome build", "can I trust this annotation", "where do I submit sequencing data". Use sequence-formats for file formats, bioinformatics-review to audit how annotations were used, and reproducible-research-code to record versions.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Biological databases

## Purpose and activation

Make sure the right record, at the right version, from a source that can be trusted, is what the
analysis uses, and that anyone else can get the same one. Most database errors are quiet: an
identifier that fits two databases, an accession whose sequence changed, a gene symbol that Excel
turned into a date. Activate when the user names an identifier, asks where data live, maps IDs
between sources, or needs to cite or deposit data.

## Required inputs

The entity (gene, transcript, protein, genome, variant, sample, dataset, paper); the identifiers
the user has and where they came from; the organism and genome build; the date or release of any
download; the licence or access terms; and the purpose (analysis, citation, deposition).

## Workflow

1. **Name the entity.** A gene, its transcripts and its protein have different identifiers. Say
   which one is wanted.
2. **Classify each identifier.** `python3 scripts/accessions.py classify ID ...` lists every format
   a string fits. If it fits more than one, find out where it came from. Do not guess.
3. **Pin the version.** Record accession and version, the database release, the genome build and
   the download date. `accessions.py check FILE` flags identifiers with no version.
4. **Choose the source for the entity** (`references/using-databases-well.md`). Prefer the
   primary or curated source and say which release.
5. **Map identifiers carefully.** Mapping between databases can be one-to-many, many-to-one or
   absent, and old identifiers are retired. Keep the unmapped and ambiguous lists, not only the
   matches.
6. **Check the evidence behind an annotation.** An entry inferred by similarity to another entry
   inherits that entry's errors. Prefer experimentally supported annotations for conclusions.
7. **Check licence and access** before copying or redistributing data.
8. **Cite and deposit.** Cite datasets by accession and version, software by name and version, and
   deposit your own raw data and metadata in a public repository where the terms allow.
9. **Record it** in the methods record from `reproducible-research-code`.

## Decision framework

| Situation | Choice |
|---|---|
| An identifier fits two databases | Ask for the source; both candidates stay in the notes until resolved |
| Same accession, different version | Different records; compare the sequences before mixing |
| Gene symbol as the key | Do not; use a stable identifier, and store symbols as text |
| Annotation from a different genome build | Convert or re-fetch; never mix builds |
| Annotation labelled "inferred" or "predicted" | Treat as a lead, not as evidence |
| Human or controlled-access data | `data-governance-ethics` first |
| Raw reads for a paper | Deposit in a public archive and cite the accession |

## Implementation guidance

- Store the identifier, its version and the source in separate columns.
- Treat identifiers as case-sensitive text. Never let a spreadsheet reformat them; gene symbols such
  as SEPT2 and MARCH1 are known to be turned into dates.
- Keep a mapping table with its provenance: source, release, date, and the rule for choosing among
  several matches.
- Download by script from a fixed release and record the checksum.
- `references/identifiers.md` lists the formats and says which were verified.

## Failure and edge cases

- **Version drift:** the same accession with a different sequence a year later.
- **Retired or merged identifiers** that silently drop out of a mapping.
- **One-to-many mappings** that duplicate rows and inflate counts.
- **Species mix-ups** from a symbol shared across organisms.
- **Genome build mismatch** between a sequence file and an annotation file.
- **Copied annotation errors,** passed from entry to entry by similarity.
- **Predicted records** (labelled as models) treated as curated ones.
- **Licence terms ignored** when redistributing.
- **Spreadsheet damage** to identifiers.

## Validation

- `python3 scripts/accessions.py --selftest` must pass.
- Hand check: `NM_000546.6` is a RefSeq record, version 6; `P12345` fits two databases.
- Every identifier in the analysis has a source, a version and a download date.
- Falsifier: someone else, following the record, retrieves a different sequence.

## Expected output

The entity and identifiers with their classification, the versions and releases pinned, the mapping
with its unmapped and ambiguous lists, the evidence level of each annotation, the licence status,
and the citation or deposition plan.

## Sources and confidence

- INSDC (GenBank) nucleotide and protein accession layouts and the RefSeq underscore rule: NCBI
  accession-prefix page, read 2026-10-14. The Ensembl layout of ENS, species, feature and eleven
  digits: Ensembl stable-ID page, read 2026-10-14
- The UniProt accession pattern, PDB, SRA and GEO patterns, RefSeq prefix meanings and Ensembl feature
  letters: general knowledge; the pages that hold them could not be read, so the script marks them
  unverified. VERIFY against the database's own documentation
- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: ch. 13.4.1 (database reliability, section
  title only), ch. 18 (organization of knowledge, ontology), and ch. 1.2 (supplied text: the book
  leaves out database handling)
- Not covered: database design, running a database server, or query languages
