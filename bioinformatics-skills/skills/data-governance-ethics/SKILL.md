---
name: data-governance-ethics
description: Handles the rules, privacy and ethics of biological and health data, covering consent and permitted use, why genomes cannot be anonymised, controlled-access data, data-use agreements, secure storage and compute, sharing derived results, ethics approval, and careful use of online and automated tools with sensitive data. Use for "can I share this genome data", "is this patient data anonymous", "what do I need before using patient sequences", "is this data identifiable", "how should I store human genomic data", "data access agreement", "can I upload this to a cloud tool or chat model". Use reproducible-research-code for repository hygiene, biological-databases for where data is deposited, and bioinformatics-review for audit. This is guidance for working carefully, not legal advice.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Data governance and ethics

## Purpose and activation

Stop an analysis from breaking a promise made to the people whose data it uses. Biological and
health data carry consent terms, legal duties and a real risk to individuals, and the person writing
the code is often the last to read the terms. Activate before data are obtained, moved, shared,
uploaded to a service, or described in a paper, and whenever human, patient, or community data appear.

## Required inputs

What the data are and where they came from; whether they come from people, animals, or the
environment; the consent form, ethics approval and any data-use agreement; the institution's
policy; the country or countries involved; who will see the data; and where they will be stored
and processed, including any online or automated tool.

## Workflow

1. **Classify the data.** Human or not; identifiable, coded or anonymous in the sources' own terms;
   the type (genome, phenotype, images, samples); whether a community has its own governance rules.
2. **Find the governing documents** and read them: the consent, the approval, the data-use or
   access agreement, the repository's terms, and institutional policy. The data owner or a data
   steward can answer what the paper cannot.
3. **Check what use is permitted.** A new purpose, a new collaborator, a new country or a
   commercial partner may each need new permission.
4. **Treat genomic data as identifying.** A genome is unique to a person and shared with relatives;
   removing names does not make it anonymous, and some summaries can leak membership (VERIFY the
   current guidance for the kind of summary you hold).
5. **Plan storage and compute:** access control, encryption, logging, a secure environment for
   controlled-access data, no copies on personal devices, and a retention and deletion date.
6. **Keep identifiers out of everything else:** file names, code, notebooks, logs, commit history,
   error messages and prompts to any tool.
7. **Before using an online service or an automated assistant,** read its terms on retention and
   training and the data agreement's rules on third parties; use a local tool for sensitive data.
8. **Decide what can be shared:** open, controlled-access, summary statistics only, or nothing, and
   write the reason (`assets/templates/data-access-checklist.md`).
9. **Plan for findings and incidents:** what happens if you find something clinically important or lose data.
10. **Record the decisions** with names and dates.

## Decision framework

| Situation | Choice |
|---|---|
| Consent does not cover the new use | Stop; ask the data owner or ethics committee |
| Data are "de-identified" genomes | Still treat as identifiable; check the agreement |
| Controlled-access dataset | Use only inside the approved environment, by approved people |
| Need to share for reproducibility | Share code, checksums and summary results; point to the access route for data |
| Tool is an online service | Read its terms first; do not send identifiable or controlled data without permission |
| Samples from a community with its own governance | Follow its rules in addition to the law (VERIFY with the community or custodian) |
| Animal or environmental samples | Check permits and ethics approval for the species and place |
| Unsure | Ask the data steward or ethics office before acting |

## Implementation guidance

- Use coded sample identifiers that carry no information about the person, and keep the key
  separately under tighter control.
- Put access in writing, per person, and remove it when a person leaves.
- Use repository features for controlled access rather than emailing files.
- Check the data-use agreement for rules on publishing small counts, which can identify people.
- `references/data-classes.md` sets out kinds of data and what usually applies to each.

## Failure and edge cases

- **Anonymised genome** treated as safe to post.
- **Sample identifiers in file names** or in a public repository's history.
- **Data combined with another dataset** so that people can be re-identified.
- **Reuse for a purpose** the participants did not agree to.
- **Upload to an online tool** whose terms allow retention or training.
- **Collaborators in another country** without a transfer agreement.
- **No retention or deletion plan.**
- **Small cells** (a count of one or two) in a published table.
- **Relatives' privacy** forgotten when one family member's genome is shared.
- **Community or Indigenous data** handled only under general law.

## Validation

- Each data source in the project has a documented permission for each use.
- No identifiers appear in code, logs, history, file names or prompts (search for them).
- The access list matches the approved list.
- Falsifier: someone outside the approved group can open the data.

## Expected output

The data classification, the permissions found with the document for each, the permitted and
forbidden uses, the storage and access plan, the sharing decision with its reason, the treatment of
outside tools, and the open questions for the data steward.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: ch. 17 (the genetic basis of disease, cancer,
  automated diagnosis, drug discovery, personalized medicine): section titles only. The text on
  these topics was not supplied
- All governance guidance, legal regimes (for example data-protection and health-privacy laws in
  various countries) and agreements: general knowledge only, VERIFY with your institution's data
  steward, ethics committee and legal office. This skill gives no legal advice
- Not covered: clinical consent design, return of results policy in detail, specific national laws
