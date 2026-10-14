#!/usr/bin/env python3
"""DNA basics: reverse complement, GC, k-mers, translation and open reading frames (standard library only).

  genecode.py revcomp SEQ
  genecode.py gc SEQ [--window W]               GC fraction, and GC skew (G-C)/(G+C)
  genecode.py kmers SEQ --k K [--top N]         word occurrences
  genecode.py translate SEQ [--frame 1|2|3] [--strand +|-] [--to-stop]
  genecode.py orfs SEQ [--min-aa 30] [--starts ATG,TTG,CTG]    also prints the chance level at this sequence's GC
  genecode.py chance --gc 0.7 --codons 100                     how often chance leaves a frame open
  genecode.py --selftest

SEQ is a sequence string or the path of a file (FASTA headers are skipped). Only the standard
genetic code (NCBI translation table 1) is built in. An open reading frame is a start codon
followed by codons up to a stop in the same frame. That is a candidate coding region, not a gene:
it ignores introns, overlapping genes, non-standard codes and whether the sequence is expressed.
"""
import argparse
import os
import random
import sys
from collections import Counter

# NCBI translation table 1, codons in TCAG order for each of the three positions.
BASES = "TCAG"
AMINO = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODON_TABLE = {a + b + c: AMINO[16 * i + 4 * j + k]
               for i, a in enumerate(BASES) for j, b in enumerate(BASES) for k, c in enumerate(BASES)}
STOPS = {c for c, aa in CODON_TABLE.items() if aa == "*"}

# IUPAC complement: R=AG, Y=CT, K=GT, M=AC, B=CGT, V=ACG, D=AGT, H=ACT, S, W and N are self-complementary.
_COMP = dict(zip("ACGTRYKMBVDHSWN", "TGCAYRMKVBHDSWN"))


def clean(seq):
    return "".join(seq.split()).upper().replace("U", "T")


def revcomp(seq):
    seq = clean(seq)
    try:
        return "".join(_COMP[ch] for ch in reversed(seq))
    except KeyError as exc:
        raise ValueError("character %r is not an IUPAC nucleotide code" % exc.args[0])


def gc_fraction(seq):
    """GC fraction among unambiguous A, C, G, T bases. N and other codes are left out of the count."""
    seq = clean(seq)
    acgt = [ch for ch in seq if ch in "ACGT"]
    if not acgt:
        raise ValueError("no A, C, G or T in the sequence")
    return sum(ch in "GC" for ch in acgt) / len(acgt)


def gc_skew(seq):
    seq = clean(seq)
    g, c = seq.count("G"), seq.count("C")
    if g + c == 0:
        raise ValueError("no G or C in the sequence")
    return (g - c) / (g + c)


def kmer_counts(seq, k):
    seq = clean(seq)
    if k < 1:
        raise ValueError("k must be at least 1")
    return Counter(seq[i:i + k] for i in range(len(seq) - k + 1))


def translate(seq, frame=1, to_stop=False):
    """Translate from base `frame` (1, 2 or 3) of the given strand. Unknown codons become X."""
    if frame not in (1, 2, 3):
        raise ValueError("frame must be 1, 2 or 3")
    seq = clean(seq)
    out = []
    for i in range(frame - 1, len(seq) - 2, 3):
        aa = CODON_TABLE.get(seq[i:i + 3], "X")
        if to_stop and aa == "*":
            break
        out.append(aa)
    return "".join(out)


def stop_probability(gc):
    """Chance that a codon of independent random bases is a stop (TAA, TAG or TGA), given the GC fraction.
    A and T each have probability (1 - gc) / 2, C and G each gc / 2."""
    if not 0 <= gc <= 1:
        raise ValueError("gc must be between 0 and 1")
    a, g = (1 - gc) / 2, gc / 2
    return a * a * a + 2 * a * a * g  # TAA = a a a; TAG = a a g; TGA = a g a


def open_frame_probability(gc, codons):
    """Chance that `codons` consecutive codons of random sequence contain no stop codon."""
    if codons < 0:
        raise ValueError("codons cannot be negative")
    return (1 - stop_probability(gc)) ** codons


def chance_note(gc, min_aa):
    """One line saying how often a random ATG at this GC content is followed by min_aa - 1 codons with no stop."""
    return ("chance level at %.0f%% GC, if bases were independent: an ATG is followed by %d or more codons with no stop in %.1f%% of random cases"
            % (100 * gc, max(min_aa - 1, 0), 100 * open_frame_probability(gc, max(min_aa - 1, 0))))


