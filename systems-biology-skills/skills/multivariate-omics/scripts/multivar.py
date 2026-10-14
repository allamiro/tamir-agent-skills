#!/usr/bin/env python3
"""PCA, PLS regression and VIP scores for small tables (standard library only).

  multivar.py pca DATA.csv [--scale] [--components 3]        explained variance, loadings and scores
  multivar.py pls DATA.csv --y COLUMN [--components 2] [--scale]   PLS1 regression with VIP scores
  multivar.py --selftest

DATA.csv: one row per sample, one numeric column per variable (a first column called sample or id is ignored). Data
are always centred; --scale also divides each variable by its standard deviation, which you want when variables have
different units. The eigen-decomposition is the Jacobi method on the covariance matrix and PLS is the NIPALS
algorithm, fine for tens to a few hundred variables. For omics tables with thousands of features, use a library
(for example scikit-learn) and keep this for checking.

A VIP above about 1 is the common rule of thumb for an influential variable; it is a heuristic, not a test.
"""
import argparse
import csv
import math
import sys


def read_table(path, y=None):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    if not rows:
        raise ValueError("empty table")
    cols = [c for c in rows[0] if c.lower() not in ("sample", "id")]
    if y and y not in cols:
        raise ValueError("no column %r" % y)
    xcols = [c for c in cols if c != y]
    X = [[float(r[c]) for c in xcols] for r in rows]
    Y = [float(r[y]) for r in rows] if y else None
    return xcols, X, Y


def centre(X, scale=False):
    n, p = len(X), len(X[0])
    means = [sum(r[j] for r in X) / n for j in range(p)]
    sds = []
    for j in range(p):
        v = sum((r[j] - means[j]) ** 2 for r in X) / (n - 1)
        sds.append(math.sqrt(v) if v > 0 else 1.0)
    return [[(r[j] - means[j]) / (sds[j] if scale else 1.0) for j in range(p)] for r in X], means, sds


