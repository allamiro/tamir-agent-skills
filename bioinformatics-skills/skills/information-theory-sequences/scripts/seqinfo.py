#!/usr/bin/env python3
"""Information measures for symbol sequences (standard library only).

  seqinfo.py bits N                 variety of N equally likely kinds, log2(N)
  seqinfo.py entropy SEQ [--k K]    Shannon entropy of the K-mer frequencies, in bits
  seqinfo.py hill SEQ               diversity numbers D0, D1, D2 of the symbol frequencies
  seqinfo.py ncd SEQ1 SEQ2          normalized compression distance (zlib)
  seqinfo.py mi SEQ1 SEQ2           mutual information of two equal-length columns, in bits
  seqinfo.py --selftest

SEQ is a sequence string or the path of a file. In a file, lines starting with '>' are
skipped and whitespace is removed. Estimates are plug-in estimates from the observed
frequencies: they are biased low for short sequences and large K.
"""
import argparse
import math
import os
import sys
import zlib
from collections import Counter


def variety(n):
    """log2 of the number of equally likely kinds: the bits needed to name one."""
    if n < 1:
        raise ValueError("need at least one kind")
    return math.log2(n)


def shannon(probs, base=2.0):
    """-sum p log p. Probabilities must be non-negative and sum to 1."""
    probs = list(probs)
    if any(p < 0 for p in probs):
        raise ValueError("negative probability")
    if abs(sum(probs) - 1.0) > 1e-9:
        raise ValueError("probabilities sum to %r, not 1" % sum(probs))
    return -sum(p * math.log(p, base) for p in probs if p > 0) + 0.0


def word_freqs(seq, k=1):
    """Relative frequencies of overlapping k-mers, and how many k-mers there were."""
    seq = seq.upper()
    words = [seq[i:i + k] for i in range(len(seq) - k + 1)]
    n = len(words)
    return {w: c / n for w, c in Counter(words).items()}, n


def entropy(seq, k=1):
    freqs, n = word_freqs(seq, k)
    if n == 0:
        raise ValueError("sequence shorter than k")
    return shannon(freqs.values())


def hill(probs):
    """D0 = number of kinds, D1 = exp(Shannon index in nats), D2 = 1 / sum p^2."""
    probs = [p for p in probs if p > 0]
    h_nats = shannon(probs, base=math.e)
    return float(len(probs)), math.exp(h_nats), 1.0 / sum(p * p for p in probs)


def kl_divergence(p, q):
    """Relative entropy of p from q in bits. Needs q > 0 wherever p > 0."""
    total = 0.0
    for pi, qi in zip(p, q):
        if pi > 0:
            if qi <= 0:
                raise ValueError("q is zero where p is not")
            total += pi * math.log2(pi / qi)
    return total


def motif_column_information(column, alphabet="ACGT"):
    """log2(alphabet size) minus the entropy of the column: bits of conservation."""
    freqs, n = word_freqs(column, 1)
    if n == 0:
        raise ValueError("empty column")
    return math.log2(len(alphabet)) - shannon(freqs.values())


def ncd(x, y):
    """Normalized compression distance with zlib at level 9, symmetric by construction."""
    bx, by = x.encode(), y.encode()
    cx, cy = len(zlib.compress(bx, 9)), len(zlib.compress(by, 9))
    cxy = min(len(zlib.compress(bx + by, 9)), len(zlib.compress(by + bx, 9)))
    return (cxy - min(cx, cy)) / max(cx, cy)


def mutual_information(xs, ys):
    """Plug-in I(X;Y) in bits for two equal-length symbol columns."""
    if len(xs) != len(ys) or not xs:
        raise ValueError("columns must be non-empty and the same length")
    n = len(xs)
    px, py, pxy = Counter(xs), Counter(ys), Counter(zip(xs, ys))
    return sum((c / n) * math.log2((c / n) / ((px[a] / n) * (py[b] / n)))
               for (a, b), c in pxy.items()) + 0.0


def read_seq(arg):
    if os.path.isfile(arg):
        with open(arg, encoding="utf-8") as fh:
            lines = [ln for ln in fh.read().splitlines() if not ln.startswith(">")]
        return "".join("".join(lines).split())
    return "".join(arg.split())


