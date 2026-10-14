# `reproducible-research-code` prompts

Structure research code so a result can be rerun and a wrong one is easy to find: recorded data,
pinned environments, seeds, tests that can fail, and care with sensitive data.

- **Give it:** the language, where the data live and how large they are, whether they are public,
  private or human-subject, the compute, and who else must run it
- **Skill file:** [`skills/reproducible-research-code/SKILL.md`](../skills/reproducible-research-code/SKILL.md)
- **Testing guide:** [`testing-scientific-code.md`](../skills/reproducible-research-code/references/testing-scientific-code.md)
- **Template it fills:** [`methods-record.md`](../skills/reproducible-research-code/assets/templates/methods-record.md)
- **Plan first with:** [`bioinformatics-workflow`](bioinformatics-workflow.md)

## 1. A project layout

> Set up a project layout for an analysis of public sequencing data in Python. Keep raw data read-only, record accessions and checksums, pin the environment, and say where seeds are recorded.

A good answer: separate folders for data, code, configuration and results, a download script
with checksums instead of committed data, an environment file, and seeds written next to each result.

## 2. A result that changed

> The numbers changed when I reran my analysis a month later and I changed nothing. Give me the order to investigate in.

A good answer: package and database versions first, then reference or annotation downloads that
moved, then seeds and parallel order, then floating-point and platform differences.

## 3. Tests for a conversion function

> Write tests for my function that converts BED coordinates to 1-based closed coordinates. Use hand-computed cases, a round trip, and an off-centre example, and say what each would catch.

A good answer: BED 0-100 to 1-100, a round trip over many intervals, a slice check on a known
sequence, an off-centre interval that would expose a mirrored mapping, and a zero-length case.

## 4. Can my tests fail

> All my tests pass. How do I know they can fail? Show me how to mutate the code on purpose and what to do when a mutation survives.

A good answer: change a sign, a comparison or a term, rerun, and confirm a test fails; a surviving
mutation means that line is not covered, so add a test for it.

## 5. Before sharing

> I want to share this repository. File names contain patient sample identifiers and the data are under an access agreement. What should I do first?

A good answer: stop and read the data access agreement, remove identifiers from names and logs,
share code and checksums but not data, and ask the data owner what derived results may be shared.

## 6. A methods record

> Write the methods record for this run from what was actually executed, not from memory: <paste the commands, versions and file list>. Mark anything I did not record.

A good answer: a filled record with inputs, versions, parameters and seeds, and a list of items
that are missing and must be reconstructed or marked unknown.
