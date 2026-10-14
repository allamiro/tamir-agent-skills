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

## Skills

| Skill | Use it for |
|---|---|
| `gardiner-sign-lookup` | A sign by Gardiner code, Unicode character, MdC string or sound: section, code point, role, sourced reading |
| `transliteration` | Reading a sign sequence: uniliteral, biliteral and triliteral signs, complements, determinatives, every ambiguity flagged |
| `text-annotation` | Line-by-line layout: signs, transliteration, gloss, translation, a confidence grade per word |
| `hieroglyph-app-builder` | Data model, Unicode and fonts, joiners, direction, search by code or sound, MdC import and export |
| `accuracy-review` | Audit of a reading or a sign table: sources, consistency, smoothing, calibration |

## How researchers would use them

- Look up a sign, its Unicode character and its readings in one step.
- Get a first-pass transliteration with the doubtful signs marked and the alternatives listed.
- Produce an annotated text, then correct it instead of typing it all.
- Check a published or draft transliteration against sign values and find the claims with no source.
- Prepare a consistent corpus, or build a small search tool over signs and sounds.

## Install

```bash
bash scripts/install.sh --claude --project /path/to/your/repo   # Claude Code
bash scripts/install.sh --agents --project /path/to/your/repo   # Codex and .agents/skills readers
```

Add `--symlink`, `--force` or `--dry-run` as needed. Install all five together: they refer to
each other. A ChatGPT bundle has not been built for this collection yet.

## Try it

Ready-to-paste prompts are in [PROMPTS.md](PROMPTS.md). Or run the lookup script directly:

```bash
python3 skills/gardiner-sign-lookup/scripts/signs.py D21
python3 skills/gardiner-sign-lookup/scripts/signs.py --value nfr
python3 skills/gardiner-sign-lookup/scripts/signs.py --mdc "G17-D21:N35"
```

## Check it

```bash
python3 scripts/validate_collection.py          # structure, links, sign table, self-test
skills-ref validate skills/<name>               # official validator
```

Last run, 2026-10-14: the collection validator reports 0 errors, the lookup script's 16 self-test
checks pass on Python 3.9 and 3.14, and `skills-ref` accepts all five skills.

Not run: any end-to-end test with a live agent, a description-routing test, ChatGPT bundles.

## Contribute

See [CONTRIBUTING.md](../CONTRIBUTING.md). Add a sign to the table only with a source and a status.

## License

Apache-2.0

## Citation

Gardiner, Alan H. 1957. *Egyptian Grammar: Being an Introduction to the Study of Hieroglyphs*.
3rd ed. Oxford: Griffith Institute. Sign-list, pp. 438-548.
