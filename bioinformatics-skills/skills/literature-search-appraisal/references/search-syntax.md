# Search syntax

PubMed notes below come from library guides found in search results on 2026-10-14. Confirm in the NLM
PubMed User Guide before relying on a detail, and check each other database's own help, because tags
and operators differ.

| Element | Example | Notes |
|---|---|---|
| Boolean operators | `AND`, `OR`, `NOT` | Written in capitals; lower case is not read as an operator |
| Grouping | `(rna-seq OR "RNA sequencing")` | Use parentheses so the order is explicit |
| Phrase | `"single cell"` | Quotes keep words together; behaviour with automatic term mapping varies |
| Title and abstract | `normalization[tiab]` | Limits to those fields and skips automatic term mapping |
| Controlled vocabulary | `"Sequence Alignment"[MeSH Terms]` | MeSH terms are assigned by indexers and lag behind new papers |

## A pattern for a tool question

```text
(("differential expression"[tiab] OR "differential gene expression"[tiab])
 AND (benchmark*[tiab] OR comparison[tiab] OR evaluat*[tiab]))
AND ("RNA-seq"[tiab] OR "RNA sequencing"[tiab])
```

## Gene and protein names

Search the official symbol, the older aliases and the database identifier, then check that hits refer to the
right organism. Symbols such as short common words collide with ordinary vocabulary.

## Other sources

- Europe PMC indexes a wide range of literature and some preprints: VERIFY its scope and syntax.
- bioRxiv and medRxiv hold preprints; each preprint page says whether a reviewed version exists.
- For software, read the repository's release history, open issues and licence as well as the paper.
