---
name: systems-literature-reading
description: Reads, appraises and applies research and engineering literature on distributed systems, databases and infrastructure, covering how to find prior art, read a paper in passes, extract its claims, assumptions, workload and evaluation, decide whether a result transfers to a given system, and cite sources without inventing them. Use for "summarise this paper", "does this paper apply to us", "what does the research say about X", "find prior art for this design", "is this vendor benchmark trustworthy", "what should I read on consensus", "compare these two papers", "check my references". Use performance-evaluation-methodology to design or judge the benchmarks, system-design-review to critique an architecture, and system-design to produce a new design.
license: Apache-2.0
metadata:
  library: system-design-skills
  version: "1.0"
---

# Systems literature reading

## Purpose and activation

Design decisions often rest on a paper, a vendor whitepaper or a conference talk, and the usual
failure is to take its headline number or its name recognition as proof. This skill turns a source
into a short, checkable record of what it claims, under which assumptions, and whether those
assumptions hold for the system at hand. Activate when a decision cites a paper or product claim,
when the user asks what the research says, or when prior art must be found. It also checks reference
lists, because invented citations are the commonest way an assistant misleads in this area.

## Required inputs

The question or decision the reading feeds; the source (paper, link, pasted text) or the topic to
search; the user's system in a few lines (scale, failure domains, network, data model, consistency
needs, team capacity); and how the result will be used (design choice, literature review, interview
answer, paper related-work section).

## Workflow

1. **State the question and the decision.** "What would we do differently if this paper is right?"
   If nothing changes, say so and stop early.
2. **Classify each source** with the table below before trusting it.
3. **Find prior art from the question, not the paper.** Search the problem in several vocabularies
   (a database paper may call replication "state machine replication" or "log shipping"), then follow
   references backward and "cited by" forward. Record each search with its date.
4. **Read in passes** (the three-pass method in Keshav's *How to Read a Paper*, see
   `references/canonical-papers.md`): a quick pass for category, context and claims; a careful pass
   for the argument without the proofs; and, only if the decision depends on it, a pass that tries to
   re-derive the key step.
5. **Extract the claim record** (`assets/templates/paper-notes.md`): the claim, the evidence, the
   workload and scale, the hardware, the baseline, the metric, the failure and network model, what the
   paper does not claim, and any artifact or code.
6. **Test transfer.** For each assumption, say whether the user's system matches, differs in a way
   that matters, or is unknown. Use the verdict scale below.
7. **Cross-check once.** Find an independent source: a reimplementation, an independent test report,
   an erratum, a later paper by other authors, or the system's own current documentation.
8. **Cite with a record of how you know.** Mark each reference `read` (opened and read), `seen` (read
   about it in a secondary source) or `recalled` (from memory; treat as unverified). Run
   `scripts/citecheck.py` on the list before sending it.
9. **Report** the answer, the claim record, the verdict, the open questions, and the reading list.

## Decision framework

| Source type | Weight | Check first |
|---|---|---|
| Peer-reviewed paper, full version | High for what it measured | Workload, baselines, variance, artifact |
| Journal extension of a conference paper | Same, often corrected | Which version the user is quoting |
| Preprint or technical report | Medium | Whether a reviewed version exists and differs |
| Industry paper about the authors' own system | High for that system, low for generality | Scale, years, what was left out |
| Independent test report on a product | High for the versions tested | Version and configuration tested |
| Vendor whitepaper or benchmark | Low until reproduced | Who ran it, workload, configuration, variance |
| Blog post or talk | Lead only | Find the primary source it summarises |
| Your recollection | None | Look it up |

| Transfer verdict | Meaning |
|---|---|
| Applies | Assumptions match and the result is large compared with its uncertainty |
| Applies with changes | One or more assumptions differ; name the change and what to re-measure |
| Inspires only | The idea is useful but the numbers do not carry over |
| Does not apply | A core assumption fails (failure model, scale, consistency need) |

## Architecture and implementation guidance

- Read the evaluation section before the abstract's claims are accepted: workload, dataset, hardware,
  baselines, number of runs, and whether any variance is shown (`performance-evaluation-methodology`).
- Check the terms. "Consistency" means different things in the CAP proof, in database isolation and in
  replica convergence; read the definition the authors use (`transactions-consistency`).
- Note the date and the system version. Systems change after the paper; the paper describes one moment.
- Keep quotations short and exact, with a page or section. Do not paraphrase a number you did not see.
- A canonical-paper reading map by topic is in `references/canonical-papers.md`. Every entry there was
  checked against its publisher record or Crossref; the dates are in the file.

## Failure and edge cases

- **Quoting a figure without its workload,** such as a latency with no request mix or percentile.
- **Treating a paper about one company's system as a general result.**
- **Mixing the conference and journal versions** of one paper, which can differ in design and numbers.
- **Survivorship.** Published systems are the ones that worked; failed designs rarely appear.
- **Citing from memory.** Author lists, years, venues and page numbers recalled from memory are wrong
  often enough to matter. An assistant can also produce a convincing reference that does not exist.
- **Trusting a summary over the source,** including this skill's own reading map.
- **A search that only finds the famous papers.** Add recent surveys and the systems that replaced them.
- **No access to the paper.** Say so, work from the abstract only, and mark every claim `seen`.

## Validation

- Every number in the answer has a page, section or figure behind it, or is marked unverified.
- Every reference has a `read`, `seen` or `recalled` mark, and `scripts/citecheck.py --online` returns no
  `DOI-NOT-FOUND` or `MISMATCH`. A pass means the record matches the line; it does not mean the paper
  supports the claim.
- Each assumption in the transfer test has a stated answer for the user's system.
- Falsifier: a quoted number that the source does not contain, or a reference that does not exist.

## Expected output

A short answer to the question; the claim record; the transfer verdict with the assumptions that
decide it; one independent cross-check or a statement that none was found; a reference list with
`read`/`seen`/`recalled` marks and the citation checker's result; and what remains unknown.

## Sources and confidence

- Book (direct): none; this skill extends the library to research work and is not taken from the book
- Book (synthesized): none
- Modern: Keshav, *How to Read a Paper* (ACM SIGCOMM CCR 37(3), 2007) and every entry in `references/canonical-papers.md` - bibliographic records fetched from Crossref, USENIX and Microsoft Research on 2026-10-14; the "does not settle" notes, the source-weight table and the transfer scale are own analysis, from author knowledge, VERIFY
- Needs workload validation: the user's scale, failure model and consistency need decide the transfer verdict; not covered are running a paper's experiments (`performance-evaluation-methodology`), formal verification and artifact licensing
