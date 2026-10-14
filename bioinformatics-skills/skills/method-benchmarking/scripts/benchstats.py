#!/usr/bin/env python3
"""Statistics for comparing computational methods (standard library only).

  benchstats.py compare RESULTS.csv --a METHOD --b METHOD [--lower-better] [--boot 5000] [--seed 1]
  benchstats.py ranks RESULTS.csv [--lower-better]
  benchstats.py mcnemar --b 30 --c 12
  benchstats.py min-diff --n 200 --acc 0.8 [--corr 0.0] [--alpha 0.05] [--power 0.8]
  benchstats.py chance-gap --n 200 --k 10 --acc 0.8 [--trials 20000] [--seed 1]
  benchstats.py --selftest

RESULTS.csv has columns dataset,method,score with one row per method per dataset (higher is better
unless --lower-better).

What these answer: is method A really better than B across datasets (paired differences, a bootstrap
over datasets, an exact sign test), how do the methods rank, whether two classifiers on the same test
items differ (McNemar's exact test), how large a gap chance alone can produce on a test set of a given
size, and how large a gap the test set could detect at all.

What they do not do: pick the datasets, check for leakage, tune any method fairly, or say whether a
difference matters. Every dataset is treated as one independent unit, so a handful of datasets gives a
wide interval however many items each contains.
"""
import argparse
import csv
import math
import random
import sys
from statistics import NormalDist, mean, median

_N = NormalDist()


def binom_two_sided(k, n, p=0.5):
    """Exact two-sided binomial test of k successes in n trials at success probability p = 0.5,
    p-value = min(1, 2 * P(X <= min(k, n - k)))."""
    if n == 0:
        return 1.0
    low = min(k, n - k)
    tail = sum(math.comb(n, i) for i in range(low + 1)) / float(2 ** n)
    return min(1.0, 2 * tail)


def read_results(path):
    rows = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                rows.setdefault(r["dataset"], {})[r["method"]] = float(r["score"])
            except (KeyError, ValueError):
                raise SystemExit("%s: need columns dataset,method,score with numeric scores" % path)
    if not rows:
        raise SystemExit("%s: no rows" % path)
    return rows


def paired_differences(rows, a, b, lower_better=False):
    """Per-dataset difference a - b, sign-flipped when lower is better, for datasets where both exist."""
    sign = -1.0 if lower_better else 1.0
    out = {}
    for ds, m in rows.items():
        if a in m and b in m:
            out[ds] = sign * (m[a] - m[b])
    return out


def bootstrap_mean_ci(values, n_boot=5000, conf=0.95, seed=1):
    rng = random.Random(seed)
    n = len(values)
    reps = sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot))
    lo = (1 - conf) / 2

    def q(f):
        h = (n_boot - 1) * f
        i = int(math.floor(h))
        j = min(i + 1, n_boot - 1)
        return reps[i] + (h - i) * (reps[j] - reps[i])
    return mean(values), q(lo), q(1 - lo)


def sign_test(diffs):
    """(wins for A, ties, wins for B, exact two-sided p) ignoring ties."""
    wins = sum(1 for d in diffs if d > 0)
    losses = sum(1 for d in diffs if d < 0)
    ties = len(diffs) - wins - losses
    return wins, ties, losses, binom_two_sided(wins, wins + losses)


def average_ranks(rows, lower_better=False):
    """Average rank per method over datasets (1 = best, ties share the mean rank) and the count of datasets
    each method wins outright or ties for first. Only datasets with every method present are used."""
    methods = sorted({m for r in rows.values() for m in r})
    if not methods:
        raise ValueError("no methods in the results")
    totals = {m: 0.0 for m in methods}
    firsts = {m: 0 for m in methods}
    used = 0
    for ds, r in rows.items():
        if len(r) != len(methods):
            continue
        used += 1
        order = sorted(methods, key=lambda m: r[m] if lower_better else -r[m])
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and r[order[j + 1]] == r[order[i]]:
                j += 1
            rank = (i + j) / 2.0 + 1
            for m in order[i:j + 1]:
                totals[m] += rank
                if i == 0:
                    firsts[m] += 1
            i = j + 1
    if used == 0:
        raise ValueError("no dataset has every method")
    return {m: totals[m] / used for m in methods}, firsts, used


def mcnemar_exact(b, c):
    """b = items A got right and B wrong, c = the reverse. Exact two-sided p on the discordant items."""
    return binom_two_sided(min(b, c), b + c)


def min_detectable_difference(n, acc, corr=0.0, alpha=0.05, power=0.8):
    """Smallest difference in accuracy-like proportions two methods can show with the given power, by the
    normal approximation. corr is the correlation between the methods' errors on the same items (0 for
    separate test sets): the variance of the difference is 2 p (1 - p) (1 - corr) / n."""
    if not (0 < acc < 1 and n > 1 and 0 <= corr < 1):
        raise ValueError("need 0 < acc < 1, n > 1 and 0 <= corr < 1")
    z = _N.inv_cdf(1 - alpha / 2) + _N.inv_cdf(power)
    return z * math.sqrt(2 * acc * (1 - acc) * (1 - corr) / n)


