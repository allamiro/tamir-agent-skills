# Appraisal checklist for a method or tool paper

Answer each item with what the paper shows, not what it implies. A "no" is a finding, not a verdict.

| Area | Question |
|---|---|
| Question | What exactly did the authors test, and is it the question you have? |
| Independence | Who ran the comparison? Were the other methods run by people who know them? |
| Data | What ground truth was used (simulation, curated truth, spike-in, orthogonal measurement)? Does it resemble yours? |
| Fairness | Were all methods tuned with equal effort, run at stated versions, on the same data? |
| Leakage | Could training and test data overlap through homology, relatedness or shared samples? |
| Metrics | Were they chosen before the results? Do they suit class imbalance? Are failures counted? |
| Uncertainty | Are there intervals, repeats or only point values? How many datasets? |
| Claims | Do the conclusions follow from the results, or go beyond them? |
| Availability | Are code, data and parameters available, with a licence? Is the tool maintained? |
| Status | Peer reviewed or preprint? Any correction, comment or retraction? |
| Reporting | Does it follow the relevant guideline (PRISMA for reviews, DOME for supervised machine learning)? |
| Interests | Are there competing interests, for example the authors selling the tool? |

If several items fail, treat the paper as a lead and look for independent evidence (`method-benchmarking`).