def find_orfs(seq, min_aa=30, starts=("ATG",), both_strands=True):
    """ORFs as (strand, start, end, protein). Start and end are 1-based closed coordinates on the
    given forward sequence and include the stop codon; start < end whichever strand the ORF is on.
    Only ORFs that reach a stop codon are reported. Nested ORFs from later start codons in the
    same frame are not listed: each ORF begins at the first start codon after the previous stop.
    The protein is the literal translation, so an alternative start such as TTG shows as L; in a
    cell an initiator codon is read as methionine (VERIFY against a textbook before relying on it)."""
    seq = clean(seq)
    starts = set(s.upper().replace("U", "T") for s in starts)
    n = len(seq)
    found = []
    strands = [("+", seq)] + ([("-", revcomp(seq))] if both_strands else [])
    for strand, s in strands:
        for frame in range(3):
            i, open_at = frame, None
            while i + 3 <= n:
                codon = s[i:i + 3]
                if open_at is None and codon in starts:
                    open_at = i
                elif open_at is not None and codon in STOPS:
                    protein = translate(s[open_at:i], 1)
                    if len(protein) >= min_aa:
                        a, b = open_at + 1, i + 3
                        if strand == "-":
                            a, b = n - b + 1, n - a + 1
                        found.append((strand, a, b, protein))
                    open_at = None
                i += 3
    return sorted(found, key=lambda o: (o[1], o[2], o[0]))


