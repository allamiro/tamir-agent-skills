#!/usr/bin/env python3
"""Quantity calculus, unit conversion and a chemostat balance (standard library only).

  units.py convert 5 mM --to mol/m^3          convert a value; refuses units of different dimension
  units.py dims "mmol/L/h"                    the dimension of a unit in base SI quantities
  units.py same "L/(mol*s)" "1/(M*s)"          do two units have the same dimension, and what factor links them
  units.py chemostat --D 0.2 --mumax 0.5 --Ks 0.1 --S0 10 --Y 0.5   Monod chemostat steady state
  units.py --selftest

Units are written with *, / and ^, with parentheses allowed, for example "mmol/(L*h)" or "mol*m^-3". Known symbols:
m, g, s, mol, K, A, cd, L, M (mol/L), min, h, d, Da (g/mol), N, J, W, Pa, Hz, with prefixes p n u m c k (u for micro;
"µ" and the Greek "μ" are accepted). Temperatures in degrees Celsius are not handled: they need an offset, not a factor.

The chemostat formulas are the standard Monod ones at steady state: growth rate equals dilution rate D, substrate
S* = Ks D / (mumax - D), biomass X* = Y (S0 - S*); washout happens when D is at or above mumax S0 / (Ks + S0).
"""
import argparse
import re
import sys

