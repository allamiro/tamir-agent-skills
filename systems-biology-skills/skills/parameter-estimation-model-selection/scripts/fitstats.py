#!/usr/bin/env python3
"""Model selection statistics from least-squares fits (standard library only).

  fitstats.py ic --rss 1.2 --n 20 --k 3            AIC, AICc and BIC for one fit
  fitstats.py compare MODELS.csv                    rank models by AICc, with Akaike weights (columns: model,rss,n,k)
  fitstats.py ftest --rss1 4 --k1 2 --rss2 2.5 --k2 3 --n 20   nested models: F statistic and p-value
  fitstats.py --selftest

All three information criteria assume independent, normally distributed errors with constant variance, so that
the likelihood can be written from the residual sum of squares: AIC = n ln(RSS/n) + 2k. k counts every estimated
parameter, including the error variance if you estimated it; be consistent across the models you compare. Only
compare models fitted to the same data. AICc adds a small-sample correction and should be preferred when n/k is
below about 40 (a common rule of thumb). Differences matter, not absolute values.
"""
import argparse
import csv
import math
import sys


def ic(rss, n, k):
    if rss <= 0 or n <= 0 or k < 0:
        raise ValueError("need rss > 0, n > 0, k >= 0")
    aic = n * math.log(rss / n) + 2 * k
    aicc = aic + (2 * k * (k + 1) / (n - k - 1) if n - k - 1 > 0 else float("inf"))
    bic = n * math.log(rss / n) + k * math.log(n)
    return aic, aicc, bic


def weights(values):
    best = min(values)
    rel = [math.exp(-(v - best) / 2) for v in values]
    s = sum(rel)
    return [r / s for r in rel]


def betacf(a, b, x, maxit=300, eps=3e-16):
    """Continued fraction for the incomplete beta function (as in Numerical Recipes)."""
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, maxit + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-300 else 1e-300
        delta = d * c
        h *= delta
        if abs(delta - 1) < eps:
            break
    return h


def betainc(a, b, x):
    """Regularised incomplete beta I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lbt) * betacf(a, b, x) / a
    return 1 - math.exp(lbt) * betacf(b, a, 1 - x) / b


def f_sf(f, d1, d2):
    """Upper tail P(F > f) of the F distribution."""
    if f <= 0:
        return 1.0
    return betainc(d2 / 2.0, d1 / 2.0, d2 / (d2 + d1 * f))


def ftest(rss1, k1, rss2, k2, n):
    """Model 1 nested in model 2 (k1 < k2). Returns (F, p-value)."""
    if not k1 < k2 < n:
        raise ValueError("need k1 < k2 < n with model 1 nested in model 2")
    d1, d2 = k2 - k1, n - k2
    f = ((rss1 - rss2) / d1) / (rss2 / d2)
    return f, f_sf(f, d1, d2)


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=1e-9):
        count[0] += 1
        if abs(got - want) > tol:
            fails.append("%s: got %r, want %r" % (name, got, want))

    aic, aicc, bic = ic(2.0, 20, 2)
    eq("AIC", aic, 20 * math.log(0.1) + 4)
    eq("AICc correction", aicc - aic, 2 * 2 * 3 / 17)
    eq("BIC", bic, 20 * math.log(0.1) + 2 * math.log(20))
    w = weights([10.0, 12.0, 20.0])
    eq("weights sum to one", sum(w), 1.0)
    eq("weight ratio for delta 2", w[0] / w[1], math.e)
    eq("F tail at f=0", f_sf(0, 2, 10), 1.0)
    eq("F(1,inf) tail matches normal: P(F>3.841) about 0.05", f_sf(3.841458820694124, 1, 10 ** 7), 0.05, 1e-4)
    eq("F(2,10) critical value 4.1028 gives 0.05", f_sf(4.102821015130399, 2, 10), 0.05, 1e-7)
    eq("F(3,20) critical value 3.0984 gives 0.05", f_sf(3.0983912121407795, 3, 20), 0.05, 1e-7)
    f, p = ftest(4.0, 2, 2.5, 3, 20)
    eq("nested F statistic", f, (1.5 / 1) / (2.5 / 17))
    eq("nested p in range", 0 < p < 0.05, 1, 0)
    eq("incomplete beta symmetric", betainc(2, 2, 0.5), 0.5)
    for bad, label in ((lambda: ic(0, 10, 1), "rss 0"), (lambda: ftest(1, 3, 1, 2, 10), "not nested")):
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
    _same("AICc is infinite when n - k - 1 <= 0", ic(1.0, 4, 3)[1], float("inf"))
    _raises("RSS must be positive", lambda: ic(0, 10, 2))
    _raises("k cannot be negative", lambda: ic(1, 10, -1))
    _near("F with two extra parameters: (1.5/2)/(2.5/17)", ftest(4, 1, 2.5, 3, 20)[0], 0.75 / (2.5 / 17))
    _raises("nested models need k1 < k2", lambda: ftest(4, 2, 2.5, 2, 20))
    _near("F tail at 0 is 1", f_sf(0, 2, 10), 1.0)
    _raises("n must be positive", lambda: ic(1, 0, 1))
    _near("AIC for RSS 1.2, n 20, k 3", ic(1.2, 20, 3)[0], 20 * math.log(0.06) + 6)
    if fails:
        print("SELFTEST FAILED")
        for f_ in fails:
            print(" -", f_)
        return 1
    print("fitstats selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Model selection statistics from least-squares fits.")
    ap.add_argument("op", nargs="?", choices=["ic", "compare", "ftest"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--rss", type=float)
    ap.add_argument("--n", type=int)
    ap.add_argument("--k", type=int)
    ap.add_argument("--rss1", type=float)
    ap.add_argument("--rss2", type=float)
    ap.add_argument("--k1", type=int)
    ap.add_argument("--k2", type=int)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        if a.op == "ic":
            aic, aicc, bic = ic(a.rss, a.n, a.k)
            print("AIC %.4f   AICc %.4f   BIC %.4f   (n = %d, k = %d)" % (aic, aicc, bic, a.n, a.k))
        elif a.op == "compare":
            rows = list(csv.DictReader(open(a.file, newline="", encoding="utf-8")))
            if len({r["n"] for r in rows}) != 1:
                raise ValueError("all models must be fitted to the same data (same n)")
            vals = [(r["model"], ic(float(r["rss"]), int(r["n"]), int(r["k"]))) for r in rows]
            w = weights([v[1][1] for v in vals])
            best = min(v[1][1] for v in vals)
            print("%-20s %10s %10s %8s" % ("model", "AICc", "delta", "weight"))
            for (name, (aic, aicc, bic)), wi in sorted(zip(vals, w), key=lambda t: t[0][1][1]):
                print("%-20s %10.4f %10.4f %8.4f" % (name, aicc, aicc - best, wi))
            print("A delta under about 2 means little support for preferring one model over the other.")
        elif a.op == "ftest":
            f, p = ftest(a.rss1, a.k1, a.rss2, a.k2, a.n)
            print("F = %.4f on (%d, %d) degrees of freedom, p = %.4g" % (f, a.k2 - a.k1, a.n - a.k2, p))
        else:
            ap.error("give an operation or --selftest")
    except (ValueError, TypeError, OSError, KeyError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
