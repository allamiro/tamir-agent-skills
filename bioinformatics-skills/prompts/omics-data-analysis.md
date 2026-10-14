# `omics-data-analysis` prompts

Analyse expression, protein, interaction and metabolite tables, and the clustering and network
methods used on them, starting from the design rather than the plot.

- **Give it:** the data matrix and what its rows and columns are, the sample table with condition
  and batch, how the values were produced, and the comparison you care about
- **Skill file:** [`skills/omics-data-analysis/SKILL.md`](../skills/omics-data-analysis/SKILL.md)
- **References:** [`clustering-and-dimension-reduction.md`](../skills/omics-data-analysis/references/clustering-and-dimension-reduction.md)
  and [`network-inference.md`](../skills/omics-data-analysis/references/network-inference.md)
- **For tests:** [`sequence-statistics`](sequence-statistics.md) · **To audit:** [`bioinformatics-review`](bioinformatics-review.md)

## 1. Check the design first

> Analyse this expression matrix: 20,000 genes by 12 samples, with a sample sheet giving condition, batch and date. Before any differential test, check the design, run quality control and a PCA coloured by batch and by condition, and tell me what would make me stop.

A good answer: a count of biological replicates per group, a table of condition against batch, a
PCA or clustering of samples coloured by batch and by condition, and a stop if batch and
condition line up perfectly.

## 2. A perfect separation

> My PCA separates the treated and untreated samples perfectly, but the two groups were run on different days. What does that show, and what can I still conclude?

A good answer: the separation could be treatment or day; with no overlap between the two the
effects cannot be told apart, so the result is a lead that needs a new batch design.

## 3. Too many hits

> I found 2,000 genes with p < 0.05 out of 20,000 tested, with no correction. How many would I expect by chance, and what should I do?

A good answer: about 1,000 expected if no gene has a real effect, so perhaps half the list could
be false; adjust across all 20,000 tests and report effect sizes.

## 4. Are these clusters real

> I clustered the samples hierarchically with correlation distance and average linkage and got four clusters. How do I check they are real, and what could make them an artefact?

A good answer: stability checks (drop samples, change distance or scaling), colouring by batch and
date, testing whether clusters differ in something not used to make them, and noting that any
method returns clusters.

## 5. A correlation network

> I built a network from pairwise correlations of metabolites at a threshold of 0.7. How do I know it is not noise or an artefact of the threshold, and what does an edge mean?

A good answer: an edge means two features move together, not that they interact; show the
network at several thresholds, rebuild it from shuffled data, and expect indirect links.

## 6. Enrichment background

> Which background should I use for a gene-set enrichment test, and what goes wrong if I use the whole genome?

A good answer: the features that could have been detected in this experiment, since the
whole genome makes anything expressed in the tissue look enriched.
