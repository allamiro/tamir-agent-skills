#!/usr/bin/env python3
"""Statistics for performance experiments (standard library only).

  perfstats.py percentile FILE [-p 50 95 99] [--method nearest|linear]
  perfstats.py ci FILE [--stat mean|median|p99] [--boot 5000] [--conf 0.95] [--seed 1]
  perfstats.py compare A B [--stat median] [--boot 5000] [--conf 0.95] [--seed 1]
  perfstats.py tail --q 0.999 --k 10        samples needed so about k fall beyond the quantile
  perfstats.py tail --q 0.999 --n 2000      expected samples beyond the quantile in a run of n
  perfstats.py co FILE --interval 10        back-fill samples hidden by coordinated omission
  perfstats.py little [--lam L] [--w W] [--l N]   give two, get the third
  perfstats.py runs --cv 0.1 --rel 0.02 [--conf 0.95]   repetitions for a relative error on the mean
  perfstats.py --selftest

FILE holds numbers separated by whitespace or commas, for example one latency per line. All
resampling is seeded, so a result can be repeated.

What this does not do: model dependence between samples (successive requests in one run are often
correlated, so treat a bootstrap over raw samples as optimistic and prefer one summary number per
independent run), pick a workload, or decide whether a difference matters.
"""
import argparse
import math
import random
import re
import sys
from fractions import Fraction
from functools import lru_cache
from statistics import NormalDist, mean, median

_N = NormalDist()


