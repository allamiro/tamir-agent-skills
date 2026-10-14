# `egyptology-research-writing`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Help me write up an unpublished Middle Kingdom stela in a regional museum for publication. I have photographs, my transliteration and translation, and two parallels. Outline the article and tell me what I must settle before I write.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 3,425 | 3,003 |
| Input tokens read across all turns (including cached context) | 30,381 | 102,876 |
| Extra input tokens when the skill is installed | | +72,495 |
| Cost, US dollars at list price | 0.128 | 0.175 |
| Skills invoked in the sample run | none | `egyptology-research-writing` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 330 tokens for its name and description, which are in every session where the skill is installed, and about 2,100 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I can outline the article now. Before drafting I'd need your transliteration, translation, the parallels and the museum details, and several things below that only you or the museum can settle.

## What to settle before you write

These are listed roughly in the order they would stop the article.

1. **Permission to publish, in writing.**
   - Confirm the museum is willing for you to publish the stela. Regional museums sometimes keep first-publication rights for a curator or a catalogue in preparation.
   - Get written permission for each photograph: who took it, whether it can be printed and put online (most journals now publish both), and the exact credit line the museum wants.
   - If your own photographs aren't cleared, ask whether the museum will supply official ones or allow a facsimile drawing.

2. **Whether it really is unpublished.** Check:
   - the *Topographical Bibliography* (Porter & Moss), especially volume VIII for objects of unknown provenance;
   - the Online Egyptological Bibliography;
   - the museum's own catalogues, old guidebooks and sale or auction catalogues if it came from a collector.

   A stela that is "unpublished" often turns up as a line in an old catalogue. If you find one, cite it and say how your edition differs.

3. **Provenance and acquisition history.** Find out how and when the museum acquired it, from whom, and whether a findspot is recorded or only suspected. Abydos is common for Middle Kingdom stelae, but don't assume it. This goes in the article as a documented history, with gaps stated as gaps. If the object has no documented findspot, decide how you will present that before you start.

4. **Whether you can see the stone itself.** Find out if you can collate the original, or at least get raking-light photographs or RTI, before you fix the readings. Every damaged or doubtful sign needs a stated basis, such as "on the original" or "from photograph only". A reviewer who reads a sign differently from your published plate is the most likely objection.

5. **What exactly the two parallels are for.** For each one, decide its role:
   - **Restoring a lacuna:** say so and mark the restoration as restored from that parallel.
   - **Dating:** the parallel needs a secure date of its own.
   - **A family or prosopographical link:** check whether it is the same owner, a relative or a shared workshop. Simpson's offering-chapel groupings for Abydos are the usual starting point (*The Terrace of the Great God at Abydos*, 1974; verify before citing).

   Also check whether each parallel's published reading still stands, and look for more parallels. Two is a starting point, not a corpus.

6. **The basis for the date.** "Middle Kingdom" needs to be narrowed and argued. The usual evidence:
   - the wording and spelling of the offering formula;
   - epithets of Osiris and Anubis;
   - titles and personal names, with their dated attestations (Ilin-Tomich's *Persons and Names of the Middle Kingdom* database, Franke, Ward, Fischer);
   - layout, iconography and how the figures are carved.

   Write down which criteria you rely on and how strong each one is. A date from style alone gets "probably".

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Publishing an unpublished Middle Kingdom stela: what to settle first, then an outline

## Part 1: What to settle before you write

These are listed roughly in order of how badly each one can hold you up.

### A. Permissions and rights (sort these out first)
1. **Written permission to publish** from the museum, with the curator named. Check whether the museum expects co-authorship, a credit line, or to see the draft first.
2. **Image rights.** Who owns your photographs? If you took them in the gallery, does the museum's policy allow you to publish them? Will the journal need high-resolution official photographs, and are there fees? Get the required credit wording now.
3. **First publication.** Make sure no one else (a staff member, a former curator's student) has a publication planned.

### B. Is it really unpublished?
4. Check:
   - the Topographical Bibliography (Porter & Moss), especially **vol. VIII** (objects of unknown provenance), and the Griffith Institute's online addenda
   - the Online Egyptological Bibliography
   - the museum's own catalogues, annual reports and archive file
   - old sale catalogues (Sotheby's, Christie's, Drouot)
   - dealer and collection records

   A one-line mention in a 1920s auction catalogue still counts as prior publication, and it may give you a provenance.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
