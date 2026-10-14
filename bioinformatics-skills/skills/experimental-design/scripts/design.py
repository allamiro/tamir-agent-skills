#!/usr/bin/env python3
"""Sample size, power and batch layout for experiments (standard library only).

  design.py n --d 0.5 [--alpha 0.05] [--power 0.8] [--tests 1]   samples per group, two-group comparison
  design.py power --n 64 --d 0.5 [--alpha 0.05]                    power for a given group size
  design.py assign SAMPLES.csv --batches 3 [--seed 1]              spread groups evenly over batches
  design.py confound SHEET.csv --group COL --batch COL             is condition tangled up with batch
  design.py --selftest

d is the standardized effect: the difference in group means divided by the common standard
deviation. The sample-size formula is the normal approximation with a small-sample correction for
a two-sided two-sample t-test with equal groups. It does not model counts, unequal variances,
paired designs or many correlated features. Use it to see the order of magnitude, then check with
the tool your field uses.
"""
import argparse
import csv
import math
import random
import sys
from collections import Counter, defaultdict
from statistics import NormalDist

_N = NormalDist()


def n_per_group(d, alpha=0.05, power=0.8, tests=1):
    """Samples per group to detect standardized effect d with a two-sided test.

    n = 2 (z_{1-alpha/2} + z_{power})^2 / d^2 + z_{1-alpha/2}^2 / 4, rounded up. `tests` divides
    alpha (Bonferroni) when the same comparison is made on many features."""
    if d <= 0:
        raise ValueError("effect size d must be positive")
    if not (0 < alpha < 1 and 0 < power < 1) or tests < 1:
        raise ValueError("alpha and power must be between 0 and 1, tests at least 1")
    z_a = _N.inv_cdf(1 - alpha / tests / 2)
    z_b = _N.inv_cdf(power)
    return math.ceil(2 * (z_a + z_b) ** 2 / d ** 2 + z_a ** 2 / 4)


def power_for(n, d, alpha=0.05):
    """Approximate power of the two-sided two-sample test with n per group (normal approximation)."""
    if n < 2 or d < 0:
        raise ValueError("need n >= 2 and d >= 0")
    z_a = _N.inv_cdf(1 - alpha / 2)
    return _N.cdf(d * math.sqrt(n / 2.0) - z_a)


def assign_to_batches(samples, n_batches, seed=1):
    """samples: list of (sample_id, group). Returns {sample_id: batch}, with each group dealt out
    evenly: a group's counts differ by at most one between any two batches."""
    if n_batches < 1:
        raise ValueError("need at least one batch")
    rng = random.Random(seed)
    by_group = defaultdict(list)
    for sid, group in samples:
        by_group[group].append(sid)
    out, offset = {}, 0
    for group in sorted(by_group):
        ids = sorted(by_group[group])
        rng.shuffle(ids)
        for i, sid in enumerate(ids):
            out[sid] = (offset + i) % n_batches
        offset += len(ids)  # continue the rotation so batch sizes stay balanced overall
    return out


def contingency(pairs):
    """Counts of (group, batch) pairs as a nested dict plus the sorted labels."""
    counts = Counter(pairs)
    groups = sorted({g for g, _ in counts})
    batches = sorted({b for _, b in counts})
    return {g: {b: counts.get((g, b), 0) for b in batches} for g in groups}, groups, batches


def cramers_v(table, groups, batches):
    """Association between group and batch, 0 (none) to 1 (batch determines group)."""
    n = sum(table[g][b] for g in groups for b in batches)
    if n == 0 or len(groups) < 2 or len(batches) < 2:
        return 0.0
    rows = {g: sum(table[g].values()) for g in groups}
    cols = {b: sum(table[g][b] for g in groups) for b in batches}
    chi2 = 0.0
    for g in groups:
        for b in batches:
            expected = rows[g] * cols[b] / n
            chi2 += (table[g][b] - expected) ** 2 / expected
    return math.sqrt(chi2 / (n * (min(len(groups), len(batches)) - 1)))


