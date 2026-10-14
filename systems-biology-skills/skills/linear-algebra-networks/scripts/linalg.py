#!/usr/bin/env python3
"""Exact linear algebra for small biological network matrices (standard library only).

  linalg.py rref "1,2,3;4,5,6"           reduced row-echelon form, pivot columns and rank
  linalg.py rank "1,2;2,4"
  linalg.py det "2,1;1,3"
  linalg.py inv "2,1;1,3"
  linalg.py solve "1,1;1,-1" --b "3,1"   solve A x = b and classify it (Rouche-Capelli)
  linalg.py null "1,-1,0;0,1,-1"         basis of the right null space (A x = 0)
  linalg.py lu "4,3;6,3"                 LU factorisation with partial pivoting, P A = L U
  linalg.py eig "2,1;1,2"                characteristic polynomial and eigenvalues
  linalg.py --selftest

Matrices are written row by row: commas between entries, semicolons between rows. Entries may be
integers, decimals or fractions such as 1/3. Everything except eigenvalues is computed with exact
fractions, so there is no rounding in a rank or a null space. Eigenvalues are roots of the exact
characteristic polynomial, found numerically, and printed to 6 decimals; complex pairs are shown.
"""
import argparse
import cmath
import sys
from fractions import Fraction


def parse(text):
    rows = [r for r in text.strip().split(";") if r.strip()]
    m = [[Fraction(x.strip()) for x in r.split(",")] for r in rows]
    if not m or any(len(r) != len(m[0]) for r in m):
        raise ValueError("rows must have the same number of entries")
    return m


def fmt(x):
    return str(x) if not isinstance(x, complex) else ("%.6g%+.6gi" % (x.real, x.imag))


def show(m):
    return "\n".join("  [" + ", ".join(fmt(x) for x in r) + "]" for r in m)


