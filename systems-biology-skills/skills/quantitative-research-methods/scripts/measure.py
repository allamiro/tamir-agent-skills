#!/usr/bin/env python3
"""Measurement checks for scored instruments, assays with several readouts and group comparisons
(standard library only).

  measure.py alpha ITEMS.csv            Cronbach's alpha, alpha if each item is dropped, item-rest correlations
  measure.py sb --r 0.7 --factor 2      Spearman-Brown: reliability when the test is lengthened by a factor
  measure.py effect A.csv B.csv         Cohen's d (pooled SD), Hedges' g, and an approximate 95% interval
  measure.py rasch ITEMS.csv            dichotomous Rasch fit by joint maximum likelihood: item difficulties,
                                        person locations, infit and outfit mean squares, and Yen's Q3 for
                                        local independence
  measure.py missing ITEMS.csv          the share and pattern of missing responses per item and per person
  measure.py --selftest

ITEMS.csv: one row per respondent (or sample), one column per item (or readout), a header row, empty cell or NA
for missing. For rasch the items are scored 0 or 1. A.csv and B.csv are one number per line.

These numbers support a validity argument; they are not one. Alpha is high for a long test of several
constructs, a good Rasch fit does not show the items measure what you meant, and joint maximum likelihood
difficulties are biased for short tests (multiply by (L-1)/L as a rough correction, L the number of items).
Yen's Q3 is biased too: with independent items it averages about -1/(L-1), so judge a pair against that baseline
(a pair well above it, for example 0.2 above, suggests local dependence).
"""
import argparse
import csv
import math
import sys


def read_items(path):
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    if len(rows) < 3:
        raise ValueError("need a header and at least two rows")
    header = [h.strip() for h in rows[0]]
    data = []
    for r in rows[1:]:
        if not any(c.strip() for c in r):
            continue
        if len(r) != len(header):
            raise ValueError("row %d has %d cells, header has %d" % (len(data) + 2, len(r), len(header)))
        data.append([None if c.strip() in ("", "NA", "na", "NaN") else float(c) for c in r])
    return header, data


