# Source map

The collection follows the organisation of Ramsden, *Bioinformatics: An Introduction* (2nd ed.,
2009). The book has three parts and 18 chapters. This table says which skill draws on which
chapter, and how much of that chapter was actually available.

**Availability.** Only the front matter, both prefaces, the table of contents, chapter 1 and the
opening of chapter 2 (to about printed p. 13) were supplied. For everything else, the skills use
the chapter and section titles from the table of contents as anchors for scope, and take their
claims from general knowledge marked `VERIFY`. A section title is not a quotation of its content.

| Part | Chapter | Topic | Skill | Supplied |
|---|---|---|---|---|
| I | 1 | Introduction | `bioinformatics-workflow` | read |
| I | 2 | The nature of information | `information-theory-sequences` | opening read |
| I | 3 | The transmission of information | `information-theory-sequences` | contents only |
| I | 4 | Sets and combinatorics | `sequence-statistics` | contents only |
| I | 5 | Probability and likelihood | `sequence-statistics` | contents only |
| I | 6 | Randomness and complexity | `information-theory-sequences`, `sequence-statistics` | contents only |
| I | 7 | Systems, networks and circuits | `omics-data-analysis` | contents only |
| I | 8 | Algorithms | `omics-data-analysis` (clustering, PCA, scaling), `machine-learning-biology` (pattern recognition) | contents only |
| II | 9 | Introduction to Part II | `gene-finding-translation` | contents only |
| II | 10 | The nature of living things | `gene-finding-translation`, `phylogenetics` | contents only |
| II | 11 | The molecules of life | `gene-finding-translation`, `protein-analysis` | contents only |
| III | 12 | Introduction to Part III | `bioinformatics-workflow`, `bioinformatics-learning-path` | contents only |
| III | 13 | Genomics | `sequence-alignment`, `gene-finding-translation`, `phylogenetics`, `ngs-pipelines`, `biological-databases` | contents only |
| III | 14 | Proteomics (with transcriptomics) | `omics-data-analysis` | contents only |
| III | 15 | Interactomics | `omics-data-analysis` | contents only |
| III | 16 | Metabolomics and metabonomics | `omics-data-analysis` | contents only |
| III | 17 | Medical applications | `variants-population-genetics` and `data-governance-ethics` touch it; no clinical guidance | contents only |
| III | 18 | The organization of knowledge | `biological-databases` (ontology and annotation) | contents only |

## What the book leaves out

Chapter 1.2 says practical programming and database handling are left out because other books
cover them, and the same for the design of genetic association studies. So `sequence-formats`,
`bioinformatics-programming`, `biological-databases`, `experimental-design`,
`variants-population-genetics`, `reproducible-research-code`, `research-writing-reporting`,
`data-governance-ethics` and the scripts in this collection are original work, not a summary of the
book. They are checked by self-tests with hand-computed values, not by the text.

## Upgrade path

When the full text is available, read the chapter behind a skill, then replace its
"contents only" claims with quoted-free paraphrases and page numbers, and change this table's
"Supplied" column to `read`. Keep the book itself out of the repository.