def read_numbers(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    out = []
    for tok in re.split(r"[\s,]+", text.strip()):
        if tok:
            out.append(float(tok))
    if not out:
        raise SystemExit("%s: no numbers" % path)
    return out


def percentile(data, p, method="nearest"):
    """p in [0, 100]. nearest: the smallest value with at least p percent of the data at or below it
    (rank ceil(p/100*n)). linear: interpolate between order statistics at position (n-1)p/100, the
    default in NumPy and R type 7. They differ on small samples, so say which one you used."""
    if not data:
        raise ValueError("no data")
    if not 0 <= p <= 100:
        raise ValueError("p must be between 0 and 100")
    xs = sorted(data)
    n = len(xs)
    if method == "nearest":
        k = max(1, math.ceil(Fraction(str(p)) / 100 * n))
        return xs[k - 1]
    if method == "linear":
        h = (n - 1) * p / 100.0
        lo = int(math.floor(h))
        hi = min(lo + 1, n - 1)
        return xs[lo] + (h - lo) * (xs[hi] - xs[lo])
    raise ValueError("method must be nearest or linear")


def stat_fn(name):
    if name == "mean":
        return mean
    if name == "median":
        return median
    m = re.fullmatch(r"p(\d+(?:\.\d+)?)", name)
    if m:
        p = float(m.group(1))
        return lambda xs: percentile(xs, p, "nearest")
    raise ValueError("stat must be mean, median or pNN such as p99")


def quantile_of(sorted_vals, q):
    h = (len(sorted_vals) - 1) * q
    lo = int(math.floor(h))
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (h - lo) * (sorted_vals[hi] - sorted_vals[lo])


def bootstrap_ci(data, stat, n_boot=5000, conf=0.95, seed=1):
    """Percentile bootstrap interval for stat(data). Returns (estimate, low, high)."""
    if len(data) < 2:
        raise ValueError("need at least 2 samples")
    rng = random.Random(seed)
    n = len(data)
    reps = sorted(stat([data[rng.randrange(n)] for _ in range(n)]) for _ in range(n_boot))
    a = (1 - conf) / 2
    return stat(data), quantile_of(reps, a), quantile_of(reps, 1 - a)


def bootstrap_diff(a, b, stat, n_boot=5000, conf=0.95, seed=1):
    """Percentile bootstrap interval for stat(a) - stat(b) with independent resampling."""
    rng = random.Random(seed)
    na, nb = len(a), len(b)
    reps = sorted(stat([a[rng.randrange(na)] for _ in range(na)]) - stat([b[rng.randrange(nb)] for _ in range(nb)])
                  for _ in range(n_boot))
    lo = (1 - conf) / 2
    return stat(a) - stat(b), quantile_of(reps, lo), quantile_of(reps, 1 - lo)


@lru_cache(maxsize=None)
def _u_counts(m, n):
    """Number of arrangements of m values from A and n from B giving each Mann-Whitney U (no ties).
    The largest value is from A (adding n pairs where A wins) or from B (adding none)."""
    if m == 0 or n == 0:
        return (1,)
    a = _u_counts(m - 1, n)
    b = _u_counts(m, n - 1)
    size = m * n + 1
    out = [0] * size
    for u, c in enumerate(a):
        out[u + n] += c
    for u, c in enumerate(b):
        out[u] += c
    return tuple(out)


def mann_whitney(a, b):
    """Two-sided Mann-Whitney U test. Returns (U_a, p, method). U_a counts pairs where a beats b,
    ties as half. Exact when there are no ties and both samples have at most 30 values; otherwise a
    normal approximation with tie and continuity corrections."""
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        raise ValueError("both samples need values")
    u = 0.0
    for x in a:
        for y in b:
            u += 1.0 if x > y else 0.5 if x == y else 0.0
    pooled = a + b
    has_ties = len(set(pooled)) < len(pooled)
    if not has_ties and max(m, n) <= 30:
        counts = _u_counts(m, n)
        total = sum(counts)
        low = min(u, m * n - u)
        tail = sum(counts[: int(low) + 1]) / total
        return u, min(1.0, 2 * tail), "exact"
    N = m + n
    from collections import Counter
    ties = sum(t ** 3 - t for t in Counter(pooled).values())
    var = m * n / 12.0 * ((N + 1) - ties / (N * (N - 1)))
    if var <= 0:
        return u, 1.0, "normal"
    z = max(0.0, abs(u - m * n / 2.0) - 0.5) / math.sqrt(var)
    return u, min(1.0, 2 * (1 - _N.cdf(z))), "normal"


def cliffs_delta(a, b):
    """(pairs where a > b minus pairs where a < b) / all pairs, from -1 to 1."""
    gt = sum(1 for x in a for y in b if x > y)
    lt = sum(1 for x in a for y in b if x < y)
    return (gt - lt) / float(len(a) * len(b))


def samples_for_tail(q, k):
    """Smallest n with n*(1-q) >= k. Uses exact fractions so 0.9 and 0.999 round correctly."""
    q = Fraction(str(q))
    if not 0 < q < 1 or k < 1:
        raise ValueError("need 0 < q < 1 and k >= 1")
    return math.ceil(Fraction(k) / (1 - q))


def tail_count(n, q):
    return float(n * (1 - Fraction(str(q))))


def correct_coordinated_omission(values, interval):
    """For each value longer than the expected interval between requests, add the samples a
    fixed-rate generator would have issued while it was stuck: v - interval, v - 2*interval, ...
    while at least one interval remains. This follows the back-fill the HdrHistogram library
    documents for recordValueWithExpectedInterval (secondary source; VERIFY). It is an estimate. The
    better fix is a load generator that sends on a schedule and measures from the intended send time."""
    if interval <= 0:
        raise ValueError("interval must be positive")
    out = []
    for v in values:
        out.append(v)
        missing = v - interval
        while missing >= interval:
            out.append(missing)
            missing -= interval
    return out


def little(lam=None, w=None, l=None):
    """Little's law L = lam * W for a stable system: items in the system = arrival rate * time in system.
    Give exactly two. Keep units consistent (per second and seconds)."""
    given = [x is not None for x in (lam, w, l)]
    if sum(given) != 2:
        raise ValueError("give exactly two of --lam, --w, --l")
    if lam is None:
        return "lam", l / w
    if w is None:
        return "w", l / lam
    return "l", lam * w


def runs_for_relative_error(cv, rel, conf=0.95):
    """Repetitions n so the confidence interval half-width on the mean is about rel * mean, from
    n = (z * cv / rel)^2 with z the normal quantile. The t distribution makes small n a little larger."""
    if cv <= 0 or rel <= 0 or not 0 < conf < 1:
        raise ValueError("cv and rel must be positive and conf between 0 and 1")
    z = _N.inv_cdf(1 - (1 - conf) / 2)
    return math.ceil((z * cv / rel) ** 2)


def pstdev_sample(xs):
    """Sample standard deviation (n - 1), for the self-test only."""
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def selftest():
    fails, count = [], [0]

    def check(name, got, want, tol=0.0):
        count[0] += 1
        ok = abs(got - want) <= tol if isinstance(want, float) or tol else got == want
        if not ok:
            fails.append("%s: got %r, want %r" % (name, got, want))

    xs = list(range(1, 101))
    check("nearest p50", percentile(xs, 50), 50)
    check("nearest p99", percentile(xs, 99), 99)
    check("nearest p100", percentile(xs, 100), 100)
    check("nearest p0", percentile(xs, 0), 1)
    check("nearest p99.9 of 1000", percentile(list(range(1, 1001)), 99.9), 999)
    check("linear p50", percentile(xs, 50, "linear"), 50.5, 1e-9)
    check("linear p99", percentile(xs, 99, "linear"), 99.01, 1e-9)
    check("unsorted input", percentile([5, 1, 3, 2, 4], 50), 3)
    check("single value", percentile([7], 99), 7)

    est, lo, hi = bootstrap_ci([5.0] * 20, mean, 200)
    check("constant data ci", (lo, hi), (5.0, 5.0))
    rng = random.Random(5)
    small = [rng.gauss(100, 10) for _ in range(30)]
    large = [rng.gauss(100, 10) for _ in range(3000)]
    s = bootstrap_ci(small, mean, 500)
    l = bootstrap_ci(large, mean, 500)
    check("interval narrows with n", (s[2] - s[1]) > (l[2] - l[1]), True)
    check("interval contains estimate", s[1] <= s[0] <= s[2], True)
    check("seeded repeat", bootstrap_ci(small, median, 300, seed=3), bootstrap_ci(small, median, 300, seed=3))
    check("bootstrap can draw the last element", bootstrap_ci([0, 0, 0, 0, 100], mean, 2000)[2] > 0, True)
    rng2 = random.Random(5)
    wide = [rng2.gauss(100, 10) for _ in range(100)]
    est, lo, hi = bootstrap_ci(wide, mean, 4000, 0.95, seed=1)
    check("95 percent interval is about 1.96 standard errors either side", 1.85 < (hi - lo) / (2 * (pstdev_sample(wide) / 10)) < 2.1, True)
    d, dlo, dhi = bootstrap_diff([10.0] * 10, [4.0] * 10, mean, 100)
    check("diff of constants", (d, dlo, dhi), (6.0, 6.0, 6.0))

    check("u counts total 3,3", sum(_u_counts(3, 3)), 20)
    check("u counts total 5,5", sum(_u_counts(5, 5)), 252)
    u, p, how = mann_whitney([1, 2, 3], [4, 5, 6])
    check("mwu 3v3 U", u, 0.0)
    check("mwu 3v3 p", p, 0.1, 1e-12)
    check("mwu method", how, "exact")
    u, p, _ = mann_whitney([1, 2, 3, 4, 5], [6, 7, 8, 9, 10])
    check("mwu 5v5 p", p, 2 / 252.0, 1e-12)
    from math import comb
    u, p, _ = mann_whitney(list(range(1, 21)), list(range(21, 41)))
    check("mwu 20v20 exact p", p, 2 / comb(40, 20), 1e-18)
    u, p, how = mann_whitney([1, 2, 3, 4], [1, 2, 3, 4])
    check("mwu identical p", p, 1.0, 1e-12)
    check("mwu identical uses normal (ties)", how, "normal")
    u, p, how = mann_whitney([1, 2, 2, 3, 5], [2, 3, 4, 4, 6, 7])
    check("mwu with ties U", u, 6.5)
    check("mwu with ties p (SciPy asymptotic with continuity correction)", p, 0.138626, 1e-6)
    check("mwu with ties uses normal", how, "normal")
    u, p, how = mann_whitney(list(range(40)), list(range(100, 140)))
    check("mwu large uses normal", how, "normal")
    check("mwu large separated is small", p < 1e-10, True)
    check("mwu symmetric", mann_whitney([1, 2, 7], [3, 4, 5, 6])[1], mann_whitney([3, 4, 5, 6], [1, 2, 7])[1], 1e-12)
    check("cliff separated", cliffs_delta([5, 6], [1, 2]), 1.0)
    check("cliff reversed", cliffs_delta([1, 2], [5, 6]), -1.0)
    check("cliff equal", cliffs_delta([1, 2], [1, 2]), 0.0)

    check("tail 0.99 k10", samples_for_tail(0.99, 10), 1000)
    check("tail 0.999 k10", samples_for_tail(0.999, 10), 10000)
    check("tail 0.9 k10", samples_for_tail(0.9, 10), 100)
    check("tail rounds up", samples_for_tail(0.97, 1), 34)
    check("tail count", tail_count(2000, 0.999), 2.0, 1e-9)

    check("co 100 by 10", correct_coordinated_omission([100], 10), [100, 90, 80, 70, 60, 50, 40, 30, 20, 10])
    check("co below interval", correct_coordinated_omission([5, 10], 10), [5, 10])
    check("co 25 by 10", correct_coordinated_omission([25], 10), [25, 15])
    check("co keeps order", correct_coordinated_omission([3, 30, 4], 10), [3, 30, 20, 10, 4])

    check("little L", little(lam=1000, w=0.2), ("l", 200.0))
    check("little lam", little(w=0.5, l=50), ("lam", 100.0))
    check("little W", little(lam=250, l=50), ("w", 0.2))
    check("runs", runs_for_relative_error(0.1, 0.02), 97)
    check("runs 99%", runs_for_relative_error(0.1, 0.02, 0.99), 166)
    for bad, label in ((lambda: percentile([], 50), "empty"), (lambda: percentile([1], 101), "p>100"),
                       (lambda: little(lam=1), "little needs two"), (lambda: samples_for_tail(1.0, 1), "q=1"),
                       (lambda: correct_coordinated_omission([1], 0), "interval 0")):
        count[0] += 1
        try:
            bad()
            fails.append("%s should raise" % label)
        except ValueError:
            pass
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("perfstats selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Statistics for performance experiments.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("percentile")
    p.add_argument("file")
    p.add_argument("-p", type=float, nargs="+", default=[50, 95, 99])
    p.add_argument("--method", choices=["nearest", "linear"], default="nearest")
    c = sub.add_parser("ci")
    c.add_argument("file")
    c.add_argument("--stat", default="mean")
    c.add_argument("--boot", type=int, default=5000)
    c.add_argument("--conf", type=float, default=0.95)
    c.add_argument("--seed", type=int, default=1)
    d = sub.add_parser("compare")
    d.add_argument("a")
    d.add_argument("b")
    d.add_argument("--stat", default="median")
    d.add_argument("--boot", type=int, default=5000)
    d.add_argument("--conf", type=float, default=0.95)
    d.add_argument("--seed", type=int, default=1)
    t = sub.add_parser("tail")
    t.add_argument("--q", type=float, required=True)
    t.add_argument("--k", type=int)
    t.add_argument("--n", type=int)
    o = sub.add_parser("co")
    o.add_argument("file")
    o.add_argument("--interval", type=float, required=True)
    li = sub.add_parser("little")
    li.add_argument("--lam", type=float)
    li.add_argument("--w", type=float)
    li.add_argument("--l", type=float)
    r = sub.add_parser("runs")
    r.add_argument("--cv", type=float, required=True)
    r.add_argument("--rel", type=float, required=True)
    r.add_argument("--conf", type=float, default=0.95)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.cmd:
        ap.error("give a command or --selftest")
    try:
        if a.cmd == "percentile":
            data = read_numbers(a.file)
            print("n = %d, method = %s" % (len(data), a.method))
            for q in a.p:
                print("p%g = %g" % (q, percentile(data, q, a.method)))
        elif a.cmd == "ci":
            data = read_numbers(a.file)
            est, lo, hi = bootstrap_ci(data, stat_fn(a.stat), a.boot, a.conf, a.seed)
            print("%s = %g, %g%% bootstrap interval [%g, %g], n = %d" % (a.stat, est, a.conf * 100, lo, hi, len(data)))
            if a.stat.startswith("p") and len(data) * (1 - float(a.stat[1:]) / 100) < 10:
                print("warning: fewer than 10 samples beyond %s; this interval is not trustworthy" % a.stat)
        elif a.cmd == "compare":
            x, y = read_numbers(a.a), read_numbers(a.b)
            diff, lo, hi = bootstrap_diff(x, y, stat_fn(a.stat), a.boot, a.conf, a.seed)
            u, pv, how = mann_whitney(x, y)
            print("%s(A) - %s(B) = %g, %g%% bootstrap interval [%g, %g]" % (a.stat, a.stat, diff, a.conf * 100, lo, hi))
            print("Mann-Whitney U = %g, two-sided p = %.4g (%s)" % (u, pv, how))
            print("Cliff's delta = %.3f (A tends to be %s than B)" % (cliffs_delta(x, y), "larger" if cliffs_delta(x, y) > 0 else "smaller"))
            print("interval %s zero" % ("excludes" if lo > 0 or hi < 0 else "includes"))
        elif a.cmd == "tail":
            if a.k is not None:
                print("n >= %d gives about %d samples beyond q = %g" % (samples_for_tail(a.q, a.k), a.k, a.q))
            elif a.n is not None:
                print("expected samples beyond q = %g in %d: %.2f" % (a.q, a.n, tail_count(a.n, a.q)))
            else:
                ap.error("give --k or --n")
        elif a.cmd == "co":
            data = read_numbers(a.file)
            out = correct_coordinated_omission(data, a.interval)
            print("%d samples became %d after back-filling at interval %g" % (len(data), len(out), a.interval))
            for q in (50, 95, 99):
                print("p%d: %g -> %g" % (q, percentile(data, q), percentile(out, q)))
        elif a.cmd == "little":
            name, val = little(a.lam, a.w, a.l)
            print("%s = %g" % ({"l": "L (items in system)", "lam": "lambda (arrival rate)", "w": "W (time in system)"}[name], val))
        elif a.cmd == "runs":
            print("about %d repetitions for a %g%% interval of +/- %g%% of the mean at cv = %g" % (
                runs_for_relative_error(a.cv, a.rel, a.conf), a.conf * 100, a.rel * 100, a.cv))
    except ValueError as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