def perfectly_confounded(table, groups, batches):
    """True when knowing the batch tells you the group for every sample (each batch holds one group)."""
    return all(sum(1 for g in groups if table[g][b] > 0) <= 1 for b in batches) and len(groups) > 1


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

    # Standard table values for a two-sided two-sample t-test, alpha 0.05, power 0.8.
    check("n per group for d = 0.5", n_per_group(0.5), 64)
    check("n per group for d = 0.8", n_per_group(0.8), 26)
    check("n per group for d = 1.0", n_per_group(1.0), 17)
    check("larger effect, fewer samples", n_per_group(1.0) < n_per_group(0.5) < n_per_group(0.2), True)
    check("higher power needs more samples", n_per_group(0.5, power=0.9) > n_per_group(0.5), True)
    check("many tests need more samples", n_per_group(0.5, tests=1000) > n_per_group(0.5), True)
    check("normal quantile used for alpha 0.05", _N.inv_cdf(0.975), 1.959964, 1e-6)
    check("power at the planned size is about 0.8", power_for(64, 0.5), 0.807, 0.01)
    check("power with no effect equals the false-positive rate or less", power_for(64, 0.0) <= 0.05, True)
    check("power rises with n", power_for(100, 0.5) > power_for(20, 0.5), True)
    check("n_per_group meets its power target", power_for(n_per_group(0.6), 0.6) >= 0.8 - 0.01, True)
    raises("zero effect", lambda: n_per_group(0))
    raises("bad alpha", lambda: n_per_group(0.5, alpha=1.5))
    raises("too few samples", lambda: power_for(1, 0.5))
    # Batch assignment.
    samples = [("s%d" % i, "treated" if i < 7 else "control") for i in range(12)]  # 7 treated, 5 control
    a = assign_to_batches(samples, 3, seed=4)
    check("every sample assigned", sorted(a), sorted(s for s, _ in samples))
    table, groups, batches = contingency([(g, a[s]) for s, g in samples])
    for g in groups:
        counts = [table[g][b] for b in batches]
        check("group %s dealt evenly over batches %s" % (g, counts), max(counts) - min(counts) <= 1, True)
    sizes = [sum(table[g][b] for g in groups) for b in batches]
    check("batch sizes balanced", max(sizes) - min(sizes) <= 1, True)
    check("same seed, same layout", assign_to_batches(samples, 3, 4), a)
    check("another seed can change the layout", any(assign_to_batches(samples, 3, s) != a for s in range(2, 12)), True)
    check("one batch holds everything", set(assign_to_batches(samples, 1).values()), {0})
    raises("no batches", lambda: assign_to_batches(samples, 0))
    # Confounding, hand-computed.
    aligned = contingency([("A", 1)] * 5 + [("B", 2)] * 5)
    check("aligned design is perfectly confounded", perfectly_confounded(*aligned), True)
    check("aligned design has V = 1", cramers_v(*aligned), 1.0, 1e-12)
    mixed = contingency([("A", 1)] * 3 + [("A", 2)] * 2 + [("B", 1)] * 2 + [("B", 2)] * 3)
    check("mixed design is not confounded", perfectly_confounded(*mixed), False)
    check("V for [[3,2],[2,3]] is sqrt(0.4 / 10) = 0.2", cramers_v(*mixed), 0.2, 1e-12)
    balanced = contingency([("A", 1)] * 2 + [("A", 2)] * 2 + [("B", 1)] * 2 + [("B", 2)] * 2)
    check("balanced design has V = 0", cramers_v(*balanced), 0.0, 1e-12)
    check("a single group cannot be confounded", perfectly_confounded(*contingency([("A", 1), ("A", 2)])), False)
    print("design.py self-test: %d checks passed" % n[0])


def _read_rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sample size, power and batch layout.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("n")
    s.add_argument("--d", type=float, required=True)
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.8)
    s.add_argument("--tests", type=int, default=1)
    s = sub.add_parser("power")
    s.add_argument("--n", type=int, required=True)
    s.add_argument("--d", type=float, required=True)
    s.add_argument("--alpha", type=float, default=0.05)
    s = sub.add_parser("assign")
    s.add_argument("csv", help="CSV with columns sample and group")
    s.add_argument("--batches", type=int, required=True)
    s.add_argument("--seed", type=int, default=1)
    s = sub.add_parser("confound")
    s.add_argument("csv")
    s.add_argument("--group", required=True)
    s.add_argument("--batch", required=True)
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    try:
        if a.cmd == "n":
            print("%d per group (%d in total) for d = %g, alpha = %g over %d test(s), power %g" % (
                n_per_group(a.d, a.alpha, a.power, a.tests), 2 * n_per_group(a.d, a.alpha, a.power, a.tests),
                a.d, a.alpha, a.tests, a.power))
        elif a.cmd == "power":
            print("power %.3f with %d per group at d = %g, alpha = %g" % (power_for(a.n, a.d, a.alpha), a.n, a.d, a.alpha))
        elif a.cmd == "assign":
            rows = _read_rows(a.csv)
            layout = assign_to_batches([(r["sample"], r["group"]) for r in rows], a.batches, a.seed)
            print("sample,group,batch")
            for r in rows:
                print("%s,%s,%d" % (r["sample"], r["group"], layout[r["sample"]] + 1))
        elif a.cmd == "confound":
            rows = _read_rows(a.csv)
            table, groups, batches = contingency([(r[a.group], r[a.batch]) for r in rows])
            print("\t" + "\t".join(batches))
            for g in groups:
                print(g + "\t" + "\t".join(str(table[g][b]) for b in batches))
            print("Cramer's V %.3f; perfectly confounded: %s" % (
                cramers_v(table, groups, batches), perfectly_confounded(table, groups, batches)))
        else:
            ap.print_help()
            return 2
    except (ValueError, KeyError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
