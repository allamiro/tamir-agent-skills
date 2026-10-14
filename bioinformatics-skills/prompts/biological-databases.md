# `biological-databases` prompts

Identify, version, map, cite and deposit biological data without losing track of which record you
used.

- **Give it:** the identifiers and where they came from, the organism and genome build, the date of
  any download, and the licence or access terms
- **Skill file:** [`skills/biological-databases/SKILL.md`](../skills/biological-databases/SKILL.md)
- **References:** [`identifiers.md`](../skills/biological-databases/references/identifiers.md) and
  [`using-databases-well.md`](../skills/biological-databases/references/using-databases-well.md)
- **Related:** [`sequence-formats`](sequence-formats.md), [`data-governance-ethics`](data-governance-ethics.md)

## 1. Read an identifier

> What kind of identifier is NM_000546.6, and what does the .6 at the end mean? What should I record alongside it?

A good answer: a RefSeq record (the underscore in the third position marks RefSeq, and NM_ is a
curated mRNA), version 6; the version, the database release and the retrieval date.

## 2. An identifier that fits two databases

> Is P12345 a UniProt accession or a GenBank accession? How would I find out?

A good answer: it fits both layouts, so the string alone cannot say; check where it came from and
keep the source next to it.

## 3. Check a list

> I have a file of 500 identifiers, some with versions and some without. Tell me which need fixing before I cite them, and why.

A good answer: those without a version suffix, those that fit more than one database, and those not
recognised, each with a reason.

## 4. Mapping that multiplies rows

> I mapped 1,000 gene identifiers from one database to another and got 1,150 rows. What happened and how do I handle it?

A good answer: some identifiers map to more than one target (one-to-many); decide how to choose, keep
the unmapped and ambiguous lists, and record the rule.

## 5. Dates in a gene list

> A gene list I opened in a spreadsheet now has dates where some symbols were. What happened and how do I stop it?

A good answer: the spreadsheet converted symbols such as SEPT2 and MARCH1 into dates; keep identifier
columns as text, use stable identifiers rather than symbols, and avoid spreadsheets for them.

## 6. Depositing and citing

> Where should I deposit my raw sequencing reads and processed tables, and how should the paper cite them?

A good answer: a public archive for reads and metadata where the consent allows, with the accession
and version in the paper, and a note on any controlled-access route.
