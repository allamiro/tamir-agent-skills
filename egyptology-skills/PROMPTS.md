# Prompts

One ready-to-paste prompt per skill. Swap in your own signs and sources. You never need to type
a skill name; describe the task and the agent picks the skill.

## `gardiner-sign-lookup`

> What are the readings and roles of Gardiner sign G17, which Unicode character is it, and which section does it belong to? Then tell me which signs in your table read nfr, and say how sure you are of each.

## `transliteration`

> Transliterate this sequence of Gardiner codes: G39 A1. Classify each sign (uniliteral, biliteral, determinative), say which transliteration convention you use, and flag anything ambiguous.

## `text-annotation`

> Annotate this line, given as Gardiner codes: <codes>. Give me a table with signs, transliteration, gloss, a confidence grade per word and a translation, and list every point that needs an Egyptologist.

## `hieroglyph-app-builder`

> Design a small web app where students look up a hieroglyph by Gardiner code or by sound and see its Unicode character, readings and sources. Give me the data model, the rendering plan with fallbacks, and tests.

## `accuracy-review`

> Review this transliteration and gloss for confident errors: <paste>. Trace each claim to a source, check the conventions, and give me findings ranked by severity, plus what you could not check.
