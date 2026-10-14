# `protein-analysis`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> What is the monoisotopic mass of the peptide DRVYIHPF? Show how you got it and say whether you used average or monoisotopic residue masses.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 817 | 1,057 |
| Input tokens read across all turns (including cached context) | 30,363 | 35,652 |
| Extra input tokens when the skill is installed | | +5,290 |
| Cost, US dollars at list price | 0.076 | 0.123 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 220 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**Monoisotopic mass of DRVYIHPF = 1045.5345 Da** (neutral peptide). This sequence is angiotensin II.

I used **monoisotopic** residue masses, meaning each residue is built from the most abundant isotope of each element (¹²C, ¹H, ¹⁴N, ¹⁶O). I did not use average residue masses.

### Calculation

A peptide's mass is the sum of its residue masses plus one water (H₂O) for the free N-terminal H and C-terminal OH.

| Residue | Monoisotopic residue mass (Da) | Running total |
|---|---|---|
| D (Asp) | 115.02694 | 115.02694 |
| R (Arg) | 156.10111 | 271.12805 |
| V (Val) | 99.06841 | 370.19646 |
| Y (Tyr) | 163.06333 | 533.25979 |
| I (Ile) | 113.08406 | 646.34385 |
| H (His) | 137.05891 | 783.40276 |
| P (Pro) | 97.05276 | 880.45552 |
| F (Phe) | 147.06841 | 1027.52393 |
| + H₂O | 18.01056 | **1045.53449** |

Molecular formula: C₅₀H₇₁N₁₃O₁₂.

### Related values
- **[M+H]⁺** = 1045.5345 + 1.00728 (proton) = **1046.5418**, which is the singly charged ion you'd see by mass spectrometry.
- **[M+2H]²⁺** = (1045.5345 + 2 × 1.00728) / 2 = **523.7745**.
- **Average mass**, from average residue masses, is about **1046.19 Da**. It is about 0.65 Da higher because it includes the natural ¹³C and other heavy isotopes. Don't use it to match high-resolution MS peaks.

This assumes free termini and no modifications, such as N-terminal acetylation or C-terminal amidation.
````

## Answer without the skill (excerpt)

````text
The monoisotopic mass of DRVYIHPF (angiotensin II) is **1045.5345 Da** for the neutral molecule. I used monoisotopic residue masses throughout, not average masses.

**Method:** I added the monoisotopic residue mass of each amino acid, then added one water for the free N-terminus (H) and C-terminus (OH).

| Residue | Monoisotopic residue mass (Da) | Running total |
|---|---|---|
| D (Asp) | 115.02694 | 115.02694 |
| R (Arg) | 156.10111 | 271.12805 |
| V (Val) | 99.06841 | 370.19646 |
| Y (Tyr) | 163.06333 | 533.25979 |
| I (Ile) | 113.08406 | 646.34385 |
| H (His) | 137.05891 | 783.40276 |
| P (Pro) | 97.05276 | 880.45552 |
| F (Phe) | 147.06841 | 1027.52393 |
| + H₂O (termini) | 18.01056 | **1045.53449** |

- **Monoisotopic mass (neutral, M):** 1045.5345 Da
- **Elemental formula:** C₅₀H₇₁N₁₃O₁₂
- **Common ions:** add a proton (1.00728) to get [M+H]⁺ ≈ 1046.5418 m/z. [M+2H]²⁺ ≈ 523.7745 m/z.

For comparison, the average mass of the same peptide is about 1046.19 Da. That figure is the one you'd use for weighing out material, not for high-resolution mass spectrometry.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
