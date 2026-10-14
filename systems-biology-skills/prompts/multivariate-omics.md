# `multivariate-omics` prompts

Find structure and predictive variables in omics tables without fooling yourself.

- **Give it:** the samples-by-variables table, preprocessing so far, sample metadata (groups, batches,
  response), the number of samples per group, and the question
- **Skill file:** [`skills/multivariate-omics/SKILL.md`](../skills/multivariate-omics/SKILL.md)
- **Which method answers which question:** [`method-map.md`](../skills/multivariate-omics/references/method-map.md)

## 1. Should I scale

> Run a PCA on my omics data and tell me whether to scale: sample,g1,g2,g3 with rows s1 1,2,0.5; s2 2,4,0.4; s3 3,6,0.6; s4 4,8,0.5; s5 5,10,0.45.

A good answer: without scaling PC1 explains essentially 100 percent of the variance and is dominated by g2,
which has the largest variance. With scaling, PC1 explains 66.7 percent, with equal loadings on g1 and g2
because they are perfectly correlated, and PC2 (33.3 percent) is g3. It recommends scaling when variables
have different units or ranges, and notes that g1 and g2 carry the same information.

## 2. VIP and scaling

> In a PLS regression of y on g1, g2 and g3, g2 has twice the VIP of g1 even though g2 = 2 x g1. Why?

A good answer: the data were not scaled, so g2's larger variance gives it a larger weight. With scaling the
two have equal VIP (about 1.22 each). A VIP above about 1 is a heuristic, not a significance test, and
perfectly collinear variables cannot be told apart by any method.

## 3. Is my PLS-DA overfitted

> My PLS-DA perfectly separates 8 tumours from 8 controls using 5,000 metabolites. Is that a result?

A good answer: not by itself. With far more variables than samples, PLS-DA separates even random labels.
It needs cross-validated Q² with the number of components chosen inside the cross-validation, a
permutation test with shuffled labels, and feature selection kept inside the cross-validation loop. It
should also check whether batch is confounded with group.

## 4. PCA or factor analysis

> My collaborator calls the first principal components of my questionnaire and biomarker data "latent factors". Is that right?

A good answer: no. PCA summarises variance and does not model latent constructs or measurement error. Factor
analysis (exploratory, then confirmatory on another sample) estimates latent factors with a measurement
model. It points to `quantitative-research-methods` for the construct definition and validity evidence.

## 5. Choose the method

> I have proteomics from 30 patients in 3 treatment groups, measured twice each. Which multivariate method should I use to test treatment effects?

A good answer: repeated measures within patients call for a multilevel (mixed) model, or per-protein mixed
models with false discovery rate control. MANOVA is unsuitable with more proteins than samples; PERMANOVA
works on a distance matrix if a global test is wanted. PCA is for exploration and batch checks, not for
testing.
