<p align="center">
  <img src="assets/banner.svg" alt="Agent Skills: reusable expert workflows for Claude Code, Codex and ChatGPT" width="100%">
</p>

<p align="center">
  <img alt="License Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-096efb?style=flat-square&labelColor=15123d">
  <img alt="51 skills" src="https://img.shields.io/badge/skills-51-6c64eb?style=flat-square&labelColor=15123d">
  <img alt="Agent Skills spec valid" src="https://img.shields.io/badge/Agent%20Skills%20spec-valid-9cc464?style=flat-square&labelColor=15123d">
  <img alt="Works with Claude Code, Codex and ChatGPT" src="https://img.shields.io/badge/works%20with-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20ChatGPT-fb6373?style=flat-square&labelColor=15123d">
</p>

Step-by-step expert workflows your coding agent can follow, packaged as
[Agent Skills](https://agentskills.io/specification). Write them once, use them in Claude Code
and Codex, and as zips for ChatGPT and the OpenAI Skills API.

## Collections

| Collection | What it covers | Skills |
|---|---|---|
| [**System Design Skills**](system-design-skills/) | Design, scale, secure, operate and review software systems: capacity, databases, consistency, caching, messaging, storage, reliability, observability, payments, geospatial, architecture review, plus reading papers, benchmarking and writing research | 20 |
| [**Egyptology Skills**](egyptology-skills/) | Read and check Middle Egyptian hieroglyphic text: sign lookup by Gardiner code, transliteration, annotated layouts, tool building, accuracy review, plus literature and citations, editorial conventions, and provenance and ethics. Output is a draft for specialists | 8 |
| [**Bioinformatics Skills**](bioinformatics-skills/) | The whole of a bioinformatics project: study design, data and identifiers, privacy and ethics, file formats, sequencing pipelines, alignment, genes, proteins, trees, variants, omics, statistics, machine learning, programming, reproducibility, writing up, review, and learning the field, plus literature search, benchmarking methods and research planning. Output is a draft for review | 23 |

More collections can sit beside it. Each one is a self-contained folder.

## Which one is for my tool?

| I use | System Design Skills | Egyptology Skills | Bioinformatics Skills |
|---|---|---|---|
| **Claude Code** | [guide](system-design-skills/claude/README.md) | [guide](egyptology-skills/claude/README.md) | [guide](bioinformatics-skills/claude/README.md) |
| **OpenAI Codex** | [guide](system-design-skills/openai/README.md#codex) | [guide](egyptology-skills/openai/README.md#codex) | [guide](bioinformatics-skills/openai/README.md#codex) |
| **ChatGPT and OpenAI Skills API** | [20 zips](system-design-skills/openai/chatgpt/) | [8 zips](egyptology-skills/openai/chatgpt/) | [23 zips](bioinformatics-skills/openai/chatgpt/) |

Claude Code and Codex read the same `skills/` folder in each collection. The zips for ChatGPT and the
API are built from it and live in their own folder. Each collection has the same layout: `skills/`, `claude/`,
`openai/` and `prompts/`.

## Install

Clone once, then run the installer from the collection you want.

```bash
git clone https://github.com/allamiro/tamir-agent-skills.git
cd tamir-agent-skills/system-design-skills        # or egyptology-skills, or bioinformatics-skills
bash scripts/install.sh --claude --project /path/to/your/project   # Claude Code
bash scripts/install.sh --codex --project /path/to/your/project    # OpenAI Codex
```

For ChatGPT and the OpenAI Skills API, each collection has a folder of ready-made zips, one per
skill, in its `openai/chatgpt/`. The OpenAI documentation describes picking a skill with `@` in ChatGPT
and uploading a zip to the Skills API; it does not describe a zip upload in the ChatGPT chat app, so
read the collection's `openai/` guide for what is and is not confirmed.

Then ask in plain language:

> Design the backend for a marketplace with flash sales and card payments.
>
> Review this architecture and give me findings with evidence and severity.

Every skill has ready-to-paste prompts:
[System Design](system-design-skills/prompts/README.md),
[Egyptology](egyptology-skills/prompts/README.md) and
[Bioinformatics](bioinformatics-skills/prompts/README.md), where each skill has its own file.

## What you get

- **Workflows.** Each skill says when to use it, what it needs, the steps, how to choose between
  options, what can fail, and what to hand back.
- **Honest sources.** Every skill ends with a sources block that separates what was verified,
  what was fetched from official docs (dated), and what still needs checking.
- **Checked.** Validators cover the spec, structure, size, links, templates, scripts and
  description routing. Live runs measure whether an agent picks each skill up and whether the answer
  improves, with repeats and a no-skill comparison, and a blind kit lets people grade the answers.
  [TESTING.md](TESTING.md) lists every measure, what it can and cannot tell you, and the latest results.
- **Sample outputs.** Each collection's README shows real answers and token counts with and without the skills.

## Contribute

New skills, new collections and fixes are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[Apache-2.0](LICENSE)
