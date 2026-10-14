# Benchmark design and audit checklist

Use it to design a comparison before running it, and to audit one after. A "no" is a finding to rank, not
an automatic rejection. The items are the skill's own, written from general practice and the benchmarking
literature named in `SKILL.md`: VERIFY against the guidance your field or journal uses.

| # | Item | Question to answer |
|---|---|---|
| 1 | Purpose | What decision does the result support, and for whom? |
| 2 | Neutrality | Who ran it, and do they favour a method? Is that declared? |
| 3 | Method selection | By what rules were methods included or excluded? Are versions recorded? |
| 4 | Baselines | Is there a trivial baseline and a method known to be poor? |
| 5 | Datasets | How many, how varied, how is truth known, and who chose them and when? |
| 6 | Simulation | Does the simulator share assumptions with one of the methods? |
| 7 | Leakage | Can tuning data, training data or related items appear in the evaluation set? |
| 8 | Tuning | Did every method get equal tuning effort? Are defaults reported too? |
| 9 | Metrics | Fixed before the run? Suited to class imbalance? Secondary measures and resource use? |
| 10 | Failures | Are crashes, timeouts and empty outputs counted? |
| 11 | Test size | What is the smallest difference this test can detect (`benchstats.py min-diff`)? |
| 12 | Chance | How much would the best of this many equal methods look better by luck (`chance-gap`)? |
| 13 | Uncertainty | Paired differences with intervals across datasets, repeated seeds? |
| 14 | Controls | Does a degraded copy rank last and a duplicate tie? |
| 15 | Interpretation | Results by condition, with failure modes, not one rank? |
| 16 | Reproducibility | Code, versions, raw results and a way to add a method released? |
