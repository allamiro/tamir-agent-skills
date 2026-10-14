# Egyptology Skills for Claude Code

Use this page if you work in Claude Code. The skills themselves live in
[`../skills/`](../skills/); there is no separate Claude copy, because Claude Code reads the
standard `SKILL.md` folders as they are.

## Install

Run from the `egyptology-skills/` folder:

```bash
bash scripts/install.sh --claude --project /path/to/your/project   # this project only
bash scripts/install.sh --claude --user                            # every project on this machine
```

This copies all five skills to `.claude/skills/` (or `~/.claude/skills/` with `--user`). Install
all five together, because they refer to each other.

| Option | Effect |
|---|---|
| `--symlink` | Link to this checkout instead of copying, so a `git pull` updates the skills |
| `--force` | Replace skills that are already installed |
| `--dry-run` | Print what would happen and change nothing |

## Use

Describe the task in plain language and Claude picks the skill. You can also name one by typing
`/gardiner-sign-lookup`, `/transliteration`, `/text-annotation`, `/hieroglyph-app-builder` or
`/accuracy-review`.

Ready-to-paste prompts, one file per skill, are in [`../prompts/`](../prompts/README.md).

## Check that it worked

```bash
ls .claude/skills        # should list the five skill folders
```

## Update or remove

- Update: pull this repo and run the install again with `--force`, or install with `--symlink`
  once and skip updating.
- Remove: delete the five folders from `.claude/skills/`.

## Not covered

Uploading these skills to the Claude web or desktop chat app has not been tested for this
collection. The Claude Code path above is the one that has been checked.