def chance_gap(n, k, acc, trials=20000, seed=1):
    """Simulate k methods that are all truly acc accurate, each scored on its own n test items. Returns
    (mean of the best observed accuracy minus acc, mean of best minus median of the k)."""
    rng = random.Random(seed)
    best_minus_truth, best_minus_median = 0.0, 0.0
    for _ in range(trials):
        scores = [sum(1 for _i in range(n) if rng.random() < acc) / float(n) for _j in range(k)]
        best = max(scores)
        best_minus_truth += best - acc
        best_minus_median += best - median(scores)
    return best_minus_truth / trials, best_minus_median / trials


# expected maximum of k independent standard normals (standard values)
E_MAX_NORMAL = {2: 0.5642, 3: 0.8463, 4: 1.0294, 5: 1.1630, 10: 1.5388}


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=0.0):
        count[0] += 1
        ok = abs(got - want) <= tol if (tol or isinstance(want, float)) else got == want
        if not ok:
            fails.append("%s: got %r, want %r" % (name, got, want))

    eq("binom 5,0", binom_two_sided(0, 5), 0.0625, 1e-12)
    eq("binom symmetric", binom_two_sided(5, 5), binom_two_sided(0, 5), 1e-12)
    eq("binom balanced", binom_two_sided(3, 6), 1.0, 1e-12)
    eq("binom none", binom_two_sided(0, 0), 1.0, 1e-12)
    eq("binom 12 of 42", binom_two_sided(12, 42), 2 * sum(math.comb(42, i) for i in range(13)) / 2.0 ** 42, 1e-12)
    eq("mcnemar equal", mcnemar_exact(10, 10), 1.0, 1e-12)
    eq("mcnemar 5v0", mcnemar_exact(5, 0), 0.0625, 1e-12)
    eq("mcnemar order irrelevant", mcnemar_exact(30, 12), mcnemar_exact(12, 30), 1e-15)

    rows = {"d1": {"A": 0.9, "B": 0.8, "C": 0.7}, "d2": {"A": 0.6, "B": 0.7, "C": 0.5},
            "d3": {"A": 0.8, "B": 0.8, "C": 0.6}, "d4": {"A": 0.7, "B": 0.6, "C": 0.6}}
    diffs = paired_differences(rows, "A", "B")
    eq("paired diffs", sorted(round(v, 6) for v in diffs.values()), [-0.1, 0.0, 0.1, 0.1])
    eq("lower-better flips sign", sorted(round(v, 6) for v in paired_differences(rows, "A", "B", True).values()), [-0.1, -0.1, 0.0, 0.1])
    eq("sign test", sign_test(list(diffs.values()))[:3], (2, 1, 1))
    eq("sign test p", sign_test(list(diffs.values()))[3], binom_two_sided(2, 3), 1e-12)
    avg, firsts, used = average_ranks(rows)
    eq("ranks A", avg["A"], (1 + 2 + 1.5 + 1) / 4.0, 1e-12)
    eq("ranks sum", sum(avg.values()), 6.0, 1e-12)
    eq("ranks ties share", average_ranks({"d": {"A": 1.0, "B": 1.0, "C": 0.5}})[0], {"A": 1.5, "B": 1.5, "C": 3.0})
    eq("firsts count ties", average_ranks({"d": {"A": 1.0, "B": 1.0, "C": 0.5}})[1], {"A": 1, "B": 1, "C": 0})
    eq("lower better ranks", average_ranks({"d": {"A": 1.0, "B": 2.0}}, True)[0], {"A": 1.0, "B": 2.0})
    eq("datasets with a missing method skipped", average_ranks({"d1": {"A": 1, "B": 2}, "d2": {"A": 1}})[2], 1)
    est, lo, hi = bootstrap_mean_ci([0.05] * 8)
    eq("constant diff ci", (round(est, 9), round(lo, 9), round(hi, 9)), (0.05, 0.05, 0.05))
    est, lo, hi = bootstrap_mean_ci([0.1, -0.1, 0.2, 0.0, 0.05, 0.15], 2000)
    eq("ci brackets the mean", lo <= est <= hi, True)
    eq("seeded", bootstrap_mean_ci([1.0, 2.0, 4.0], 500, seed=2), bootstrap_mean_ci([1.0, 2.0, 4.0], 500, seed=2))

    eq("min diff 200 at 0.8", min_detectable_difference(200, 0.8), (1.959964 + 0.841621) * 0.04, 1e-5)
    eq("min diff paired corr .5", min_detectable_difference(200, 0.8, 0.5), (1.959964 + 0.841621) * 0.04 * math.sqrt(0.5), 1e-5)
    eq("min diff shrinks with n", min_detectable_difference(800, 0.8) < min_detectable_difference(200, 0.8), True)
    eq("min diff 4x n halves", min_detectable_difference(800, 0.8) / min_detectable_difference(200, 0.8), 0.5, 1e-9)

    sd = math.sqrt(0.8 * 0.2 / 400)
    g2, _ = chance_gap(400, 2, 0.8, 20000, 1)
    eq("chance gap k=2 matches sigma*0.5642", g2, sd * E_MAX_NORMAL[2], 0.0008)
    g5, _ = chance_gap(400, 5, 0.8, 20000, 1)
    eq("chance gap k=5 matches sigma*1.1630", g5, sd * E_MAX_NORMAL[5], 0.0008)
    eq("more methods, bigger gap", g5 > g2, True)
    eq("best minus median, pinned value for seed 4", chance_gap(50, 3, 0.7, 500, 4)[1], 0.05584, 1e-9)
    eq("chance gap seeded", chance_gap(50, 3, 0.7, 500, 4), chance_gap(50, 3, 0.7, 500, 4))
    for bad, label in ((lambda: min_detectable_difference(1, 0.8), "n=1"), (lambda: min_detectable_difference(100, 1.0), "acc=1"),
                       (lambda: average_ranks({"d": {}}), "no methods")):
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
    print("benchstats selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Statistics for comparing computational methods.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("compare")
    c.add_argument("file")
    c.add_argument("--a", required=True)
    c.add_argument("--b", required=True)
    c.add_argument("--lower-better", action="store_true")
    c.add_argument("--boot", type=int, default=5000)
    c.add_argument("--seed", type=int, default=1)
    r = sub.add_parser("ranks")
    r.add_argument("file")
    r.add_argument("--lower-better", action="store_true")
    m = sub.add_parser("mcnemar")
    m.add_argument("--b", type=int, required=True, help="items A got right and B wrong")
    m.add_argument("--c", type=int, required=True, help="items A got wrong and B right")
    d = sub.add_parser("min-diff")
    d.add_argument("--n", type=int, required=True)
    d.add_argument("--acc", type=float, required=True)
    d.add_argument("--corr", type=float, default=0.0)
    d.add_argument("--alpha", type=float, default=0.05)
    d.add_argument("--power", type=float, default=0.8)
    g = sub.add_parser("chance-gap")
    g.add_argument("--n", type=int, required=True)
    g.add_argument("--k", type=int, required=True)
    g.add_argument("--acc", type=float, required=True)
    g.add_argument("--trials", type=int, default=20000)
    g.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.cmd:
        ap.error("give a command or --selftest")
    try:
        if a.cmd == "compare":
            rows = read_results(a.file)
            diffs = paired_differences(rows, a.a, a.b, a.lower_better)
            if len(diffs) < 2:
                print("error: need at least 2 datasets with both methods; found %d" % len(diffs))
                return 2
            est, lo, hi = bootstrap_mean_ci(list(diffs.values()), a.boot, 0.95, a.seed)
            w, t, l, p = sign_test(list(diffs.values()))
            print("%s minus %s over %d datasets (%s)" % (a.a, a.b, len(diffs), "lower is better" if a.lower_better else "higher is better"))
            for ds in sorted(diffs):
                print("  %-20s %+.4f" % (ds, diffs[ds]))
            print("mean difference %+.4f, 95%% bootstrap interval over datasets [%+.4f, %+.4f]" % (est, lo, hi))
            print("%s better on %d, tied on %d, %s better on %d; exact sign test p = %.4g" % (a.a, w, t, a.b, l, p))
            if len(diffs) < 6:
                print("note: with %d datasets the smallest possible two-sided sign-test p is %.4g" % (len(diffs), binom_two_sided(0, len(diffs))))
            print("interval %s zero" % ("excludes" if lo > 0 or hi < 0 else "includes"))
        elif a.cmd == "ranks":
            avg, firsts, used = average_ranks(read_results(a.file), a.lower_better)
            print("average rank over %d datasets with every method (1 = best)" % used)
            for mth in sorted(avg, key=avg.get):
                print("  %-20s %.3f   best (or tied) on %d" % (mth, avg[mth], firsts[mth]))
        elif a.cmd == "mcnemar":
            print("McNemar exact test on %d discordant items (b=%d, c=%d): two-sided p = %.4g" % (a.b + a.c, a.b, a.c, mcnemar_exact(a.b, a.c)))
        elif a.cmd == "min-diff":
            md = min_detectable_difference(a.n, a.acc, a.corr, a.alpha, a.power)
            print("with %d test items at accuracy %.2f, %.0f%% power and alpha %.2f, the smallest difference detectable is about %.3f" % (
                a.n, a.acc, a.power * 100, a.alpha, md))
        elif a.cmd == "chance-gap":
            g1, g2 = chance_gap(a.n, a.k, a.acc, a.trials, a.seed)
            print("%d methods, all truly %.2f accurate, each scored on %d items (%d simulations):" % (a.k, a.acc, a.n, a.trials))
            print("  the best looks %.3f above the truth on average, and %.3f above the median method" % (g1, g2))
    except ValueError as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
