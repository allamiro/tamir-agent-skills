#!/usr/bin/env python3
"""Enzyme rate laws and fitting (standard library only).

  kinetics.py rate mm --S 2 --Vmax 10 --Km 1
  kinetics.py rate competitive --S 2 --Vmax 10 --Km 1 --I 1 --Ki 0.5        (also uncompetitive, mixed --Ki --Kii)
  kinetics.py rate substrate-inhibition --S 2 --Vmax 10 --Km 1 --Ksi 5
  kinetics.py rate hill --S 2 --Vmax 10 --K 1 --n 2
  kinetics.py rate reversible --S 2 --P 1 --Vf 10 --Vr 4 --Ks 1 --Kp 2
  kinetics.py fit DATA.csv [--model mm|hill]      nonlinear least squares, compared with the Lineweaver-Burk estimate
  kinetics.py --selftest

DATA.csv has columns S,v (substrate concentration and initial rate), one measurement per row.

The fit is Levenberg-Marquardt on the untransformed rates. The Lineweaver-Burk (double reciprocal) estimate is shown
for comparison only: taking 1/v magnifies the error of the slowest, least precise measurements, so it is a poor way
to estimate parameters even though it is a clear way to draw them.
"""
import argparse
import csv
import math
import sys


def mm(S, Vmax, Km):
    return Vmax * S / (Km + S)


def competitive(S, Vmax, Km, I, Ki):
    return Vmax * S / (Km * (1 + I / Ki) + S)


def uncompetitive(S, Vmax, Km, I, Kii):
    return Vmax * S / (Km + S * (1 + I / Kii))


def mixed(S, Vmax, Km, I, Ki, Kii):
    """Ki for binding to free enzyme, Kii for binding to the enzyme-substrate complex; Ki = Kii is noncompetitive."""
    return Vmax * S / (Km * (1 + I / Ki) + S * (1 + I / Kii))


def substrate_inhibition(S, Vmax, Km, Ksi):
    return Vmax * S / (Km + S + S * S / Ksi)


def hill(S, Vmax, K, n):
    return Vmax * S ** n / (K ** n + S ** n)


def reversible(S, P, Vf, Vr, Ks, Kp):
    """Reversible Michaelis-Menten in the form v = (Vf S/Ks - Vr P/Kp) / (1 + S/Ks + P/Kp)."""
    return (Vf * S / Ks - Vr * P / Kp) / (1 + S / Ks + P / Kp)


