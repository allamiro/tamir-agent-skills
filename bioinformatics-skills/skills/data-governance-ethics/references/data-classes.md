# Data classes

General guidance, not legal advice. Rules differ by country, institution and agreement; VERIFY with
your data steward.

## What usually applies

| Data | Identifiable? | Usual treatment |
|---|---|---|
| Human whole genome or exome | Yes, even without a name | Controlled access; secure environment; consent-limited use |
| Human genotype array data | Yes | The same |
| Human RNA or protein data from identified donors | Often | Controlled or restricted; check consent |
| Aggregate allele frequencies from many people | Low risk for large groups; higher for small groups | Check the agreement and group size |
| Summary statistics from association studies | Lower, but not zero in some cases | Many are shared openly; follow the data provider's rule |
| Clinical records and phenotypes | Yes, in combination | Health-privacy rules; minimal necessary |
| Microbiome of a person | Can be linked to the person | Treat with care; check consent |
| Non-human model organism sequences | No | Open, with licence |
| Environmental or wild-animal samples | No person | Permits and ethics approval for the species and site |
| Community-held or Indigenous data | Group-level harm possible | The community's governance as well as law |

## Why a genome is not anonymous

A genome is unique to a person (identical twins aside), is inherited from and shared with
relatives, and can be matched against other genome data held elsewhere. Removing names and dates
does not remove these properties. Treat all individual-level genomic data as identifying.

## Terms to know

| Term | Meaning |
|---|---|
| Consent scope | What participants agreed their data could be used for |
| Ethics approval | Permission from an ethics committee for a defined study |
| Data-use or access agreement | A contract setting who may use data, for what, and how |
| Controlled access | Data released only to approved users under an agreement |
| Coded or pseudonymised | Identifiers replaced by codes, with a key held elsewhere; not anonymous |
| Anonymised | Cannot be linked back to a person; hard to achieve for genomic data |
| Data steward | The person responsible for data governance at an institution or repository |

## Practical habits

- Ask early who the data steward is.
- Keep a data register: source, permissions, location, who has access, retention date.
- Never put identifiers in file names, code, commit messages, logs or prompts.
- Keep derived results at the same level of protection as the data until the agreement says otherwise.
- Check small counts in tables before publishing.
- Delete data when the agreement says so, and record the deletion.
