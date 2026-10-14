# Bioinformatics Skills for OpenAI

OpenAI has more than one place that takes skills, and they do not take them the same way. What each
accepts below is as the OpenAI documentation states it (read 2026-10-14); anything the documentation
does not say is marked as unconfirmed.

| Tool | How skills get in | Status for this collection | Read |
|---|---|---|---|
| **Codex** (CLI and IDE extension) | Folders of `SKILL.md` files in `.agents/skills` | Works | [Codex](#codex) |
| **ChatGPT desktop app** | Standalone skills show in a Skills sidebar and are picked with `@` | 23 zips built; how the app takes a skill is not confirmed | [ChatGPT](#chatgpt) |
| **OpenAI Skills API** | A zip with one top-level folder | 23 zips built and checked against the documented limits | [OpenAI Skills API](#openai-skills-api) |

## Codex

Codex reads the standard `SKILL.md` folders. There is no separate OpenAI copy of the skills.

Run from the `bioinformatics-skills/` folder:

```bash
bash scripts/install.sh --codex --project /path/to/your/project   # this project only
bash scripts/install.sh --codex --user                            # every project on this machine
```

`--codex` and `--agents` do the same thing. Install all 23 skills together, because the coordinator hands work to the specialists.
`--symlink`, `--force` and `--dry-run` work as they do for Claude Code.

Codex scans `.agents/skills` in every directory from the working directory up to the repository root,
`$HOME/.agents/skills` for your user, and `/etc/codex/skills` for an administrator, and it follows
symlinked skill folders. To use a skill, describe the task and Codex picks one from the description,
or run `/skills` or type `$` and the skill name to choose one yourself. (Codex skills documentation
at learn.chatgpt.com, read 2026-10-14.)

**Tested.** On 2026-10-14, with codex-cli 0.162.1, each skill's starter prompt was run with `codex exec` once with the skills installed in `.agents/skills` and once with none ([results](../evals/results/codex.md)). Codex read the expected skill's `SKILL.md` in 23 of 23 runs, and 21 of 23 answers contained every expected fact with the skills against 21 of 23 without. That checks that Codex finds and uses the skills from that folder; with one run per prompt and no judge, it says little about answer quality.

Ready-to-paste prompts, one file per skill, are in [`../prompts/`](../prompts/README.md).

## ChatGPT

The ChatGPT documentation says standalone skills are available in the ChatGPT desktop app as well
as in Codex, that in ChatGPT you type `@` and pick the skill, and that the desktop app has a Skills
sidebar. It describes the optional `agents/openai.yaml` file as display and invocation settings for
the desktop app, and every zip here includes one. For wider distribution it recommends packaging
skills as a plugin, which this collection does not do.

What the documentation read does **not** describe is uploading a zip as a standalone skill in the
ChatGPT chat app, and it does not say where the desktop app looks for skills. So how you add these
skills to the desktop app is unconfirmed. Two things to try, neither verified here: install the skill
folders as for Codex (the documentation lists the desktop app next to Codex but does not say they
read the same folders), or use a zip upload if your ChatGPT version offers one. Follow the in-product
flow.

## OpenAI Skills API

The OpenAI skills guide (read 2026-10-14) says you can upload a directory, or a `.zip` that contains
a single top-level folder; a bundle may hold exactly one `SKILL.md`; the zip may be at most 50 MB;
there may be at most 500 files per skill version; and an uncompressed file may be at most 25 MB. The
zips in [`chatgpt/`](chatgpt/) meet all of these, one zip per skill:

Start with `bioinformatics-workflow.zip`, the coordinator, then add the specialists you need.

| Zip | Skill |
|---|---|
| [`bioinformatics-workflow.zip`](chatgpt/bioinformatics-workflow.zip) | The coordinator: plan an analysis from question to result |
| [`experimental-design.zip`](chatgpt/experimental-design.zip) | Replicates, controls, batches, sample size and power |
| [`biological-databases.zip`](chatgpt/biological-databases.zip) | Identifiers, versions, mapping, citing and depositing data |
| [`data-governance-ethics.zip`](chatgpt/data-governance-ethics.zip) | Consent, privacy and sharing of sensitive data (guidance, not legal advice) |
| [`sequence-formats.zip`](chatgpt/sequence-formats.zip) | FASTA, FASTQ, GFF3, BED and SAM, and coordinates |
| [`ngs-pipelines.zip`](chatgpt/ngs-pipelines.zip) | Reads to alignments, variants or counts; flags, CIGAR, coverage |
| [`sequence-alignment.zip`](chatgpt/sequence-alignment.zip) | Global and local alignment and a shuffle test for the score |
| [`gene-finding-translation.zip`](chatgpt/gene-finding-translation.zip) | Translation, open reading frames and their chance level |
| [`protein-analysis.zip`](chatgpt/protein-analysis.zip) | Protein mass, hydropathy, structure and function evidence |
| [`phylogenetics.zip`](chatgpt/phylogenetics.zip) | Distances, UPGMA and neighbour-joining trees |
| [`variants-population-genetics.zip`](chatgpt/variants-population-genetics.zip) | VCF, allele frequencies, Hardy-Weinberg, linkage |
| [`omics-data-analysis.zip`](chatgpt/omics-data-analysis.zip) | Design checks, batch effects, clustering and networks for omics tables |
| [`information-theory-sequences.zip`](chatgpt/information-theory-sequences.zip) | Entropy, diversity, conservation, compression distance |
| [`sequence-statistics.zip`](chatgpt/sequence-statistics.zip) | Counting, tails, expected counts, multiple testing |
| [`machine-learning-biology.zip`](chatgpt/machine-learning-biology.zip) | Leakage-safe evaluation and metrics for imbalanced data |
| [`bioinformatics-programming.zip`](chatgpt/bioinformatics-programming.zip) | Large files, packed sequences, log space, common bugs |
| [`reproducible-research-code.zip`](chatgpt/reproducible-research-code.zip) | Records, environments, seeds, tests that can fail |
| [`research-writing-reporting.zip`](chatgpt/research-writing-reporting.zip) | Methods, claim wording, figures, availability statements |
| [`bioinformatics-review.zip`](chatgpt/bioinformatics-review.zip) | Audit of an analysis or claim, with ranked findings |
| [`literature-search-appraisal.zip`](chatgpt/literature-search-appraisal.zip) | A documented search, appraising method papers, retraction checks, a citation checker |
| [`method-benchmarking.zip`](chatgpt/method-benchmarking.zip) | Designing and auditing tool comparisons, detectable differences, paired tests |
| [`research-proposal-planning.zip`](chatgpt/research-proposal-planning.zip) | Question to aims, data management plan check, schedule with critical path |
| [`bioinformatics-learning-path.zip`](chatgpt/bioinformatics-learning-path.zip) | A study plan, exercises and projects for your background |

### Rebuild the zips

Only needed after you change a skill. The zips are built deterministically.
Each skill is packaged as it is, since the skills name each other but never link into each other's folders.

```bash
python3 scripts/build_chatgpt.py            # rebuild openai/chatgpt/*.zip
python3 scripts/build_chatgpt.py --fresh    # verify limits and that the committed zips match the skills
```