# The full table as printed by NCBI (read 2026-10-14), used only to check the compact string above.
_NCBI_TABLE_1 = """
TTT F TCT S TAT Y TGT C   TTC F TCC S TAC Y TGC C   TTA L TCA S TAA * TGA *   TTG L TCG S TAG * TGG W
CTT L CCT P CAT H CGT R   CTC L CCC P CAC H CGC R   CTA L CCA P CAA Q CGA R   CTG L CCG P CAG Q CGG R
ATT I ACT T AAT N AGT S   ATC I ACC T AAC N AGC S   ATA I ACA T AAA K AGA R   ATG M ACG T AAG K AGG R
GTT V GCT A GAT D GGT G   GTC V GCC A GAC D GGC G   GTA V GCA A GAA E GGA G   GTG V GCG A GAG E GGG G
"""


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

    # The compact code string against the full table fetched from NCBI.
    tokens = _NCBI_TABLE_1.split()
    ncbi = dict(zip(tokens[0::2], tokens[1::2]))
    check("NCBI fixture has 64 codons", len(ncbi), 64)
    check("compact string equals the NCBI table, codon by codon", CODON_TABLE, ncbi)
    # Structure that does not depend on either copy: degeneracy classes of the standard code.
    per_aa = Counter(CODON_TABLE.values())
    check("64 codons", sum(per_aa.values()), 64)
    check("three stops", sorted(STOPS), ["TAA", "TAG", "TGA"])
    check("Met and Trp have one codon", (per_aa["M"], per_aa["W"]), (1, 1))
    check("Leu, Ser, Arg have six", (per_aa["L"], per_aa["S"], per_aa["R"]), (6, 6, 6))
    check("Ile has three", per_aa["I"], 3)
    check("fourfold amino acids", sorted(a for a, c in per_aa.items() if c == 4), ["A", "G", "P", "T", "V"])
    check("twofold amino acids", sorted(a for a, c in per_aa.items() if c == 2), sorted("FYHQNKDEC"))
    check("20 amino acids and a stop", len(per_aa), 21)
    # Reverse complement.
    check("revcomp", revcomp("ATGC"), "GCAT")
    check("revcomp lower case and U", revcomp("auGc"), "GCAT")
    check("revcomp is an involution on all IUPAC codes", revcomp(revcomp("ACGTRYKMBVDHSWN")), "ACGTRYKMBVDHSWN")
    # Every IUPAC code against an independent definition: the code whose base set is the complement.
    sets = {"R": "AG", "Y": "CT", "K": "GT", "M": "AC", "B": "CGT", "V": "ACG", "D": "AGT", "H": "ACT",
            "S": "CG", "W": "AT", "N": "ACGT", "A": "A", "C": "C", "G": "G", "T": "T"}
    base_comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    by_set = {frozenset(v): k for k, v in sets.items()}
    for code, bases in sets.items():
        want = by_set[frozenset(base_comp[b] for b in bases)]
        check("complement of IUPAC code %s is %s" % (code, want), revcomp(code), want)
    check("revcomp of R is Y", revcomp("R"), "Y")
    check("revcomp of B is V", revcomp("B"), "V")
    raises("revcomp bad character", lambda: revcomp("ACGX"))
    # GC and skew.
    check("gc fraction", gc_fraction("AATTGC"), 1 / 3)
    check("gc ignores N", gc_fraction("GCNN"), 1.0)
    check("gc skew", gc_skew("GGGC"), 0.5)
    raises("gc of nothing", lambda: gc_fraction("NNN"))
    check("kmer counts", kmer_counts("ACACA", 2), Counter({"AC": 2, "CA": 2}))
    check("kmer counts overlapping", kmer_counts("AAAA", 2), Counter({"AA": 3}))
    # Translation.
    check("translate", translate("ATGAAATAG"), "MK*")
    check("translate to stop", translate("ATGAAATAGGGG", to_stop=True), "MK")
    check("translate frame 2", translate("CATGAAATAG", frame=2), "MK*")
    check("translate drops a partial codon", translate("ATGAA"), "M")
    check("translate unknown codon", translate("ATGNNNTGG"), "MXW")
    raises("translate bad frame", lambda: translate("ATG", frame=4))
    # Chance of a stop codon, by hand: TAA + TAG + TGA with A = T = (1 - gc) / 2 and C = G = gc / 2.
    check("stop probability at 50% GC is 3/64", stop_probability(0.5), 3 / 64, 1e-12)
    check("stop probability at 70% GC", stop_probability(0.7), 0.15 ** 3 + 2 * 0.15 * 0.15 * 0.35, 1e-12)
    check("0.70 GC value is 0.019125", stop_probability(0.7), 0.019125, 1e-9)
    check("stop probability at 30% GC", stop_probability(0.3), 0.079625, 1e-9)
    check("all A/T: only TAA is possible, 1/8", stop_probability(0.0), 0.125, 1e-12)
    check("all G/C: no stop is possible", stop_probability(1.0), 0.0, 1e-12)
    check("stops get rarer as GC rises", all(stop_probability(g / 10) > stop_probability((g + 1) / 10) for g in range(10)), True)
    check("open frame, 30 codons at 50% GC", open_frame_probability(0.5, 30), (61 / 64) ** 30, 1e-12)
    check("open frame, 100 codons at 70% GC is about 14.5%", open_frame_probability(0.7, 100), 0.145, 1e-3)
    check("zero codons are always open", open_frame_probability(0.4, 0), 1.0)
    # The formula against an independent simulation: random sequence at 60% GC, stops counted in frame.
    rng = random.Random(11)
    gc_target, bases = 0.6, []
    for _ in range(300_000):
        r = rng.random()
        bases.append("G" if r < gc_target / 2 else "C" if r < gc_target else "A" if r < gc_target + (1 - gc_target) / 2 else "T")
    codons = ["".join(bases[i:i + 3]) for i in range(0, len(bases) - 2, 3)]
    observed = sum(c in STOPS for c in codons) / len(codons)
    check("simulated stop-codon rate matches the formula at 60% GC", observed, stop_probability(0.6), 0.003)
    raises("bad gc", lambda: stop_probability(1.5))
    raises("negative codons", lambda: open_frame_probability(0.5, -1))
    check("chance note mentions the percentage", "%.1f%%" % (100 * open_frame_probability(0.5, 29)) in chance_note(0.5, 30), True)
    # ORFs: ATG AAA TAG sits at 1-based 3-11 in CCATGAAATAGCC.
    seq = "CCATGAAATAGCC"
    check("orf on the forward strand", find_orfs(seq, min_aa=2), [("+", 3, 11, "MK")])
    flipped = revcomp(seq)
    check("orf on the reverse strand maps back to forward coordinates",
          find_orfs(flipped, min_aa=2), [("-", 3, 11, "MK")])
    # An asymmetric case: the ORF is 2-10 on the forward strand of a 14-base sequence, so on the
    # reverse complement it must come back as 5-13, not as 2-10.
    asym = "CATGAAATAGCCCC"
    check("asymmetric forward ORF", find_orfs(asym, min_aa=2), [("+", 2, 10, "MK")])
    check("asymmetric reverse ORF maps to 5-13", find_orfs(revcomp(asym), min_aa=2), [("-", 5, 13, "MK")])
    check("min length filters", find_orfs(seq, min_aa=3), [])
    check("no stop, no ORF", find_orfs("CCATGAAACC", min_aa=1), [])
    check("alternative start codon", find_orfs("CCTTGAAATAGCC", min_aa=2, starts=("TTG",)), [("+", 3, 11, "LK")])
    check("the default start is ATG only", find_orfs("CCTTGAAATAGCC", min_aa=2), [])
    check("both strands off", find_orfs(flipped, min_aa=2, both_strands=False), [])
    check("two ORFs one after another in a frame", len(find_orfs("ATGAAATAGATGCCCTGA", min_aa=2)), 2)
    # An ORF coordinate on '-' must read back to the same protein from the forward sequence.
    s = "GGATGGCCAAATGACC"
    for strand, a, b, protein in find_orfs(s, min_aa=1):
        piece = s[a - 1:b]
        piece = piece if strand == "+" else revcomp(piece)
        check("orf %s %d-%d reads back" % (strand, a, b), translate(piece, to_stop=True), protein)
    print("genecode.py self-test: %d checks passed" % n[0])


