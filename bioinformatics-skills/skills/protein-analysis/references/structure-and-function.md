# Structure and function

General knowledge; VERIFY against the resource's documentation. Resource names are examples.

## Levels of structure

| Level | Meaning |
|---|---|
| Primary | The amino acid sequence |
| Secondary | Local regular shapes such as helices and strands |
| Tertiary | The three-dimensional fold of one chain |
| Quaternary | Assembly of several chains |

Sequence determines structure, but a sequence alone does not give the structure without a method,
and the method has error.

## Evidence for structure

| Source | What it gives | Caution |
|---|---|---|
| Experimental structure (X-ray crystallography, NMR, cryo-electron microscopy) | Atomic coordinates with resolution or quality metrics | Conditions may differ from the cell; flexible regions are often missing |
| Homology model | Structure built on a similar solved protein | Only as good as the template and alignment |
| Predicted structure | A model with a per-residue confidence score | Low-confidence regions, often disordered ones, are not reliable |

Check method, resolution and the date of the entry. Record the entry's identifier and version.

## Evidence for function

| Evidence | Strength |
|---|---|
| Direct experiment on this protein | Strong |
| Experiment on a close ortholog | Good, if identity and coverage are high |
| Domain or motif match | Suggests a family; function may differ |
| Similarity to an annotated protein that was itself inferred | Weak; errors propagate |
| Gene neighbourhood, co-expression | Hint only |

Annotation databases often record the evidence type; use it.

## Domains, motifs and signals

- A domain is a conserved region that folds and functions semi-independently; a protein can have
  several.
- Motifs are short patterns; they match by chance, so a short motif hit needs a context.
- Signal peptides and transmembrane segments are predicted from composition and pattern; the
  hydropathy window in `protein.py` is a crude screen for the latter.
- Use curated domain resources and read the e-values or scores they report.

## Orthologs and paralogs

Orthologs arose by speciation and usually keep function; paralogs arose by duplication and often
diverge. A best hit in another species may be a paralog. Tree-based or reciprocal-best-hit methods
reduce, but do not remove, the error (`phylogenetics`).

## From sequence to measurement

| Measurement | Compare with |
|---|---|
| Intact mass | Mass of the mature chain, with modifications considered |
| Peptide masses after digestion | Masses of the digestion products; missed cleavages and modifications change them |
| Size on a gel | Rough only; modifications and shape change migration |
| Charge or pI | Depends on the pKa set; modifications shift it |

The source's proteomics chapter covers two-dimensional gels, chromatography, protein identification,
isotope-coded affinity tags and protein microarrays (section titles only).