def read_column(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip().split(",")[0]
        if line:
            try:
                out.append(float(line))
            except ValueError:
                pass  # header
    return out


def mean(xs):
    return sum(xs) / len(xs)


def var(xs):
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def corr(a, b):
    ma, mb = mean(a), mean(b)
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    saa = sum((x - ma) ** 2 for x in a)
    sbb = sum((y - mb) ** 2 for y in b)
    if saa == 0 or sbb == 0:
        return float("nan")
    return sab / math.sqrt(saa * sbb)


def complete(data):
    return [r for r in data if all(v is not None for v in r)]


def alpha(data):
    """Cronbach's alpha on complete rows: k/(k-1) * (1 - sum item variances / total variance)."""
    rows = complete(data)
    k = len(rows[0])
    if k < 2 or len(rows) < 2:
        raise ValueError("alpha needs at least two items and two complete rows")
    cols = list(zip(*rows))
    totals = [sum(r) for r in rows]
    vt = var(totals)
    if vt == 0:
        raise ValueError("total scores do not vary")
    return k / (k - 1) * (1 - sum(var(c) for c in cols) / vt), len(rows)


def alpha_report(data):
    a, n = alpha(data)
    rows = complete(data)
    k = len(rows[0])
    drops, rests = [], []
    for j in range(k):
        sub = [[v for i, v in enumerate(r) if i != j] for r in rows]
        drops.append(alpha(sub)[0] if k > 2 else float("nan"))
        rests.append(corr([r[j] for r in rows], [sum(v for i, v in enumerate(r) if i != j) for r in rows]))
    return a, n, drops, rests


def spearman_brown(r, factor):
    if not -1 < r < 1 or factor <= 0:
        raise ValueError("need -1 < r < 1 and a positive factor")
    return factor * r / (1 + (factor - 1) * r)


def effect(a, b):
    """Cohen's d with pooled SD, Hedges' g, and a normal-approximation 95% interval for g."""
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        raise ValueError("each group needs at least two values")
    sp = math.sqrt(((n1 - 1) * var(a) + (n2 - 1) * var(b)) / (n1 + n2 - 2))
    if sp == 0:
        raise ValueError("no variation within groups")
    d = (mean(a) - mean(b)) / sp
    j = 1 - 3 / (4 * (n1 + n2) - 9)
    g = j * d
    se = math.sqrt((n1 + n2) / (n1 * n2) + g * g / (2 * (n1 + n2)))
    return d, g, (g - 1.96 * se, g + 1.96 * se)


def rasch(data, iters=200, tol=1e-6):
    """Joint maximum likelihood for the dichotomous Rasch model, P(X=1) = exp(theta-delta)/(1+exp(theta-delta)).

    Persons with all-0 or all-1 scores and items everyone (or no one) got right have no finite estimate and are
    set aside and reported. Item difficulties are centred to mean 0. Missing cells are skipped.
    """
    persons = list(range(len(data)))
    items = list(range(len(data[0])))
    for r in data:
        for v in r:
            if v not in (None, 0.0, 1.0):
                raise ValueError("rasch needs items scored 0 or 1 (or missing)")
    dropped_p, dropped_i = [], []
    changed = True
    while changed:
        changed = False
        for p in list(persons):
            obs = [data[p][i] for i in items if data[p][i] is not None]
            if not obs or sum(obs) in (0, len(obs)):
                persons.remove(p)
                dropped_p.append(p)
                changed = True
        for i in list(items):
            obs = [data[p][i] for p in persons if data[p][i] is not None]
            if not obs or sum(obs) in (0, len(obs)):
                items.remove(i)
                dropped_i.append(i)
                changed = True
    if len(items) < 2 or len(persons) < 2:
        raise ValueError("too few items or persons with mixed responses to estimate")
    theta = {p: 0.0 for p in persons}
    delta = {i: 0.0 for i in items}

    def prob(t, d):
        return 1 / (1 + math.exp(-(t - d)))

    for _ in range(iters):
        biggest = 0.0
        for i in items:
            obs = [(p, data[p][i]) for p in persons if data[p][i] is not None]
            e = sum(prob(theta[p], delta[i]) for p, _ in obs)
            w = sum(prob(theta[p], delta[i]) * (1 - prob(theta[p], delta[i])) for p, _ in obs)
            step = (e - sum(x for _, x in obs)) / w
            step = max(-1.0, min(1.0, step))
            delta[i] += step
            biggest = max(biggest, abs(step))
        m = mean(list(delta.values()))
        for i in items:
            delta[i] -= m
        for p in persons:
            obs = [(i, data[p][i]) for i in items if data[p][i] is not None]
            e = sum(prob(theta[p], delta[i]) for i, _ in obs)
            w = sum(prob(theta[p], delta[i]) * (1 - prob(theta[p], delta[i])) for i, _ in obs)
            step = (sum(x for _, x in obs) - e) / w
            step = max(-1.0, min(1.0, step))
            theta[p] += step
            biggest = max(biggest, abs(step))
        if biggest < tol:
            break
    resid = {}
    fit = {}
    for i in items:
        z2, wsum, rsum, n = 0.0, 0.0, 0.0, 0
        for p in persons:
            x = data[p][i]
            if x is None:
                continue
            pr = prob(theta[p], delta[i])
            w = pr * (1 - pr)
            z2 += (x - pr) ** 2 / w
            rsum += (x - pr) ** 2
            wsum += w
            n += 1
            resid[(p, i)] = x - pr
        fit[i] = (rsum / wsum, z2 / n)  # infit, outfit mean squares
    q3 = []
    for a_ in range(len(items)):
        for b_ in range(a_ + 1, len(items)):
            i, j = items[a_], items[b_]
            pairs = [(resid[(p, i)], resid[(p, j)]) for p in persons if (p, i) in resid and (p, j) in resid]
            if len(pairs) > 2:
                q3.append((i, j, corr([x for x, _ in pairs], [y for _, y in pairs])))
    return {"delta": delta, "theta": theta, "fit": fit, "q3": q3, "dropped_persons": dropped_p, "dropped_items": dropped_i}


def missing(header, data):
    n = len(data)
    per_item = [(h, sum(1 for r in data if r[j] is None) / n) for j, h in enumerate(header)]
    per_person = [sum(1 for v in r if v is None) for r in data]
    # trailing runs: missing from some item to the end, a sign of not reaching the end rather than skipping
    trailing = 0
    for r in data:
        k = len(r)
        while k > 0 and r[k - 1] is None:
            k -= 1
        if k < len(r) and all(v is not None for v in r[:k]):
            trailing += 1
    return per_item, per_person, trailing


def selftest():
    fails, count = [], [0]

    def close(name, got, want, tol=1e-3):
        count[0] += 1
        if abs(got - want) > tol:
            fails.append("%s: got %.6f, want %.6f" % (name, got, want))

    # Hand-computed alpha: items 1,2,3 over rows (1,2,3),(2,3,4),(3,4,5),(4,4,4): item variances 1.6667, 0.9167,
    # 0.6667 sum 3.25; totals 6,9,12,12 variance 8.25; alpha = 1.5 * (1 - 3.25/8.25) = 0.909091.
    data = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 4, 4]]
    close("cronbach alpha", alpha(data)[0], 1.5 * (1 - 3.25 / 8.25))
    close("identical items give alpha 1", alpha([[1, 1], [2, 2], [3, 3]])[0], 1.0)
    close("Spearman-Brown doubling 0.5 gives 2/3", spearman_brown(0.5, 2), 2 / 3)
    close("Spearman-Brown halving 0.8 gives 2/3", spearman_brown(0.8, 0.5), 2 / 3)
    # d: means 3 and 2, both SD 1 (1,2,3,4,5 has SD 1.5811; use 2,3,4 and 1,2,3): pooled SD 1, d = 1.
    d, g, ci = effect([2, 3, 4], [1, 2, 3])
    close("Cohen's d", d, 1.0)
    close("Hedges' g with J = 1 - 3/(4*6-9) = 0.8", g, 0.8)
    # Rasch on a symmetric design: two items with opposite difficulty.
    rows = [[1, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1]]
    res = rasch(rows)
    close("difficulties centred to zero", sum(res["delta"].values()), 0.0)
    eq_pairs = sorted(res["delta"].items(), key=lambda kv: kv[1])
    count[0] += 1
    if eq_pairs[0][0] != 0:
        fails.append("item 0 is endorsed most often, so it should be easiest; got order %r" % eq_pairs)
    # A person who answered everything correctly cannot be located.
    res2 = rasch([[1, 1, 1], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1]])
    count[0] += 1
    if res2["dropped_persons"] != [0]:
        fails.append("the all-correct person should be set aside, got %r" % res2["dropped_persons"])
    # Two duplicated items show strong positive residual correlation (local dependence).
    import random
    rng = random.Random(4)
    sim = []
    for _ in range(300):
        t = rng.gauss(0, 1)
        row = [1.0 if rng.random() < 1 / (1 + math.exp(-(t - dd))) else 0.0 for dd in (-1, -0.5, 0, 0.5, 1)]
        row.append(row[2])  # item 6 copies item 3
        sim.append(row)
    q3 = {(i, j): r for i, j, r in rasch(sim)["q3"]}
    count[0] += 1
    if not q3.get((2, 5), 0) > 0.3:
        fails.append("a copied item should give Q3 above 0.3, got %r" % q3.get((2, 5)))
    per_item, per_person, trailing = missing(["a", "b", "c"], [[1, None, None], [1, 1, 1], [None, 1, 1], [1, 1, None]])
    close("missing share of item c", per_item[2][1], 0.5)
    count[0] += 1
    if trailing != 2:
        fails.append("two rows stop early, got %d" % trailing)
    for bad, label in ((lambda: alpha([[1, 2], [1, 2]]), "no variation"), (lambda: spearman_brown(1.0, 2), "r=1"),
                       (lambda: rasch([[2, 0], [1, 0]]), "non-binary"), (lambda: effect([1], [2, 3]), "n=1")):
        count[0] += 1
        try:
            bad()
            fails.append("%s should raise" % label)
        except ValueError:
            pass
    # Added after a mutation test: each case below is hand-computed and covers a path the earlier checks missed.
    def _near(label, got, want, tol=1e-6):
        count[0] += 1
        if not abs(got - want) <= tol:
            fails.append("%s: got %r, want %r" % (label, got, want))

    def _same(label, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (label, got, want))

    def _raises(label, fn):
        count[0] += 1
        try:
            fn()
            fails.append("%s should raise" % label)
        except (ValueError, ZeroDivisionError):
            pass
    _d, _g, _ci = effect([1, 2, 3, 4], [2, 4])
    _near("d with unequal groups uses the pooled SD", _d, -0.3779644730)
    _near("g with J = 0.8", _g, -0.3023715784)
    _near("interval lower bound", _ci[0], -2.0083813478)
    _near("interval upper bound", _ci[1], 1.4036381910)
    _rng2 = random.Random(9)
    _true = (-1.0, -0.5, 0.0, 0.5, 1.0)
    _sim2 = []
    for _ in range(400):
        _t = _rng2.gauss(0, 1)
        _sim2.append([1.0 if _rng2.random() < 1 / (1 + math.exp(-(_t - _dd))) else 0.0 for _dd in _true])
    _res = rasch(_sim2)
    _same("difficulties recovered in order", sorted(_res["delta"], key=_res["delta"].get), [0, 1, 2, 3, 4])
    _same("difficulties after the (L-1)/L correction within 0.2 of the truth", all(abs(_res["delta"][i] * 4 / 5 - _true[i]) < 0.2 for i in range(5)), True)
    _same("infit and outfit near 1 when the model holds", all(0.8 < a < 1.25 and 0.75 < b < 1.3 for a, b in _res["fit"].values()), True)
    _q3 = [r for _i, _j, r in _res["q3"]]
    _near("independent items: mean Q3 near its baseline -1/(L-1) = -0.25", sum(_q3) / len(_q3), -0.25, 0.08)
    _same("independent items: no Q3 above 0.1", max(_q3) < 0.1, True)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("measure selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Reliability, effect sizes, a Rasch fit and missing-data patterns.")
    ap.add_argument("op", nargs="?", choices=["alpha", "sb", "effect", "rasch", "missing"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--r", type=float)
    ap.add_argument("--factor", type=float)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        if a.op == "sb":
            print("reliability at %.3g times the length: %.4f" % (a.factor, spearman_brown(a.r, a.factor)))
        elif a.op == "effect":
            d, g, ci = effect(read_column(a.files[0]), read_column(a.files[1]))
            print("Cohen's d %.3f   Hedges' g %.3f   approximate 95%% interval for g %.3f to %.3f" % (d, g, ci[0], ci[1]))
        elif a.op in ("alpha", "rasch", "missing"):
            header, data = read_items(a.files[0])
            if a.op == "alpha":
                al, n, drops, rests = alpha_report(data)
                print("Cronbach's alpha %.4f on %d complete rows of %d (%d items)" % (al, n, len(data), len(header)))
                for h, dr, rr in zip(header, drops, rests):
                    print("  %-14s alpha if dropped %.4f   item-rest r %.3f" % (h, dr, rr))
            elif a.op == "rasch":
                res = rasch(data)
                print("item          difficulty   infit   outfit")
                for i, dd in sorted(res["delta"].items(), key=lambda kv: kv[1]):
                    print("  %-12s %8.3f   %5.2f   %5.2f" % (header[i], dd, res["fit"][i][0], res["fit"][i][1]))
                worst = sorted(res["q3"], key=lambda t: -t[2])[:3]
                print("largest residual correlations (Q3): " + ", ".join("%s-%s %.2f" % (header[i], header[j], r) for i, j, r in worst)
                      + "  (baseline for independent items about %.2f)" % (-1.0 / max(1, len(res["delta"]) - 1)))
                if res["dropped_items"] or res["dropped_persons"]:
                    print("set aside (extreme scores): items %s, %d persons" % ([header[i] for i in res["dropped_items"]], len(res["dropped_persons"])))
            else:
                per_item, per_person, trailing = missing(header, data)
                for h, s in per_item:
                    print("  %-14s missing %.1f%%" % (h, 100 * s))
                print("persons with any missing: %d of %d; stopping early (all missing from some item on): %d"
                      % (sum(1 for x in per_person if x), len(per_person), trailing))
        else:
            ap.error("give an operation or --selftest")
    except (ValueError, OSError, IndexError, TypeError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