def linreg(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    if sxx == 0:
        raise ValueError("x values must differ")
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sxx
    return slope, my - slope * mx


def lineweaver_burk(S, v):
    """Vmax and Km from the double-reciprocal regression 1/v = (Km/Vmax)(1/S) + 1/Vmax."""
    slope, icpt = linreg([1 / s for s in S], [1 / r for r in v])
    if icpt <= 0:
        raise ValueError("double-reciprocal intercept is not positive; the data do not fit this form")
    vmax = 1 / icpt
    return vmax, slope * vmax


def solve(a, b):
    n = len(a)
    m = [row[:] + [bi] for row, bi in zip(a, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(m[i][c]))
        if abs(m[p][c]) < 1e-300:
            raise ValueError("singular system")
        m[c], m[p] = m[p], m[c]
        for i in range(n):
            if i != c:
                f = m[i][c] / m[c][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def levenberg_marquardt(f, params, xs, ys, iters=500, tol=1e-13):
    """Least-squares fit of ys ~ f(x, *params). Returns (params, residual sum of squares)."""
    p = list(params)
    lam = 1e-3

    def rss(q):
        return sum((y - f(x, *q)) ** 2 for x, y in zip(xs, ys))
    cur = rss(p)
    for _ in range(iters):
        jac = []
        for x in xs:
            row = []
            for j in range(len(p)):
                h = 1e-7 * max(1.0, abs(p[j]))
                q1, q2 = list(p), list(p)
                q1[j] += h
                q2[j] -= h
                row.append((f(x, *q1) - f(x, *q2)) / (2 * h))
            jac.append(row)
        r = [y - f(x, *p) for x, y in zip(xs, ys)]
        jtj = [[sum(jac[k][i] * jac[k][j] for k in range(len(xs))) for j in range(len(p))] for i in range(len(p))]
        jtr = [sum(jac[k][i] * r[k] for k in range(len(xs))) for i in range(len(p))]
        improved = False
        while lam < 1e12:
            a = [[jtj[i][j] + (lam * jtj[i][i] if i == j else 0) for j in range(len(p))] for i in range(len(p))]
            try:
                step = solve(a, jtr)
            except ValueError:
                lam *= 10
                continue
            q = [pi + si for pi, si in zip(p, step)]
            try:
                new = rss(q)
            except (ZeroDivisionError, OverflowError, ValueError):
                new = float("inf")
            if new < cur:
                done = cur - new < tol * max(1.0, cur)
                p, cur, lam = q, new, lam / 10
                improved = True
                break
            lam *= 10
        if not improved or done:
            break
    return p, cur


def fit(S, v, model="mm"):
    if len(S) < 3:
        raise ValueError("need at least 3 points")
    vmax0 = max(v) * 1.1
    half = min(range(len(v)), key=lambda i: abs(v[i] - max(v) / 2))
    km0 = max(S[half], 1e-9)
    if model == "mm":
        p, r = levenberg_marquardt(lambda s, a, b: mm(s, a, b), [vmax0, km0], S, v)
    elif model == "hill":
        p, r = levenberg_marquardt(lambda s, a, b, c: hill(s, a, b, c), [vmax0, km0, 1.0], S, v)
    else:
        raise ValueError("model must be mm or hill")
    return p, r


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=1e-9):
        count[0] += 1
        if abs(got - want) > tol:
            fails.append("%s: got %r, want %r" % (name, got, want))

    eq("MM at S = Km is half Vmax", mm(2, 10, 2), 5)
    eq("MM saturates", mm(1e9, 10, 2), 10, 1e-6)
    eq("competitive raises apparent Km", competitive(2, 10, 1, 1, 0.5), 10 * 2 / (3 + 2))
    eq("uncompetitive", uncompetitive(2, 10, 1, 1, 1), 10 * 2 / (1 + 4))
    eq("mixed reduces to competitive when Kii is huge", mixed(2, 10, 1, 1, 0.5, 1e12), competitive(2, 10, 1, 1, 0.5), 1e-9)
    eq("noncompetitive halves Vmax at I = Ki", mixed(1e9, 10, 1, 1, 1, 1), 5, 1e-6)
    eq("substrate inhibition peaks at sqrt(Km Ksi)", max(range(1, 1000), key=lambda i: substrate_inhibition(i / 100, 10, 1, 4)) / 100, 2.0, 0.011)
    eq("Hill at S = K is half Vmax", hill(3, 10, 3, 4), 5)
    eq("Hill n = 1 is MM", hill(2, 10, 1, 1), mm(2, 10, 1))
    eq("reversible rate zero at equilibrium", reversible(2, 2 * (10 / 1) / (4 / 2) / 1, 10, 4, 1, 2), 0, 1e-12)
    S = [0.25, 0.5, 1, 2, 4, 8]
    v = [mm(s, 10, 1.5) for s in S]
    vm, km = lineweaver_burk(S, v)
    eq("Lineweaver-Burk exact on noiseless data Vmax", vm, 10, 1e-9)
    eq("Lineweaver-Burk exact on noiseless data Km", km, 1.5, 1e-9)
    (fv, fk), r = fit(S, v)
    eq("LM recovers Vmax", fv, 10, 1e-6)
    eq("LM recovers Km", fk, 1.5, 1e-6)
    noisy = [vi * f for vi, f in zip(v, [1.25, 0.95, 1.02, 0.98, 1.01, 0.99])]   # the slowest point is 25 % high
    (nv, nk), r = fit(S, noisy)
    lv, lk = lineweaver_burk(S, noisy)
    eq("one bad slow point moves Lineweaver-Burk Km more than the direct fit", abs(lk - 1.5) > abs(nk - 1.5), 1, 0)
    (hv, hk, hn), r = fit(S, [hill(s, 8, 2, 2.5) for s in S], "hill")
    eq("Hill fit recovers n", hn, 2.5, 1e-4)
    count[0] += 1
    try:
        lineweaver_burk([1, 2], [1, 3])
        fails.append("a negative double-reciprocal intercept should raise")
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
    _near("reversible MM (20 - 2) / 3.5", reversible(2, 1, 10, 4, 1, 2), 18 / 3.5)
    _near("reversible MM with Ks = 2, Kp = 4: (10 - 1) / 2.25", reversible(2, 1, 10, 4, 2, 4), 4.0)
    _p3, _rss3 = fit([0.5, 1, 4], [mm(s, 10, 1) for s in [0.5, 1, 4]])
    _near("three exact points are enough to fit Vmax", _p3[0], 10, 1e-6)
    _vm, _km = lineweaver_burk([0.5, 1, 2, 4], [mm(s, 10, 1) for s in [0.5, 1, 2, 4]])
    _near("Lineweaver-Burk Vmax on exact data", _vm, 10)
    _near("Lineweaver-Burk Km on exact data", _km, 1)
    _near("mixed inhibition with Ki = Kii = 1, I = 1 halves Vmax and keeps Km", mixed(1, 10, 1, 1, 1, 1), 2.5)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("kinetics selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Enzyme rate laws and fitting.")
    ap.add_argument("op", nargs="?", choices=["rate", "fit"])
    ap.add_argument("what", nargs="?")
    for name in ("S", "P", "Vmax", "Km", "I", "Ki", "Kii", "Ksi", "K", "n", "Vf", "Vr", "Ks", "Kp"):
        ap.add_argument("--" + name, type=float)
    ap.add_argument("--model", default="mm")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        if a.op == "rate":
            fn = {"mm": lambda: mm(a.S, a.Vmax, a.Km), "competitive": lambda: competitive(a.S, a.Vmax, a.Km, a.I, a.Ki),
                  "uncompetitive": lambda: uncompetitive(a.S, a.Vmax, a.Km, a.I, a.Kii),
                  "mixed": lambda: mixed(a.S, a.Vmax, a.Km, a.I, a.Ki, a.Kii),
                  "substrate-inhibition": lambda: substrate_inhibition(a.S, a.Vmax, a.Km, a.Ksi),
                  "hill": lambda: hill(a.S, a.Vmax, a.K, a.n),
                  "reversible": lambda: reversible(a.S, a.P, a.Vf, a.Vr, a.Ks, a.Kp)}.get(a.what)
            if fn is None:
                raise ValueError("rate law must be one of mm, competitive, uncompetitive, mixed, substrate-inhibition, hill, reversible")
            print("v = %.6g" % fn())
        elif a.op == "fit":
            rows = list(csv.DictReader(open(a.what, newline="", encoding="utf-8")))
            S = [float(r["S"]) for r in rows]
            v = [float(r["v"]) for r in rows]
            p, r = fit(S, v, a.model)
            names = ["Vmax", "Km"] if a.model == "mm" else ["Vmax", "K", "n"]
            print("nonlinear least squares (%s): %s; residual sum of squares %.6g" % (a.model, ", ".join("%s = %.6g" % kv for kv in zip(names, p)), r))
            if a.model == "mm":
                vm, km = lineweaver_burk(S, v)
                print("Lineweaver-Burk regression for comparison: Vmax = %.6g, Km = %.6g (biased by the slowest points)" % (vm, km))
        else:
            ap.error("give rate or fit, or --selftest")
    except (ValueError, TypeError, OSError, KeyError, ZeroDivisionError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
