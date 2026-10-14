# Prompts

Each skill has its own file of ready-to-paste prompts. Open the skill you need, copy a prompt, and
replace the `<angle-bracket>` parts with your own model, data and files. Every prompt has an "A good
answer" line saying what a sound answer contains; the computable ones are checked by
`scripts/check_answers.py`.

## Plan, design and learn

| Skill | Prompts | Use them to |
|---|---|---|
| `systems-biology-workflow` | [5 prompts](systems-biology-workflow.md) | Start a project from the question and choose the formalism |
| `model-building-design` | [5 prompts](model-building-design.md) | Make assumptions, quantities and model class explicit |
| `systems-biology-learning-path` | [5 prompts](systems-biology-learning-path.md) | Get a study plan, worked exercises and teaching designs |

## Research and writing

| Skill | Prompts | Use them to |
|---|---|---|
| `modeling-research-planning` | [5 prompts](modeling-research-planning.md) | Plan aims, the model–experiment cycle, measurement and design |
| `quantitative-research-methods` | [5 prompts](quantitative-research-methods.md) | Define and validate a measurement, pick a method, size an effect |
| `systems-biology-literature` | [5 prompts](systems-biology-literature.md) | Find papers, models and parameters, and check references |
| `modeling-paper-writing` | [5 prompts](modeling-paper-writing.md) | Write, submit and revise a modelling paper |
| `model-review` | [5 prompts](model-review.md) | Audit a model or modelling paper and rank the problems |

## Networks and matrices

| Skill | Prompts | Use them to |
|---|---|---|
| `linear-algebra-networks` | [5 prompts](linear-algebra-networks.md) | Solve, classify and decompose matrices, and read eigenvalues |
| `network-analysis` | [5 prompts](network-analysis.md) | Build graph matrices, measure centrality, find motifs |
| `stoichiometric-networks` | [5 prompts](stoichiometric-networks.md) | Get flux spaces, conservation relations, modes and MFA status |
| `flux-balance-analysis` | [5 prompts](flux-balance-analysis.md) | Run FBA, flux variability and knockouts |

## Dynamics and kinetics

| Skill | Prompts | Use them to |
|---|---|---|
| `quantities-units-balances` | [5 prompts](quantities-units-balances.md) | Check units, write balances, solve a chemostat |
| `ode-dynamics` | [5 prompts](ode-dynamics.md) | Simulate, find steady states, classify stability, rank parameters |
| `control-systems-feedback` | [5 prompts](control-systems-feedback.md) | Test controllability and stability, analyse feedback |
| `enzyme-kinetics` | [5 prompts](enzyme-kinetics.md) | Choose and fit rate laws, read inhibition |
| `pharmacokinetic-modeling` | [5 prompts](pharmacokinetic-modeling.md) | Compute half-life, AUC, accumulation and effect |
| `stochastic-discrete-models` | [5 prompts](stochastic-discrete-models.md) | Simulate noise, find Boolean attractors, iterate maps |

## Data, statistics and code

| Skill | Prompts | Use them to |
|---|---|---|
| `parameter-estimation-model-selection` | [5 prompts](parameter-estimation-model-selection.md) | Fit, check identifiability, compare models |
| `multivariate-omics` | [5 prompts](multivariate-omics.md) | Run PCA and PLS, and validate them |
| `systems-biology-programming` | [5 prompts](systems-biology-programming.md) | Write, balance-check, test and share model files |

## Which tool are these for

All of them. A prompt is plain text, so the same wording works in every tool that has the skills
installed: Claude Code ([`claude/`](../claude/README.md)) and OpenAI Codex or ChatGPT
([`openai/`](../openai/README.md)).

You never need to type a skill name. Describe the task and the agent picks the skill.
