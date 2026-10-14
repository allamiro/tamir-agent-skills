---
name: reproducible-research-code
description: Writes and structures research code so a bioinformatics result can be repeated and trusted, using pinned environments, recorded data versions and genome builds, seeds, a clean split between data, code and results, tests for scientific code, workflow structure, and rules for sensitive human data. Use for "make this analysis reproducible", "set up a pipeline project", "how do I test my analysis code", "what should I record about my data", "my result changed when I reran it", "organise this repository". Use bioinformatics-workflow to plan the analysis, sequence-formats to read the files, and bioinformatics-review to audit the finished work.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Reproducible research code

## Purpose and activation

Make an analysis something another person, or the same person next year, can rerun and get the
same answer from, and make a wrong answer easy to find. Activate when the user is starting a
project, turning a notebook into a pipeline, is surprised by a changed result, or is about to
share code. The source text leaves practical programming out on purpose, so this skill is
original guidance and says where it is uncertain.

## Required inputs

The language and platform; where the data live and how large they are; whether the data are
public, private or human-subject; the compute (laptop, server, cluster); who else must run it; and
what existing code and notes there are.

## Workflow

1. **Separate data, code, configuration and results** into different folders. Raw data are read-only.
2. **Record the data.** For each input: source, accession and version, date downloaded, checksum,
   licence or consent terms, and for genomic data the genome build and annotation release. Use
   `assets/templates/methods-record.md`.
3. **Pin the environment.** Record the language and every package version (a lock file or an
   environment file), and the operating system. Rebuild the environment from the file once to test it.
4. **Set seeds** for every random step and record them with the result, not only in the code.
5. **Write the steps as a script or workflow,** not as manual actions. Every step takes named
   inputs and writes named outputs, so a missing step is visible.
6. **Test the code on known answers** before real data: hand-computed cases, an independent
   implementation, properties that must hold, and synthetic data with a planted signal
   (`references/testing-scientific-code.md`).
7. **Make tests able to fail.** Break the code on purpose and confirm a test notices.
8. **Rerun end to end** from raw data in a clean checkout and compare the outputs.
9. **Write the methods record** from what was run, not from memory.

## Decision framework

| Situation | Choice |
|---|---|
| One-off exploration | A notebook is fine; move anything that matters into a script |
| A result that will be reported | A script or workflow run from raw data, with a recorded environment |
| Many samples or steps | A workflow manager with declared inputs and outputs (several exist; VERIFY which your site supports) |
| Large data | Keep the data outside the repository; commit the checksums and the download script |
| Human-subject or controlled-access data | Follow the data access agreement; keep identifiers out of code and logs; ask the data owner before sharing anything derived |
| Randomness in the method | Fixed seed for the record, and a run over several seeds to show the result is stable |
| Result differs on another machine | Compare versions first, then floating-point and thread order |

## Implementation guidance

- A script should do one thing and print what it did: versions, inputs, row counts, seed.
- Name files for their content and date, not `final2`. Record the commit that produced each result.
- Compute once and cache with a key that includes the input checksum, so stale files are detected.
- Keep unit conversion and coordinate conversion in one tested function each.
- This collection's own scripts follow the pattern: standard library only, a `--selftest` with
  hand-computed values, and an independent cross-check where one exists (an exhaustive search
  against the alignment table; recovery of known trees by neighbour-joining).

## Failure and edge cases

- **Unpinned packages:** a rerun a year later gives a different answer, silently.
- **Moving reference:** a "latest" genome or database download changes between runs.
- **Hidden manual steps:** a spreadsheet edit or a renamed file nobody recorded.
- **Seeds recorded nowhere,** or set once at the top while parallel workers use their own.
- **Tests that cannot fail,** or compare the code with itself.
- **Results committed without the code version** that made them.
- **Private data in a public repository,** including sample identifiers in file names.
- **Floating-point differences** across machines treated as errors, or real differences hidden by rounding.
- **Everything in one notebook** run out of order.

## Validation

- A clean checkout, a rebuilt environment and the raw data reproduce the outputs byte for byte
  or within a stated tolerance.
- Each test fails when the thing it tests is deliberately broken (mutate, rerun, confirm).
- The methods record lists every input with a version and a checksum.
- Falsifier: someone else cannot rerun it from the record alone.

## Expected output

A project layout, the environment file, the data record, the run script or workflow, the test list
with what each test would catch, and the methods record.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed., ch. 1.2 (supplied text): practical
  programming and database handling are left out of the book. Nothing here is from it
- The practices in this skill: general research-software practice from author knowledge, VERIFY
  against your institution's data-management policy and the tools' documentation
- The testing approach is demonstrated by the self-tests of the scripts in this collection, which
  were run on Python 3.9 and 3.14
- Not covered: containers and cluster scheduling in detail, licensing advice, ethics review
