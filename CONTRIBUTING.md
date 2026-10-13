# Contributing

Thanks for helping improve these skills. The bar is: a skill must make an agent *do better
engineering work*, and every claim in it must be traceable or clearly marked as unverified.

## Adding a skill to an existing collection

1. Create `<collection>/skills/<name>/SKILL.md`. The name equals the folder name and uses
   lowercase letters, digits and single hyphens (maximum 64 characters).
2. Write the frontmatter: `name`, a `description` of at most 1024 characters that says what
   the skill does, when to use it and which sibling skill to use instead, plus `license` and
   `metadata`.
3. Follow the body structure in
   [`system-design-skills/docs/authoring-guide.md`](system-design-skills/docs/authoring-guide.md):
   purpose and activation, required inputs, workflow, decision framework, architecture and
   implementation guidance, failure and edge cases, validation, expected output, and a
   *Sources and confidence* block.
4. Keep `SKILL.md` under 500 lines and about 5,000 tokens. Put long reference material in
   `references/` and link to it directly from `SKILL.md`.
5. Do not duplicate another skill's content; link to it by name.
6. Run the checks below and fix every failure.

## Adding a new collection

Create `<domain>-skills/` with the same shape as `system-design-skills/`: a `skills/`
directory, a README that states scope and verification status, and validators. Add the
collection to the table in the root README.

## Content rules

- No copied passages or diagrams from books or documentation. Write original explanations
  and new diagrams; short factual attributions are fine.
- No invented citations, benchmarks, standards numbers or vendor limits. If you cannot
  verify a claim, mark it `VERIFY` and say what to check. Claims fetched from a primary
  source say so with the date.
- Do not commit source books, PDFs or text extracted from them.
- Illustrative numbers are labelled *illustrative*; formulas carry units.
- Vendor-neutral by default: name products as examples, not requirements.

## Checks to run

From the collection directory (for example `system-design-skills/`):

```bash
python3 scripts/validate_library.py          # spec rules, sections, size, links, templates, script self-tests
python3 scripts/check_routing.py --verbose   # description routing smoke test
python3 scripts/build_chatgpt.py --check     # bundle limits for ChatGPT / OpenAI uploads
skills-ref validate skills/<name>            # official Agent Skills validator
```

`skills-ref` comes from the
[agentskills reference library](https://github.com/agentskills/agentskills/tree/main/skills-ref).
Do not report a check as passed unless you ran it.

## Commits and pull requests

Keep commits focused and describe *why*. Do not add attribution trailers for tools. Mention
which checks you ran in the pull request description.
