#!/usr/bin/env python3
"""Pairwise sequence alignment by dynamic programming (standard library only).

  align.py global SEQ1 SEQ2 [--match 1] [--mismatch=-1] [--gap=-1]   Needleman-Wunsch
  align.py local  SEQ1 SEQ2 [--match 2] [--mismatch=-1] [--gap=-2]   Smith-Waterman
  align.py significance SEQ1 SEQ2 [--shuffles 200] [--seed 1]    empirical p-value of the local score
  align.py --selftest

Scoring is match / mismatch / linear gap: every gap position costs the same. There are no
substitution matrices and no affine gap penalties here, so this is for learning, for checking a
result, and for small inputs. Memory and time are O(len1 * len2).
Ties in the traceback prefer diagonal, then a gap in SEQ2, then a gap in SEQ1, so the alignment
printed is one optimal alignment, not the only one. The score is unique.
"""
import argparse
import random
import sys
from collections import namedtuple

Alignment = namedtuple("Alignment", "score top bottom a_span b_span")
GAP = "-"


def _sub(x, y, match, mismatch):
    return match if x == y else mismatch


def global_align(a, b, match=1, mismatch=-1, gap=-1):
    n, m = len(a), len(b)
    h = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        h[i][0] = i * gap
    for j in range(1, m + 1):
        h[0][j] = j * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            h[i][j] = max(h[i - 1][j - 1] + _sub(a[i - 1], b[j - 1], match, mismatch),
                          h[i - 1][j] + gap, h[i][j - 1] + gap)
    top, bottom, i, j = [], [], n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and h[i][j] == h[i - 1][j - 1] + _sub(a[i - 1], b[j - 1], match, mismatch):
            top.append(a[i - 1]); bottom.append(b[j - 1]); i -= 1; j -= 1
        elif i > 0 and h[i][j] == h[i - 1][j] + gap:
            top.append(a[i - 1]); bottom.append(GAP); i -= 1
        else:
            top.append(GAP); bottom.append(b[j - 1]); j -= 1
    return Alignment(h[n][m], "".join(reversed(top)), "".join(reversed(bottom)), (0, n), (0, m))


def local_align(a, b, match=2, mismatch=-1, gap=-2):
    n, m = len(a), len(b)
    h = [[0] * (m + 1) for _ in range(n + 1)]
    best, bi, bj = 0, 0, 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            h[i][j] = max(0, h[i - 1][j - 1] + _sub(a[i - 1], b[j - 1], match, mismatch),
                          h[i - 1][j] + gap, h[i][j - 1] + gap)
            if h[i][j] > best:
                best, bi, bj = h[i][j], i, j
    top, bottom, i, j = [], [], bi, bj
    while i > 0 and j > 0 and h[i][j] > 0:
        if h[i][j] == h[i - 1][j - 1] + _sub(a[i - 1], b[j - 1], match, mismatch):
            top.append(a[i - 1]); bottom.append(b[j - 1]); i -= 1; j -= 1
        elif h[i][j] == h[i - 1][j] + gap:
            top.append(a[i - 1]); bottom.append(GAP); i -= 1
        else:
            top.append(GAP); bottom.append(b[j - 1]); j -= 1
    return Alignment(best, "".join(reversed(top)), "".join(reversed(bottom)), (i, bi), (j, bj))


def rescore(top, bottom, match, mismatch, gap):
    """Score an alignment column by column, independently of the dynamic-programming table."""
    if len(top) != len(bottom):
        raise ValueError("rows differ in length")
    total = 0
    for x, y in zip(top, bottom):
        if x == GAP and y == GAP:
            raise ValueError("column with two gaps")
        total += gap if GAP in (x, y) else _sub(x, y, match, mismatch)
    return total


def identity(top, bottom):
    """Fraction of alignment columns that are identical residues."""
    return sum(1 for x, y in zip(top, bottom) if x == y and x != GAP) / len(top) if top else 0.0


def midline(top, bottom):
    return "".join("|" if x == y and x != GAP else " " for x, y in zip(top, bottom))


