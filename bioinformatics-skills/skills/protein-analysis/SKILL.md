---
name: protein-analysis
description: Analyses protein sequences and the evidence behind claims about protein structure and function, covering composition, mass, hydropathy, sequence features, domains and motifs, experimental and predicted structure, and inferring function by similarity. Use for "what is the mass of this peptide", "is this protein hydrophobic or a membrane protein", "compute amino acid composition", "what does this domain mean", "how reliable is a predicted structure", "can I infer function from similarity". Use sequence-alignment to compare proteins, gene-finding-translation to get a protein from DNA, and bioinformatics-review to audit functional claims.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Protein analysis

## Purpose and activation

Describe a protein from its sequence with numbers that can be checked, and grade the evidence for
any claim about its structure or function. A calculation from sequence is exact; a statement about
what the protein does is an inference, and the skill keeps the two apart. Activate when the user has
a protein or peptide sequence, a mass spectrum result, or a claim about structure or function.

## Required inputs

The sequence and its source (accession with version, isoform, whether it is the precursor or the
mature form); the organism; whether modifications or processing are expected; the question (mass,
composition, hydrophobicity, structure, function); and any experimental data to compare with.

## Workflow

1. **Get the right sequence.** Record the accession and version, the isoform, and whether signal
   peptides or propeptides are removed in the mature protein (`biological-databases`).
2. **Clean it.** Only the 20 standard letters have a mass and a hydropathy value. Letters such as
   X, B, Z, J, U and O are refused by the script; decide what each means before going on.
3. **Compute.** `python3 scripts/protein.py composition SEQ`, `mass SEQ` (add `--mono` for
   monoisotopic), `gravy SEQ`, and `window SEQ --size 19` for hydrophobic stretches.
4. **Compare with measurement.** A mass-spectrometry value differs from the calculated mass if the
   protein is processed or modified; list the likely reasons before concluding.
5. **Look for features** from curated resources, such as domains, motifs, signal peptides and
   transmembrane regions (`references/structure-and-function.md`), and note which are experimental
   and which predicted.
6. **Structure.** Use experimentally determined structures where they exist and state method and
   resolution; treat a predicted structure as a model with a per-residue confidence score.
7. **Function by similarity.** Align to characterised proteins (`sequence-alignment`), state the
   identity and coverage, and say whether the relative is an ortholog or a paralog.
8. **Grade the claim** with the evidence ladder and write it as a prediction unless there is direct
   evidence.

## Decision framework

| Question | Answer |
|---|---|
| Mass of a peptide | Sum of residue masses plus one water; average or monoisotopic by instrument |
| Is it hydrophobic | GRAVY for the whole protein; windows for local stretches |
| Could it span a membrane | A window mean above about 1.6 over 19 residues is a screen; confirm with a dedicated predictor |
| Leucine or isoleucine | Cannot be told apart by mass |
| Domain match in a database | Names a family relationship; the function may differ in your protein |
| Predicted structure | A model; check its confidence, and do not read side-chain detail from low-confidence regions |
| Similar sequence, known function | A hypothesis; stronger for orthologs with high identity over the whole length |

## Implementation guidance

- Residue masses and hydropathy values are in `references/amino-acids.md`, generated from the
  script's constants. The self-test recomputes every residue mass from its elemental formula.
- Calculate from the mature chain when a signal peptide or propeptide is removed.
- For charge or isoelectric point the answer depends on the pKa set chosen; the script does not
  calculate it. Use a tool that states its pKa values.
- Peptide masses in spectra are often seen as m/z with a charge state; convert before comparing.

## Failure and edge cases

- **Precursor versus mature** sequence giving the wrong mass.
- **Post-translational modifications** and disulfide bonds shifting the measured mass.
- **Average mass compared with monoisotopic mass.**
- **X and ambiguous residues** silently treated as a standard one.
- **Whole-protein GRAVY** hiding a single membrane segment.
- **Function transferred** from a distant relative or from a family that holds many functions.
- **Paralog mistaken for ortholog.**
- **Confidence of a predicted structure** ignored, especially in disordered regions.
- **Isoforms** differing in the very region of interest.

## Validation

- `python3 scripts/protein.py --selftest` must pass.
- Hand check: glycine is 75.07 daltons as a free amino acid; diglycine is 132.12.
- Hand check: DRVYIHPF (angiotensin II) has monoisotopic mass 1045.5345.
- Hand check: GRAVY of AR is (1.8 - 4.5) / 2 = -1.35.
- Falsifier: the calculated mass of a well-characterised protein does not match its published mass
  once processing is accounted for.

## Expected output

The sequence and its source, composition, mass (type stated), hydropathy and any flagged windows,
features with their evidence type, structure source and confidence, the function claim at its
evidence level, and what would settle it.

## Sources and confidence

- Residue masses, Expasy FindMod, and Kyte and Doolittle hydropathy values, Expasy ProtScale, both
  read 2026-10-14; checked against elemental formulas in the self-test. Published peptide masses used
  in the self-test were recalled from memory and agree with the table to four decimals; VERIFY
- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: ch. 11.5 (amino acids, protein folding and
  interaction, experimental techniques for structure determination, structure overview) and ch. 14
  (proteomics, protein identification): section titles only, from the table of contents
- The 1.6 and 19-residue rule of thumb, domain resources, prediction confidence scores: general
  knowledge, VERIFY against the resource's documentation
- Not covered: structure prediction or docking, molecular dynamics, protein design, isoelectric point
