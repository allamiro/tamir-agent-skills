#!/usr/bin/env python3
"""Read-alignment arithmetic for sequencing pipelines (standard library only).

  ngs.py flags 99                              what the SAM FLAG bits mean
  ngs.py cigar 5S10M3D10M2S --pos 100          query and reference length, alignment end
  ngs.py coverage --reads 1000000 --length 150 --genome 5000000
  ngs.py reads-needed --depth 30 --length 150 --genome 5000000
  ngs.py --selftest

FLAG bits and CIGAR operations follow the SAM specification (hts-specs, read 2026-10-14).
Coverage uses the Lander-Waterman model: reads land independently and uniformly, so the number
of reads covering a base is about Poisson with mean C = N L / G. Real sequencing has bias in GC,
repeats and mappability, so treat these numbers as the best case.
"""
import argparse
import math
import re
import sys

FLAG_BITS = [
    (0x1, "template having multiple segments in sequencing"),
    (0x2, "each segment properly aligned according to the aligner"),
    (0x4, "segment unmapped"),
    (0x8, "next segment in the template unmapped"),
    (0x10, "SEQ being reverse complemented"),
    (0x20, "SEQ of the next segment in the template being reverse complemented"),
    (0x40, "the first segment in the template"),
    (0x80, "the last segment in the template"),
    (0x100, "secondary alignment"),
    (0x200, "not passing filters, such as platform/vendor quality controls"),
    (0x400, "PCR or optical duplicate"),
    (0x800, "supplementary alignment"),
]
# operation -> (consumes query, consumes reference)
CIGAR_OPS = {"M": (True, True), "I": (True, False), "D": (False, True), "N": (False, True),
             "S": (True, False), "H": (False, False), "P": (False, False), "=": (True, True), "X": (True, True)}
_CIGAR_TOKEN = re.compile(r"(\d+)([MIDNSHP=X])")


def decode_flag(flag):
    """Descriptions of every bit set in a SAM FLAG."""
    if not 0 <= flag <= 0xFFF:
        raise ValueError("FLAG must be between 0 and 4095")
    return [text for bit, text in FLAG_BITS if flag & bit]


def encode_flag(bits):
    return sum(bits)


def parse_cigar(cigar):
    """[(length, op), ...]. '*' (no alignment information) is returned as an empty list."""
    if cigar == "*":
        return []
    if not cigar or "".join("%d%s" % (int(n), op) for n, op in _CIGAR_TOKEN.findall(cigar)) != cigar:
        raise ValueError("not a valid CIGAR string: %r" % cigar)
    ops = [(int(n), op) for n, op in _CIGAR_TOKEN.findall(cigar)]
    if any(n == 0 for n, _ in ops):
        raise ValueError("CIGAR operation of length 0 in %r" % cigar)
    return ops


def cigar_lengths(cigar):
    """(bases of the read the alignment accounts for, reference bases it spans)."""
    ops = parse_cigar(cigar)
    query = sum(n for n, op in ops if CIGAR_OPS[op][0])
    ref = sum(n for n, op in ops if CIGAR_OPS[op][1])
    return query, ref


def alignment_end(pos, cigar):
    """1-based position of the last reference base the alignment covers, given 1-based POS."""
    if pos < 1:
        raise ValueError("POS is 1-based; 0 means unmapped")
    _, ref = cigar_lengths(cigar)
    if ref == 0:
        raise ValueError("this CIGAR consumes no reference bases")
    return pos + ref - 1


def mean_depth(reads, read_length, genome_length):
    """Lander-Waterman mean coverage C = N L / G."""
    if min(reads, read_length, genome_length) <= 0:
        raise ValueError("reads, read length and genome length must be positive")
    return reads * read_length / genome_length


def fraction_covered(depth):
    """Expected fraction of the genome covered by at least one read: 1 - e^(-C)."""
    if depth < 0:
        raise ValueError("depth cannot be negative")
    return 1.0 - math.exp(-depth)


