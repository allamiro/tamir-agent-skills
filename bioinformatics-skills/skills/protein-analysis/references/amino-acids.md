# Amino acids

The 20 standard amino acids. Residue masses are from Expasy FindMod and hydropathy values from
Expasy ProtScale (Kyte and Doolittle 1982), both read 2026-10-14. The table is generated from the
constants in `protein.py` (in the skill's scripts folder), which the script's self-test checks against each residue's
elemental formula.

| Letter | Code | Name | Average residue mass | Monoisotopic residue mass | Hydropathy (Kyte-Doolittle) |
|---|---|---|---|---|---|
| A | Ala | Alanine | 71.0788 | 71.03711 | +1.8 |
| R | Arg | Arginine | 156.1875 | 156.10111 | -4.5 |
| N | Asn | Asparagine | 114.1038 | 114.04293 | -3.5 |
| D | Asp | Aspartic acid | 115.0886 | 115.02694 | -3.5 |
| C | Cys | Cysteine | 103.1388 | 103.00919 | +2.5 |
| E | Glu | Glutamic acid | 129.1155 | 129.04259 | -3.5 |
| Q | Gln | Glutamine | 128.1307 | 128.05858 | -3.5 |
| G | Gly | Glycine | 57.0519 | 57.02146 | -0.4 |
| H | His | Histidine | 137.1411 | 137.05891 | -3.2 |
| I | Ile | Isoleucine | 113.1594 | 113.08406 | +4.5 |
| L | Leu | Leucine | 113.1594 | 113.08406 | +3.8 |
| K | Lys | Lysine | 128.1741 | 128.09496 | -3.9 |
| M | Met | Methionine | 131.1926 | 131.04049 | +1.9 |
| F | Phe | Phenylalanine | 147.1766 | 147.06841 | +2.8 |
| P | Pro | Proline | 97.1167 | 97.05276 | -1.6 |
| S | Ser | Serine | 87.0782 | 87.03203 | -0.8 |
| T | Thr | Threonine | 101.1051 | 101.04768 | -0.7 |
| W | Trp | Tryptophan | 186.2132 | 186.07931 | -0.9 |
| Y | Tyr | Tyrosine | 163.1760 | 163.06333 | -1.3 |
| V | Val | Valine | 99.1326 | 99.06841 | +4.2 |

Water: average 18.01524, monoisotopic 18.01056. The mass of a free peptide is the sum of its residue
masses plus one water.

## Not in the table

| Letter | Meaning |
|---|---|
| X | any or unknown residue |
| B | Asn or Asp |
| Z | Gln or Glu |
| J | Leu or Ile |
| U | selenocysteine |
| O | pyrrolysine |
| * | stop |

These have no single mass or hydropathy value here, and the script refuses them instead of guessing.

## Reading the numbers

- **Average mass** is the weighted mean over isotopes and suits bulk molecular weight. **Monoisotopic
  mass** is for the most abundant isotope of each element and is what high-resolution mass
  spectrometry resolves.
- Leucine and isoleucine have the same mass; mass cannot tell them apart.
- A positive hydropathy value means hydrophobic. GRAVY is the mean over the whole protein.
  A window mean above about 1.6 over 19 residues is the usual rule of thumb for a membrane-spanning
  segment (unverified here); treat it as a screen.
- A measured mass often differs from the calculated one because of processing (signal peptide
  removal), modifications, or a different isoform. Calculate from the mature sequence.

## Checks that use real peptides

The self-test reproduces published monoisotopic masses, recalled from memory and matched to four
decimals: angiotensin II DRVYIHPF 1045.5345, bradykinin RPPGFSPFR 1059.5614, leucine-enkephalin
YGGFL 555.2693, methionine-enkephalin YGGFM 573.2257 and Glu-fibrinopeptide B EGVNDNEEGFFSAR 1569.6696.
