#!/usr/bin/env python3
"""Counting, probability and multiple-testing helpers for sequence work (standard library only).

  seqstats.py sampling N K                  the four ways to draw K from N
  seqstats.py binom N K P                   P(X = K) and P(X >= K) for a binomial
  seqstats.py hypergeom N K n k             P(X = k) and P(X >= k), drawing n from N with K marked
  seqstats.py expect LENGTH WORD [--gc G]   expected count of WORD in a random sequence
  seqstats.py adjust P1 P2 ... [--method bh|bonferroni]
  seqstats.py stationary "0.9,0.1;0.5,0.5"  stationary distribution of a Markov chain
  seqstats.py --selftest

The expected count assumes independent positions with fixed base probabilities. Overlapping
occurrences are positively correlated, so the count is not binomial and a binomial tail
probability from this script is only a rough guide for a word that can overlap itself.
"""
import argparse
import math
import sys


def sampling_counts(n, k):
    """Ordered or unordered draws of k from n, with or without replacement."""
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative")
    return {
        "ordered, with replacement": n ** k,
        "ordered, without replacement": math.perm(n, k),
        "unordered, without replacement": math.comb(n, k),
        "unordered, with replacement": math.comb(n + k - 1, k) if n + k - 1 >= 0 else 0,
    }


def binom_pmf(n, k, p):
    if not 0 <= p <= 1 or not 0 <= k <= n:
        raise ValueError("need 0 <= k <= n and 0 <= p <= 1")
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def binom_sf(n, k, p):
    """P(X >= k)."""
    return sum(binom_pmf(n, i, p) for i in range(max(k, 0), n + 1))


def hypergeom_pmf(total, marked, drawn, k):
    """P(X = k): `drawn` items taken without replacement from `total`, of which `marked` are marked."""
    if not (0 <= marked <= total and 0 <= drawn <= total):
        raise ValueError("need 0 <= marked, drawn <= total")
    if k < max(0, drawn - (total - marked)) or k > min(drawn, marked):
        return 0.0
    return math.comb(marked, k) * math.comb(total - marked, drawn - k) / math.comb(total, drawn)


def hypergeom_sf(total, marked, drawn, k):
    """P(X >= k)."""
    return sum(hypergeom_pmf(total, marked, drawn, i) for i in range(max(k, 0), min(drawn, marked) + 1))


def base_probs(gc=0.5):
    """A, C, G, T probabilities for a given GC fraction, A = T and C = G."""
    if not 0 <= gc <= 1:
        raise ValueError("gc must be between 0 and 1")
    return {"A": (1 - gc) / 2, "T": (1 - gc) / 2, "C": gc / 2, "G": gc / 2}


def expected_count(length, word, probs=None):
    """Expected number of (overlapping) occurrences of `word` in a random sequence of `length`."""
    probs = probs or base_probs(0.5)
    word = word.upper()
    positions = length - len(word) + 1
    if positions <= 0:
        return 0.0
    p = 1.0
    for ch in word:
        p *= probs[ch]
    return positions * p


def bonferroni(pvals):
    m = len(pvals)
    return [min(1.0, p * m) for p in pvals]