def selftest():
    n = [0]

    def check(name, got, want, tol=1e-9):
        n[0] += 1
        ok = (got == want) if isinstance(want, (str, bool)) else abs(got - want) <= tol
        if not ok:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    # Worked values printed in the source text (ch. 2), which rounds to two places.
    check("variety of 3 kinds, 1.585 bits", variety(3), 1.585, 0.006)
    check("variety of 12 kinds, 3.585 bits", variety(12), 3.585, 0.006)
    check("variety of 120 kinds, 6.91 bits", variety(120), 6.91, 0.006)
    prior = [0.25, 0.25, 0.25] + [0.25 / 9] * 9
    check("weighted case, 2.79 bits", shannon(prior), 2.79, 0.006)
    check("weighted case equals 3/4 log2 4 + 1/4 log2 36",
          shannon(prior), 0.75 * 2 + 0.25 * math.log2(36), 1e-12)
    # Hand-computed entropies.
    check("H(ACGT)", entropy("ACGT"), 2.0)
    check("H(AAAA)", entropy("AAAA"), 0.0)
    check("H(AACC)", entropy("AACC"), 1.0)
    check("H(AAAC)", entropy("AAAC"), 0.8112781244591328, 1e-12)
    check("H of 2-mers in ACAC", entropy("ACAC", 2), 0.9182958340544896, 1e-12)
    check("case does not matter", entropy("acgt"), 2.0)
    # Diversity numbers (equations 2.1-2.3 of the source) and their ordering.
    d0, d1, d2 = hill([0.25] * 4)
    check("D0 uniform", d0, 4.0)
    check("D1 uniform", d1, 4.0, 1e-9)
    check("D2 uniform", d2, 4.0, 1e-9)
    d0, d1, d2 = hill([0.5, 0.25, 0.25])
    check("D0", d0, 3.0)
    check("D1 = 2^1.5", d1, 2 ** 1.5, 1e-9)
    check("D2 = 1/0.375", d2, 1 / 0.375, 1e-9)
    check("D0 >= D1 >= D2", d0 >= d1 >= d2, True)
    # Relative entropy and motif conservation.
    check("KL(0.5,0.5 || 0.25,0.75)", kl_divergence([0.5, 0.5], [0.25, 0.75]),
          0.5 + 0.5 * math.log2(0.5 / 0.75), 1e-12)
    check("KL of p from itself", kl_divergence([0.2, 0.8], [0.2, 0.8]), 0.0)
    check("fully conserved column", motif_column_information("AAAA"), 2.0)
    check("unconserved column", motif_column_information("ACGT"), 0.0)
    # Mutual information.
    check("MI identical ACGT", mutual_information("ACGT", "ACGT"), 2.0)
    check("MI identical AACC", mutual_information("AACC", "AACC"), 1.0)
    check("MI independent", mutual_information("AACC", "AGAG"), 0.0, 1e-12)
    # Compression distance: properties, with a fixed pseudo-random generator.
    state = [12345]

    def rand_dna(length):
        out = []
        for _ in range(length):
            state[0] = (state[0] * 1103515245 + 12345) % (2 ** 31)
            out.append("ACGT"[(state[0] >> 16) % 4])
        return "".join(out)

    x, other = rand_dna(400), rand_dna(400)
    mutated = x[:100] + ("A" if x[100] != "A" else "C") + x[101:300] + ("G" if x[300] != "G" else "T") + x[301:]
    check("NCD(x,x) is small", ncd(x, x) < 0.1, True)
    check("NCD(x, 2 changes) < NCD(x, unrelated)", ncd(x, mutated) < ncd(x, other), True)
    check("NCD is symmetric", ncd(x, other), ncd(other, x), 1e-12)
    short, long_ = rand_dna(40), rand_dna(600)
    check("NCD of unrelated sequences of very different length stays near 1", 0.7 < ncd(short, long_) < 1.1, True)
    # Error handling.
    for name, fn in (("empty", lambda: entropy("", 1)), ("k too long", lambda: entropy("AC", 3)),
                     ("bad probs", lambda: shannon([0.5, 0.6])), ("zero kinds", lambda: variety(0))):
        try:
            fn()
        except ValueError:
            n[0] += 1
        else:
            raise AssertionError("%s: expected ValueError" % name)
    print("seqinfo.py self-test: %d checks passed" % n[0])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Information measures for sequences.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("bits", help="log2 of N equally likely kinds")
    s.add_argument("n", type=int)
    s = sub.add_parser("entropy", help="Shannon entropy of k-mer frequencies")
    s.add_argument("seq")
    s.add_argument("--k", type=int, default=1)
    s = sub.add_parser("hill", help="diversity numbers D0, D1, D2")
    s.add_argument("seq")
    s = sub.add_parser("ncd", help="normalized compression distance")
    s.add_argument("a")
    s.add_argument("b")
    s = sub.add_parser("mi", help="mutual information of two columns")
    s.add_argument("a")
    s.add_argument("b")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    if a.cmd == "bits":
        print("%.4f bits" % variety(a.n))
    elif a.cmd == "entropy":
        seq = read_seq(a.seq)
        h = entropy(seq, a.k)
        _, count = word_freqs(seq, a.k)
        print("%d %d-mers, entropy %.4f bits per %d-mer, %.4f bits per symbol" % (count, a.k, h, a.k, h / a.k))
        print("maximum for a 4-letter alphabet: %.4f bits per %d-mer" % (2.0 * a.k, a.k))
    elif a.cmd == "hill":
        freqs, _ = word_freqs(read_seq(a.seq), 1)
        d0, d1, d2 = hill(freqs.values())
        print("D0 %.4f  D1 %.4f  D2 %.4f" % (d0, d1, d2))
    elif a.cmd == "ncd":
        print("%.4f" % ncd(read_seq(a.a), read_seq(a.b)))
    elif a.cmd == "mi":
        print("%.4f bits" % mutual_information(read_seq(a.a), read_seq(a.b)))
    else:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
