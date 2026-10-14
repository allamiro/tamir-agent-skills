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

## Which tool are these for

All of them. A prompt is plain text, so the same wording works in every tool that has the skills
installed. Today that means Claude Code ([`claude/`](../claude/README.md)) and OpenAI Codex
([`openai/`](../openai/README.md)). There is no ChatGPT bundle for this collection yet.

You never need to type a skill name. Describe the task and the agent picks the skill.

## The order the skills hand off

```text
gardiner-sign-lookup  ->  transliteration  ->  text-annotation  ->  accuracy-review
   one sign               a sign sequence      a laid-out text      a challenge to the result
```

`hieroglyph-app-builder` sits beside this chain: it holds the sign facts that `gardiner-sign-lookup`
supplies and uses `accuracy-review` to design its data checks.

Every prompt here uses signs from the collection's checked table, except where a prompt tests what
happens with a sign that is not in it.
