#!/usr/bin/env python3
"""Flux balance analysis for small networks, with an exact simplex solver (standard library only).

  fba.py fba NETWORK.txt --objective R6 [--min]           optimal flux distribution
  fba.py fva NETWORK.txt --objective R6 [--fraction 1.0]  each flux's range at (a fraction of) the optimum
  fba.py ko NETWORK.txt --objective R6                     objective after knocking out each reaction alone
  fba.py --selftest

NETWORK.txt uses the same reaction lines as stoich.py ("R2: A -> B", "<->" for reversible, "_ext" suffix for
external metabolites), plus optional bound lines:

    bounds R1 0 10        lower and upper bound for R1

Default bounds are 0 to 1000 for irreversible reactions and -1000 to 1000 for reversible ones; 1000 stands for
"unbounded", so an objective that reaches it means a bound is missing. The solver is a two-phase simplex with
Bland's rule on exact fractions: it is meant for teaching-size networks and for checking a result, not for
genome-scale models (use COBRApy or the COBRA Toolbox for those). An FBA optimum is usually not unique; the flux
distribution printed is one optimal solution, and fva shows which fluxes can vary.
"""
import argparse
import re
import sys
from fractions import Fraction

ARROW = re.compile(r"\s*(<->|<=>|->|=>)\s*")
BIG = Fraction(1000)


def parse_side(text):
    out = {}
    for term in [t.strip() for t in text.split("+") if t.strip()]:
        m = re.match(r"^(\d+(?:\.\d+)?(?:/\d+)?)?\s*([A-Za-z_][\w\[\]]*)$", term)
        if not m:
            raise ValueError("cannot read the term %r" % term)
        out[m.group(2)] = out.get(m.group(2), 0) + (Fraction(m.group(1)) if m.group(1) else Fraction(1))
    return out


def parse(text):
    """(metabolites, names, columns {name: {met: coef}}, bounds {name: (lb, ub)})."""
    mets, names, cols, bounds, rev = [], [], {}, {}, {}
    pending = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("bounds "):
            parts = line.split()
            if len(parts) != 4:
                raise ValueError("bounds lines are 'bounds NAME LOWER UPPER': %r" % raw)
            pending.append((parts[1], Fraction(parts[2]), Fraction(parts[3])))
            continue
        name, eq = line.split(":", 1)
        parts = ARROW.split(eq)
        if len(parts) != 3:
            raise ValueError("each reaction needs exactly one arrow: %r" % raw)
        name = name.strip()
        if name in cols:
            raise ValueError("duplicate reaction %s" % name)
        col = {}
        for met, c in parse_side(parts[0]).items():
            col[met] = col.get(met, 0) - c
        for met, c in parse_side(parts[2]).items():
            col[met] = col.get(met, 0) + c
        col = {m: c for m, c in col.items() if c and not m.endswith("_ext")}
        for m in col:
            if m not in mets:
                mets.append(m)
        names.append(name)
        cols[name] = col
        rev[name] = parts[1] in ("<->", "<=>")
        bounds[name] = (-BIG if rev[name] else Fraction(0), BIG)
    for name, lb, ub in pending:
        if name not in cols:
            raise ValueError("bounds for unknown reaction %s" % name)
        if lb > ub:
            raise ValueError("lower bound above upper bound for %s" % name)
        bounds[name] = (lb, ub)
    if not names:
        raise ValueError("no reactions")
    return mets, names, cols, bounds


def simplex_max(c, a_eq, b_eq):
    """Maximise c.x subject to a_eq x = b_eq, x >= 0. Returns ('optimal', x, value), ('infeasible', ...) or
    ('unbounded', ...). Two-phase tableau simplex with Bland's rule on exact fractions."""
    m, n = len(a_eq), len(c)
    a = [row[:] for row in a_eq]
    b = list(b_eq)
    for i in range(m):
        if b[i] < 0:
            a[i] = [-x for x in a[i]]
            b[i] = -b[i]
    # tableau with artificials n..n+m-1
    t = [a[i] + [Fraction(int(i == j)) for j in range(m)] + [b[i]] for i in range(m)]
    basis = [n + i for i in range(m)]
    width = n + m

    def pivot(r, col):
        pv = t[r][col]
        t[r] = [x / pv for x in t[r]]
        for i in range(m):
            if i != r and t[i][col] != 0:
                f = t[i][col]
                t[i] = [x - f * y for x, y in zip(t[i], t[r])]
        basis[r] = col

    def run(cost, allowed):
        while True:
            # reduced costs for maximisation: cost_j - sum(cost_basis * column)
            entering = None
            for j in range(width):
                if j not in allowed or j in basis:
                    continue
                rc = cost[j] - sum(cost[basis[i]] * t[i][j] for i in range(m))
                if rc > 0:
                    entering = j
                    break   # Bland: smallest index
            if entering is None:
                return "optimal"
            rows = [(t[i][-1] / t[i][entering], basis[i], i) for i in range(m) if t[i][entering] > 0]
            if not rows:
                return "unbounded"
            _ratio, _b, r = min(rows)
            pivot(r, entering)

    phase1 = [Fraction(0)] * n + [Fraction(-1)] * m
    run(phase1, set(range(width)))
    if sum(t[i][-1] for i in range(m) if basis[i] >= n) != 0:
        return "infeasible", None, None
    # drive remaining artificials out of the basis where possible
    for i in range(m):
        if basis[i] >= n:
            col = next((j for j in range(n) if t[i][j] != 0), None)
            if col is not None:
                pivot(i, col)
    cost = list(c) + [Fraction(0)] * m
    status = run(cost, set(range(n)))
    if status == "unbounded":
        return "unbounded", None, None
    x = [Fraction(0)] * n
    for i in range(m):
        if basis[i] < n:
            x[basis[i]] = t[i][-1]
    return "optimal", x, sum(ci * xi for ci, xi in zip(c, x))


