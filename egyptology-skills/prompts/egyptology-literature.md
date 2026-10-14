# `egyptology-literature` prompts

Find, read and cite Egyptological scholarship, and check a reference list for citations that cannot be
what they claim. The skill chooses the right reference tool for the question, records whether each source
was read, seen or only recalled, and never fills in a page number from memory.

- **Give it:** the target (sign, word, text, monument or object), what you already have, and which
  databases you can open
- **Skill file:** [`skills/egyptology-literature/SKILL.md`](../skills/egyptology-literature/SKILL.md)
- **Reference tools it uses:** [`reference-tools.md`](../skills/egyptology-literature/references/reference-tools.md)
- **Template it fills:** [`citation-record.md`](../skills/egyptology-literature/assets/templates/citation-record.md)
- **Find objects' histories with:** [`provenance-research-ethics`](provenance-research-ethics.md) · **Audit readings with:** [`accuracy-review`](accuracy-review.md)

## 1. Where is it published

> Where is the stela with museum number <number> in <museum> published? Which reference tool would list it, what would you search under, and what do you need from me, given that you cannot open the subscription databases?

A good answer: the Topographical Bibliography (by site, or the volume for objects of unknown provenance),
the museum's own catalogue and the Online Egyptological Bibliography, a list of spellings and numbers to
search under, a plain statement that it cannot open the databases, and no invented citation.

## 2. Check a reference list

> Check this reference list for references that might be invented or wrong: <paste>. Mark each one read, seen or recalled, run the citation checker on any with a DOI, and tell me which entries a librarian must confirm.

A good answer: a read, seen or recalled mark per entry; the checker's result for the DOI entries; books and
monographs listed as not checkable by DOI and passed to a librarian to confirm; and no entry presented as
verified that was not.

## 3. Which dictionary

> Which dictionary should I consult for the meaning and attestations of the word <word>, and in what order? Tell me what you cannot confirm.

A good answer: the Wörterbuch and the Thesaurus Linguae Aegyptiae as first stops, a specialised dictionary
for the period or genre flagged for checking, spellings to search under, and no made-up entry or volume numbers.

## 4. Is the translation still current

> A 1930s translation of <text> is the only one I have. How do I find out whether its readings are still current, and what should I look for?

A good answer: find the edition behind the translation, search for newer editions and reviews, compare
the key readings, and name the date; it does not claim from memory which specific readings are outdated.

## 5. Format a reference

> Format this reference for a journal that uses author-date style, and tell me which parts you cannot confirm: <paste>

A good answer: it asks for the journal's style guide, formats what it has, and lists the missing or unconfirmed
parts, such as pages and series volume, without inventing them.

## 6. Read an article

> Read the article I pasted and tell me exactly what it claims about <sign or word>, the evidence it gives, and how certain the author is. Quote briefly with the page.

A good answer: short quotations with locations, the author's own certainty words (certain, probable,
restored, disputed), and nothing added that the article does not say.
