# Agent Skills

Reusable, validated [Agent Skills](https://agentskills.io/specification) that turn
expert engineering knowledge into step-by-step workflows an AI coding agent can follow.
Built to work in **Claude Code**, **Codex** and **ChatGPT** from a single source, and
organized as independent collections so the repository can grow beyond one domain.

## Collections

| Collection | Skills | Focus | Status |
|---|---|---|---|
| [`system-design-skills`](system-design-skills/) | 17 | Designing, scaling, securing, operating and reviewing software systems: capacity estimation, databases, consistency, caching, messaging, storage, reliability, observability, payments, geospatial, architecture review | Available |

Each collection is a self-contained folder with its own `skills/`, README and tooling.
Add a new domain by adding a new `<domain>-skills/` folder (see
[CONTRIBUTING.md](CONTRIBUTING.md)).

## What a skill is

A skill is a folder with a `SKILL.md` (a short YAML header plus instructions) and optional
`references/`, `assets/` and `scripts/`. Agents load only each skill's name and description at
startup and read the full instructions when a request matches. Supporting files load on
demand, so a large body of guidance costs almost nothing until it is needed.

These skills are written as **workflows, not summaries**: each one states when to activate
(and when a sibling skill is the better choice), what inputs it needs, numbered steps, a
decision framework with trade-offs, failure modes, how to validate the result, and the exact
deliverable to produce.

## Quick start

Install into a project (all skills of a collection together):

```bash
git clone https://github.com/allamiro/tamir-claude-skills.git
cd tamir-claude-skills/system-design-skills

# Claude Code
bash scripts/install.sh --claude --project /path/to/your/project

# Codex (and other agents that read .agents/skills)
bash scripts/install.sh --agents --project /path/to/your/project
```

Then ask for outcomes in plain language, for example *"Design the backend for a marketplace
with flash sales and card payments"* or *"Review this architecture and give me findings with
evidence and severity"*. For ChatGPT, upload the ready-made bundles from
[`system-design-skills/chatgpt/`](system-design-skills/chatgpt/); see the collection README
for details and what has and has not been verified.

| Tool | How skills are found | Notes |
|---|---|---|
| Claude Code | `.claude/skills/` in a project or `~/.claude/skills/` | Installed by `--claude` |
| Codex | `.agents/skills/` in the repo or any parent up to the repo root, `~/.agents/skills/`, `/etc/codex/skills/` | Per OpenAI's Codex skills documentation; installed by `--agents` |
| ChatGPT | Upload a zip: one top-level folder with exactly one `SKILL.md` (limits: 50 MB zip, 500 files, 25 MB per file); select a skill with `@` | Bundle rules from OpenAI's developer docs; the in-app upload menu varies by plan and admin settings |

## Quality bar

- **Evidence over assertion.** Every skill ends with a *Sources and confidence* block that
  says what is verified against supplied text, what was fetched from vendor or standards
  documentation (with the date), what comes from author knowledge and needs verification, and
  what needs validation against your own workload.
- **No invented facts.** No made-up benchmarks, citations or vendor limits; illustrative
  numbers are labelled as such and every formula carries units.
- **Simplest thing first.** Skills must justify added infrastructure with a requirement or a
  measured number rather than defaulting to fashionable components.
- **Machine-checked.** Each collection ships validators for the specification, structure,
  size limits, links, templates, bundled scripts and description routing. See the collection
  README for the commands and for exactly what has been run.

## Repository layout

```text
.
├── README.md
├── CONTRIBUTING.md
├── LICENSE                     Apache-2.0
└── system-design-skills/       one collection
    ├── skills/                 the Agent Skills (source of truth)
    ├── chatgpt/                generated, upload-ready ChatGPT bundles
    ├── scripts/                install, package, validate, build tooling
    ├── evals/                  scenarios, negative tests, routing cases
    └── docs/                   authoring guide
```

## Contributing

Contributions are welcome: new skills, new collections, corrections, and verification of
claims marked `VERIFY`. Read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

[Apache-2.0](LICENSE).
