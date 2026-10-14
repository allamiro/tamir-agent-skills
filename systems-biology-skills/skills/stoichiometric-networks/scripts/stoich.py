#!/usr/bin/env python3
"""Stoichiometric matrix, steady-state fluxes, conservation relations, elementary modes and flux determinacy
(standard library only).

  stoich.py matrix NETWORK.txt                         the stoichiometric matrix N (internal metabolites x reactions)
  stoich.py null NETWORK.txt                           basis of steady-state fluxes, N v = 0
  stoich.py conserved NETWORK.txt                      conservation relations (left null space, g N = 0)
  stoich.py efm NETWORK.txt                            elementary flux modes (small networks only)
  stoich.py mfa NETWORK.txt --measured R1=10,R4=3     which fluxes the measurements determine
  stoich.py --selftest

NETWORK.txt has one reaction per line, "name: substrates -> products" for an irreversible reaction or
"<->" for a reversible one, for example:

    R1: -> A            (uptake: nothing on the left)
    R2: A -> B
    R3: 2 B <-> C + D
    R4: C ->            (export)

Lines starting with # are ignored. A metabolite written with the suffix _ext (or listed with --external) is
treated as external and left out of N, as is the usual convention for boundary metabolites. Everything is computed
with exact fractions. Elementary modes are found by checking every support set, so the program refuses networks
with more than 16 irreversible directions; use a dedicated tool (for example efmtool, or the EFM functions of
COBRA toolboxes) for anything larger.
"""
import argparse
import itertools
import re
import sys
from fractions import Fraction

ARROW = re.compile(r"\s*(<->|<=>|->|=>)\s*")


def parse_side(text):
    out = {}
    text = text.strip()
    if not text:
        return out
    for term in text.split("+"):
        term = term.strip()
        m = re.match(r"^(\d+(?:\.\d+)?(?:/\d+)?)?\s*([A-Za-z_][\w\[\]]*)$", term)
        if not m:
            raise ValueError("cannot read the term %r" % term)
        coef = Fraction(m.group(1)) if m.group(1) else Fraction(1)
        out[m.group(2)] = out.get(m.group(2), 0) + coef
    return out


def parse_network(text, external=()):
    """Returns (metabolites, reactions) where reactions are (name, {metabolite: coefficient}, reversible)."""
    reactions, mets = [], []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError("each line needs 'name: equation': %r" % raw)
        name, eq = line.split(":", 1)
        parts = ARROW.split(eq)
        if len(parts) != 3:
            raise ValueError("each reaction needs exactly one arrow: %r" % raw)
        left, arrow, right = parts
        rev = arrow in ("<->", "<=>")
        coeffs = {}
        for met, c in parse_side(left).items():
            coeffs[met] = coeffs.get(met, 0) - c
        for met, c in parse_side(right).items():
            coeffs[met] = coeffs.get(met, 0) + c
        coeffs = {m: c for m, c in coeffs.items() if c != 0 and not m.endswith("_ext") and m not in external}
        for m in coeffs:
            if m not in mets:
                mets.append(m)
        reactions.append((name.strip(), coeffs, rev))
    if not reactions:
        raise ValueError("no reactions")
    names = [r[0] for r in reactions]
    if len(set(names)) != len(names):
        raise ValueError("reaction names must be unique")
    return mets, reactions


def matrix(mets, reactions):
    return [[r[1].get(m, Fraction(0)) for r in reactions] for m in mets]


def rref(m):
    a = [row[:] for row in m]
    rows = len(a)
    cols = len(a[0]) if a else 0
    piv, r = [], 0
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
        piv.append(c)
        r += 1
        if r == rows:
            break
    return a, piv


def nullspace(m, ncols=None):
    ncols = ncols if ncols is not None else (len(m[0]) if m else 0)
    if not m:
        return [[Fraction(int(i == j)) for i in range(ncols)] for j in range(ncols)]
    red, piv = rref(m)
    basis = []
    for f in [c for c in range(ncols) if c not in piv]:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -red[i][f]
        basis.append(v)
    return basis


def transpose(m):
    return [list(r) for r in zip(*m)] if m else []


