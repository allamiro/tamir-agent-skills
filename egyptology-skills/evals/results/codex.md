# Codex smoke test: egyptology-skills

The same starter prompts were run once with the skills installed in `.agents/skills` and once with none, using `codex exec` (Codex CLI codex-cli 0.162.1, model default). Grading is by the same regular expressions as the Claude runs. A skill counts as used when the agent reads its SKILL.md. Codex reports tokens but not cost, and there is no model judge here, so this checks that the skills are found and used in Codex, not how good the answers are. One run per prompt and arm.

| | Every expected fact | Expected skill used | Any skill used | Mean output tokens | Mean input tokens |
|---|---|---|---|---|---|
| With the skills | 7/8 | 8/8 | 8/8 | 1,074 | 145,857 |
| No skills | 5/8 | n/a | n/a | 932 | 113,622 |

| Skill | Facts with | Facts without | Skill used |
|---|---|---|---|
| `accuracy-review` | 3/3 | 3/3 | yes |
| `edition-conventions` | 2/3 | 2/3 | yes |
| `egyptology-literature` | 3/3 | 3/3 | yes |
| `gardiner-sign-lookup` | 4/4 | 3/4 | yes |
| `hieroglyph-app-builder` | 3/3 | 3/3 | yes |
| `provenance-research-ethics` | 4/4 | 2/4 | yes |
| `text-annotation` | 3/3 | 3/3 | yes |
| `transliteration` | 3/3 | 3/3 | yes |
