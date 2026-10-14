# `literature-search-appraisal` prompts

Turn a question into a documented search, read the results with a method paper's usual weaknesses in
mind, and keep every reference honest. The skill logs each search, appraises each paper, and records
whether each source was read, seen or only recalled.

- **Give it:** the question and its type, the scope, what you already have, and which databases you can open
- **Skill file:** [`skills/literature-search-appraisal/SKILL.md`](../skills/literature-search-appraisal/SKILL.md)
- **Search syntax:** [`search-syntax.md`](../skills/literature-search-appraisal/references/search-syntax.md) · **Appraisal checklist:** [`appraisal-checklist.md`](../skills/literature-search-appraisal/references/appraisal-checklist.md)
- **Template it fills:** [`search-log.md`](../skills/literature-search-appraisal/assets/templates/search-log.md)
- **Compare methods with:** [`method-benchmarking`](method-benchmarking.md) · **Write up with:** [`research-writing-reporting`](research-writing-reporting.md)

## 1. Build a search

> I need the literature on benchmarks of differential expression methods for bulk RNA-seq with few replicates. Write the search as concept blocks with synonyms, give me a PubMed query with explicit parentheses, say which other sources to search, and tell me how to check that the query found what it should.

A good answer: concept blocks with synonyms, a query using capital Boolean operators and field tags
with explicit parentheses, preprint and software sources named, and a known-item test of three papers
that must be returned.

## 2. Check a reference list

> Check this reference list for citations that might be invented or wrong, mark each one read, seen or recalled, and tell me what the checker proves and what it does not: <paste references>

A good answer: a mark per entry, the checker's result for entries with a DOI, a statement that a match does
not show the paper supports the claim, and entries without a DOI passed to manual confirmation.

## 3. Is this method paper reliable

> Appraise this method paper: <paste abstract and methods>. Who ran the comparison, how were the other methods tuned, could the training and test data overlap, and what would you want to see before choosing this tool?

A good answer: a table against the checklist, a note that the developers' own benchmark is not
independent evidence, questions on tuning and leakage, and a suggestion to look for an independent comparison.

## 4. Preprint or reviewed

> This result is only on a preprint server. How do I find out whether a reviewed version exists, whether anything changed, and whether I can rely on it?

A good answer: check the preprint page and the literature databases for a reviewed version, compare the
versions, treat the preprint as a lead until then, and look for corrections or retractions.

## 5. Which tool does the literature support

> Which long-read assembler does the literature support for a 5 Mb bacterial genome? Give me the evidence, mark what you read and what you recalled, and tell me what you cannot access.

A good answer: it does not name a winner from memory as settled; it lists independent benchmarks to find,
marks anything recalled as unverified, asks about the data type and error profile, and says what it could not open.

## 6. Retractions and corrections

> Before I cite these ten papers in my methods, how do I check whether any has been retracted or corrected? <paste list>

A good answer: use the publishers' notices and a retraction database, record the date checked, and keep
the check in the log; it does not claim from memory that any paper was retracted.
