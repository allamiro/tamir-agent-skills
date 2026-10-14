# `protein-analysis` prompts

Describe a protein from its sequence with checkable numbers, and grade the evidence for claims about
its structure or function.

- **Give it:** the sequence and its source, whether it is the precursor or the mature form, the
  organism, and any measurement to compare with
- **Skill file:** [`skills/protein-analysis/SKILL.md`](../skills/protein-analysis/SKILL.md)
- **References:** [`amino-acids.md`](../skills/protein-analysis/references/amino-acids.md) and
  [`structure-and-function.md`](../skills/protein-analysis/references/structure-and-function.md)
- **Related:** [`sequence-alignment`](sequence-alignment.md), [`gene-finding-translation`](gene-finding-translation.md)

## 1. Peptide mass

> What is the monoisotopic mass of the peptide DRVYIHPF? Show how you got it and say whether you used average or monoisotopic residue masses.

A good answer: 1045.5345 daltons (angiotensin II), the sum of the residue masses plus one water,
with the monoisotopic table named.

## 2. Hydrophobicity

> Compute the GRAVY of this sequence and flag the windows that could be membrane-spanning: <paste>. Say how reliable that screen is.

A good answer: the mean hydropathy, the windows of 19 residues with a mean above about 1.6, and a
statement that this is a screen to confirm with a dedicated predictor.

## 3. A mass that does not match

> The measured mass of my protein is about 80 daltons higher than the mass I calculated. List the possible reasons without choosing one.

A good answer: a modification (a phosphate adds about 80 daltons, one candidate among several),
processing differences, a different isoform or precursor, or an error in the sequence used.

## 4. Leucine and isoleucine

> Why can't a mass measurement tell leucine from isoleucine, and how would I tell them apart?

A good answer: they have the same residue mass (isomers); other evidence is needed, such as
fragmentation patterns, the gene sequence, or the structure.

## 5. A predicted structure

> A predicted structure of my protein has low confidence in the first 40 residues. How should I treat the model there?

A good answer: as unreliable, often disordered; do not read side-chain contacts from it, and
base claims on the confident regions or on experimental data.

## 6. Function by similarity

> My protein is 45% identical to an enzyme of known function over its full length. Can I say it has the same function?

A good answer: as a hypothesis only; it depends on whether it is an ortholog or a paralog, on
conservation of the catalytic residues, and on any direct evidence.
