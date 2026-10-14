# Review dimensions for a model

| # | Dimension | Questions | Typical evidence |
|---|---|---|---|
| 1 | Question and formalism | Is the question stated as an observable? Is the formalism the lightest that answers it? | Introduction, methods |
| 2 | Assumptions | Listed? Justified for this purpose? Which would reverse the conclusion? | Assumption list |
| 3 | Units, balances, conservation | Every term dimensionally consistent? Reactions balanced? Conserved totals constant? | Equations, model file |
| 4 | Parameters | Each with value, unit, source, status? Organism and conditions? | Parameter table |
| 5 | Numerics | Solver suitable (stiff or not)? Results stable when tolerances tighten? | Methods, supplement |
| 6 | Fitting and identifiability | Error model stated? Many starts? Profiles or other identifiability analysis? | Fitting section |
| 7 | Validation | Data not used for fitting? Prediction stated before the test? | Results |
| 8 | Sensitivity and robustness | Which parameters drive the conclusions? Local or global? | Sensitivity analysis |
| 9 | Alternatives | Competing structures compared (AICc, discriminating experiment)? | Model comparison |
| 10 | Data and measurement | Do the readouts measure the intended property? Reliability, validity evidence, missing data handled? | Data description |
| 11 | Reproducibility | SBML or CellML, SED-ML, code, versions, identifiers; does it run? | Availability statement |
| 12 | Claims and interpretation | Wording matches evidence level? Consequences of being wrong stated? | Abstract, discussion |

Dimension 10 and the interpretation part of 12 follow the measurement and interpretation lessons
paraphrased from Teo (Ed.) 2013 (`quantitative-research-methods`). The rest is author knowledge, VERIFY.
