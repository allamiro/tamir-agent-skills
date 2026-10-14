# `data-governance-ethics` prompts

Work carefully with human, health and other sensitive biological data: consent, access, storage,
sharing, and the use of online and automated tools. This is guidance, not legal advice.

- **Give it:** what the data are and where they came from, the consent, approval and agreement
  documents, the countries involved, and who will see the data
- **Skill file:** [`skills/data-governance-ethics/SKILL.md`](../skills/data-governance-ethics/SKILL.md)
- **Reference and template:** [`data-classes.md`](../skills/data-governance-ethics/references/data-classes.md) and
  [`data-access-checklist.md`](../skills/data-governance-ethics/assets/templates/data-access-checklist.md)
- **Related:** [`biological-databases`](biological-databases.md), [`reproducible-research-code`](reproducible-research-code.md)

## 1. Is it anonymous

> I have whole-genome sequences from patients with coded sample IDs only. Is this patient data anonymous, and can I share it?

A good answer: no; a genome is unique to a person and shared with relatives, coded data are
pseudonymised at best, and the consent and access agreement decide what is allowed.

## 2. An online tool

> Can I paste a few of these sequences, with their sample IDs, into an online chat tool to get help with my code?

A good answer: not without checking the data agreement and the tool's terms; use synthetic or
invented data instead, strip identifiers, and prefer a local tool for anything sensitive.

## 3. Sending data abroad

> A collaborator in another country wants a copy of the data. What do I need to check before sending anything?

A good answer: the consent scope, the access agreement's rules on third parties and transfers, the
rules of both countries, and written permission from the data owner or steward.

## 4. Identifiers in a public repository

> My file names contain patient IDs and my code repository is public. What do I do first?

A good answer: stop sharing, remove identifiers from the files and from the repository history,
tell the data steward, and replace the names with coded identifiers.

## 5. Small counts in a table

> Is it all right to publish a table of allele counts for 8 people?

A good answer: probably not without checking the agreement, because small groups can identify
individuals; aggregate more, or share through controlled access.

## 6. A data access checklist

> Fill in the data access checklist for <describe the dataset>. Mark everything I have not told you as unknown and list the questions for my data steward.

A good answer: a completed checklist with unknowns marked, the permissions still to be found, and
a short list of specific questions for the steward.