def solve(mets, names, cols, bounds, objective, sense=1, extra=()):
    """Optimise sense * v[objective] (sense 1 maximises, -1 minimises). extra: additional (coeffs {name: a}, '>=', value)
    constraints. Returns (status, fluxes {name: value}, objective value)."""
    if objective not in cols:
        raise ValueError("unknown objective reaction %s" % objective)
    k = len(names)
    lbs = [bounds[nm][0] for nm in names]
    ubs = [bounds[nm][1] for nm in names]
    # v = lb + x, 0 <= x <= ub - lb  ->  x + s = ub - lb
    rows, rhs = [], []
    for met in mets:
        row = [cols[nm].get(met, Fraction(0)) for nm in names]
        rows.append(row + [Fraction(0)] * k + [Fraction(0)] * len(extra))
        rhs.append(-sum(r * lb for r, lb in zip(row, lbs)))
    for i in range(k):
        row = [Fraction(0)] * (2 * k + len(extra))
        row[i] = Fraction(1)
        row[k + i] = Fraction(1)
        rows.append(row)
        rhs.append(ubs[i] - lbs[i])
    for e, (coeffs, op, value) in enumerate(extra):
        row = [Fraction(coeffs.get(nm, 0)) for nm in names] + [Fraction(0)] * k + [Fraction(0)] * len(extra)
        row[2 * k + e] = Fraction(-1)   # a.x - surplus = value - a.lb
        rows.append(row)
        rhs.append(Fraction(value) - sum(Fraction(coeffs.get(nm, 0)) * lb for nm, lb in zip(names, lbs)))
    c = [Fraction(0)] * (2 * k + len(extra))
    c[names.index(objective)] = Fraction(sense)
    status, x, _val = simplex_max(c, rows, rhs)
    if status != "optimal":
        return status, None, None
    fluxes = {nm: lbs[i] + x[i] for i, nm in enumerate(names)}
    return status, fluxes, fluxes[objective]


def fva(mets, names, cols, bounds, objective, fraction=Fraction(1)):
    st, _f, opt = solve(mets, names, cols, bounds, objective)
    if st != "optimal":
        raise ValueError("the FBA problem is %s" % st)
    floor = ({objective: 1}, ">=", fraction * opt)
    out = {}
    for nm in names:
        s1, _a, lo = solve(mets, names, cols, bounds, nm, -1, (floor,))
        s2, _b, hi = solve(mets, names, cols, bounds, nm, 1, (floor,))
        out[nm] = (lo if s1 == "optimal" else None, hi if s2 == "optimal" else None)
    return opt, out


def knockouts(mets, names, cols, bounds, objective):
    out = {}
    for nm in names:
        b = dict(bounds)
        b[nm] = (Fraction(0), Fraction(0))
        st, _f, val = solve(mets, names, cols, b, objective)
        out[nm] = val if st == "optimal" else None
    return out


