---
name: literature-search-appraisal
description: Finds and appraises bioinformatics and computational biology literature, covering search strategy (PubMed fields and MeSH terms, Europe PMC, preprint servers), forward and backward citation chasing, reading a methods paper, judging a tool or benchmark claim, checking for retractions and corrections, reporting guidelines such as PRISMA and DOME, a search log, and citing without inventing references. Use for "find papers on", "which tool does the literature support", "is this method paper reliable", "is this preprint peer reviewed", "has this paper been retracted", "write a PubMed query", "review the literature on X", "check my references". Use method-benchmarking to design or judge a comparison, research-proposal-planning for the plan, research-writing-reporting for the write-up, and bioinformatics-review to audit an analysis.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Literature search and appraisal

## Purpose and activation

Most wasted effort in a computational project starts with the wrong tool or an unchecked claim from a
paper. This skill turns a question into a documented search, reads what it finds with a method paper's
usual weaknesses in mind, and records how each source is known so that no reference is invented.
Activate when the user needs prior work, a tool choice backed by evidence, a literature section, or a
reference list checked. It does not run the experiments in a paper (`method-benchmarking`) or write the
manuscript (`research-writing-reporting`).

## Required inputs

The question in one sentence and its type (tool choice, method background, biology of a gene or pathway,
benchmark evidence, dataset discovery, novelty check); scope (organism, data type, years, languages);
what the user already has (key papers, accessions); the databases the user can open; and how the answer
will be used.

## Workflow

1. **Write the question and its type,** then split it into concept blocks: the biological system, the data
   type, the method or tool, and the outcome or metric.
2. **List synonyms for each block,** including gene and protein name variants (symbols collide and change,
   so add identifiers from the gene database) and both spellings of methods.
3. **Build the query** with parentheses around synonyms joined by OR and blocks joined by AND
   (`references/search-syntax.md`). Run it in more than one source: a bibliographic database, a literature
   database that includes preprints, a preprint server, and, for tools, the software repository and its release history.
4. **Log every search** (`assets/templates/search-log.md`): source, date, query, filters, hits.
5. **Check recall with a known-item test:** choose three papers that must be found and confirm the query returns them.
6. **Screen** titles and abstracts, then full texts, and record why each paper is kept or dropped.
7. **Chase citations** backward (the references of the best papers) and forward (who cites them), and look for
   later corrections, comments and independent evaluations.
8. **Appraise** each kept paper with `references/appraisal-checklist.md`, and check retraction and correction status.
9. **Extract** claim, evidence, data, metric and limits into a table, then synthesise: what is agreed, what is
   contested, what is unknown.
10. **Cite** with a `read`, `seen` or `recalled` mark per source, and run
    `python3 scripts/citecheck.py LIST --online` on the reference list.
11. **Report** the answer, the search log, the appraisal table, the gaps and the open questions.

## Decision framework

| Question | Start with | Then |
|---|---|---|
| Which tool for this task | Independent benchmarks and community challenges | The developers' paper, release notes, issue tracker |
| Background on a method | A recent review and the original method paper | Papers that correct or extend it |
| Biology of a gene or pathway | The gene database entry and its linked references | A literature search with identifiers |
| Does a dataset exist | The sequence and expression repositories (`biological-databases`) | Papers that cite the accession |
| Is the idea new | Several sources, including preprints and software lists | Forward citations of the closest papers |

| Source | Weight | Check first |
|---|---|---|
| Independent benchmark | High for what it tested | Neutrality, versions, datasets (`method-benchmarking`) |
| Developers' own method paper | Medium | Who ran the comparison and how methods were tuned |
| Community challenge | High for its task | Whether your data resemble the task |
| Preprint | Lead until a reviewed version exists | Whether the reviewed version changed the result |
| Review article | Context | The date and the papers it selects |
| Documentation or blog | Lead only | The paper or code it describes |
| Your recollection | None | Look it up |

## Implementation guidance

- Use explicit parentheses; do not rely on operator precedence. Boolean operators are written in capitals in PubMed.
- Search by identifier as well as by name, and note the database release or date for each accession.
- Count how many results each concept block alone returns; a block that returns almost everything or almost
  nothing is badly worded.
- Reporting guidelines help read a paper: the PRISMA 2020 statement for systematic reviews, and the DOME
  recommendations for supervised machine learning in biology.
- Keep the search log even for an informal search; it is what lets someone rerun it.
- For tools, record version, licence, last release and whether the repository is maintained.

## Failure and edge cases

- **Taking the developers' benchmark as independent evidence.** A method's authors tend to find their method best.
- **Citation counts as a quality measure.** They track age and popularity.
- **A single database or a single synonym,** so the search misses preprints, software and renamed genes.
- **Gene symbols that mean something else** in another organism or era.
- **A retracted or corrected paper** still cited. Check before relying on a result.
- **Preprint treated as reviewed,** or the reviewed version not checked for changes.
- **Reading only abstracts.**
- **Invented references.** A plausible title, journal and year can be produced without any paper behind them.
- **Selection bias:** keeping only the papers that agree.
- **Paywalled sources not reached.** Say so and mark the claim `seen`.

## Validation

- The known-item test passes: all three chosen papers are returned by the query.
- Every reference has a `read`, `seen` or `recalled` mark, and `python3 scripts/citecheck.py --selftest` passes;
  on the real list `--online` shows no `DOI-NOT-FOUND` or `MISMATCH`. A pass means the record matches the line,
  not that the paper says what is cited.
- Every claim in the synthesis traces to a location in a source someone saw.
- Falsifier: a key paper known to the user's lab that the search should have found, or a reference that does not exist.

## Expected output

A short answer; the search log; an appraisal table (source, type, claim, evidence, limits, status checks);
a synthesis with confidence; a reference list with `read`/`seen`/`recalled` marks and the checker's result;
and the gaps.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: nothing in the supplied text covers literature
  search practice; this skill extends the collection to research work
- PubMed syntax: library guides found in search results, 2026-10-14 (field tags, capital Boolean operators,
  parentheses); the NLM user guide was not read: VERIFY
- Guidelines: the PRISMA 2020 statement (BMJ 2021) and the DOME recommendations (Nature Methods 2021), records
  checked on Crossref 2026-10-14; the Retraction Watch database moved to Crossref in 2023 (Crossref announcement
  record); the self-assessment trap (Norel et al., Mol Syst Biol 2011), record checked
- Appraisal checklist and source-weight table: own design, VERIFY against the standards of the user's field
- Not covered: running a full systematic review, meta-analysis statistics, or access to paywalled databases
