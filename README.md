<p align="center">
  <img src="assets/banner.svg" alt="Agent Skills: reusable expert workflows for Claude Code, Codex and ChatGPT" width="100%">
</p>

<p align="center">
  <img alt="License Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-096efb?style=flat-square&labelColor=15123d">
  <img alt="17 skills" src="https://img.shields.io/badge/skills-17-6c64eb?style=flat-square&labelColor=15123d">
  <img alt="Agent Skills spec valid" src="https://img.shields.io/badge/Agent%20Skills%20spec-valid-9cc464?style=flat-square&labelColor=15123d">
  <img alt="Works with Claude Code, Codex and ChatGPT" src="https://img.shields.io/badge/works%20with-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20ChatGPT-fb6373?style=flat-square&labelColor=15123d">
</p>

Step-by-step expert workflows your coding agent can follow, packaged as
[Agent Skills](https://agentskills.io/specification). Write them once, use them in Claude Code,
Codex and ChatGPT.

## Collections

| Collection | What it covers | Skills |
|---|---|---|
| [**System Design Skills**](system-design-skills/) | Design, scale, secure, operate and review software systems: capacity, databases, consistency, caching, messaging, storage, reliability, observability, payments, geospatial, architecture review | 17 |

More collections can sit beside it. Each one is a self-contained folder.

## Install

### Claude Code

```bash
git clone https://github.com/allamiro/tamir-claude-skills.git
cd tamir-claude-skills/system-design-skills
bash scripts/install.sh --claude --project /path/to/your/project
```

### Codex

Codex reads `.agents/skills`.

```bash
bash scripts/install.sh --agents --project /path/to/your/project
```

### ChatGPT

Upload a ready-made zip from
[`system-design-skills/chatgpt/`](system-design-skills/chatgpt/) and pick it with `@`. Start with
`system-design.zip`.

Then ask in plain language:

> Design the backend for a marketplace with flash sales and card payments.
>
> Review this architecture and give me findings with evidence and severity.

## What you get

- **Workflows.** Each skill says when to use it, what it needs, the steps, how to choose between
  options, what can fail, and what to hand back.
- **Honest sources.** Every skill ends with a sources block that separates what was verified,
  what was fetched from official docs (dated), and what still needs checking.
- **Checked.** Validators cover the spec, structure, size, links, templates, scripts and
  description routing. The collection README lists what has and has not been run.

## Contribute

New skills, new collections and fixes are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[Apache-2.0](LICENSE)