def read_seq(arg):
    if os.path.isfile(arg):
        with open(arg, encoding="utf-8") as fh:
            return "".join(ln.strip() for ln in fh if not ln.startswith(">"))
    return arg


def main(argv=None):
    ap = argparse.ArgumentParser(description="DNA basics, translation and ORFs.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("revcomp").add_argument("seq")
    s = sub.add_parser("gc")
    s.add_argument("seq")
    s.add_argument("--window", type=int, default=0)
    s = sub.add_parser("kmers")
    s.add_argument("seq")
    s.add_argument("--k", type=int, required=True)
    s.add_argument("--top", type=int, default=10)
    s = sub.add_parser("translate")
    s.add_argument("seq")
    s.add_argument("--frame", type=int, default=1, choices=(1, 2, 3))
    s.add_argument("--strand", choices=("+", "-"), default="+")
    s.add_argument("--to-stop", action="store_true")
    s = sub.add_parser("orfs")
    s.add_argument("seq")
    s.add_argument("--min-aa", type=int, default=30)
    s.add_argument("--starts", default="ATG")
    s = sub.add_parser("chance")
    s.add_argument("--gc", type=float, required=True)
    s.add_argument("--codons", type=int, required=True)
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    try:
        if a.cmd == "revcomp":
            print(revcomp(read_seq(a.seq)))
        elif a.cmd == "gc":
            seq = clean(read_seq(a.seq))
            print("GC %.4f   skew %.4f" % (gc_fraction(seq), gc_skew(seq)))
            if a.window:
                for i in range(0, max(len(seq) - a.window + 1, 1), a.window):
                    print("%d-%d  GC %.4f" % (i + 1, min(i + a.window, len(seq)), gc_fraction(seq[i:i + a.window])))
        elif a.cmd == "kmers":
            for word, count in kmer_counts(read_seq(a.seq), a.k).most_common(a.top):
                print("%s %d" % (word, count))
        elif a.cmd == "translate":
            seq = read_seq(a.seq)
            print(translate(seq if a.strand == "+" else revcomp(seq), a.frame, a.to_stop))
        elif a.cmd == "orfs":
            orfs = find_orfs(read_seq(a.seq), a.min_aa, tuple(a.starts.split(",")))
            for strand, start, end, protein in orfs:
                print("%s %d-%d %d aa  %s" % (strand, start, end, len(protein), protein))
            print("%d ORF(s) of at least %d aa (candidates, not gene calls)" % (len(orfs), a.min_aa))
            seq = clean(read_seq(a.seq))
            if any(ch in "ACGT" for ch in seq):
                print(chance_note(gc_fraction(seq), a.min_aa))
        elif a.cmd == "chance":
            p = stop_probability(a.gc)
            print("at %.0f%% GC: P(codon is a stop) = %.4f; mean codons to a stop %s; P(%d codons with no stop) = %.4f" % (
                100 * a.gc, p, "%.1f" % (1 / p) if p else "unbounded", a.codons, open_frame_probability(a.gc, a.codons)))
        else:
            ap.print_help()
            return 2
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
