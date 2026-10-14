#!/usr/bin/env python3
"""Systems-theory checks for linear models (standard library only).

  control.py ctrb "A" "B"                controllability matrix rank (Kalman)
  control.py obsv "A" "C"                observability matrix rank
  control.py routh "1,6,11,6"            Routh-Hurwitz test of a characteristic polynomial (highest power first)
  control.py tf "1" "1,3,2"              poles, zeros and steady-state gain of a transfer function num/den
  control.py second --wn 2 --zeta 0.3    overshoot, peak time and settling time of a second-order system
  control.py loop --K 4 --tau 10         unity-feedback loop around K/(tau s + 1): closed-loop gain and time constant
  control.py --selftest

Matrices are written row by row with commas and semicolons, for example "0,1;-2,-3". Ranks use exact fractions.
The second-order formulas are the standard ones for an underdamped system (0 < zeta < 1) with no zeros; the settling
time uses the 2 percent rule of thumb 4 / (zeta wn), which is an approximation.
"""
import argparse
import cmath
import math
import sys
from fractions import Fraction


def parse(text):
    rows = [r for r in text.strip().split(";") if r.strip()]
    m = [[Fraction(x.strip()) for x in r.split(",")] for r in rows]
    if not m or any(len(r) != len(m[0]) for r in m):
        raise ValueError("rows must have the same number of entries")
    return m


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def rank(m):
    a = [row[:] for row in m]
    rows, cols = len(a), len(a[0])
    r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if a[i][c] != 0), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for i in range(rows):
            if i != r and a[i][c] != 0:
                f = a[i][c] / a[r][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == rows:
            break
    return r


def ctrb(a, b):
    n = len(a)
    if len(b) != n:
        raise ValueError("B needs as many rows as A")
    blocks, cur = [], b
    for _ in range(n):
        blocks.append(cur)
        cur = matmul(a, cur)
    return [sum((blk[i] for blk in blocks), []) for i in range(n)]


def obsv(a, c):
    n = len(a)
    if len(c[0]) != n:
        raise ValueError("C needs as many columns as A")
    rows, cur = [], c
    for _ in range(n):
        rows.extend(cur)
        cur = matmul(cur, a)
    return rows


def routh(coeffs, eps=Fraction(1, 10 ** 9)):
    """Routh array for a polynomial with real coefficients (highest power first). Returns (first column, sign changes,
    note). The number of sign changes in the first column equals the number of roots with positive real part."""
    c = [Fraction(x) for x in coeffs]
    while c and c[0] == 0:
        c.pop(0)
    n = len(c) - 1
    if n < 1:
        raise ValueError("need a polynomial of degree 1 or more")
    r0, r1 = c[0::2], c[1::2]
    width = len(r0)
    r1 += [Fraction(0)] * (width - len(r1))
    table = [r0, r1]
    note = ""
    for _ in range(n - 1):
        a, b = table[-2], table[-1]
        if b[0] == 0:
            if all(x == 0 for x in b):
                note = "a row of zeros appeared: roots symmetric about the origin (for example on the imaginary axis)"
                # replace with the derivative of the auxiliary polynomial
                order = n - len(table) + 2
                b = [x * (order - 2 * i) for i, x in enumerate(a)]
                table[-1] = b
            else:
                note = "a zero in the first column was replaced by a small positive number"
                b = [eps] + b[1:]
                table[-1] = b
        new = [(b[0] * a[i + 1] - a[0] * b[i + 1]) / b[0] if i + 1 < width else Fraction(0) for i in range(width)]
        table.append(new)
    first = [row[0] for row in table]
    signs = [1 if x > 0 else -1 for x in first if x != 0]
    changes = sum(1 for p, q in zip(signs, signs[1:]) if p != q)
    return first, changes, note


def roots(coeffs):
    c = [complex(x) for x in coeffs]
    while c and c[0] == 0:
        c.pop(0)
    n = len(c) - 1
    if n < 1:
        return []
    c = [x / c[0] for x in c]
    z = [complex(0.4, 0.9) ** k for k in range(n)]
    for _ in range(2000):
        new = []
        for i in range(n):
            num = sum(ck * z[i] ** (n - k) for k, ck in enumerate(c))
            den = 1
            for j in range(n):
                if j != i:
                    den *= z[i] - z[j]
            new.append(z[i] - num / den if den != 0 else z[i] + 1e-9)
        done = max(abs(p - q) for p, q in zip(new, z)) < 1e-15
        z = new
        if done:
            break
    return sorted((complex(round(r.real, 9), round(r.imag, 9)) for r in z), key=lambda v: (v.real, v.imag))


def second_order(wn, zeta):
    if wn <= 0 or not 0 < zeta < 1:
        raise ValueError("these formulas need wn > 0 and 0 < zeta < 1 (underdamped)")
    wd = wn * math.sqrt(1 - zeta ** 2)
    return {"overshoot_percent": 100 * math.exp(-zeta * math.pi / math.sqrt(1 - zeta ** 2)),
            "peak_time": math.pi / wd, "settling_time_2pct": 4 / (zeta * wn), "damped_frequency": wd}


def unity_loop(k, tau):
    """Unity negative feedback around G = K/(tau s + 1): closed loop K/(1+K) / ((tau/(1+K)) s + 1)."""
    if tau <= 0 or k <= -1:
        raise ValueError("need tau > 0 and K > -1")
    return k / (1 + k), tau / (1 + k), 1 / (1 + k)


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=None):
        count[0] += 1
        ok = abs(got - want) <= tol if tol is not None else got == want
        if not ok:
            fails.append("%s: got %r, want %r" % (name, got, want))

    a = parse("0,1;-2,-3")
    eq("controllable from the second state", rank(ctrb(a, parse("0;1"))), 2)
    eq("uncontrollable decoupled input", rank(ctrb(parse("-1,0;0,-2"), parse("1;0"))), 1)
    eq("observable from the first state", rank(obsv(a, parse("1,0"))), 2)
    eq("unobservable decoupled output", rank(obsv(parse("-1,0;0,-2"), parse("1,0"))), 1)
    first, ch, note = routh([1, 6, 11, 6])
    eq("Routh stable (roots -1,-2,-3)", (ch, first), (0, [1, 6, 10, 6]))
    first, ch, note = routh([1, -1, 2])
    eq("Routh two unstable roots", ch, 2)
    first, ch, note = routh([1, 2, 3, 4, 5])
    eq("Routh quartic with two right-half-plane roots", ch, 2)
    first, ch, note = routh([1, 0, 1])
    eq("Routh imaginary pair flagged", ("zeros" in note, ch), (True, 0))
    eq("roots of s^2+3s+2", [r.real for r in roots([1, 3, 2])], [-2.0, -1.0])
    eq("roots of s^2+1", [r.imag for r in roots([1, 0, 1])], [-1.0, 1.0])
    so = second_order(2.0, 0.3)
    eq("overshoot zeta 0.3", so["overshoot_percent"], 37.2326, 1e-3)
    eq("peak time", so["peak_time"], math.pi / (2 * math.sqrt(0.91)), 1e-12)
    eq("settling time", so["settling_time_2pct"], 4 / 0.6, 1e-12)
    g, tc, err = unity_loop(4.0, 10.0)
    eq("feedback loop gain, time constant, error", (g, tc, err), (0.8, 2.0, 0.2))
    for bad, label in ((lambda: second_order(1, 1.2), "overdamped"), (lambda: routh([0, 0]), "degree 0"),
                       (lambda: ctrb(parse("1,0;0,1"), parse("1")), "B rows")):
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
    _first, _ch, _note = routh([1, 1, 1, 1])
    _same("zero row handled by the auxiliary polynomial: first column", _first, [1, 1, 2, 1])
    _same("zero row: no root in the right half-plane", _ch, 0)
    _same("zero row is reported", "row of zeros" in _note, True)
    _raises("critically damped is outside the formulas", lambda: second_order(2, 1))
    _raises("natural frequency must be positive", lambda: second_order(0, 0.5))
    _raises("time constant must be positive", lambda: unity_loop(4, 0))
    _raises("loop gain -1 has no closed-loop steady state", lambda: unity_loop(-1, 2))
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("control selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Systems-theory checks for linear models.")
    ap.add_argument("op", nargs="?", choices=["ctrb", "obsv", "routh", "tf", "second", "loop"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--wn", type=float)
    ap.add_argument("--zeta", type=float)
    ap.add_argument("--K", type=float)
    ap.add_argument("--tau", type=float)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.op:
        ap.error("give an operation or --selftest")
    try:
        if a.op in ("ctrb", "obsv"):
            A, M = parse(a.args[0]), parse(a.args[1])
            mat = ctrb(A, M) if a.op == "ctrb" else obsv(A, M)
            r, n = rank(mat), len(A)
            word = "controllable" if a.op == "ctrb" else "observable"
            print("rank %d of %d: %s" % (r, n, word if r == n else "not " + word))
        elif a.op == "routh":
            first, ch, note = routh([Fraction(x) for x in a.args[0].split(",")])
            print("first column: %s" % ", ".join(str(x) for x in first))
            print("%d sign change(s): %d root(s) with positive real part; %s" % (ch, ch, "stable" if ch == 0 and not note else "check the note" if note else "unstable"))
            if note:
                print("note: " + note)
        elif a.op == "tf":
            num = [float(x) for x in a.args[0].split(",")]
            den = [float(x) for x in a.args[1].split(",")]
            fmtc = lambda z: ("%.6g" % z.real) if abs(z.imag) < 1e-9 else "%.6g%+.6gi" % (z.real, z.imag)
            print("zeros: %s" % (", ".join(fmtc(z) for z in roots(num)) or "none"))
            poles = roots(den)
            print("poles: %s" % ", ".join(fmtc(p) for p in poles))
            if den[-1] != 0:
                print("steady-state gain (s = 0): %.6g" % (num[-1] / den[-1]))
            print("stable" if all(p.real < 0 for p in poles) else "not asymptotically stable (a pole has real part >= 0)")
        elif a.op == "second":
            for k, v in second_order(a.wn, a.zeta).items():
                print("%-20s %.6g" % (k, v))
        elif a.op == "loop":
            g, tc, err = unity_loop(a.K, a.tau)
            print("closed-loop gain %.6g, time constant %.6g (open loop %.6g), steady-state error %.6g of the set point" % (g, tc, a.tau, err))
    except (ValueError, IndexError, TypeError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
