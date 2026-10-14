---
name: provenance-research-ethics
description: Handles provenance, legality, permissions and research ethics when working with Egyptian antiquities and inscriptions, covering object and collection histories, the 1970 UNESCO benchmark and why societies and museums use different cut-off dates, publishing objects with no documented provenance, museum numbers and image rights, heritage-country and community perspectives, disclosing AI-assisted work, and what an agent must not assert. Use for "is this object's provenance documented", "can I publish this unprovenanced stela", "can I use this museum image", "how do I cite an object I only saw in a photo", "what should I say about how this draft was made", "is this safe to put in a paper". Use egyptology-literature to find publications, accuracy-review to audit readings, and hieroglyph-app-builder for software that stores objects.
license: Apache-2.0
metadata:
  library: egyptology-skills
  version: "1.0"
---

# Provenance and research ethics

## Purpose and activation

Where an object has been, who has held it and on what evidence decide whether it can be published,
exhibited or used as evidence, and the rules differ by journal, society, museum and country. This skill
builds the history as a record with evidence for each step, flags gaps for a specialist, and keeps an
assistant from saying more than the record supports. Activate before a text or object is studied, published
or put into a dataset, and whenever a question touches legality, ownership, permissions or disclosure.
It gives no legal advice and no certificate of authenticity or legality.

## Required inputs

The object or text and any identifiers (museum or inventory number, publication reference); its current
holder; what is claimed about its findspot and history, and the evidence for each claim; where it will be
published or used, with that venue's policy; the images and data involved, with their sources; and who is
responsible for the project.

## Workflow

1. **Identify the object** with every identifier available, and note the current holder.
2. **Build the record** of events in order (`assets/templates/provenance-record.md`, or the JSON form in
   `assets/templates/provenance-record.json`): date, kind of event, from whom, to whom, place, evidence type
   and reference.
3. **Run the checker:** `python3 scripts/provrecord.py check RECORD.json`. Read each flag as a question for a specialist.
4. **Find the rules that apply to this project:** the journal or press, the learned society, the institution and
   funder, and the holding museum. Do not assume one benchmark year; list the ones that apply and where they are stated.
5. **Say only what the record supports,** using the wording ladder below.
6. **Check images and data:** the licence of each image or dataset, the credit line, and the museum's photography
   rules. Museum open-access terms differ and change, so read the object page.
7. **Note public positions:** if the holder, the country of origin or a community has stated a claim or concern about
   the object, report it neutrally with its source. Do not adjudicate.
8. **Disclose how the draft was made,** including AI assistance, following the venue's policy.
9. **Escalate** legal or ownership questions to qualified counsel or the institution's provenance researcher.

## Decision framework

| Wording | Use when |
|---|---|
| Documented | A named, dated document, label or publication supports the step, and you saw it |
| Reported | A source says so but you have not seen the underlying document |
| Claimed | The seller, owner or author asserts it with no evidence given |
| Unknown | Nothing supports a statement |

| Situation | Action |
|---|---|
| Continuous documented chain from an excavation | Describe it with its references; still note the benchmarks it satisfies |
| Gaps or an unnamed source | Report the gaps; ask a provenance researcher before publication |
| Documentation only after a benchmark year | Treat as high risk for venues with a policy; seek advice first |
| No documentation | Do not present as established; check the venue's rule on first publication |
| An image of unknown licence | Do not reproduce it; ask the holder or find a licensed image |

Policies seen on 2026-10-14, to be confirmed at the source:

| Rule | What was seen |
|---|---|
| UNESCO 1970 Convention | Adopted in Paris on 14 November 1970 and in force from 24 April 1972; aimed at illicit import, export and transfer of cultural property. Party numbers change |
| A learned society's publication policy | One society's policy (the Archaeological Institute of America) bars its venues from first publication of objects acquired after 30 December 1973 unless documented earlier or legally exported, and has them marked as unprovenanced; another society's policy (ASOR) is dated by 1970. The two dates differ |
| Museum ethics | The ICOM Code of Ethics for Museums, 2004 text, section 2.3 on checking before acquisition that an object was not illegally obtained or exported. A newer revision may exist: VERIFY |
| Egyptian law | Law 117 of 1983 on the protection of antiquities, amended by laws in 2010 and 2018, per the Ministry's own site; the provisions were not read |
| Museum images | The Metropolitan Museum of Art opened images of public-domain works under CC0 in February 2017. Other museums differ |

## Implementation guidance

- Keep the record as data, not prose, so gaps are visible and every step has a reference.
- A date before a benchmark year does not show that an object left its country lawfully; it shows only when it was documented.
- Give each uncertain step a status word from the ladder, not a softening adjective.
- Credit images in the form the holder asks, and keep the licence text with the file.
- State AI use plainly: what the assistant did, that its output is a draft, and who checked it.
- Human remains and sacred or sensitive material need specific institutional guidance that this skill does not provide.

## Failure and edge cases

- **Treating "pre-1970" as proof of legality,** or museum ownership as proof of lawful acquisition.
- **A provenance story written to fit,** including backdating or "cleaning" a history. Refuse to do this.
- **Collection names used as provenance** with no document behind them.
- **A forged or mis-dated document.** The checker cannot see this.
- **Assuming one rule applies everywhere.**
- **Using an image because it is online.**
- **Reproducing an unpublished object or text** shown to the user in confidence.
- **An agent giving a confident legal opinion.**
- **Advice on moving objects across borders** or avoiding export controls. Decline.

## Validation

- `python3 scripts/provrecord.py --selftest` passes, and every flag from `check` has a written response.
- Each event has a reference, and each statement in the draft uses a word from the ladder.
- Every image has a licence and a credit.
- Falsifier: a statement of provenance or legality in the draft that the record does not support.

## Expected output

A provenance record with the checker's flags and a response to each; the applicable rules with where they are
stated; draft wording for provenance using the ladder; an image and permissions table; the disclosure statement;
and a list of what needs a specialist or counsel.

## Sources and confidence

- UNESCO 1970 Convention dates, the learned societies' policies and the ICOM 2004 section: from search results
  read 2026-10-14; the policies' own pages were not all opened, and the ASOR policy was seen in part only
- Egyptian law: the Ministry of Tourism and Antiquities page listing the amending laws, 2026-10-14; the statute
  text, including ownership and export provisions, was not read
- Met Open Access: the Met's announcement in February 2017, 2026-10-14; the British Museum and other licences were not confirmed
- The wording ladder, the checker's flags and the escalation advice: own design, VERIFY with the institution
- Not covered: legal advice, authentication of objects, human remains, or the law outside Egypt
