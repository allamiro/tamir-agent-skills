# `data-governance-ethics`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I have whole-genome sequences from patients with coded sample IDs only. Is this patient data anonymous, and can I share it?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,653 | 1,210 |
| Input tokens read across all turns (including cached context) | 30,351 | 73,407 |
| Extra input tokens when the skill is installed | | +43,055 |
| Cost, US dollars at list price | 0.093 | 0.150 |
| Skills invoked in the sample run | none | `data-governance-ethics` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 270 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**No. Coded whole-genome sequences are not anonymous, and you shouldn't share them until you've checked your permissions.** This is general guidance, not legal advice.

## Why coded IDs don't make the data anonymous

- **The genome identifies the person.** A whole genome is unique to one individual. Taking off names doesn't change that. People have been re-identified by matching genomes against genealogy databases, public variant data, or the Y-chromosome against surnames.
- **The data are coded (pseudonymised), not anonymous.** If anyone still holds the key linking codes to patients, the data count as personal data under most regimes. GDPR, for example, treats pseudonymised data as personal data, and genetic data as a special category on top of that.
- **Relatives are exposed too.** A genome reveals information about family members, who never consented to anything.
- **Summaries can leak.** Some summary statistics, such as allele frequencies from small cohorts or rare-variant counts, can show whether a particular person was in the study. Small counts (1 or 2) in published tables are a known risk.
- **Other data increase the risk.** Combining genomes with phenotype, age, location or diagnosis dates makes re-identification much easier.

## Whether you can share depends on what you were given permission for

Find and read these before sharing anything:

1. **The consent form.** Does it cover sharing, and with whom (your institution only, named collaborators, controlled-access repositories, open release)? Does it allow commercial use or transfer to another country?
2. **The ethics approval.** Does it cover this use and this recipient?
3. **Any data-use or data-transfer agreement**, if you received the data from someone else.
4. **Your institution's policy** and the law in each country involved.

| Your situation | Usual route |
|---|---|
| Consent and approval cover sharing with a named collaborator | A data-transfer agreement, then secure transfer (not email) |
| Sharing with the research community | A controlled-access repository such as EGA or dbGaP, where requests go through a data access committee |
| The paper needs the data for reproducibility | Share code, checksums and safe summary results, and give the controlled-access route for the raw data |
| Consent doesn't cover the use, or you can't tell | Stop and ask the data owner or ethics committee |
| Open public posting | Almost never appropriate for patient genomes without explicit consent for it |

## Practical safeguards

- Keep the code-to-patient key separate from the data, under tighter access control, and make sure it never travels with the data.
- Keep sample IDs and any patient details out of file names, code, logs, git history and prompts to online tools, including AI assistants. Don't send the sequences to any online service whose terms allow retention or training.
- Store the data in an access-controlled, encrypted environment, with a written list of who has access and a date for deletion.

## Questions to take to your data steward or ethics office

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Short answer: it isn't anonymous, and you probably can't share it openly

Coded IDs make the data **pseudonymized**, not anonymous. A whole genome identifies the person by itself, so removing names and medical record numbers doesn't fix that.

## Why WGS can't really be anonymized

- **The genome is a unique identifier.** Except for identical twins, it matches one person and stays the same for life.
- **Re-identification has been demonstrated.** Gymrek et al. (2013, *Science*) recovered participants' surnames from Y-chromosome markers by cross-referencing public genealogy databases. Consumer genealogy databases such as GEDmatch have since been used to identify people through distant relatives.
- **Relatives are exposed too.** The data reveals information about family members who never consented.
- **Phenotype can be inferred.** Ancestry, some physical traits and disease risk can be predicted and linked with other data sources.
- **Even summary data can leak.** Homer et al. (2008) showed that aggregate allele frequencies can reveal whether a person was in a cohort.

## How the main legal frameworks treat it

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