DIMS = ("L", "M", "T", "N", "Theta", "I", "J")   # length, mass, time, amount, temperature, current, luminous intensity
PREFIX = {"p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "μ": 1e-6, "m": 1e-3, "c": 1e-2, "k": 1e3}


def dimvec(**kw):
    return tuple(kw.get(d, 0) for d in DIMS)


UNITS = {
    "m": (1.0, dimvec(L=1)), "g": (1e-3, dimvec(M=1)), "s": (1.0, dimvec(T=1)), "mol": (1.0, dimvec(N=1)),
    "K": (1.0, dimvec(Theta=1)), "A": (1.0, dimvec(I=1)), "cd": (1.0, dimvec(J=1)),
    "L": (1e-3, dimvec(L=3)), "M": (1e3, dimvec(N=1, L=-3)), "min": (60.0, dimvec(T=1)), "h": (3600.0, dimvec(T=1)),
    "d": (86400.0, dimvec(T=1)), "Da": (1e-3, dimvec(M=1, N=-1)), "N": (1.0, dimvec(M=1, L=1, T=-2)),
    "J": (1.0, dimvec(M=1, L=2, T=-2)), "W": (1.0, dimvec(M=1, L=2, T=-3)), "Pa": (1.0, dimvec(M=1, L=-1, T=-2)),
    "Hz": (1.0, dimvec(T=-1)),
}
NO_PREFIX = {"min", "h", "d", "Hz"}


def symbol(tok):
    if tok in UNITS:
        return UNITS[tok]
    if len(tok) > 1 and tok[0] in PREFIX and tok[1:] in UNITS and tok[1:] not in NO_PREFIX:
        f, d = UNITS[tok[1:]]
        return PREFIX[tok[0]] * f, d
    raise ValueError("unknown unit %r" % tok)


def parse_unit(text):
    """(factor to SI, dimension vector) for a unit expression."""
    tokens = re.findall(r"[A-Za-zµμ]+|\d+|\^|\*|/|\(|\)|-", text.replace(" ", ""))
    if "".join(tokens) != text.replace(" ", ""):
        raise ValueError("cannot read the unit %r" % text)
    pos = [0]

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def take():
        if pos[0] >= len(tokens):
            raise ValueError("unit %r ends too early" % text)
        pos[0] += 1
        return tokens[pos[0] - 1]

    def atom():
        t = peek()
        if t == "(":
            take()
            v = expr()
            if take() != ")":
                raise ValueError("unbalanced parentheses in %r" % text)
        elif t is not None and t.isdigit():
            if take() != "1":
                raise ValueError("only 1 may stand alone as a number, as in 1/s")
            v = (1.0, dimvec())
        elif t is not None and re.match(r"[A-Za-zµμ]+$", t):
            v = symbol(take())
        else:
            raise ValueError("cannot read the unit %r" % text)
        if peek() == "^":
            take()
            sign = -1 if peek() == "-" else 1
            if sign < 0:
                take()
            p = take()
            if not p or not p.isdigit():
                raise ValueError("powers must be integers in %r" % text)
            n = sign * int(p)
            v = (v[0] ** n, tuple(x * n for x in v[1]))
        return v

    def expr():
        f, d = atom()
        while peek() in ("*", "/"):
            op = take()
            f2, d2 = atom()
            if op == "*":
                f, d = f * f2, tuple(a + b for a, b in zip(d, d2))
            else:
                f, d = f / f2, tuple(a - b for a, b in zip(d, d2))
        return f, d
    v = expr()
    if pos[0] != len(tokens):
        raise ValueError("cannot read the unit %r" % text)
    return v


def describe(d):
    parts = ["%s^%d" % (n, p) if p != 1 else n for n, p in zip(DIMS, d) if p]
    return " ".join(parts) or "dimensionless"


def convert(value, frm, to):
    f1, d1 = parse_unit(frm)
    f2, d2 = parse_unit(to)
    if d1 != d2:
        raise ValueError("cannot convert %s (%s) to %s (%s): different dimensions" % (frm, describe(d1), to, describe(d2)))
    return value * f1 / f2


def chemostat(D, mumax, Ks, S0, Y):
    if D <= 0 or mumax <= 0:
        raise ValueError("need D > 0 and mumax > 0")
    crit = mumax * S0 / (Ks + S0)
    if D >= crit:
        return {"washout": True, "critical_D": crit, "S": S0, "X": 0.0}
    s = Ks * D / (mumax - D)
    return {"washout": False, "critical_D": crit, "S": s, "X": Y * (S0 - s), "productivity": D * Y * (S0 - s)}


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=1e-12):
        count[0] += 1
        if isinstance(want, float) or isinstance(got, float):
            ok = abs(got - want) <= tol * max(1.0, abs(want))
        else:
            ok = got == want
        if not ok:
            fails.append("%s: got %r, want %r" % (name, got, want))

    eq("5 mM is 5 mol per cubic metre", convert(5, "mM", "mol/m^3"), 5.0)
    eq("1 mmol/L/h in mol/(m^3*s)", convert(1, "mmol/L/h", "mol/(m^3*s)"), 1 / 3600.0)
    eq("1 L in m^3", convert(1, "L", "m^3"), 1e-3)
    eq("micro written u or µ", convert(1, "uM", "nM"), convert(1, "µM", "nM"))
    eq("1 uM is 1000 nM", convert(1, "uM", "nM"), 1000.0)
    eq("second-order rate constant units", convert(1, "1/(M*s)", "L/(mol*s)"), 1.0)
    eq("per minute to per second", convert(6, "1/min", "1/s"), 0.1)
    eq("kDa to g/mol", convert(50, "kDa", "g/mol"), 50000.0)
    eq("molar dimension", parse_unit("M")[1], parse_unit("mol/L")[1])
    eq("negative powers", parse_unit("mol*m^-3")[1], parse_unit("mol/m^3")[1])
    eq("energy is force times length", parse_unit("J")[1], parse_unit("N*m")[1])
    eq("dimensionless ratio", describe(parse_unit("mol/mol")[1]), "dimensionless")
    c = chemostat(0.2, 0.5, 0.1, 10, 0.5)
    eq("chemostat substrate", c["S"], 0.1 * 0.2 / 0.3)
    eq("chemostat biomass", c["X"], 0.5 * (10 - 0.1 * 0.2 / 0.3))
    eq("washout above the critical dilution rate", chemostat(0.499, 0.5, 0.1, 10, 0.5)["washout"], True)
    eq("critical D", chemostat(0.2, 0.5, 0.1, 10, 0.5)["critical_D"], 0.5 * 10 / 10.1)
    for bad, label in ((lambda: convert(1, "mM", "g/L"), "molar to mass concentration"), (lambda: parse_unit("furlong"), "unknown unit"),
                       (lambda: parse_unit("m^x"), "non-integer power"), (lambda: parse_unit("(m/s"), "unbalanced"),
                       (lambda: parse_unit("kmin"), "prefix on min")):
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
    _c = chemostat(0.2, 0.5, 0.1, 10, 0.5)
    _near("chemostat biomass Y (S0 - S*)", _c["X"], 0.5 * (10 - 0.02 / 0.3))
    _near("chemostat productivity D X*", _c["productivity"], 0.2 * 0.5 * (10 - 0.02 / 0.3))
    _same("washout exactly at the critical dilution rate", chemostat(0.25, 0.5, 1, 1, 0.5)["washout"], True)
    _same("just below the critical rate there is no washout", chemostat(0.24, 0.5, 1, 1, 0.5)["washout"], False)
    _near("ms is 1e-3 s", convert(1, "ms", "s"), 1e-3)
    _near("micro sign: 1 µM = 1000 nM", convert(1, "µM", "nM"), 1000)
    _raises("no prefix on hours (mh)", lambda: convert(1, "mh", "s"))
    _raises("no micro prefix on hours either", lambda: convert(1, "µh", "s"))
    _near("Greek mu: 1 μM = 1000 nM", convert(1, "μM", "nM"), 1000)
    _near("compound units multiply: 1 mmol*min = 0.06 mol*s", convert(1, "mmol*min", "mol*s"), 0.06)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("units selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Quantity calculus, unit conversion and a chemostat balance.")
    ap.add_argument("op", nargs="?", choices=["convert", "dims", "same", "chemostat"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--to")
    for name in ("D", "mumax", "Ks", "S0", "Y"):
        ap.add_argument("--" + name, type=float)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        if a.op == "convert":
            v = convert(float(a.args[0]), a.args[1], a.to)
            print("%s %s = %.6g %s" % (a.args[0], a.args[1], v, a.to))
        elif a.op == "dims":
            f, d = parse_unit(a.args[0])
            print("%s = %.6g x SI, dimension %s" % (a.args[0], f, describe(d)))
        elif a.op == "same":
            f1, d1 = parse_unit(a.args[0])
            f2, d2 = parse_unit(a.args[1])
            if d1 == d2:
                print("same dimension (%s); 1 %s = %.6g %s" % (describe(d1), a.args[0], f1 / f2, a.args[1]))
            else:
                print("different dimensions: %s versus %s" % (describe(d1), describe(d2)))
                return 1
        elif a.op == "chemostat":
            r = chemostat(a.D, a.mumax, a.Ks, a.S0, a.Y)
            if r["washout"]:
                print("washout: D = %g is at or above the critical dilution rate %.6g" % (a.D, r["critical_D"]))
            else:
                print("steady state: growth rate = D = %g; S* = %.6g; X* = %.6g; productivity D X* = %.6g; critical D %.6g" % (
                    a.D, r["S"], r["X"], r["productivity"], r["critical_D"]))
        else:
            ap.error("give an operation or --selftest")
    except (ValueError, IndexError, TypeError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