def jacobi_eigen(a, tol=1e-12, maxit=200):
    """Eigenvalues and eigenvectors (columns) of a symmetric matrix, sorted by decreasing eigenvalue."""
    n = len(a)
    a = [row[:] for row in a]
    v = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(maxit):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    vals = [a[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: -vals[i])
    return [vals[i] for i in order], [[v[k][i] for i in order] for k in range(n)]


def pca(X, scale=False):
    Z, _m, _s = centre(X, scale)
    n, p = len(Z), len(Z[0])
    cov = [[sum(r[i] * r[j] for r in Z) / (n - 1) for j in range(p)] for i in range(p)]
    vals, vecs = jacobi_eigen(cov)
    vals = [max(v, 0.0) for v in vals]
    total = sum(vals)
    # fix the sign so each loading vector's largest entry is positive (signs are arbitrary)
    for k in range(p):
        col = [vecs[i][k] for i in range(p)]
        j = max(range(p), key=lambda i: abs(col[i]))
        if col[j] < 0:
            for i in range(p):
                vecs[i][k] = -vecs[i][k]
    scores = [[sum(r[i] * vecs[i][k] for i in range(p)) for k in range(p)] for r in Z]
    return vals, [v / total if total else 0 for v in vals], vecs, scores


def pls1(X, y, ncomp=2, scale=False):
    """NIPALS PLS1. Returns (coefficients on the processed X scale, VIP per variable, R^2 of y per component)."""
    Z, _m, _s = centre(X, scale)
    n, p = len(Z), len(Z[0])
    ym = sum(y) / n
    yv = [v - ym for v in y]
    E = [r[:] for r in Z]
    f = yv[:]
    W, P, Q, T = [], [], [], []
    ss_y = sum(v * v for v in yv)
    r2 = []
    for _ in range(min(ncomp, p, n - 1)):
        w = [sum(E[i][j] * f[i] for i in range(n)) for j in range(p)]
        norm = math.sqrt(sum(x * x for x in w))
        if norm < 1e-14:
            break
        w = [x / norm for x in w]
        t = [sum(E[i][j] * w[j] for j in range(p)) for i in range(n)]
        tt = sum(x * x for x in t)
        pl = [sum(E[i][j] * t[i] for i in range(n)) / tt for j in range(p)]
        q = sum(f[i] * t[i] for i in range(n)) / tt
        E = [[E[i][j] - t[i] * pl[j] for j in range(p)] for i in range(n)]
        f = [f[i] - q * t[i] for i in range(n)]
        W.append(w)
        P.append(pl)
        Q.append(q)
        T.append(t)
        r2.append(1 - sum(x * x for x in f) / ss_y if ss_y else 0.0)
    a = len(W)
    # coefficients B = W (P' W)^-1 q
    pw = [[sum(P[i][j] * W[k][j] for j in range(p)) for k in range(a)] for i in range(a)]
    inv = invert(pw)
    coef = [sum(W[k][j] * sum(inv[k][m] * Q[m] for m in range(a)) for k in range(a)) for j in range(p)]
    ssy_comp = [Q[k] ** 2 * sum(x * x for x in T[k]) for k in range(a)]
    tot = sum(ssy_comp)
    vip = [math.sqrt(p * sum(ssy_comp[k] * W[k][j] ** 2 for k in range(a)) / tot) if tot else 0.0 for j in range(p)]
    return coef, vip, r2


def invert(m):
    n = len(m)
    a = [row[:] + [float(i == j) for j in range(n)] for i, row in enumerate(m)]
    for c in range(n):
        piv = max(range(c, n), key=lambda i: abs(a[i][c]))
        if abs(a[piv][c]) < 1e-14:
            raise ValueError("singular matrix in PLS")
        a[c], a[piv] = a[piv], a[c]
        pv = a[c][c]
        a[c] = [x / pv for x in a[c]]
        for i in range(n):
            if i != c:
                fct = a[i][c]
                a[i] = [x - fct * y for x, y in zip(a[i], a[c])]
    return [row[n:] for row in a]


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=1e-9):
        count[0] += 1
        if abs(got - want) > tol:
            fails.append("%s: got %r, want %r" % (name, got, want))

    vals, vecs = jacobi_eigen([[2.0, 1.0], [1.0, 2.0]])
    eq("Jacobi eigenvalue 3", vals[0], 3.0)
    eq("Jacobi eigenvalue 1", vals[1], 1.0)
    X = [[1, 2], [2, 4], [3, 6], [4, 8]]
    vals, frac, vecs, scores = pca(X)
    eq("collinear data: PC1 explains everything", frac[0], 1.0)
    eq("PC1 direction (1,2)/sqrt5", vecs[1][0] / vecs[0][0], 2.0)
    X = [[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0], [2.3, 2.7], [2.0, 1.6], [1.0, 1.1], [1.5, 1.6], [1.1, 0.9]]
    vals, frac, vecs, scores = pca(X)
    eq("classic PCA example eigenvalue 1", vals[0], 1.28402771, 1e-7)
    eq("classic PCA example eigenvalue 2", vals[1], 0.0490833989, 1e-8)
    eq("scores have variance equal to eigenvalues", sum(s[0] ** 2 for s in scores) / (len(scores) - 1), vals[0], 1e-9)
    vals_s, frac_s, _v, _s = pca(X, scale=True)
    eq("scaled PCA eigenvalues sum to the number of variables", sum(vals_s), 2.0, 1e-9)
    Xp = [[1, 0, 3], [2, 1, 1], [3, 0, 2], [4, 1, 5], [5, 0, 4], [6, 1, 6]]
    y = [2 * r[0] + 0.0 * r[1] for r in Xp]
    coef, vip, r2 = pls1(Xp, y, ncomp=3)
    eq("PLS recovers an exact linear model", sum(c * (r[j] - sum(rr[j] for rr in Xp) / 6) for j, c in enumerate(coef) for r in Xp[:1]) + sum(y) / 6, y[0], 1e-6)
    eq("PLS full-rank R^2 is 1", r2[-1], 1.0, 1e-9)
    eq("VIP of the driving variable exceeds 1", vip[0] > 1, 1, 0)
    eq("mean squared VIP is 1", sum(v * v for v in vip) / len(vip), 1.0, 1e-9)
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
    _X = [[1, 2], [2, 1], [3, 5], [4, 3], [5, 6]]
    _y = [r[0] + r[1] for r in _X]
    _coef, _vip, _r2 = pls1(_X, _y, 2)
    _near("PLS with all components fits an exact linear y", _r2[-1], 1.0, 1e-9)
    _same("R2 never exceeds 1 and grows with components", all(0 <= a <= b <= 1 + 1e-12 for a, b in zip(_r2, _r2[1:])), True)
    _near("coefficient of x1 is 1", _coef[0], 1.0, 1e-9)
    _c1, _v1, _r1 = pls1([[1], [2], [3], [4]], [1, 3, 2, 4], 1)
    _near("one-variable PLS equals OLS: R2 = r^2 = 0.64", _r1[0], 0.64, 1e-9)
    _near("one-variable PLS slope 0.8", _c1[0], 0.8, 1e-9)
    _c2, _v2, _r2b = pls1(_X, [3, 2, 9, 6, 12], 1)
    _near("VIP of x1, one component (scikit-learn reference)", _v2[0], 0.76509822, 1e-6)
    _near("VIP of x2, one component (scikit-learn reference)", _v2[1], 1.18937997, 1e-6)
    _c2, _v2, _r2b = pls1(_X, [3, 2, 9, 6, 12], 2)
    _near("VIP of x1, two components (scikit-learn reference)", _v2[0], 0.7707188, 1e-6)
    _near("PLS coefficient of x2, two components (scikit-learn reference)", _c2[1], 1.69444444, 1e-6)
    _vals, _frac, _vecs, _sc = pca(_X)
    _same("each loading vector's largest entry is positive", all(max((_vecs[i][k] for i in range(2)), key=abs) > 0 for k in range(2)), True)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("multivar selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="PCA, PLS regression and VIP scores for small tables.")
    ap.add_argument("op", nargs="?", choices=["pca", "pls"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--y")
    ap.add_argument("--components", type=int, default=2)
    ap.add_argument("--scale", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        if a.op == "pca":
            names, X, _ = read_table(a.file)
            vals, frac, vecs, scores = pca(X, a.scale)
            k = min(a.components, len(vals))
            print("component  eigenvalue  explained  cumulative")
            cum = 0
            for i in range(len(vals)):
                cum += frac[i]
                print("PC%-8d %10.4g %9.1f%% %10.1f%%" % (i + 1, vals[i], 100 * frac[i], 100 * cum))
            print("loadings (first %d components):" % k)
            for j, nm in enumerate(names):
                print("  %-16s %s" % (nm, " ".join("%8.4f" % vecs[j][c] for c in range(k))))
        elif a.op == "pls":
            if not a.y:
                raise ValueError("give --y")
            names, X, y = read_table(a.file, a.y)
            coef, vip, r2 = pls1(X, y, a.components, a.scale)
            print("R^2 of %s after each component: %s" % (a.y, ", ".join("%.3f" % v for v in r2)))
            print("variable            coefficient     VIP")
            for nm, c, v in sorted(zip(names, coef, vip), key=lambda t: -t[2]):
                print("  %-16s %12.4g %8.3f%s" % (nm, c, v, "  (above 1)" if v > 1 else ""))
            print("R^2 here is on the training data; judge prediction with cross-validation, not with this number.")
        else:
            ap.error("give pca or pls, or --selftest")
    except (ValueError, OSError, KeyError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
