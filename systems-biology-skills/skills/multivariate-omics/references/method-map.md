# Which multivariate method answers which question

| Method | Question it answers | Needs | Common misuse |
|---|---|---|---|
| PCA | Where is the variance? | Centred (and perhaps scaled) data | Treating components as biological factors |
| Exploratory factor analysis | Which latent constructs explain the correlations? | A measurement model, enough samples per variable | Running PCA and calling it factor analysis |
| Confirmatory factor analysis / SEM | Does a hypothesised latent structure fit? | A model stated in advance | Modifying the model until it fits, then reporting it as confirmed |
| Cluster analysis | Are there groups? | A distance and a linkage or a number of clusters | Reporting clusters without a stability check |
| Mixture models | Are there latent classes, with probabilities? | A distribution for each class | Choosing the number of classes by fit alone |
| MANOVA | Do group means differ on several variables jointly? | More samples than variables, similar covariances | Using it on omics tables with thousands of variables |
| Multiple regression | How does a response depend on several predictors? | More samples than predictors, low collinearity | Interpreting coefficients of correlated predictors |
| Logistic regression | Odds of a binary outcome | Events per variable large enough | Perfect separation ignored |
| PLS / PLS-DA | Directions predicting a response in collinear, wide data | Cross-validation, permutation | Unvalidated separation |
| Multilevel (hierarchical) models | Effects when samples are nested (cells in patients, repeated measures) | Group identifiers | Treating nested samples as independent |
| Meta-analysis | Combined effect across studies | Effect sizes with standard errors | Mixing incompatible designs |

The method list follows the chapter titles of Teo (Ed.) 2013; the descriptions are author knowledge, VERIFY.