def reads_needed(depth, read_length, genome_length):
    return math.ceil(depth * genome_length / read_length)


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

    # FLAGs. 99 = 1 + 2 + 32 + 64 and 147 = 1 + 2 + 16 + 128 are the usual proper-pair flags.
    check("flag 0 sets nothing", decode_flag(0), [])
    check("flag 4 is unmapped", decode_flag(4), ["segment unmapped"])
    check("flag 16 is reverse", decode_flag(16), ["SEQ being reverse complemented"])
    check("flag 99", len(decode_flag(99)), 4)
    check("flag 99 is paired, proper, mate reverse, first", [FLAG_BITS[i][0] for i in range(12) if 99 & FLAG_BITS[i][0]], [1, 2, 32, 64])
    check("flag 147", [b for b, _ in FLAG_BITS if 147 & b], [1, 2, 16, 128])
    check("flag 1024 is a duplicate", decode_flag(1024), ["PCR or optical duplicate"])
    check("flag 2048 is supplementary", decode_flag(2048), ["supplementary alignment"])
    check("twelve distinct bits", len({b for b, _ in FLAG_BITS}), 12)
    check("bits are powers of two", all(b & (b - 1) == 0 for b, _ in FLAG_BITS), True)
    for f in range(0, 4096):
        if encode_flag([b for b, _ in FLAG_BITS if f & b]) != f:
            raise AssertionError("flag %d does not round-trip" % f)
    n[0] += 1
    raises("flag out of range", lambda: decode_flag(4096))
    # CIGAR, hand-computed. M I S = X consume the query; M D N = X consume the reference.
    check("10M2I5M query", cigar_lengths("10M2I5M"), (17, 15))
    check("5S10M3D10M2S", cigar_lengths("5S10M3D10M2S"), (27, 23))
    check("hard clips consume neither", cigar_lengths("3H10M3H"), (10, 10))
    check("spliced read spans the intron", cigar_lengths("50M1000N50M"), (100, 1100))
    check("padding consumes neither", cigar_lengths("5M2P5M"), (10, 10))
    check("= and X count as M", cigar_lengths("4=1X5="), (10, 10))
    check("star means no information", parse_cigar("*"), [])
    check("end of a plain match", alignment_end(1, "100M"), 100)
    check("end with a deletion and clips", alignment_end(100, "5S10M3D10M2S"), 122)
    check("end of a spliced read", alignment_end(1000, "50M1000N50M"), 2099)
    check("one-base alignment ends where it starts", alignment_end(7, "1M"), 7)
    raises("unmapped POS", lambda: alignment_end(0, "10M"))
    raises("bad operation", lambda: parse_cigar("10Q"))
    raises("missing length", lambda: parse_cigar("M10"))
    raises("empty", lambda: parse_cigar(""))
    raises("zero length", lambda: parse_cigar("0M"))
    raises("no reference bases", lambda: alignment_end(5, "10I"))
    # Coverage.
    check("mean depth", mean_depth(1_000_000, 150, 5_000_000), 30.0)
    check("one-fold coverage leaves 1/e uncovered", fraction_covered(1.0), 1 - math.exp(-1), 1e-12)
    check("1 - 1/e", fraction_covered(1.0), 0.6321205588, 1e-9)
    check("no reads, no coverage", fraction_covered(0.0), 0.0)
    check("5-fold covers 99.3%", fraction_covered(5.0), 0.993262053, 1e-8)
    check("30-fold leaves almost nothing", 1 - fraction_covered(30.0) < 1e-12, True)
    check("reads needed", reads_needed(30, 150, 5_000_000), 1_000_000)
    check("reads needed rounds up", reads_needed(1, 150, 1000), 7)
    check("round trip depth", mean_depth(reads_needed(30, 150, 5_000_000), 150, 5_000_000), 30.0, 1e-9)
    raises("zero genome", lambda: mean_depth(10, 100, 0))
    raises("negative depth", lambda: fraction_covered(-1))
    print("ngs.py self-test: %d checks passed" % n[0])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-alignment arithmetic for sequencing pipelines.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("flags").add_argument("flag", type=int)
    s = sub.add_parser("cigar")
    s.add_argument("cigar")
    s.add_argument("--pos", type=int, default=0)
    s = sub.add_parser("coverage")
    s.add_argument("--reads", type=float, required=True)
    s.add_argument("--length", type=float, required=True)
    s.add_argument("--genome", type=float, required=True)
    s = sub.add_parser("reads-needed")
    s.add_argument("--depth", type=float, required=True)
    s.add_argument("--length", type=float, required=True)
    s.add_argument("--genome", type=float, required=True)
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    try:
        if a.cmd == "flags":
            bits = decode_flag(a.flag)
            print("FLAG %d (0x%x)%s" % (a.flag, a.flag, ": no bits set" if not bits else ""))
            for text in bits:
                print("  - " + text)
            if not a.flag & 0x4:
                print("  (bit 0x4 is clear: the segment is mapped)")
        elif a.cmd == "cigar":
            q, r = cigar_lengths(a.cigar)
            print("accounts for %d read bases, spans %d reference bases" % (q, r))
            if a.pos:
                print("POS %d (1-based) to end %d" % (a.pos, alignment_end(a.pos, a.cigar)))
        elif a.cmd == "coverage":
            c = mean_depth(a.reads, a.length, a.genome)
            print("mean depth %.2fx; expected fraction covered at least once %.4f (best case)" % (c, fraction_covered(c)))
        elif a.cmd == "reads-needed":
            print("%d reads of %g bases for %.1fx over %g bases" % (reads_needed(a.depth, a.length, a.genome), a.length, a.depth, a.genome))
        else:
            ap.print_help()
            return 2
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
