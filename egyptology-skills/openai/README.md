# Egyptology Skills for OpenAI

OpenAI has two tools that matter here. They are not the same, and this collection supports only one
of them today.

| Tool | Status for this collection | Where to read |
|---|---|---|
| **Codex** (CLI and IDE) | Works. Install the skills from [`../skills/`](../skills/) | [Codex](#codex) |
| **ChatGPT** | **Not built yet.** No zips exist for this collection | [ChatGPT](#chatgpt) |

## Codex

Codex reads the standard `SKILL.md` folders from `.agents/skills`. There is no separate OpenAI copy.

Run from the `egyptology-skills/` folder:

```bash
bash scripts/install.sh --codex --project /path/to/your/project   # this project only
bash scripts/install.sh --codex --user                            # every project on this machine
```

`--codex` and `--agents` do the same thing. Install all five skills together, because they refer to
each other. `--symlink`, `--force` and `--dry-run` work as they do for Claude Code.

Codex looks for skills in `.agents/skills` in the repo and in each parent folder up to the repo
root, in `~/.agents/skills`, and in `/etc/codex/skills` (OpenAI Codex documentation, read
2026-10-14). Tool versions change, so confirm in your tool's docs.

Ready-to-paste prompts, one file per skill, are in [`../prompts/`](../prompts/README.md).

## ChatGPT

ChatGPT takes a zip with one top-level folder and exactly one `SKILL.md`. This collection has no
such zips, and no script to build them. Until that exists you have two options:

- Use Codex, as above.
- Use Claude Code: see [`../claude/`](../claude/README.md).

The System Design collection already ships a ChatGPT bundle for each of its skills, in
[`../../system-design-skills/openai/chatgpt/`](../../system-design-skills/openai/chatgpt/). That is
a different collection and does not contain Egyptology.
