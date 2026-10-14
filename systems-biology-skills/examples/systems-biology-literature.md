# `systems-biology-literature`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Find papers on modelling the circadian clock in mammals, and tell me whether there is a published model I can reuse and where to get kinetic parameters.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 3,041 | 4,880 |
| Input tokens read across all turns (including cached context) | 93,717 | 228,917 |
| Extra input tokens when the skill is installed | | +135,200 |
| Cost, US dollars at list price | 0.145 | 0.294 |
| Skills invoked in the sample run | none | `systems-biology-literature` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 300 tokens for its name and description, which are in every session where the skill is installed, and about 1,700 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
Web search and fetch were both blocked in this session, so I couldn't search PubMed or BioModels or check DOIs online. Everything below is from memory and unverified, so check each item before you cite it. I saved the references to a file you can check with one command (see the end).

## Published models you can reuse

All of these are deterministic ODE models of the transcription–translation feedback loops (CLOCK/BMAL1 → Per/Cry, plus the REV-ERB/ROR loop).

| Model | Size / scope | Reuse notes |
|---|---|---|
| **Leloup & Goldbeter 2003**, PNAS, doi:10.1073/pnas.1132112100 | 16–19 variables; Per, Cry, Bmal1, phosphorylation, nuclear transport | The classic choice. I think several variants are in BioModels (around BIOMD0000000073–078), but check the IDs. |
| **Forger & Peskin 2003**, PNAS, doi:10.1073/pnas.2036281100 | About 70 mass-action variables | Very detailed. Mass-action form makes stochastic versions easy. |
| **Becker-Weimann et al. 2004**, Biophys J, doi:10.1529/biophysj.104.040824 | 7 variables, two interlocked loops | Small and good for analysis and teaching. |
| **Mirsky et al. 2009**, PNAS, doi:10.1073/pnas.0904837106 | Cell-autonomous clock including Rev-erb/Ror | Fitted to knockout phenotypes. |
| **Relógio et al. 2011**, PLoS Comput Biol, doi:10.1371/journal.pcbi.1002309 | About 19 variables, Per/Cry and Rev-erb/Ror loops | **A good default:** compact, current biology, fitted to mouse data, and the parameter table is in the paper. |
| **Kim & Forger 2012**, Mol Syst Biol, doi:10.1038/msb.2012.62 | Detailed; protein ratios and sequestration | Use this if you care about how robust the period is to gene dosage. |
| **Korenčič et al. 2012**, PLoS One, doi:10.1371/journal.pone.0046835 | Gene regulatory network fitted to mouse-liver time courses | Parameters come from fitting to data. |

**My recommendation:** start with **Relógio 2011**, or **Leloup–Goldbeter 2003** if you want a model that is easy to find as SBML. Download the file from BioModels (search "circadian", filter to *Mus musculus* or *Homo sapiens*) and confirm it reproduces one figure from its paper before you change anything. A curated BioModels entry only means the file reproduces the paper, not that the biology is right. Published equations and files sometimes don't match, so trust the file only once it reproduces a figure.

## Where to get kinetic parameters

**BRENDA and SABIO-RK won't help much here.** Clock models are mostly about transcription, degradation, binding and transport, not enzyme kinetics, and **most published clock parameters were fitted, not measured.** Many models also copy parameters from earlier models, so trace each value back to its original source. Better places to look:

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
I couldn't search the web because WebSearch permission was denied. Everything below comes from what I already know about the field. The papers are standard and well known, but I couldn't check the database IDs or links. Please confirm them on BioModels before you rely on them.

## Short answer

**Yes, you can reuse a published model.** Several mammalian clock models are on **BioModels** (ebi.ac.uk/biomodels) as SBML files you can download and run. The choice depends on the level of detail you need:

| Your goal | Model to start from |
|---|---|
| Small and easy to analyse (phase response, entrainment) | **Becker-Weimann et al. 2004**, *Biophys J* – about 7 ODEs, one interlocked loop for Per/Cry and Bmal1 |
| A widely cited mechanistic model of medium size | **Leloup & Goldbeter 2003**, *PNAS* – about 16–19 ODEs covering PER, CRY, BMAL1, CLOCK and REV-ERBα, with constant-darkness and light–dark versions. I believe these are BIOMD0000000073 and BIOMD0000000078. |
| Detailed transcription with two loops (RORE and E-box), tuned to data | **Relógio et al. 2011**, *PLoS Comput Biol* ("Tuning the mammalian circadian clock: robust synergy of two loops") |
| Detailed mechanism with phosphorylation and predictions for mutants | **Forger & Peskin 2003**, *PNAS*. **Kim & Forger 2012**, *Mol Syst Biol*, adds stoichiometric balance of activator and repressor. |
| Tissue-specific gene timing fitted to mouse liver data | **Korenčič et al. 2012** (*PLoS ONE*) and **Korenčič et al. 2014** (*Sci Rep*) |

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
