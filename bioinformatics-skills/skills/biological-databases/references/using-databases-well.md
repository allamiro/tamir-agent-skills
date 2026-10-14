# Using databases well

General practice; VERIFY details against each database's documentation. Database names are
examples, not requirements.

## Where to look, by entity

| Entity | Typical sources (examples) |
|---|---|
| Nucleotide sequences, assemblies | INSDC members (GenBank, ENA, DDBJ); RefSeq for curated records |
| Genes, transcripts, genomes with annotation | Ensembl, NCBI Gene and RefSeq, organism-specific databases |
| Proteins and their annotation | UniProt |
| Structures | PDB |
| Sequencing reads | SRA, ENA |
| Expression and array data | GEO, ArrayExpress |
| Pathways and ontologies | Gene Ontology, KEGG, Reactome |
| Variants | dbSNP, ClinVar, gnomAD, 1000 Genomes |
| Literature | PubMed, preprint servers |

Prefer the source closest to the original submitter or curator, and say which release you used.

## Mapping identifiers

| Case | Consequence |
|---|---|
| One-to-one | Safe |
| One-to-many (one gene, several transcripts) | Rows multiply; decide which to keep and why |
| Many-to-one | Information merged; counts can double up |
| No match | Retired, renamed or absent; list them and do not drop silently |
| Different organism | Same symbol, different gene |

Keep the mapping as a table with its source and release. Prefer stable identifiers to symbols.

## Reliability of annotation

The source text lists database reliability as a topic in its comparison chapter (section title only).
In practice:

- Each annotation has a type of evidence behind it: experiment, curator judgement, or inference by
  similarity or by computation. Many databases record the evidence type; use it.
- Inference chains copy errors: an entry labelled by similarity to a labelled entry has no
  independent support.
- Predicted models are not curated records.
- Sequence databases contain mistakes, contamination and mislabelled species; check suspicious entries
  against other sources.

## Licences and access

Some data are open, some require attribution, some restrict commercial use or redistribution, and
human data may be controlled-access. Read the terms before copying or sharing, and see
`data-governance-ethics`.

## Citing and depositing

- Cite a dataset by repository, accession (with version) and date; cite the paper describing it if
  one exists.
- Cite software by name and version.
- Deposit raw reads, processed matrices and metadata in a public archive where the consent and
  terms allow, and give the accession in the paper.
- Metadata that cannot be understood without you (sample names such as S1) are a deposition failure.

## Spreadsheet hazard

Spreadsheet programs can convert gene symbols such as SEPT2 and MARCH1 into dates and long
identifiers into scientific notation. Keep identifier columns as text, or avoid spreadsheets for them.
