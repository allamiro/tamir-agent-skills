#!/usr/bin/env python3
"""Protein sequence basics: composition, mass and hydropathy (standard library only).

  protein.py composition SEQ            residue counts and fractions
  protein.py mass SEQ [--mono]          peptide mass in daltons (average by default)
  protein.py gravy SEQ                  grand average of hydropathy (Kyte-Doolittle)
  protein.py window SEQ [--size 19]     sliding-window hydropathy, with windows above 1.6 flagged
  protein.py --selftest

Residue masses are from Expasy FindMod and hydropathy values from Expasy ProtScale (Kyte and
Doolittle 1982), both read 2026-10-14. Only the 20 standard amino acids are accepted: a letter
such as X, B, Z, J, U or O has no single mass or hydropathy value here, so it is refused rather
than guessed. The window threshold of 1.6 over 19 residues is the commonly quoted rule of thumb
for a membrane-spanning segment (unverified here); it is a screen, not a prediction method.
"""
import argparse
import re
import sys
from collections import Counter

AVG = {"A": 71.0788, "R": 156.1875, "N": 114.1038, "D": 115.0886, "C": 103.1388, "E": 129.1155,
       "Q": 128.1307, "G": 57.0519, "H": 137.1411, "I": 113.1594, "L": 113.1594, "K": 128.1741,
       "M": 131.1926, "F": 147.1766, "P": 97.1167, "S": 87.0782, "T": 101.1051, "W": 186.2132,
       "Y": 163.1760, "V": 99.1326}
MONO = {"A": 71.03711, "R": 156.10111, "N": 114.04293, "D": 115.02694, "C": 103.00919, "E": 129.04259,
        "Q": 128.05858, "G": 57.02146, "H": 137.05891, "I": 113.08406, "L": 113.08406, "K": 128.09496,
        "M": 131.04049, "F": 147.06841, "P": 97.05276, "S": 87.03203, "T": 101.04768, "W": 186.07931,
        "Y": 163.06333, "V": 99.06841}
WATER_AVG, WATER_MONO = 18.01524, 18.01056
KD = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2,
      "I": 4.5, "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9,
      "Y": -1.3, "V": 4.2}
TM_THRESHOLD = 1.6


def clean(seq):
    s = "".join(seq.split()).upper().rstrip("*")
    if not s:
        raise ValueError("empty sequence")
    bad = sorted({c for c in s if c not in AVG})
    if bad:
        raise ValueError("not a standard amino acid: %s (X, B, Z, J, U and O have no single mass or hydropathy value)"
                         % ", ".join(bad))
    return s


def composition(seq):
    s = clean(seq)
    counts = Counter(s)
    return {aa: (counts[aa], counts[aa] / len(s)) for aa in sorted(counts)}


def mass(seq, mono=False):
    """Mass of the free peptide: the sum of the residue masses plus one water."""
    s = clean(seq)
    table, water = (MONO, WATER_MONO) if mono else (AVG, WATER_AVG)
    return sum(table[c] for c in s) + water


def gravy(seq):
    s = clean(seq)
    return sum(KD[c] for c in s) / len(s)


def window_hydropathy(seq, size=19):
    """Mean hydropathy of each window of `size` residues, as (1-based start, mean)."""
    s = clean(seq)
    if size < 1 or size > len(s):
        raise ValueError("window size must be between 1 and the sequence length (%d)" % len(s))
    total = sum(KD[c] for c in s[:size])
    out = [(1, total / size)]
    for i in range(1, len(s) - size + 1):
        total += KD[s[i + size - 1]] - KD[s[i - 1]]
        out.append((i + 1, total / size))
    return out


