#!/usr/bin/env python3
"""Stochastic, Boolean and discrete-time models (standard library only).

  discrete.py ssa REACTIONS.txt --t 50 [--runs 200] [--seed 1]   Gillespie direct method: mean and spread at time t
  discrete.py boolean RULES.txt                                  attractors of a synchronous Boolean network
  discrete.py map --r 2.8 [--x0 0.1] [--steps 50]               logistic map x' = r x (1 - x): orbit and fixed points
  discrete.py --selftest

REACTIONS.txt for ssa (molecule counts, mass-action propensities):

    init A = 100          initial molecule count
    rate R1 0.1: A ->     reaction with stochastic rate constant 0.1 (0 or more reactants, at most two)
    rate R2 5: -> A

RULES.txt for boolean: one rule per node, written with and, or, not and parentheses:

    A = not C
    B = A
    C = B

Boolean attractors are found by visiting every state, so the program stops at 16 nodes (65,536 states). Use the
synchronous update only when it is justified; asynchronous updating can give different attractors.
"""
import argparse
import math
import random
import re
import sys


def parse_reactions(text):
    init, reactions = {}, []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.match(r"^init\s+(\w+)\s*=\s*(\d+)$", line)
        if m:
            init[m.group(1)] = int(m.group(2))
            continue
        m = re.match(r"^rate\s+(\w+)\s+([0-9.eE+-]+)\s*:\s*(.*?)\s*->\s*(.*)$", line)
        if not m:
            raise ValueError("cannot read %r" % raw)
        name, k, lhs, rhs = m.group(1), float(m.group(2)), m.group(3), m.group(4)

        def side(s):
            out = {}
            for term in [x.strip() for x in s.split("+") if x.strip()]:
                mm = re.match(r"^(\d+)?\s*(\w+)$", term)
                if not mm:
                    raise ValueError("cannot read the term %r" % term)
                out[mm.group(2)] = out.get(mm.group(2), 0) + int(mm.group(1) or 1)
            return out
        reac, prod = side(lhs), side(rhs)
        if sum(reac.values()) > 2:
            raise ValueError("%s: mass-action propensities here handle at most two reactant molecules" % name)
        reactions.append((name, k, reac, prod))
        for s in list(reac) + list(prod):
            init.setdefault(s, 0)
    return init, reactions


def propensity(k, reac, x):
    a = k
    for s, n in reac.items():
        if n == 1:
            a *= x[s]
        elif n == 2:
            a *= x[s] * (x[s] - 1) / 2.0   # combinatorial count of distinct pairs
    return a


def ssa(init, reactions, t_end, rng):
    x = dict(init)
    t = 0.0
    while True:
        props = [propensity(k, r, x) for _n, k, r, _p in reactions]
        a0 = sum(props)
        if a0 <= 0:
            return x
        tau = rng.expovariate(a0)
        if t + tau > t_end:
            return x
        t += tau
        u = rng.random() * a0
        acc = 0.0
        for (name, k, reac, prod), a in zip(reactions, props):
            acc += a
            if u < acc:
                for s, n in reac.items():
                    x[s] -= n
                for s, n in prod.items():
                    x[s] += n
                break


def parse_rules(text):
    rules = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        name, eq, expr = line.partition("=")
        name = name.strip()
        if not eq or not name.isidentifier():
            raise ValueError("cannot read %r" % raw)
        rules[name] = expr.strip()
    nodes = list(rules)
    allowed = set(nodes) | {"and", "or", "not", "True", "False"}
    for n, e in rules.items():
        for tok in re.findall(r"[A-Za-z_]\w*", e):
            if tok not in allowed:
                raise ValueError("rule for %s uses unknown name %r" % (n, tok))
        if re.search(r"[^\w\s()]", e):
            raise ValueError("rule for %s may only use names, and, or, not and parentheses" % n)
    code = {n: compile(e, "<rule>", "eval") for n, e in rules.items()}
    return nodes, code


def attractors(nodes, code, limit=16):
    n = len(nodes)
    if n > limit:
        raise ValueError("%d nodes; exhaustive search stops at %d" % (n, limit))

    def step(state):
        env = dict(zip(nodes, state))
        return tuple(bool(eval(code[v], {"__builtins__": {}}, env)) for v in nodes)
    seen_attr = []
    for i in range(2 ** n):
        state = tuple(bool(i >> (n - 1 - j) & 1) for j in range(n))
        path, idx = [], {}
        while state not in idx:
            idx[state] = len(path)
            path.append(state)
            state = step(state)
        cycle = path[idx[state]:]
        k = min(range(len(cycle)), key=lambda j: cycle[j])
        canon = tuple(cycle[k:] + cycle[:k])
        if canon not in seen_attr:
            seen_attr.append(canon)
    return seen_attr


def logistic_orbit(r, x0, steps):
    xs = [x0]
    for _ in range(steps):
        xs.append(r * xs[-1] * (1 - xs[-1]))
    return xs


