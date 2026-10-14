# Clustering and dimension reduction

The source's chapter on algorithms names clustering, principal component and linear discriminant
analysis, wavelets, multidimensional scaling, seriation and visualization (section titles from its
table of contents). The guidance below is general practice; VERIFY it against a statistics text.

## Before any method: distance and scale

| Choice | Effect |
|---|---|
| Euclidean distance on raw values | Dominated by the features with the largest values |
| Scale each feature (divide by its spread) | Every feature counts equally, which also boosts noise features |
| Distance from correlation, 1 - r | Groups by profile shape, ignores level |
| Log-transform before distance | Often needed for intensities and counts that span orders of magnitude |

The result depends more on these choices than on the clustering algorithm. State them.

## Clustering

| Method | Idea | Watch for |
|---|---|---|
| Hierarchical, average linkage | Repeatedly join the closest groups; average linkage is the method called UPGMA in `phylogenetics` | You must cut the tree to get clusters, and the cut is a choice |
| Hierarchical, single linkage | Join by closest members | Chaining: long thin clusters |
| Hierarchical, complete linkage | Join by farthest members | Compact clusters, sensitive to outliers |
| k-means | Assign points to k centres and iterate | k is chosen by you; results depend on the random start, so run many starts and fix a seed |

Every method returns clusters, whether or not clusters exist. Check:

- Stability: remove a few samples or add noise; do the same groups appear?
- Batch: colour the clusters by batch and date; if they match, the structure is technical.
- Separation: a measure such as the silhouette value helps, but is no proof (VERIFY).
- Meaning: test whether clusters differ in something that was not used to make them.

## Principal component analysis

PCA rotates the data to new axes (components) ordered by the variance they explain. Centre the
features first; decide whether to scale them. Report the fraction of variance in the first
components. Component signs are arbitrary. A component is a summary of variation, not a biological
process; loadings show which features contribute. With far fewer samples than features, at most
(samples - 1) components are non-zero.

## Linear discriminant analysis

A supervised method that finds directions separating known groups. With many features and few
samples it separates the training data perfectly and fails on new data; validate on held-out
samples that played no part in choosing features or settings.

## Multidimensional scaling and seriation

Multidimensional scaling places samples in two or three dimensions so that plotted distances
approximate the original ones; report how well (the stress or the correlation with the original
distances). Seriation orders items so that similar ones are adjacent. Both give a picture, not a test.

## Visualisation

- A heatmap's row and column order, colour scale and clipping are all choices; say what they are.
- Nonlinear embeddings (such as t-SNE or UMAP) can distort global distances and cluster sizes;
  do not read distances between far-apart groups from them (VERIFY).
- Plot individual points where the sample is small; do not hide them in a summary.

## Checks that catch most problems

1. Colour every plot by batch, then by condition.
2. Rerun on shuffled labels.
3. Repeat with a different distance or scaling and compare.
4. Hold out samples and test the finding on them.
