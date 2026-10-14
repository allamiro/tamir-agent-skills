# Prompts

Each skill has its own file of ready-to-paste prompts. Open the skill you need, copy a prompt, and
replace the `<angle-bracket>` parts with your own signs, text and sources.

| Skill | Prompts | Use them to |
|---|---|---|
| `gardiner-sign-lookup` | [6 prompts](gardiner-sign-lookup.md) | Look up a sign by code, sound or MdC string, and see what the table does not cover |
| `transliteration` | [6 prompts](transliteration.md) | Read a sign sequence, with every ambiguity flagged at the sign |
| `text-annotation` | [5 prompts](text-annotation.md) | Lay a short text out with glosses, grades and a review list |
| `hieroglyph-app-builder` | [5 prompts](hieroglyph-app-builder.md) | Design the data model, rendering, search and exchange for a tool |
| `accuracy-review` | [6 prompts](accuracy-review.md) | Audit a reading, an annotation or a sign table before you rely on it |
| `egyptology-literature` | [6 prompts](egyptology-literature.md) | Find, read and cite scholarship, and check a reference list for invented citations |
| `edition-conventions` | [6 prompts](edition-conventions.md) | Mark lacunae and restorations with a declared key, and set out notes and witnesses |
| `provenance-research-ethics` | [6 prompts](provenance-research-ethics.md) | Build an object's history, flag the gaps, and say only what the record supports |

## Which tool are these for

All of them. A prompt is plain text, so the same wording works in every tool that has the skills
installed: Claude Code ([`claude/`](../claude/README.md)) and OpenAI Codex or ChatGPT
([`openai/`](../openai/README.md)).

You never need to type a skill name. Describe the task and the agent picks the skill.

## The order the skills hand off

```text
gardiner-sign-lookup  ->  transliteration  ->  text-annotation  ->  accuracy-review
   one sign               a sign sequence      a laid-out text      a challenge to the result
```

`hieroglyph-app-builder` sits beside this chain: it holds the sign facts that `gardiner-sign-lookup`
supplies and uses `accuracy-review` to design its data checks.

The academic and research skills sit around the chain. `egyptology-literature` finds the editions and
parallels, `edition-conventions` marks what is restored, and `provenance-research-ethics` covers where the
object has been and what may be said or shown.

Every prompt here uses signs from the collection's checked table, except where a prompt tests what
happens with a sign that is not in it.