def logistic_fixed_points(r):
    """Fixed points of x' = r x (1-x) with stability from |f'(x*)| < 1."""
    out = [(0.0, abs(r) < 1)]
    if r != 0:
        xs = 1 - 1 / r
        out.append((xs, abs(2 - r) < 1))
    return out


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=None):
        count[0] += 1
        ok = abs(got - want) <= tol if tol is not None else got == want
        if not ok:
            fails.append("%s: got %r, want %r" % (name, got, want))

    init, rx = parse_reactions("init A = 0\nrate R1 10: -> A\nrate R2 0.5: A ->")
    rng = random.Random(1)
    finals = [ssa(init, rx, 50.0, rng)["A"] for _ in range(400)]
    mean = sum(finals) / len(finals)
    var = sum((f - mean) ** 2 for f in finals) / (len(finals) - 1)
    eq("birth-death mean near k1/k2 = 20", mean, 20.0, 1.0)
    eq("birth-death variance near the mean (Poisson)", var / mean, 1.0, 0.2)
    init, rx = parse_reactions("init A = 1000\nrate R1 0.1: A ->")
    rng = random.Random(2)
    finals = [ssa(init, rx, 5.0, rng)["A"] for _ in range(200)]
    eq("decay mean follows 1000 exp(-0.5)", sum(finals) / len(finals), 1000 * math.exp(-0.5), 5.0)
    eq("dimerisation propensity counts pairs", propensity(1.0, {"A": 2}, {"A": 4}), 6.0)
    eq("extinction stops the run", ssa({"A": 0}, [("R", 1.0, {"A": 1}, {})], 10.0, random.Random(0))["A"], 0)
    nodes, code = parse_rules("A = not C\nB = A\nC = B")
    att = attractors(nodes, code)
    eq("negative three-node loop gives oscillation, no fixed point", all(len(a) > 1 for a in att), True)
    nodes, code = parse_rules("A = B\nB = A")
    att = attractors(nodes, code)
    eq("positive two-node loop is bistable plus a 2-cycle", sorted(len(a) for a in att), [1, 1, 2])
    nodes, code = parse_rules("A = A or B\nB = False")
    eq("constant rules", sorted(attractors(nodes, code)), sorted([((False, False),), ((True, False),)]))
    fp = logistic_fixed_points(2.8)
    eq("logistic r = 2.8 nonzero fixed point", fp[1][0], 1 - 1 / 2.8, 1e-12)
    eq("and it is stable", fp[1][1], True)
    eq("r = 3.2 makes it unstable", logistic_fixed_points(3.2)[1][1], False)
    orb = logistic_orbit(2.8, 0.1, 500)
    eq("orbit converges to the fixed point", orb[-1], 1 - 1 / 2.8, 1e-9)
    orb = logistic_orbit(3.2, 0.1, 1000)
    eq("r = 3.2 settles on a 2-cycle", abs(orb[-1] - orb[-3]) < 1e-9 and abs(orb[-1] - orb[-2]) > 0.1, True)
    for bad, label in ((lambda: parse_rules("A = __import__"), "unknown name"), (lambda: parse_rules("A = B.x\nB = A"), "attribute"),
                       (lambda: parse_reactions("rate R 1: 3 A ->"), "three reactants"), (lambda: attractors(*parse_rules("\n".join("N%d = N%d" % (i, i) for i in range(17)))), "too many nodes")):
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
    _raises("three reactant molecules are refused", lambda: parse_reactions("init A = 5\nrate R1 1: 3 A ->"))
    _nodes, _code = parse_rules("\n".join("N%d = N%d" % (i, i) for i in range(17)))
    _raises("more than 16 nodes are refused", lambda: attractors(_nodes, _code))
    _same("r = 0.5: zero is the stable fixed point", logistic_fixed_points(0.5)[0], (0.0, True))
    _same("r = 2.8: the inner fixed point is stable", logistic_fixed_points(2.8)[1][1], True)
    _same("r = 3: the inner fixed point is neutral, not stable", logistic_fixed_points(3)[1][1], False)
    _same("r = 1: zero is neutral, not stable", logistic_fixed_points(1)[0][1], False)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("discrete selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Stochastic, Boolean and discrete-time models.")
    ap.add_argument("op", nargs="?", choices=["ssa", "boolean", "map"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--t", type=float, default=10.0)
    ap.add_argument("--runs", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--r", type=float)
    ap.add_argument("--x0", type=float, default=0.1)
    ap.add_argument("--steps", type=int, default=50)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        if a.op == "ssa":
            init, rx = parse_reactions(open(a.file, encoding="utf-8").read())
            rng = random.Random(a.seed)
            runs = [ssa(init, rx, a.t, rng) for _ in range(a.runs)]
            print("%d runs to t = %g (seed %d)" % (a.runs, a.t, a.seed))
            for s in sorted(init):
                vals = sorted(r[s] for r in runs)
                mean = sum(vals) / len(vals)
                sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / max(1, len(vals) - 1))
                print("  %-10s mean %.4g   sd %.4g   range %d to %d   zero in %d runs" % (s, mean, sd, vals[0], vals[-1], sum(1 for v in vals if v == 0)))
        elif a.op == "boolean":
            nodes, code = parse_rules(open(a.file, encoding="utf-8").read())
            att = attractors(nodes, code)
            print("%d attractor(s), synchronous update; nodes %s" % (len(att), " ".join(nodes)))
            for cyc in att:
                kind = "fixed point" if len(cyc) == 1 else "cycle of length %d" % len(cyc)
                print("  %s: %s" % (kind, " -> ".join("".join("1" if b else "0" for b in st) for st in cyc)))
        elif a.op == "map":
            orb = logistic_orbit(a.r, a.x0, a.steps)
            print("last values: " + ", ".join("%.6g" % v for v in orb[-6:]))
            for x, stable in logistic_fixed_points(a.r):
                print("fixed point %.6g: %s" % (x, "stable" if stable else "unstable"))
        else:
            ap.error("give an operation or --selftest")
    except (ValueError, OSError, TypeError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
