# Genetic code

Source: NCBI genetic codes page, table 1 (the standard code), read 2026-10-14. T is shown for DNA;
read U for RNA.

| 1st \ 2nd | T | C | A | G |
|---|---|---|---|---|
| **T** | TTT F, TTC F, TTA L, TTG L | TCT S, TCC S, TCA S, TCG S | TAT Y, TAC Y, TAA stop, TAG stop | TGT C, TGC C, TGA stop, TGG W |
| **C** | CTT L, CTC L, CTA L, CTG L | CCT P, CCC P, CCA P, CCG P | CAT H, CAC H, CAA Q, CAG Q | CGT R, CGC R, CGA R, CGG R |
| **A** | ATT I, ATC I, ATA I, ATG M | ACT T, ACC T, ACA T, ACG T | AAT N, AAC N, AAA K, AAG K | AGT S, AGC S, AGA R, AGG R |
| **G** | GTT V, GTC V, GTA V, GTG V | GCT A, GCC A, GCA A, GCG A | GAT D, GAC D, GAA E, GAG E | GGT G, GGC G, GGA G, GGG G |

## Structure

| Codons per amino acid | Amino acids |
|---|---|
| 6 | Leu, Ser, Arg |
| 4 | Ala, Gly, Pro, Thr, Val |
| 3 | Ile |
| 2 | Phe, Tyr, His, Gln, Asn, Lys, Asp, Glu, Cys |
| 1 | Met, Trp |
| stop | TAA, TAG, TGA (3 codons) |

The counts total 64. The self-test checks this structure and the codon-by-codon table.

## Start codons

In table 1 the NCBI page marks ATG, and also TTG and CTG, as possible initiators. ATG is the
standard start. The script accepts alternative starts with `--starts`.

## Other codes

NCBI lists many translation tables. The page lists table 2 (vertebrate mitochondrial) as differing
from table 1 in these places: AGA and AGG are stops instead of Arg, ATA is Met instead of Ile, and
TGA is Trp instead of a stop. Other tables differ elsewhere (some bacteria, yeast mitochondria,
ciliates). Only table 1 is implemented here; for another organism read the NCBI page for its table
and check the organism's table number in its taxonomy record (VERIFY).

## One-letter codes

A Ala, R Arg, N Asn, D Asp, C Cys, Q Gln, E Glu, G Gly, H His, I Ile, L Leu, K Lys, M Met,
F Phe, P Pro, S Ser, T Thr, W Trp, Y Tyr, V Val. `*` is a stop and `X` an unknown residue.