def shuffle_significance(a, b, shuffles=200, seed=1, match=2, mismatch=-1, gap=-2):
    """Empirical p-value for the best local score of a vs b against shuffles of b.

    Shuffling keeps the composition of b and destroys its order, so the null is "same letters,
    no meaningful arrangement". p = (1 + shuffles scoring at least as high) / (1 + shuffles), so it
    can never be 0 and cannot be smaller than 1 / (1 + shuffles). Seeded, so a rerun gives the same answer."""
    if shuffles < 1:
        raise ValueError("need at least one shuffle")
    observed = local_align(a, b, match, mismatch, gap).score
    rng = random.Random(seed)
    letters = list(b)
    at_least = 0
    for _ in range(shuffles):
        rng.shuffle(letters)
        if local_align(a, "".join(letters), match, mismatch, gap).score >= observed:
            at_least += 1
    return observed, (1 + at_least) / (1 + shuffles)


def _exhaustive(a, b, match, mismatch, gap):
    """Best global score by trying every alignment. Exponential: only for tiny inputs."""
    if not a and not b:
        return 0
    best = None
    options = []
    if a and b:
        options.append(_sub(a[0], b[0], match, mismatch) + _exhaustive(a[1:], b[1:], match, mismatch, gap))
    if a:
        options.append(gap + _exhaustive(a[1:], b, match, mismatch, gap))
    if b:
        options.append(gap + _exhaustive(a, b[1:], match, mismatch, gap))
    for value in options:
        best = value if best is None else max(best, value)
    return best


def _exhaustive_local(a, b, match, mismatch, gap):
    best = 0
    for i in range(len(a) + 1):
        for j in range(i + 1, len(a) + 1):
            for k in range(len(b) + 1):
                for l in range(k + 1, len(b) + 1):
                    best = max(best, _exhaustive(a[i:j], b[k:l], match, mismatch, gap))
    return best


