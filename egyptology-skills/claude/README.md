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

This copies all 8 skills to `.claude/skills/` (or `~/.claude/skills/` with `--user`), the two
locations the Claude Code documentation gives for project and personal skills. Install all of them
together, because they refer to each other.

| Option | Effect |
|---|---|
| `--symlink` | Link to this checkout instead of copying, so a `git pull` updates the skills |
| `--force` | Replace skills that are already installed |
| `--dry-run` | Print what would happen and change nothing |

## Use

The Claude Code documentation (skills page, read 2026-10-14) says Claude uses a skill when it is
relevant, or you can invoke one directly with `/skill-name`, and that the skill's `description` is
what Claude uses to decide when to load it. So you can describe the task in plain words, or type `/gardiner-sign-lookup`, `/transliteration`, `/text-annotation`, `/hieroglyph-app-builder`, `/accuracy-review`, `/egyptology-literature`, `/edition-conventions` or `/provenance-research-ethics`.

The skills call their bundled scripts by a path relative to the skill folder, for example
`python3 scripts/signs.py`. If Claude cannot find a script, tell it the folder the skill was installed
in. The documentation also describes a `${CLAUDE_SKILL_DIR}` variable that resolves to the skill's folder
wherever it is installed, which you can use in your own skills.

Ready-to-paste prompts, one file per skill, are in [`../prompts/`](../prompts/README.md).

## Check that it worked

```bash
ls .claude/skills                      # should list 8 skill folders
claude plugin validate .claude/skills  # Claude Code's own check of the skill files (v2.1.233 or later, per the docs)
```

The same check run on this collection's `skills/` folder passed with Claude Code 2.1.296. One caution:
in a test, that check accepted a description containing a colon followed by a space, which strict YAML
parsers reject. The stricter `skills-ref validate skills/<name>` does reject it, so these skills are
written to pass both.

## Update or remove

- Update: pull this repo and run the install again with `--force`, or install with `--symlink`
  once and skip updating.
- Remove: delete the 8 folders from `.claude/skills/`.

## Not covered

Uploading these skills to the Claude web or desktop chat app has not been tested for this
collection. The Claude Code path above is the one that has been checked.