def integerise(v):
    """Scale a rational vector to the smallest integer vector with the same direction."""
    from math import gcd
    den = 1
    for x in v:
        den = den * x.denominator // gcd(den, x.denominator)
    w = [int(x * den) for x in v]
    g = 0
    for x in w:
        g = gcd(g, abs(x))
    return [x // g for x in w] if g else w


def rank(m):
    return len(rref(m)[1]) if m else 0


def efms(mets, reactions, limit=16):
    """Elementary flux modes as integer vectors over the original reactions (reversible ones may be negative)."""
    dirs = []   # (original index, sign)
    for i, (_n, _c, rev) in enumerate(reactions):
        dirs.append((i, 1))
        if rev:
            dirs.append((i, -1))
    if len(dirs) > limit:
        raise ValueError("%d irreversible directions; this exhaustive method stops at %d" % (len(dirs), limit))
    n = matrix(mets, reactions)
    cols = [[row[i] * s for row in n] for i, s in dirs]
    found = []
    for size in range(1, len(dirs) + 1):
        for sup in itertools.combinations(range(len(dirs)), size):
            if any(set(f) <= set(sup) for f in found):
                continue
            if len({dirs[k][0] for k in sup}) < size:
                continue   # a reaction used in both directions is a futile pair, not a mode
            sub = [[cols[k][r] for k in sup] for r in range(len(mets))] if mets else []
            ns = nullspace(sub, size)
            if len(ns) != 1:
                continue
            v = ns[0]
            if all(x > 0 for x in v) or all(x < 0 for x in v):
                found.append(sup)
    modes = []
    for sup in found:
        sub = [[cols[k][r] for k in sup] for r in range(len(mets))] if mets else []
        v = nullspace(sub, len(sup))[0]
        if v[0] < 0:
            v = [-x for x in v]
        full = [Fraction(0)] * len(reactions)
        for k, x in zip(sup, v):
            i, s = dirs[k]
            full[i] += s * x
        modes.append(integerise(full))
    return modes


def flux_determinacy(mets, reactions, measured):
    """Given measured fluxes {name: value}, return (status, determined {name: value}, free names, redundancy)."""
    names = [r[0] for r in reactions]
    for k in measured:
        if k not in names:
            raise ValueError("unknown reaction %r" % k)
    n = matrix(mets, reactions)
    unknown = [i for i, nm in enumerate(names) if nm not in measured]
    known = [i for i, nm in enumerate(names) if nm in measured]
    nu = [[row[i] for i in unknown] for row in n]
    rhs = [-sum(row[i] * Fraction(measured[names[i]]) for i in known) for row in n]
    ru = rank(nu) if nu else 0
    aug = [r + [b] for r, b in zip(nu, rhs)]
    if aug and rank(aug) > ru:
        return "inconsistent", {}, [], len(mets) - ru
    ns = nullspace(nu, len(unknown)) if unknown else []
    red, piv = rref(aug) if aug else ([], [])
    particular = [Fraction(0)] * len(unknown)
    for i, c in enumerate(piv):
        if c < len(unknown):
            particular[c] = red[i][len(unknown)]
    determined, free = {}, []
    for j, idx in enumerate(unknown):
        if all(v[j] == 0 for v in ns):
            determined[names[idx]] = particular[j]
        else:
            free.append(names[idx])
    redundancy = len(mets) - ru
    status = "determined" if not free else "underdetermined"
    return status, determined, free, redundancy


NETWORK = """
R1: -> A
R2: A -> B
R3: A -> C
R4: B -> D
R5: C -> D
R6: D ->
"""


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    mets, rx = parse_network("R1: -> A\nR2: A -> B\nR3: B ->")
    eq("chain metabolites", mets, ["A", "B"])
    eq("chain matrix", matrix(mets, rx), [[1, -1, 0], [0, 1, -1]])
    eq("chain null space", [integerise(v) for v in nullspace(matrix(mets, rx))], [[1, 1, 1]])
    mets, rx = parse_network("R1: 2 A + B -> C\nR2: C <-> 2 A + B  # comment")
    eq("coefficients and reversibility", (rx[0][1], rx[1][2]), ({"A": -2, "B": -1, "C": 1}, True))
    mets, rx = parse_network("R1: A_ext -> A\nR2: A -> B\nR3: B -> B_ext")
    eq("_ext metabolites left out", mets, ["A", "B"])
    mets, rx = parse_network("R1: X -> A\nR2: A -> Y", external=("X", "Y"))
    eq("--external list", mets, ["A"])
    mets, rx = parse_network(NETWORK)
    n = matrix(mets, rx)
    eq("branched rank", rank(n), 4)
    eq("branched flux space dimension", len(nullspace(n)), 2)
    eq("branched EFMs", sorted(efms(mets, rx)), sorted([[1, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 1]]))
    # conservation: ATP + ADP pool in a closed cycle
    mets, rx = parse_network("R1: ATP + G -> ADP + G6P\nR2: ADP -> ATP\nR3: -> G\nR4: G6P ->")
    cons = [integerise(v) for v in nullspace(transpose(matrix(mets, rx)), len(mets))]
    eq("conservation relation ATP + ADP", cons, [[1, 0, 1, 0]])
    eq("metabolite order for that check", mets, ["ATP", "G", "ADP", "G6P"])
    # reversible reaction: a cycle through it in both directions
    mets, rx = parse_network("R1: -> A\nR2: A <-> B\nR3: B ->\nR4: A -> C\nR5: C -> B")
    modes = sorted(efms(mets, rx))
    eq("reversible EFMs include the negative direction", [0, -1, 0, 1, 1] in modes and [1, 1, 1, 0, 0] in modes and [1, 0, 1, 1, 1] in modes, True)
    eq("each EFM is a steady state", all(all(sum(r * x for r, x in zip(row, m)) == 0 for row in matrix(mets, rx)) for m in modes), True)
    eq("no futile forward-backward pair", any(m == [0, 0, 0, 0, 0] for m in modes), False)
    mets, rx = parse_network(NETWORK)
    st, det, free, red = flux_determinacy(mets, rx, {"R1": 10, "R2": 6})
    eq("MFA determined", (st, det), ("determined", {"R3": 4, "R4": 6, "R5": 4, "R6": 10}))
    st, det, free, red = flux_determinacy(mets, rx, {"R1": 10})
    eq("MFA underdetermined keeps R6 determined", (st, det, sorted(free)), ("underdetermined", {"R6": 10}, ["R2", "R3", "R4", "R5"]))
    st, det, free, red = flux_determinacy(mets, rx, {"R1": 10, "R6": 9})
    eq("MFA inconsistent measurements", st, "inconsistent")
    eq("integerise", integerise([Fraction(1, 2), Fraction(3, 4)]), [2, 3])
    for bad, label in ((lambda: parse_network("R1 A -> B"), "missing name"), (lambda: parse_network("R1: A -> B -> C"), "two arrows"),
                       (lambda: parse_network("R1: A -> B\nR1: B -> C"), "duplicate names"), (lambda: parse_network("R1: 2x A -> B"), "bad term"),
                       (lambda: efms(*parse_network("\n".join("R%d: A <-> B" % i for i in range(10)))), "too large for EFM enumeration")):
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
    _m, _r = parse_network("R1: -> A\nR2: A ->")
    _same("measurements that violate the balance are inconsistent", flux_determinacy(_m, _r, {"R1": 10, "R2": 5})[0], "inconsistent")
    _same("inconsistent: the one balance is redundant and violated", flux_determinacy(_m, _r, {"R1": 10, "R2": 5})[3], 1)
    _same("null space of a matrix with no rows is the identity", nullspace([], 2), [[1, 0], [0, 1]])
    _st = flux_determinacy(_m, _r, {"R1": 10, "R2": 10})
    _same("consistent over-measurement is determined with redundancy 1", (_st[0], _st[3]), ("determined", 1))
    _m, _r = parse_network("R1: -> A\nR2: A <-> B\nR3: B ->\nR4: -> B\nR5: A ->")
    _modes = efms(_m, _r)
    _same("four elementary modes with a reversible reaction", len(_modes), 4)
    _same("one mode runs the reversible reaction backwards", sum(1 for v in _modes if v[1] < 0), 1)
    _same("no mode runs an irreversible reaction backwards", all(v[i] >= 0 for v in _modes for i in (0, 2, 3, 4)), True)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("stoich selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Stoichiometric analysis of small metabolic networks.")
    ap.add_argument("op", nargs="?", choices=["matrix", "null", "conserved", "efm", "mfa"])
    ap.add_argument("network", nargs="?")
    ap.add_argument("--external", default="", help="comma-separated external metabolites")
    ap.add_argument("--measured", default="", help="for mfa: name=value pairs, comma separated")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.op or not a.network:
        ap.error("give an operation and a network file, or --selftest")
    try:
        mets, rx = parse_network(open(a.network, encoding="utf-8").read(), tuple(x.strip() for x in a.external.split(",") if x.strip()))
        names = [r[0] for r in rx]
        n = matrix(mets, rx)
        if a.op == "matrix":
            print("%-12s %s" % ("", " ".join("%6s" % x for x in names)))
            for m, row in zip(mets, n):
                print("%-12s %s" % (m, " ".join("%6s" % x for x in row)))
            print("%d internal metabolites, %d reactions, rank %d" % (len(mets), len(rx), rank(n)))
        elif a.op == "null":
            ns = nullspace(n, len(rx))
            print("steady-state flux space: dimension %d (= %d reactions - rank %d)" % (len(ns), len(rx), rank(n)))
            for v in ns:
                print("  " + ", ".join("%s=%s" % (nm, x) for nm, x in zip(names, integerise(v)) if x))
            print("A basis vector is not a pathway: it may need reversed irreversible reactions. Use efm for pathways.")
        elif a.op == "conserved":
            ns = nullspace(transpose(n), len(mets)) if mets else []
            print("%d conservation relation(s)" % len(ns))
            for v in ns:
                print("  " + " + ".join("%s %s" % (c, m) if c != 1 else m for m, c in zip(mets, integerise(v)) if c) + " = constant")
        elif a.op == "efm":
            modes = efms(mets, rx)
            print("%d elementary flux mode(s)" % len(modes))
            for v in modes:
                print("  " + ", ".join("%s=%s" % (nm, x) for nm, x in zip(names, v) if x))
        elif a.op == "mfa":
            measured = dict((k.strip(), Fraction(v)) for k, v in (p.split("=") for p in a.measured.split(",") if p.strip()))
            st, det, free, red = flux_determinacy(mets, rx, measured)
            print("system: %s; redundancy (balances beyond what the unknowns use): %d" % (st, red))
            for k, v in det.items():
                print("  %s = %s" % (k, v))
            if free:
                print("not determined by these measurements: %s" % ", ".join(free))
    except (ValueError, OSError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