def selftest():
    n = [0]

    def check(name, got, want, tol=None):
        n[0] += 1
        ok = (abs(got - want) <= tol) if tol is not None else got == want
        if not ok:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    def raises(name, fn):
        n[0] += 1
        try:
            fn()
        except ValueError:
            return
        raise AssertionError("%s: expected ValueError" % name)

    check("twenty residues in each table", (len(AVG), len(MONO), len(KD)), (20, 20, 20))
    check("same residues in each table", set(AVG) == set(MONO) == set(KD), True)
    check("Ile and Leu are isomers", AVG["I"] == AVG["L"] and MONO["I"] == MONO["L"], True)
    check("average mass exceeds monoisotopic for every residue", all(AVG[a] > MONO[a] for a in AVG), True)
    # Free glycine and diglycine, by hand: residues plus one water.
    check("glycine, average", mass("G"), 57.0519 + 18.01524, 1e-9)
    check("glycine is about 75.07 Da", mass("G"), 75.07, 0.005)
    check("glycine, monoisotopic", mass("G", mono=True), 57.02146 + 18.01056, 1e-9)
    check("diglycine is about 132.12 Da", mass("GG"), 132.119, 0.001)
    check("mass adds residue by residue", mass("AG") - mass("A"), AVG["G"], 1e-9)
    check("order does not change the mass", mass("ACDK"), mass("KDCA"), 1e-9)
    check("case and spaces ignored", mass("a c d k"), mass("ACDK"), 1e-9)
    check("a trailing stop is ignored", mass("ACDK*"), mass("ACDK"), 1e-9)
    # Every residue mass against its elemental formula (C, H, N, O, S), independent of the table.
    formulas = {"A": "C3H5NO", "R": "C6H12N4O", "N": "C4H6N2O2", "D": "C4H5NO3", "C": "C3H5NOS", "E": "C5H7NO3",
                "Q": "C5H8N2O2", "G": "C2H3NO", "H": "C6H7N3O", "I": "C6H11NO", "L": "C6H11NO", "K": "C6H12N2O",
                "M": "C5H9NOS", "F": "C9H9NO", "P": "C5H7NO", "S": "C3H5NO2", "T": "C4H7NO2", "W": "C11H10N2O",
                "Y": "C9H9NO2", "V": "C5H9NO"}
    mono_atoms = {"C": 12.0, "H": 1.00782503, "N": 14.0030740, "O": 15.9949146, "S": 31.9720707}
    avg_atoms = {"C": 12.0107, "H": 1.00794, "N": 14.0067, "O": 15.9994, "S": 32.065}

    def from_formula(formula, atoms):
        return sum(atoms[el] * int(num or 1) for el, num in re.findall(r"([A-Z])(\d*)", formula))

    for aa, formula in formulas.items():
        check("%s monoisotopic mass matches %s" % (aa, formula), MONO[aa], from_formula(formula, mono_atoms), 5e-4)
        check("%s average mass matches %s" % (aa, formula), AVG[aa], from_formula(formula, avg_atoms), 0.005)
    # Real peptides with published monoisotopic masses.
    check("angiotensin II DRVYIHPF, 1045.5345", mass("DRVYIHPF", mono=True), 1045.5345, 5e-4)
    check("bradykinin RPPGFSPFR, 1059.5614", mass("RPPGFSPFR", mono=True), 1059.5614, 5e-4)
    check("leu-enkephalin YGGFL, 555.2693", mass("YGGFL", mono=True), 555.2693, 5e-4)
    check("met-enkephalin YGGFM, 573.2257", mass("YGGFM", mono=True), 573.2257, 5e-4)
    check("Glu-fibrinopeptide B EGVNDNEEGFFSAR, 1569.6696", mass("EGVNDNEEGFFSAR", mono=True), 1569.6696, 5e-4)
    check("angiotensin II average mass is about 1046.2", mass("DRVYIHPF"), 1046.2, 0.05)
    # Hydropathy, by hand.
    check("GRAVY of AAAA", gravy("AAAA"), 1.8, 1e-12)
    check("GRAVY of AR = (1.8 - 4.5) / 2", gravy("AR"), -1.35, 1e-12)
    check("GRAVY of IL is the mean of 4.5 and 3.8", gravy("IL"), 4.15, 1e-12)
    w = window_hydropathy("IIIII", 3)
    check("three windows", len(w), 3)
    check("window mean", w[0][1], 4.5, 1e-12)
    w = window_hydropathy("AARRA", 2)
    check("sliding windows match direct means", [round(m, 6) for _, m in w], [1.8, (1.8 - 4.5) / 2, -4.5, (-4.5 + 1.8) / 2])
    seq = "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVV"
    inc = window_hydropathy(seq, 7)
    direct = [sum(KD[c] for c in seq[i:i + 7]) / 7 for i in range(len(seq) - 6)]
    check("incremental windows equal direct means", all(abs(a[1] - b) < 1e-9 for a, b in zip(inc, direct)), True)
    check("window count", len(inc), len(seq) - 6)
    comp = composition("AAGT")
    check("composition counts", {k: v[0] for k, v in comp.items()}, {"A": 2, "G": 1, "T": 1})
    check("composition fractions sum to 1", abs(sum(v[1] for v in comp.values()) - 1) < 1e-12, True)
    for bad in ("ACGX", "ACGB", "ACGU", "AC1G", "", "   ", "*"):
        raises("refuses %r" % bad, lambda b=bad: mass(b))
    raises("window larger than the sequence", lambda: window_hydropathy("ACD", 4))
    raises("window of zero", lambda: window_hydropathy("ACD", 0))
    print("protein.py self-test: %d checks passed" % n[0])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Protein composition, mass and hydropathy.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("composition").add_argument("seq")
    s = sub.add_parser("mass")
    s.add_argument("seq")
    s.add_argument("--mono", action="store_true")
    sub.add_parser("gravy").add_argument("seq")
    s = sub.add_parser("window")
    s.add_argument("seq")
    s.add_argument("--size", type=int, default=19)
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    try:
        if a.cmd == "composition":
            for aa, (count, frac) in composition(a.seq).items():
                print("%s %d %.3f" % (aa, count, frac))
        elif a.cmd == "mass":
            print("%.4f Da (%s)" % (mass(a.seq, a.mono), "monoisotopic" if a.mono else "average"))
        elif a.cmd == "gravy":
            print("GRAVY %.4f" % gravy(a.seq))
        elif a.cmd == "window":
            hits = 0
            for start, mean in window_hydropathy(a.seq, a.size):
                flag = " above %.1f" % TM_THRESHOLD if mean > TM_THRESHOLD else ""
                hits += bool(flag)
                print("%d-%d %.3f%s" % (start, start + a.size - 1, mean, flag))
            print("%d window(s) above %.1f: a screen for hydrophobic stretches, not a prediction" % (hits, TM_THRESHOLD))
        else:
            ap.print_help()
            return 2
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
