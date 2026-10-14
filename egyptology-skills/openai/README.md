# Egyptology Skills for OpenAI

OpenAI has more than one place that takes skills, and they do not take them the same way. What each
accepts below is as the OpenAI documentation states it (read 2026-10-14); anything the documentation
does not say is marked as unconfirmed.

| Tool | How skills get in | Status for this collection | Read |
|---|---|---|---|
| **Codex** (CLI and IDE extension) | Folders of `SKILL.md` files in `.agents/skills` | Works | [Codex](#codex) |
| **ChatGPT desktop app** | Standalone skills show in a Skills sidebar and are picked with `@` | 5 zips built; how the app takes a skill is not confirmed | [ChatGPT](#chatgpt) |
| **OpenAI Skills API** | A zip with one top-level folder | 5 zips built and checked against the documented limits | [OpenAI Skills API](#openai-skills-api) |

## Codex

Codex reads the standard `SKILL.md` folders. There is no separate OpenAI copy of the skills.

Run from the `egyptology-skills/` folder:

```bash
bash scripts/install.sh --codex --project /path/to/your/project   # this project only
bash scripts/install.sh --codex --user                            # every project on this machine
```

`--codex` and `--agents` do the same thing. Install all 5 skills together, because they refer to each other.
`--symlink`, `--force` and `--dry-run` work as they do for Claude Code.

Codex scans `.agents/skills` in every directory from the working directory up to the repository root,
`$HOME/.agents/skills` for your user, and `/etc/codex/skills` for an administrator, and it follows
symlinked skill folders. To use a skill, describe the task and Codex picks one from the description,
or run `/skills` or type `$` and the skill name to choose one yourself. (Codex skills documentation
at learn.chatgpt.com, read 2026-10-14.)

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

Upload the skills you need; they refer to each other by name, so take all five if you can.

| Zip | Skill |
|---|---|
| [`gardiner-sign-lookup.zip`](chatgpt/gardiner-sign-lookup.zip) | Look up a sign by Gardiner code, character, MdC string or sound |
| [`transliteration.zip`](chatgpt/transliteration.zip) | Read a sign sequence, with every ambiguity flagged |
| [`text-annotation.zip`](chatgpt/text-annotation.zip) | Lay a text out line by line with glosses and a grade per word |
| [`hieroglyph-app-builder.zip`](chatgpt/hieroglyph-app-builder.zip) | Data model, rendering, search and exchange for a hieroglyph tool |
| [`accuracy-review.zip`](chatgpt/accuracy-review.zip) | Audit a reading or sign table for confident errors |

### Rebuild the zips

Only needed after you change a skill. The zips are built deterministically.
Each skill is packaged as it is, since the skills name each other but never link into each other's folders.

```bash
python3 scripts/build_chatgpt.py            # rebuild openai/chatgpt/*.zip
python3 scripts/build_chatgpt.py --fresh    # verify limits and that the committed zips match the skills
```
