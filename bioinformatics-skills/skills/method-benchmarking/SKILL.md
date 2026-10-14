---
name: method-benchmarking
description: Designs and judges comparisons of computational methods in biology, covering the question and scope, choosing methods and datasets, ground truth from simulation or real data, neutrality, fair tuning, metrics for imbalanced problems, uncertainty across datasets, rankings, leakage, runtime and failures, and reporting so others can rerun it. Use for "benchmark these tools", "is this tool comparison fair", "which aligner is best", "design a benchmark", "is method A really better than B", "how many test items do I need", "is a 2 percent gain real", "review the comparison in this paper". Use machine-learning-biology for model-level splits and metrics, experimental-design for wet-lab design, literature-search-appraisal to find existing benchmarks, and bioinformatics-review to audit an analysis.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Method benchmarking

## Purpose and activation

Choosing a tool, or claiming a new one is better, rests on a comparison. Comparisons go wrong in
predictable ways: the authors tune their own method hardest, the data resemble the method's model, a
small gain on a small test set is read as a win, and failed runs are quietly dropped. This skill designs a
comparison that can fail, or audits one. Activate when two or more methods are being compared, when a paper
claims superiority, or when someone asks which tool to use. It does not run the tools.

## Required inputs

The decision the comparison serves; the methods and their versions; the task and the output to compare;
the datasets, with how truth is known; the metric candidates; the compute budget; who is running it (a
neutral party or the method's authors); and, for an audit, the paper or report.

## Workflow

1. **State the purpose and audience.** A neutral comparison, a new-method paper and a community challenge
   need different safeguards. Write the decision the result will support.
2. **Choose the methods by stated rules** (available, documented, runs on the stated system), and include a
   simple baseline and a method known to be poor. Record versions; justify every exclusion.
3. **Choose the datasets,** each with how truth is known. Simulated data give known truth but favour whichever
   method shares the simulator's assumptions; real data with trusted truth are scarce; controls such as spike-ins
   or mock communities help. Use a range of conditions, not only the easy ones.
4. **Prevent leakage.** Tuning data must be separate from evaluation data, and related items (homologous
   sequences, relatives, repeated measures) must stay on one side of the split (`machine-learning-biology`).
5. **Tune every method with equal effort** on the tuning data, record all parameters and seeds, and report
   defaults and tuned results separately.
6. **Fix the primary metric before running.** For rare positives, precision-recall measures are more
   informative than ROC curves alone. Add secondary metrics, runtime, memory, and the count of failed or
   timed-out runs, which count as failures, not as missing values.
7. **Size the test.** How large a difference can this test set detect?
   `python3 scripts/benchstats.py min-diff --n 200 --acc 0.8`.
8. **Show what chance alone does.** If ten equally good methods are scored on the same size of test, the best
   looks better than the truth: `python3 scripts/benchstats.py chance-gap --n 200 --k 10 --acc 0.8`.
9. **Compare with uncertainty.** Across datasets use paired differences, an interval over datasets and an exact
   sign test: `python3 scripts/benchstats.py compare RESULTS.csv --a METHOD_A --b METHOD_B`. Rank methods with
   `benchstats.py ranks`. For two classifiers on the same items use `benchstats.py mcnemar`.
10. **Add controls:** a degraded copy of a method (output shuffled) must rank last, and a duplicate of a method
    must tie with the original. If not, the harness is broken.
11. **Interpret by condition,** not by one overall rank, and say where each method fails.
12. **Release** code, workflow, versions, raw results and a way to add a method
    (`assets/templates/benchmark-plan.md`).

## Decision framework

| Situation | Safeguards |
|---|---|
| Neutral comparison by people with no stake | Pre-registered methods, datasets and metric; equal tuning |
| New-method paper | Run the others at their best settings, ideally with their authors' advice; report defaults too; avoid datasets the method was tuned on |
| Community challenge | Hidden truth, a fixed metric, a held-out final set |
| Choosing a tool for your own data | A small benchmark on a sample of your own data, with truth you trust |

| Evidence | Reading |
|---|---|
| Gain smaller than the minimum detectable difference | Not supported, whatever the point estimate |
| Interval over datasets includes zero | No reliable advantage across these datasets |
| Few datasets | A wide interval whatever the items per dataset; the sign test cannot reach small p below a count |
| Best of many methods, small test set | Expect an inflated win (winner's curse) |

## Implementation guidance

- The design and audit checklist is in `references/checklist.md`.
- Keep a long-format table `dataset,method,score` and rerun the statistics from it, never from a figure.
- Treat each dataset as one unit when comparing across datasets; thousands of items in one dataset are not independent datasets.
- Record failures as rows with a score of zero or a flag, and report them.
- Use the same compute limits for all methods or report resource use beside accuracy.
- Report the metric's definition and any threshold, because thresholds are tuned too.
- The calculations in `scripts/benchstats.py` use normal approximations for proportions and exact tests for counts;
  they do not cover AUROC variance or correlated test items.

## Failure and edge cases

- **The self-assessment trap:** the people who built a method tune it hardest and pick the data.
- **Simulation that mirrors one method's model.**
- **Test data reused for tuning,** directly or by repeated looks.
- **Datasets chosen after seeing results.**
- **Failures dropped,** so a fragile method looks accurate.
- **A metric that suits one method,** or a threshold tuned on the test set.
- **A tiny gain on a small test set** announced as an improvement.
- **Ranking by the average of unlike datasets,** hiding a method that fails badly on one.
- **Different versions or compute budgets** between methods.
- **Leakage through homology or relatedness.**
- **Truth that is itself an output of one of the methods.**

## Validation

- `python3 scripts/benchstats.py --selftest` passes.
- The degraded-copy control ranks last and the duplicate ties with its original.
- The claimed difference is larger than the minimum detectable difference for the test size, and the interval
  across datasets excludes zero.
- Rerunning from the stored table reproduces every reported number.
- Falsifier: a method that wins on the published datasets and loses on a new one with the same properties.

## Expected output

A benchmark plan or an audit: purpose, methods and versions, datasets and how truth is known, tuning rules,
metrics decided in advance, the detectable difference, results as differences with intervals, ranks, failures
and resource use, the control checks, limits, and how to rerun it.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: nothing in the supplied text covers benchmarking
  practice; this skill extends the collection to research work
- Guidance: Weber et al., *Essential guidelines for computational method benchmarking* (Genome Biology 2019);
  Mangul et al., *Systematic benchmarking of omics computational tools* (Nature Communications 2019); Boulesteix
  et al., *A plea for neutral comparison studies* (PLoS ONE 2013) and *Ten simple rules for reducing overoptimistic
  reporting* (PLoS Comput Biol 2015); Norel et al., the self-assessment trap (Mol Syst Biol 2011); Saito and
  Rehmsmeier on precision-recall plots (PLoS ONE 2015); Whalen et al. on machine learning pitfalls in genomics
  (Nat Rev Genet 2021). Records checked on Crossref 2026-10-14; the papers were not read, so the workflow is own
  design informed by their titles and general practice: VERIFY against them
- Statistics: sign test, McNemar and rank code cross-checked 2026-10-14 against SciPy on 901 random cases
- Not covered: AUROC confidence intervals, bootstrapping within datasets, or choosing the biological truth