TOY = """
R1: -> A
R2: A -> B
R3: A -> C
R4: B -> D
R5: C -> 2 D
R6: D ->
bounds R1 0 10
bounds R4 0 3
"""


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    F = Fraction
    # maximise 3 x1 + 5 x2 with x1 <= 4, 2 x2 <= 12, 3 x1 + 2 x2 <= 18 (slacks added): optimum 36 at (2, 6)
    st, x, v = simplex_max([F(3), F(5), F(0), F(0), F(0)],
                           [[F(1), F(0), F(1), F(0), F(0)], [F(0), F(2), F(0), F(1), F(0)], [F(3), F(2), F(0), F(0), F(1)]],
                           [F(4), F(12), F(18)])
    eq("textbook LP optimum", (st, v, x[:2]), ("optimal", 36, [2, 6]))
    eq("infeasible LP", simplex_max([F(1)], [[F(1)], [F(1)]], [F(1), F(2)])[0], "infeasible")
    eq("unbounded LP", simplex_max([F(1), F(0)], [[F(1), F(-1)]], [F(0)])[0], "unbounded")
    mets, names, cols, bounds = parse(TOY)
    st, fl, obj = solve(mets, names, cols, bounds, "R6")
    eq("FBA optimum uses the 2 D branch", (st, obj), ("optimal", 20))
    eq("FBA steady state", all(sum(cols[nm].get(m, 0) * fl[nm] for nm in names) == 0 for m in mets), True)
    eq("FBA respects bounds", all(bounds[nm][0] <= fl[nm] <= bounds[nm][1] for nm in names), True)
    st, fl, obj = solve(mets, names, cols, bounds, "R6", -1)
    eq("minimum export is zero", obj, 0)
    opt, ranges = fva(mets, names, cols, bounds, "R6")
    eq("FVA at optimum fixes R3", ranges["R3"], (10, 10))
    eq("FVA at optimum forces R4 to zero", ranges["R4"], (0, 0))
    opt, ranges = fva(mets, names, cols, bounds, "R6", Fraction(9, 10))
    eq("FVA at 90 percent lets R4 rise", ranges["R4"], (0, 2))
    ko = knockouts(mets, names, cols, bounds, "R6")
    eq("knockouts (without R3 only the R4 route, capped at 3, remains)", (ko["R1"], ko["R3"], ko["R2"]), (0, 3, 20))
    mets, names, cols, bounds = parse("R1: -> A\nR2: A ->")
    eq("missing bound shows as the 1000 default", solve(mets, names, cols, bounds, "R2")[2], 1000)
    mets, names, cols, bounds = parse("R1: -> A\nR2: A <-> B\nR3: B ->\nbounds R1 0 5")
    eq("reversible reaction runs forward", solve(mets, names, cols, bounds, "R3")[2], 5)
    mets, names, cols, bounds = parse("R1: -> A\nR2: A ->\nbounds R1 2 4\nbounds R2 0 1")
    eq("infeasible bounds detected", solve(mets, names, cols, bounds, "R2")[0], "infeasible")
    for bad, label in ((lambda: parse("bounds R9 0 1\nR1: -> A"), "bounds for unknown reaction"), (lambda: parse("R1: -> A\nbounds R1 5 1"), "lower above upper"),
                       (lambda: solve(*parse("R1: -> A"), "R9"), "unknown objective")):
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
    _mets, _names, _cols, _bounds = parse("R1: -> A\nR2: A -> B\nR3: B ->\nR4: A ->\nbounds R1 0 10\nbounds R3 3 10")
    _same("phase 1 needed: minimum uptake with R3 >= 3", solve(_mets, _names, _cols, _bounds, "R1", -1)[2], 3)
    _same("phase 1 needed: the rest of the uptake goes to R4", solve(_mets, _names, _cols, _bounds, "R4")[2], 7)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("fba selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Flux balance analysis for small networks.")
    ap.add_argument("op", nargs="?", choices=["fba", "fva", "ko"])
    ap.add_argument("network", nargs="?")
    ap.add_argument("--objective")
    ap.add_argument("--min", action="store_true", help="minimise instead of maximise")
    ap.add_argument("--fraction", default="1", help="fva: keep the objective at least this fraction of its optimum")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.op or not a.network or not a.objective:
        ap.error("give an operation, a network file and --objective, or --selftest")
    try:
        mets, names, cols, bounds = parse(open(a.network, encoding="utf-8").read())
        if a.op == "fba":
            st, fl, obj = solve(mets, names, cols, bounds, a.objective, -1 if a.min else 1)
            print("status: %s" % st)
            if fl:
                print("objective %s = %s" % (a.objective, obj))
                for nm in names:
                    print("  %-10s %s" % (nm, fl[nm]))
                hit = [nm for nm in names if abs(fl[nm]) == BIG]
                if hit:
                    print("warning: %s reached the default bound of 1000; a real bound is probably missing" % ", ".join(hit))
                print("This is one optimal solution; run fva to see which fluxes can vary at the optimum.")
        elif a.op == "fva":
            opt, ranges = fva(mets, names, cols, bounds, a.objective, Fraction(a.fraction))
            print("optimum %s = %s; ranges with the objective at least %s of it:" % (a.objective, opt, a.fraction))
            for nm in names:
                lo, hi = ranges[nm]
                print("  %-10s [%s, %s]" % (nm, lo, hi))
        else:
            for nm, v in knockouts(mets, names, cols, bounds, a.objective).items():
                print("  knock out %-10s objective %s" % (nm, v if v is not None else "infeasible"))
    except (ValueError, OSError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
