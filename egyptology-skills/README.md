<p align="center">
  <img src="assets/banner.svg" alt="Egyptology Skills: read, annotate and check hieroglyphic text, with the doubt shown" width="100%">
</p>

<p align="center">
  <img alt="5 skills" src="https://img.shields.io/badge/skills-5-6c64eb?style=flat-square&labelColor=3a2410">
  <img alt="86 checked signs" src="https://img.shields.io/badge/checked%20signs-86-096efb?style=flat-square&labelColor=3a2410">
  <img alt="skills-ref valid" src="https://img.shields.io/badge/skills--ref-valid-9cc464?style=flat-square&labelColor=3a2410">
  <img alt="License Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-fb6373?style=flat-square&labelColor=3a2410">
</p>

Five skills that help a coding agent work with Middle Egyptian hieroglyphs: look up signs,
transliterate, lay out annotated texts, build tools, and audit the result. They are made for
researchers, students and digital-humanities teams. Every output is a draft for someone who
reads the language; the skills show where the doubt is instead of hiding it.

## Which one is for my tool?

| I use | Read | Install | Status |
|---|---|---|---|
| **Claude Code** | [`claude/`](claude/README.md) | `bash scripts/install.sh --claude --project DIR` | Works |
| **OpenAI Codex** | [`openai/`](openai/README.md#codex) | `bash scripts/install.sh --codex --project DIR` | Works |
| **ChatGPT desktop app** | [`openai/`](openai/README.md#chatgpt) | [5 zips](openai/chatgpt/) | Zips built; how the app takes them is not confirmed |
| **OpenAI Skills API** | [`openai/`](openai/README.md#openai-skills-api) | [5 zips](openai/chatgpt/) | Zips built to the documented format and limits |

Claude Code and Codex read the same files from [`skills/`](skills/). Nothing is copied per
platform, so there is one place to fix a skill.

## What is in this folder

```text
egyptology-skills/
├── skills/     the 5 skills (SKILL.md plus references, scripts and templates)
├── claude/     Claude Code: install and use
├── openai/     OpenAI: Codex, ChatGPT and the Skills API, with chatgpt/ holding one zip per skill
├── prompts/    ready-to-paste prompts, one file per skill
├── scripts/    install.sh, build_chatgpt.py, validate_collection.py and check_answers.py
└── assets/     banner
```

## Skills

| Skill | Use it for | Prompts |
|---|---|---|
| [`gardiner-sign-lookup`](skills/gardiner-sign-lookup/) | A sign by Gardiner code, Unicode character, MdC string or sound: section, code point, role, sourced reading | [6](prompts/gardiner-sign-lookup.md) |
| [`transliteration`](skills/transliteration/) | Reading a sign sequence: uniliteral, biliteral and triliteral signs, complements, determinatives, every ambiguity flagged | [6](prompts/transliteration.md) |
| [`text-annotation`](skills/text-annotation/) | Line-by-line layout: signs, transliteration, gloss, translation, a confidence grade per word | [5](prompts/text-annotation.md) |
| [`hieroglyph-app-builder`](skills/hieroglyph-app-builder/) | Data model, Unicode and fonts, joiners, direction, search by code or sound, MdC import and export | [5](prompts/hieroglyph-app-builder.md) |
| [`accuracy-review`](skills/accuracy-review/) | Audit of a reading or a sign table: sources, consistency, smoothing, calibration | [6](prompts/accuracy-review.md) |

## How researchers would use them

- Look up a sign, its Unicode character and its readings in one step.
- Get a first-pass transliteration with the doubtful signs marked and the alternatives listed.
- Produce an annotated text, then correct it instead of typing it all.
- Check a published or draft transliteration against sign values and find the claims with no source.
- Prepare a consistent corpus, or build a small search tool over signs and sounds.

## Install

Run from this folder. Install all five skills together: they refer to each other.

```bash
bash scripts/install.sh --claude --project /path/to/your/repo   # Claude Code
bash scripts/install.sh --codex --project /path/to/your/repo    # OpenAI Codex
```

Add `--user` to install for every project on the machine, `--symlink` to link instead of copy,
`--force` to replace, or `--dry-run` to preview. Details: [`claude/`](claude/README.md) and
[`openai/`](openai/README.md).

## Try it

Pick a skill's prompt file from [`prompts/`](prompts/README.md). Or run the lookup script directly:

```bash
python3 skills/gardiner-sign-lookup/scripts/signs.py D21
python3 skills/gardiner-sign-lookup/scripts/signs.py --value nfr
python3 skills/gardiner-sign-lookup/scripts/signs.py --mdc "G17-D21:N35"
```

## Check it

```bash
python3 scripts/validate_collection.py          # structure, links, prompts, sign table, self-test, bundles current
python3 scripts/check_answers.py                # the lookup prompts' good-answer lines against signs.py
python3 scripts/build_chatgpt.py --fresh        # zips are valid and match the skills
skills-ref validate skills/<name>               # official validator
claude plugin validate skills                   # Claude Code's own check of the skill files
```

Last run, 2026-10-14: the collection validator reports 0 errors on Python 3.9 and 3.14, including the
navigation, prompt and bundle checks; the lookup script's 16 self-test checks pass on both; `skills-ref`
accepts all five skills and all five zips; `claude plugin validate` accepts the skills; markdownlint
reports 0 issues; and 11 answer checks pass against the lookup script.

### Live runs

The five starter prompts were run once each through a real Claude Code session (2.1.296, model
claude-opus-5-5) with the skills installed ([results](evals/live-results.md)), and again with no skills
installed ([baseline](evals/live-results-baseline.md)). Grading is by regular expression for the key
facts, one run per prompt, on one day.

| | Expected skill invoked | Answers with every expected fact | Cost |
|---|---|---|---|
| With the skills | 5 of 5 | 5 of 5 | 0.76 US dollars |
| No skills installed | 0 of 5 | 4 of 5 | 0.54 US dollars |

Here the skills fired every time and the answers were complete every time, against one incomplete answer
without them (the baseline missed one fact for `accuracy-review`). Five prompts, one run each, is too
few to call that a measured benefit, and the skills cost more per answer. The checks cannot see the
skills' main purpose, showing the doubt in a reading. Not run: independent grading by an Egyptologist,
repeated runs, or a description-routing test.

## Contribute

See [CONTRIBUTING.md](../CONTRIBUTING.md). Add a sign to the table only with a source and a status.

## License

Apache-2.0

## Citation

Gardiner, Alan H. 1957. *Egyptian Grammar: Being an Introduction to the Study of Hieroglyphs*.
3rd ed. Oxford: Griffith Institute. Sign-list, pp. 438-548.