def _levenshtein(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def selftest():
    n = [0]

    def check(name, got, want):
        n[0] += 1
        if got != want:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    # Hand-computed cases.
    check("identical sequences", global_align("ACGT", "ACGT").score, 4)
    check("one deletion", global_align("ACGT", "AGT").score, 2)
    r = global_align("ACGT", "AGT")
    check("one deletion, alignment", (r.top, r.bottom), ("ACGT", "A-GT"))
    check("empty vs sequence", global_align("", "ACG").score, -3)
    check("both empty", global_align("", "").score, 0)
    check("substring found by local", local_align("TTACGTT", "ACGT", 1, -1, -1).score, 4)
    r = local_align("TTACGTT", "ACGT", 1, -1, -1)
    check("local alignment text", (r.top, r.bottom, r.a_span, r.b_span), ("ACGT", "ACGT", (2, 6), (0, 4)))
    check("local with no similarity", local_align("AAAA", "CCCC").score, 0)
    check("local empty alignment", local_align("AAAA", "CCCC").top, "")
    state = [2024]

    def rnd(max_len):
        state[0] = (state[0] * 1103515245 + 12345) % (2 ** 31)
        length = (state[0] >> 16) % (max_len + 1)
        out = []
        for _ in range(length):
            state[0] = (state[0] * 1103515245 + 12345) % (2 ** 31)
            out.append("ACGT"[(state[0] >> 16) % 4])
        return "".join(out)

    params = [(1, -1, -1), (2, -3, -2), (5, -4, -6), (3, -1, -1)]
    # The table must equal an exhaustive search over every alignment, and the printed alignment
    # must re-score to the reported score and spell out the inputs.
    for t in range(60):
        a, b = rnd(5), rnd(5)
        mt, mm, gp = params[t % len(params)]
        r = global_align(a, b, mt, mm, gp)
        check("global vs exhaustive %r %r %r" % (a, b, params[t % 4]), r.score, _exhaustive(a, b, mt, mm, gp))
        check("global rescore %r %r" % (a, b), rescore(r.top, r.bottom, mt, mm, gp), r.score)
        check("global top spells a", r.top.replace(GAP, ""), a)
        check("global bottom spells b", r.bottom.replace(GAP, ""), b)
    for t in range(25):
        a, b = rnd(4), rnd(4)
        mt, mm, gp = params[t % len(params)]
        r = local_align(a, b, mt, mm, gp)
        check("local vs exhaustive %r %r %r" % (a, b, params[t % 4]), r.score, _exhaustive_local(a, b, mt, mm, gp))
        check("local rescore %r %r" % (a, b), rescore(r.top, r.bottom, mt, mm, gp) if r.top else 0, r.score)
        check("local top is a slice of a", r.top.replace(GAP, ""), a[r.a_span[0]:r.a_span[1]])
        check("local bottom is a slice of b", r.bottom.replace(GAP, ""), b[r.b_span[0]:r.b_span[1]])
    # With match 0 and every edit costing -1, the score is minus the edit distance.
    for _ in range(80):
        a, b = rnd(9), rnd(9)
        check("edit distance %r %r" % (a, b), global_align(a, b, 0, -1, -1).score, -_levenshtein(a, b))
    check("identity of a perfect alignment", identity("ACGT", "ACGT"), 1.0)
    check("identity with a gap", identity("ACGT", "A-GT"), 0.75)
    check("midline", midline("ACGT", "A-GT"), "| ||")
    check("two gaps in a column are never counted as identical", identity("A-", "A-"), 0.5)
    check("midline leaves two gaps blank", midline("A-", "A-"), "| ")
    long_seq = "ACGTTGCAAGCTTAGGCATCCGATA"
    score, p = shuffle_significance(long_seq, long_seq, shuffles=50, seed=3)
    check("identical sequences: score is 2 per base", score, 2 * len(long_seq))
    check("identical sequences: p-value is the smallest possible", p, 1 / 51)
    check("same seed, same p-value", shuffle_significance(long_seq, long_seq[::-1], 30, 7), shuffle_significance(long_seq, long_seq[::-1], 30, 7))
    check("p-value stays in (0, 1]", 0 < shuffle_significance("ACGTAC", "TTGACA", 40, 5)[1] <= 1, True)
    check("a shuffle that cannot lower the score gives p = 1", shuffle_significance("AAAA", "AAAA", 20, 1)[1], 1.0)
    for name, fn in (("two gaps in a column", lambda: rescore("A-", "A-", 1, -1, -1)),
                     ("no shuffles", lambda: shuffle_significance("A", "A", 0)),
                     ("unequal rows", lambda: rescore("AC", "A", 1, -1, -1))):
        try:
            fn()
        except ValueError:
            n[0] += 1
        else:
            raise AssertionError("%s: expected ValueError" % name)
    print("align.py self-test: %d checks passed" % n[0])


def show(result, match, mismatch, gap):
    print("score %d" % result.score)
    if result.top:
        print(result.top)
        print(midline(result.top, result.bottom))
        print(result.bottom)
        print("identity %.1f%% over %d columns; seq1 %d-%d, seq2 %d-%d (0-based, end exclusive)" % (
            100 * identity(result.top, result.bottom), len(result.top),
            result.a_span[0], result.a_span[1], result.b_span[0], result.b_span[1]))
    else:
        print("no positive-scoring local alignment")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pairwise alignment by dynamic programming.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="mode")
    for mode, defaults in (("global", (1, -1, -1)), ("local", (2, -1, -2))):
        s = sub.add_parser(mode)
        s.add_argument("a")
        s.add_argument("b")
        s.add_argument("--match", type=int, default=defaults[0])
        s.add_argument("--mismatch", type=int, default=defaults[1])
        s.add_argument("--gap", type=int, default=defaults[2])
    s = sub.add_parser("significance")
    s.add_argument("a")
    s.add_argument("b")
    s.add_argument("--shuffles", type=int, default=200)
    s.add_argument("--seed", type=int, default=1)
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    if a.mode == "significance":
        score, p = shuffle_significance(a.a.upper(), a.b.upper(), a.shuffles, a.seed)
        print("local score %d; empirical p = %.4f from %d shuffles of seq2 (smallest possible %.4f)" % (
            score, p, a.shuffles, 1 / (1 + a.shuffles)))
        return 0
    if a.mode is None:
        ap.print_help()
        return 2
    fn = global_align if a.mode == "global" else local_align
    show(fn(a.a.upper(), a.b.upper(), a.match, a.mismatch, a.gap), a.match, a.mismatch, a.gap)
    return 0


if __name__ == "__main__":
    sys.exit(main())
