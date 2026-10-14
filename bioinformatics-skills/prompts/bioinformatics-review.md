# `bioinformatics-review` prompts

Audit a finished analysis, pipeline or claim for errors that look fine, and get back findings
ranked by how much they could mislead.

- **Give it:** the claim, the methods or code, the data description, the figures behind the claim,
  and what the result will be used for
- **Skill file:** [`skills/bioinformatics-review/SKILL.md`](../skills/bioinformatics-review/SKILL.md)
- **Checklist it follows:** [`checklist.md`](../skills/bioinformatics-review/references/checklist.md)
- **Template it fills:** [`review-report.md`](../skills/bioinformatics-review/assets/templates/review-report.md)
- **Plan first with:** [`bioinformatics-workflow`](bioinformatics-workflow.md) · **Fix with:** [`reproducible-research-code`](reproducible-research-code.md)

## 1. Review an analysis

> Review this analysis for errors that look fine: <paste methods and results>. State the claim in a falsifiable form, trace each number to a script and input, and give me findings ranked critical, major, minor or note, each with evidence, impact and a fix. Say what you could not check.

A good answer: counts of claims checked and traced, ranked findings with the file or cell behind
each, and a plain list of what was not checked.

## 2. Thousands of tests

> My paper says 300 genes are significant out of 15,000 tests. What do you need from me to check that claim, and what are you looking for?

A good answer: the test used, the correction applied across all 15,000, the raw and adjusted
values, the effect sizes, and a shuffled-label rerun to see how many "hits" appear by chance.

## 3. Leakage

> I trained a classifier and report 98% accuracy on a held-out set. Check whether training and test data overlap: <describe how the split was made>.

A good answer: questions about duplicate or near-duplicate sequences, related samples, features
chosen on all the data, and settings tuned on the test set, with a fix such as splitting by family or by subject.

## 4. Genome build and coordinates

> Is the genome build consistent between my BED file and my annotation? Tell me how you would check, and what error a mismatch or a 0-based versus 1-based mix would cause.

A good answer: compare the build names and chromosome lengths, test a few known features, and
expect features shifted by one base for a convention mix and wrong locations for a build mix.

## 5. Test the reviewer

> I planted three errors in this analysis and I am not telling you where. Review it as you would any other, and report every finding with evidence. <paste>

A good answer: all three planted errors appear among the findings, each with the evidence. If one
is missed, do not trust the "no findings" elsewhere. Plant the errors yourself.

## 6. Is it safe to submit

> Is this safe to submit? Give me an overall statement, the corrections it needs, and the claims that need a specialist before anyone relies on them. <paste>

A good answer: a verdict in the report's terms, such as usable for hypothesis generation with the
listed corrections or not ready to publish, with the reason in one sentence.