def benjamini_hochberg(pvals):
    """Adjusted p-values (q-values) for the Benjamini-Hochberg false-discovery-rate procedure."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adjusted = [0.0] * m
    running = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        running = min(running, pvals[i] * m / rank)
        adjusted[i] = running
    return adjusted


def log_likelihood(seq, probs):
    """Natural-log likelihood of a sequence under independent positions."""
    return sum(math.log(probs[ch]) for ch in seq.upper())


def stationary(matrix, tol=1e-12, max_iter=1_000_000):
    """Stationary distribution of an irreducible, aperiodic Markov chain by power iteration."""
    n = len(matrix)
    for row in matrix:
        if len(row) != n or abs(sum(row) - 1.0) > 1e-9 or min(row) < 0:
            raise ValueError("each row must have n non-negative entries summing to 1")
    pi = [1.0 / n] * n
    for _ in range(max_iter):
        nxt = [sum(pi[i] * matrix[i][j] for i in range(n)) for j in range(n)]
        if max(abs(a - b) for a, b in zip(pi, nxt)) < tol:
            return nxt
        pi = nxt
    raise ValueError("power iteration did not converge: the chain may be periodic. "
                     "Check that every state can reach every other before trusting a result")


def _fails_to_converge(matrix):
    try:
        stationary(matrix, max_iter=2000)
    except ValueError:
        return True
    return False


def selftest():
    n = [0]

    def check(name, got, want, tol=1e-9):
        n[0] += 1
        if isinstance(want, list):
            ok = len(got) == len(want) and all(abs(a - b) <= tol for a, b in zip(got, want))
        elif isinstance(want, (dict, bool)):
            ok = got == want
        else:
            ok = abs(got - want) <= tol
        if not ok:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    check("four sampling counts, n=4 k=2", sampling_counts(4, 2),
          {"ordered, with replacement": 16, "ordered, without replacement": 12,
           "unordered, without replacement": 6, "unordered, with replacement": 10})
    check("sampling k=0", sampling_counts(5, 0)["unordered, with replacement"], 1)
    check("binom pmf 5,2,0.5", binom_pmf(5, 2, 0.5), 10 / 32)
    check("binom tail 10,8,0.5", binom_sf(10, 8, 0.5), 56 / 1024)
    check("binom pmf sums to 1", sum(binom_pmf(12, i, 0.3) for i in range(13)), 1.0, 1e-12)
    check("hypergeom pmf", hypergeom_pmf(10, 4, 3, 2), 0.3)
    check("hypergeom tail", hypergeom_sf(10, 4, 3, 2), 1 / 3, 1e-12)
    check("hypergeom impossible", hypergeom_pmf(10, 4, 3, 4), 0.0)
    check("hypergeom pmf sums to 1", sum(hypergeom_pmf(20, 7, 6, i) for i in range(7)), 1.0, 1e-12)
    check("expected count, 4-mer, uniform", expected_count(1000, "ACGT"), 997 / 256, 1e-12)
    gc = base_probs(0.4)
    check("expected count, GATC at 40% GC", expected_count(1000, "GATC", gc), 997 * 0.2 * 0.3 * 0.3 * 0.2, 1e-12)
    check("expected count, word longer than sequence", expected_count(3, "ACGT"), 0.0)
    check("probs sum to 1", sum(base_probs(0.37).values()), 1.0, 1e-12)
    pv = [0.01, 0.04, 0.03, 0.005]
    check("Bonferroni", bonferroni(pv), [0.04, 0.16, 0.12, 0.02], 1e-12)
    check("Bonferroni caps at 1", bonferroni([0.6, 0.7]), [1.0, 1.0])
    check("Benjamini-Hochberg", benjamini_hochberg(pv), [0.02, 0.04, 0.04, 0.02], 1e-12)
    # Raw values p*m/rank here are 0.004, 0.08, 0.0547, 0.042, so the running minimum must pull
    # the middle ones down to 0.042; input order is shuffled to test the mapping back.
    check("Benjamini-Hochberg enforces monotonicity", benjamini_hochberg([0.042, 0.001, 0.041, 0.04]),
          [0.042, 0.004, 0.042, 0.042], 1e-12)
    check("BH never below the raw p", all(q >= p for q, p in zip(benjamini_hochberg(pv), pv)), True)
    check("BH never above Bonferroni", all(q <= b + 1e-12 for q, b in zip(benjamini_hochberg(pv), bonferroni(pv))), True)
    check("log-likelihood AAC", log_likelihood("AAC", {"A": 0.5, "C": 0.25}), math.log(0.0625), 1e-12)
    check("stationary of a 2-state chain", stationary([[0.9, 0.1], [0.5, 0.5]]), [5 / 6, 1 / 6], 1e-9)
    check("stationary of a symmetric chain", stationary([[0.5, 0.5], [0.5, 0.5]]), [0.5, 0.5], 1e-9)
    # A period-2 chain started from the uniform distribution oscillates and never settles.
    periodic = [[0, 1, 0], [0.5, 0, 0.5], [0, 1, 0]]
    check("periodic chain: power iteration reports failure to converge", _fails_to_converge(periodic), True)
    # A reducible chain has several stationary distributions; the answer depends on the start.
    check("reducible chain: returns the uniform start, one of many valid answers",
          stationary([[1, 0], [0, 1]]), [0.5, 0.5], 1e-12)
    for name, fn in (("bad p", lambda: binom_pmf(5, 2, 1.5)), ("bad rows", lambda: stationary([[0.5, 0.6], [0.5, 0.5]])),
                     ("bad gc", lambda: base_probs(2.0)), ("negative n", lambda: sampling_counts(-1, 2))):
        try:
            fn()
        except ValueError:
            n[0] += 1
        else:
            raise AssertionError("%s: expected ValueError" % name)
    print("seqstats.py self-test: %d checks passed" % n[0])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Counting, probability and multiple-testing helpers.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("sampling")
    s.add_argument("n", type=int)
    s.add_argument("k", type=int)
    s = sub.add_parser("binom")
    s.add_argument("n", type=int)
    s.add_argument("k", type=int)
    s.add_argument("p", type=float)
    s = sub.add_parser("hypergeom")
    for name in ("total", "marked", "drawn", "k"):
        s.add_argument(name, type=int)
    s = sub.add_parser("expect")
    s.add_argument("length", type=int)
    s.add_argument("word")
    s.add_argument("--gc", type=float, default=0.5)
    s = sub.add_parser("adjust")
    s.add_argument("pvals", type=float, nargs="+")
    s.add_argument("--method", choices=("bh", "bonferroni"), default="bh")
    s = sub.add_parser("stationary")
    s.add_argument("matrix", help='rows separated by ";", entries by ",", e.g. "0.9,0.1;0.5,0.5"')
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    if a.cmd == "sampling":
        for label, value in sampling_counts(a.n, a.k).items():
            print("%-32s %d" % (label, value))
    elif a.cmd == "binom":
        print("P(X = %d) = %.6g   P(X >= %d) = %.6g" % (a.k, binom_pmf(a.n, a.k, a.p), a.k, binom_sf(a.n, a.k, a.p)))
    elif a.cmd == "hypergeom":
        print("P(X = %d) = %.6g   P(X >= %d) = %.6g" % (
            a.k, hypergeom_pmf(a.total, a.marked, a.drawn, a.k), a.k, hypergeom_sf(a.total, a.marked, a.drawn, a.k)))
    elif a.cmd == "expect":
        print("%.6g expected occurrences of %s in %d positions at %.0f%% GC" % (
            expected_count(a.length, a.word, base_probs(a.gc)), a.word.upper(), a.length, 100 * a.gc))
    elif a.cmd == "adjust":
        adj = benjamini_hochberg(a.pvals) if a.method == "bh" else bonferroni(a.pvals)
        for p, q in zip(a.pvals, adj):
            print("%.6g -> %.6g" % (p, q))
    elif a.cmd == "stationary":
        matrix = [[float(x) for x in row.split(",")] for row in a.matrix.split(";")]
        print(", ".join("%.6f" % x for x in stationary(matrix)))
    else:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
