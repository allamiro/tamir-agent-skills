# Systems Biology Skills for OpenAI

OpenAI has more than one place that takes skills, and they do not take them the same way. What each
accepts below is as the OpenAI documentation states it (read 2026-10-14); anything the documentation
does not say is marked as unconfirmed.

| Tool | How skills get in | Status for this collection | Read |
|---|---|---|---|
| **Codex** (CLI and IDE extension) | Folders of `SKILL.md` files in `.agents/skills` | Works | [Codex](#codex) |
| **ChatGPT desktop app** | Standalone skills show in a Skills sidebar and are picked with `@` | 21 zips built; how the app takes a skill is not confirmed | [ChatGPT](#chatgpt) |
| **OpenAI Skills API** | A zip with one top-level folder | 21 zips built and checked against the documented limits | [OpenAI Skills API](#openai-skills-api) |

## Codex

Codex reads the standard `SKILL.md` folders. There is no separate OpenAI copy of the skills.

Run from the `systems-biology-skills/` folder:

```bash
bash scripts/install.sh --codex --project /path/to/your/project   # this project only
bash scripts/install.sh --codex --user                            # every project on this machine
```

`--codex` and `--agents` do the same thing. Install all 21 skills together, because the coordinator hands work to the specialists.
`--symlink`, `--force` and `--dry-run` work as they do for Claude Code.

Codex scans `.agents/skills` in every directory from the working directory up to the repository root,
`$HOME/.agents/skills` for your user, and `/etc/codex/skills` for an administrator, and it follows
symlinked skill folders. To use a skill, describe the task and Codex picks one from the description,
or run `/skills` or type `$` and the skill name to choose one yourself. (Codex skills documentation
at learn.chatgpt.com, read 2026-10-14.)

**Not yet tested with Codex for this collection.** The other collections in this repository were checked with `codex exec` (each skill's starter prompt with and without the skills installed); the same command, `python3 ../tools/run_evals.py codex .`, has not been run here.

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

Start with `systems-biology-workflow.zip`, the coordinator, then add the specialists you need.

| Zip | Skill |
|---|---|
| [`systems-biology-workflow.zip`](chatgpt/systems-biology-workflow.zip) | The coordinator: question to formalism to plan |
| [`model-building-design.zip`](chatgpt/model-building-design.zip) | Assumptions, variables and parameters, model classification, well-posedness |
| [`quantities-units-balances.zip`](chatgpt/quantities-units-balances.zip) | Units, dimensions, balances and chemostat steady states |
| [`linear-algebra-networks.zip`](chatgpt/linear-algebra-networks.zip) | Matrix form, rank, Rouché–Capelli, determinants, eigenvalues |
| [`network-analysis.zip`](chatgpt/network-analysis.zip) | Graph matrices, centrality, motifs, network medicine, provenance |
| [`stoichiometric-networks.zip`](chatgpt/stoichiometric-networks.zip) | Stoichiometric matrix, null spaces, conservation, elementary modes, MFA |
| [`flux-balance-analysis.zip`](chatgpt/flux-balance-analysis.zip) | FBA, flux variability, knockouts, genome-scale checks |
| [`ode-dynamics.zip`](chatgpt/ode-dynamics.zip) | Simulation, steady states, stability, phase portraits, sensitivity |
| [`control-systems-feedback.zip`](chatgpt/control-systems-feedback.zip) | State space, transfer functions, controllability, observability, feedback |
| [`enzyme-kinetics.zip`](chatgpt/enzyme-kinetics.zip) | Rate laws, inhibition, cooperativity, nonlinear fitting |
| [`pharmacokinetic-modeling.zip`](chatgpt/pharmacokinetic-modeling.zip) | One-compartment PK, AUC, accumulation, Emax, links to QSP |
| [`parameter-estimation-model-selection.zip`](chatgpt/parameter-estimation-model-selection.zip) | Fitting, identifiability, AICc and Akaike weights, F-tests |
| [`stochastic-discrete-models.zip`](chatgpt/stochastic-discrete-models.zip) | Gillespie simulation, Boolean attractors, difference equations |
| [`multivariate-omics.zip`](chatgpt/multivariate-omics.zip) | PCA, PLS regression, VIP, validation of supervised models |
| [`quantitative-research-methods.zip`](chatgpt/quantitative-research-methods.zip) | Construct maps, reliability, validity, Rasch, effect sizes, method choice |
| [`systems-biology-programming.zip`](chatgpt/systems-biology-programming.zip) | SBML, SED-ML, annotation, element balance, model tests, reproducibility |
| [`systems-biology-literature.zip`](chatgpt/systems-biology-literature.zip) | Searching papers, models and parameters; checking references |
| [`modeling-paper-writing.zip`](chatgpt/modeling-paper-writing.zip) | Writing, submitting and revising a modelling paper |
| [`modeling-research-planning.zip`](chatgpt/modeling-research-planning.zip) | Aims, model–experiment cycle, measurement and design, plan check |
| [`model-review.zip`](chatgpt/model-review.zip) | Layer-by-layer audit of a model or modelling paper |
| [`systems-biology-learning-path.zip`](chatgpt/systems-biology-learning-path.zip) | Study plan, checklist, worked exercises, flipped classroom |

### Rebuild the zips

Only needed after you change a skill. The zips are built deterministically.
Each skill is packaged as it is, since the skills name each other but never link into each other's folders.

```bash
python3 scripts/build_chatgpt.py            # rebuild openai/chatgpt/*.zip
python3 scripts/build_chatgpt.py --fresh    # verify limits and that the committed zips match the skills
```
