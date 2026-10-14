# `bioinformatics-workflow` prompts

Plan an analysis from question to result: the claim, the null model, the data and its provenance,
the skill for each step, the controls, and the point at which to stop.

- **Give it:** the biological question in your words, the data (type, organism, accession, size),
  what has been done, and who will use the result
- **Skill file:** [`skills/bioinformatics-workflow/SKILL.md`](../skills/bioinformatics-workflow/SKILL.md)
- **Template it fills:** [`analysis-plan.md`](../skills/bioinformatics-workflow/assets/templates/analysis-plan.md)
- **Hands work to:** every other skill, and to [`bioinformatics-review`](bioinformatics-review.md) at the end

## 1. A plan from a loose question

> I have RNA-seq from treated and untreated cells, three replicates each, sequenced in two batches. Plan the analysis. State the claim so the data could show it false, name the null model, list what to record about the data, and say which skill handles each step.

A good answer: a falsifiable claim, a null such as shuffled sample labels, a data record with
accessions and genome build, a check of how the two batches fall across the conditions before any
test, and a hand-off to `omics-data-analysis` and `sequence-statistics`.

## 2. A new genome

> I have a newly assembled bacterial genome. Plan how to find its genes and check them. Say what would count as evidence for a gene, what I should compare against, and what the chance level is for an open reading frame at this genome's GC content.

A good answer: ORF finding with a length cutoff set for the GC content, similarity to known
proteins as the next evidence level, and a statement that open frames alone are candidates.

## 3. Turn a topic into a claim

> My question is: <paste your question>. Rewrite it as a claim that the data could show false, tell me which random baseline it should be tested against, and say what result would make me drop it.

A good answer: one sentence of the form "X differs from Y in way Z", a named null model, and a
stated falsifying result.

## 4. Test small before running big

> I plan to run this pipeline on the full dataset tomorrow: <paste the steps>. For each step, give me a toy input with a known answer to run first, and say how I will know the step is right.

A good answer: a small known-answer input for each step, such as a hand-checked coordinate
conversion or an alignment with a computed score, before any real data.

## 5. Find the gaps in a plan

> Review my plan against the analysis-plan template and list everything missing or vague: <paste plan>. Do not rewrite it; list gaps in order of how much they could change the conclusion.

A good answer: a ranked list of gaps such as no null model, no controls, an unrecorded genome
build, or a stopping rule decided after looking.