def rref(m):
    """(reduced row-echelon form, pivot column indices)."""
    a = [row[:] for row in m]
    rows, cols = len(a), len(a[0])
    pivots, r = [], 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if a[i][c] != 0), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        pv = a[r][c]
        a[r] = [x / pv for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return a, pivots


def rank(m):
    return len(rref(m)[1])


def det(m):
    n = len(m)
    if any(len(r) != n for r in m):
        raise ValueError("determinant needs a square matrix")
    a = [row[:] for row in m]
    d = Fraction(1)
    for c in range(n):
        p = next((i for i in range(c, n) if a[i][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            a[c], a[p] = a[p], a[c]
            d = -d
        d *= a[c][c]
        for i in range(c + 1, n):
            f = a[i][c] / a[c][c]
            a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return d


def identity(n):
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def inverse(m):
    n = len(m)
    if det(m) == 0:
        raise ValueError("matrix is singular (determinant 0), so it has no inverse")
    aug = [row + idr for row, idr in zip(m, identity(n))]
    red, _ = rref(aug)
    return [r[n:] for r in red]


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def solve(a, b):
    """Return (kind, solution or None). kind is 'unique', 'infinite' or 'none' (Rouche-Capelli)."""
    if len(b) != len(a):
        raise ValueError("b needs one entry per row of A")
    ra = rank(a)
    rab = rank([row + [bi] for row, bi in zip(a, b)])
    n = len(a[0])
    if ra < rab:
        return "none", None
    red, piv = rref([row + [bi] for row, bi in zip(a, b)])
    x = [Fraction(0)] * n
    for i, c in enumerate(piv):
        x[c] = red[i][n]
    return ("unique" if ra == n else "infinite"), x


def nullspace(m):
    """Basis vectors v with m v = 0 (free variables set to 1 in turn)."""
    red, piv = rref(m)
    n = len(m[0])
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * n
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -red[i][f]
        basis.append(v)
    return basis


def lu(m):
    """Partial pivoting: returns (P, L, U) with P A = L U."""
    n = len(m)
    u = [row[:] for row in m]
    l = [[Fraction(0)] * n for _ in range(n)]
    perm = list(range(n))
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(u[i][c]))
        if u[p][c] == 0:
            raise ValueError("matrix is singular")
        u[c], u[p] = u[p], u[c]
        l[c], l[p] = l[p], l[c]
        perm[c], perm[p] = perm[p], perm[c]
        for i in range(c + 1, n):
            f = u[i][c] / u[c][c]
            l[i][c] = f
            u[i] = [x - f * y for x, y in zip(u[i], u[c])]
    for i in range(n):
        l[i][i] = Fraction(1)
    pm = [[Fraction(int(perm[i] == j)) for j in range(n)] for i in range(n)]
    return pm, l, u


def charpoly(m):
    """Coefficients [1, c1, ..., cn] of det(lambda I - A) by the Faddeev-LeVerrier recursion (exact)."""
    n = len(m)
    coeffs = [Fraction(1)]
    mk = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        mk = matmul(m, mk)
        mk = [[mk[i][j] + (coeffs[-1] if i == j else 0) for j in range(n)] for i in range(n)]
        am = matmul(m, mk)
        ck = -sum(am[i][i] for i in range(n)) / k
        coeffs.append(ck)
    return coeffs


def roots(coeffs, iters=500):
    """Roots of a monic polynomial by the Durand-Kerner iteration."""
    c = [complex(x) for x in coeffs]
    n = len(c) - 1
    if n == 0:
        return []
    z = [complex(0.4, 0.9) ** k for k in range(n)]
    for _ in range(iters):
        new = []
        for i in range(n):
            num = sum(c[k] * z[i] ** (n - k) for k in range(n + 1))
            den = 1
            for j in range(n):
                if j != i:
                    den *= (z[i] - z[j])
            new.append(z[i] - num / den if den != 0 else z[i] + 1e-9)
        if max(abs(a - b) for a, b in zip(new, z)) < 1e-14:
            z = new
            break
        z = new
    out = []
    for r in z:
        r = complex(round(r.real, 10), round(r.imag, 10))
        out.append(r.real if r.imag == 0 else r)
    return sorted(out, key=lambda v: (complex(v).real, complex(v).imag))


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=None):
        count[0] += 1
        if tol is not None:
            ok = all(abs(complex(a) - complex(b)) <= tol for a, b in zip(got, want)) and len(got) == len(want)
        else:
            ok = got == want
        if not ok:
            fails.append("%s: got %r, want %r" % (name, got, want))

    F = Fraction
    eq("parse fractions", parse("1/2, 0.25;3,4"), [[F(1, 2), F(1, 4)], [F(3), F(4)]])
    red, piv = rref(parse("1,2,3;4,5,6"))
    eq("rref", red, [[1, 0, -1], [0, 1, 2]])
    eq("pivots", piv, [0, 1])
    eq("rank full", rank(parse("1,2;3,4")), 2)
    eq("rank deficient", rank(parse("1,2;2,4")), 1)
    eq("rank zero", rank(parse("0,0;0,0")), 0)
    eq("det 2x2", det(parse("2,1;1,3")), 5)
    eq("det 3x3 Sarrus example", det(parse("1,2,3;0,1,4;5,6,0")), 1)
    eq("det row swap sign", det(parse("0,1;1,0")), -1)
    eq("det singular", det(parse("1,2;2,4")), 0)
    eq("inverse 2x2", inverse(parse("2,1;1,3")), [[F(3, 5), F(-1, 5)], [F(-1, 5), F(2, 5)]])
    eq("inverse times A is I", matmul(inverse(parse("1,2,3;0,1,4;5,6,0")), parse("1,2,3;0,1,4;5,6,0")), identity(3))
    eq("solve unique", solve(parse("1,1;1,-1"), [F(3), F(1)]), ("unique", [2, 1]))
    eq("solve none", solve(parse("1,1;2,2"), [F(1), F(3)])[0], "none")
    kind, x = solve(parse("1,1;2,2"), [F(2), F(4)])
    eq("solve infinite", (kind, x), ("infinite", [2, 0]))
    ns = nullspace(parse("1,-1,0;0,1,-1"))
    eq("null space of a chain", ns, [[1, 1, 1]])
    eq("null space vectors solve A v = 0", all(sum(a * b for a, b in zip(row, v)) == 0 for v in nullspace(parse("1,2,3;4,5,6")) for row in parse("1,2,3;4,5,6")), True)
    eq("rank-nullity", len(nullspace(parse("1,2,3,4;2,4,6,8"))) + rank(parse("1,2,3,4;2,4,6,8")), 4)
    p, l, u = lu(parse("4,3;6,3"))
    eq("LU reproduces PA", matmul(p, parse("4,3;6,3")), matmul(l, u))
    eq("LU pivots the larger entry", u[0][0], 6)
    eq("charpoly 2x2", charpoly(parse("2,1;1,2")), [1, -4, 3])
    cp = charpoly(parse("1,2,3;0,1,4;5,6,0"))
    eq("charpoly c1 is minus trace", cp[1], -2)
    eq("charpoly cn is (-1)^n det", cp[3], -det(parse("1,2,3;0,1,4;5,6,0")))
    eq("eigenvalues symmetric", roots(charpoly(parse("2,1;1,2"))), [1.0, 3.0], 1e-9)
    eq("eigenvalues rotation are complex", roots(charpoly(parse("0,-1;1,0"))), [complex(0, -1), complex(0, 1)], 1e-9)
    eq("eigenvalues triangular", roots(charpoly(parse("2,5,1;0,-1,3;0,0,4"))), [-1.0, 2.0, 4.0], 1e-8)
    for bad, label in ((lambda: parse("1,2;3"), "ragged"), (lambda: inverse(parse("1,2;2,4")), "singular inverse"),
                       (lambda: det(parse("1,2,3;4,5,6")), "non-square det")):
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
    _A = parse("1,2,3;4,5,6;7,8,10")
    _P, _L, _U = lu(_A)
    _same("P A = L U for a 3 x 3 that needs pivoting", matmul(_P, _A), matmul(_L, _U))
    _same("U is upper triangular", all(_U[i][j] == 0 for i in range(3) for j in range(i)), True)
    _same("determinant of a permutation matrix", det(parse("0,1;1,0")), -1)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("linalg selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Exact linear algebra for small biological network matrices.")
    ap.add_argument("op", nargs="?", choices=["rref", "rank", "det", "inv", "solve", "null", "lu", "eig"])
    ap.add_argument("matrix", nargs="?")
    ap.add_argument("--b", help="right-hand side for solve, comma separated")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.op or not a.matrix:
        ap.error("give an operation and a matrix, or --selftest")
    try:
        m = parse(a.matrix)
        if a.op == "rref":
            red, piv = rref(m)
            print(show(red))
            print("pivot columns (from 1): %s; rank %d" % ([p + 1 for p in piv], len(piv)))
        elif a.op == "rank":
            print("rank %d of a %d x %d matrix" % (rank(m), len(m), len(m[0])))
        elif a.op == "det":
            print("determinant %s" % det(m))
        elif a.op == "inv":
            print(show(inverse(m)))
        elif a.op == "solve":
            if not a.b:
                raise ValueError("give --b")
            kind, x = solve(m, [Fraction(v.strip()) for v in a.b.split(",")])
            msg = {"unique": "rank A = rank [A|b] = number of unknowns: one solution",
                   "infinite": "rank A = rank [A|b] < number of unknowns: infinitely many solutions; one of them (free variables 0)",
                   "none": "rank A < rank [A|b]: no solution"}[kind]
            print(msg)
            if x:
                print("  x = [%s]" % ", ".join(str(v) for v in x))
        elif a.op == "null":
            ns = nullspace(m)
            print("null space dimension %d" % len(ns))
            for v in ns:
                print("  [%s]" % ", ".join(str(x) for x in v))
        elif a.op == "lu":
            p, l, u = lu(m)
            print("P =\n%s\nL =\n%s\nU =\n%s" % (show(p), show(l), show(u)))
        elif a.op == "eig":
            cp = charpoly(m)
            print("characteristic polynomial coefficients (highest power first): %s" % ", ".join(str(c) for c in cp))
            print("eigenvalues: %s" % ", ".join(("%.6g" % r) if not isinstance(r, complex) else fmt(r) for r in roots(cp)))
    except (ValueError, ZeroDivisionError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
