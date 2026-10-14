#!/usr/bin/env python3
"""Element and charge balance of reactions, a basic quality check for metabolic and kinetic models
(standard library only).

  balance.py check REACTIONS.txt FORMULAS.txt     element and charge balance of every reaction
  balance.py formula "C6H12O6"                    parse one formula into element counts
  balance.py --selftest

REACTIONS.txt uses the same reaction lines as the other scripts ("R1: glc + atp -> g6p + adp"). FORMULAS.txt maps
each metabolite to a formula and, optionally, a charge:

    glc   C6H12O6   0
    atp   C10H12N5O13P3   -4

Formulas may use parentheses and integer counts, for example Ca(OH)2. A reaction with no formula for one of its
metabolites is reported as unchecked, not as balanced. Exchange and biomass reactions are normally unbalanced by
design; name them so they are easy to exclude when you read the report.
"""
import argparse
import re
import sys
from fractions import Fraction

ARROW = re.compile(r"\s*(<->|<=>|->|=>)\s*")


def parse_formula(text):
    tokens = re.findall(r"[A-Z][a-z]?|\d+|\(|\)", text)
    if "".join(tokens) != text.replace(" ", ""):
        raise ValueError("cannot read the formula %r" % text)
    stack = [{}]
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "(":
            stack.append({})
            i += 1
            continue
        if t == ")":
            if len(stack) == 1:
                raise ValueError("unbalanced parentheses in %r" % text)
            group = stack.pop()
            n = 1
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                n = int(tokens[i + 1])
                i += 1
            for el, c in group.items():
                stack[-1][el] = stack[-1].get(el, 0) + c * n
            i += 1
            continue
        if t.isdigit():
            raise ValueError("a count must follow an element or a closing parenthesis in %r" % text)
        n = 1
        if i + 1 < len(tokens) and tokens[i + 1].isdigit():
            n = int(tokens[i + 1])
            i += 1
        stack[-1][t] = stack[-1].get(t, 0) + n
        i += 1
    if len(stack) != 1:
        raise ValueError("unbalanced parentheses in %r" % text)
    return stack[0]


def parse_side(text):
    out = {}
    for term in [t.strip() for t in text.split("+") if t.strip()]:
        m = re.match(r"^(\d+(?:\.\d+)?(?:/\d+)?)?\s*([A-Za-z_][\w\[\]]*)$", term)
        if not m:
            raise ValueError("cannot read the term %r" % term)
        out[m.group(2)] = out.get(m.group(2), 0) + (Fraction(m.group(1)) if m.group(1) else Fraction(1))
    return out


def parse_reactions(text):
    out = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        name, eq = line.split(":", 1)
        parts = ARROW.split(eq)
        if len(parts) != 3:
            raise ValueError("each reaction needs exactly one arrow: %r" % raw)
        coeffs = {}
        for met, c in parse_side(parts[0]).items():
            coeffs[met] = coeffs.get(met, 0) - c
        for met, c in parse_side(parts[2]).items():
            coeffs[met] = coeffs.get(met, 0) + c
        out.append((name.strip(), coeffs))
    return out


def parse_formulas(text):
    table = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) not in (2, 3):
            raise ValueError("formula lines are 'name formula [charge]': %r" % raw)
        table[parts[0]] = (parse_formula(parts[1]), int(parts[2]) if len(parts) == 3 else 0)
    return table


def check(reactions, table):
    """List of (name, status, details) with status balanced, unbalanced or unchecked."""
    out = []
    for name, coeffs in reactions:
        missing = [m for m in coeffs if m not in table]
        if missing:
            out.append((name, "unchecked", "no formula for %s" % ", ".join(missing)))
            continue
        net, charge = {}, Fraction(0)
        for m, c in coeffs.items():
            f, q = table[m]
            for el, n in f.items():
                net[el] = net.get(el, 0) + c * n
            charge += c * q
        bad = {el: v for el, v in net.items() if v != 0}
        if bad or charge != 0:
            parts = ["%s %+g" % (el, float(v)) for el, v in sorted(bad.items())]
            if charge != 0:
                parts.append("charge %+g" % float(charge))
            out.append((name, "unbalanced", "products minus substrates: " + ", ".join(parts)))
        else:
            out.append((name, "balanced", ""))
    return out


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    eq("glucose", parse_formula("C6H12O6"), {"C": 6, "H": 12, "O": 6})
    eq("parentheses", parse_formula("Ca(OH)2"), {"Ca": 1, "O": 2, "H": 2})
    eq("nested parentheses", parse_formula("K4(Fe(CN)6)"), {"K": 4, "Fe": 1, "C": 6, "N": 6})
    table = parse_formulas("glc C6H12O6 0\no2 O2\nco2 CO2\nh2o H2O\nh H 1\nlac C3H5O3 -1\npyr C3H3O3 -1\nnadh C21H27N7O14P2 -2\nnad C21H26N7O14P2 -1")
    rx = parse_reactions("R1: glc + 6 o2 -> 6 co2 + 6 h2o\nR2: glc + o2 -> co2\nR3: pyr + nadh + h -> lac + nad\nR4: pyr + nadh -> lac + nad\nR5: glc -> biomass")
    res = {n: (s, d) for n, s, d in check(rx, table)}
    eq("respiration balanced", res["R1"][0], "balanced")
    eq("partial reaction unbalanced", res["R2"][0], "unbalanced")
    eq("lactate dehydrogenase with the proton balanced", res["R3"][0], "balanced")
    eq("without the proton: H and charge off by one", res["R4"], ("unbalanced", "products minus substrates: H +1, charge +1"))
    eq("missing formula is unchecked", res["R5"][0], "unchecked")
    for bad, label in ((lambda: parse_formula("C6H12O6)"), "unbalanced"), (lambda: parse_formula("6C"), "leading count"),
                       (lambda: parse_formula("c6"), "lower-case element"), (lambda: parse_formulas("glc"), "short line")):
        count[0] += 1
        try:
            bad()
            fails.append("%s should raise" % label)
        except ValueError:
            pass
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("balance selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Element and charge balance of reactions.")
    ap.add_argument("op", nargs="?", choices=["check", "formula"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        if a.op == "formula":
            print(", ".join("%s %d" % kv for kv in parse_formula(a.args[0]).items()))
        elif a.op == "check":
            res = check(parse_reactions(open(a.args[0], encoding="utf-8").read()), parse_formulas(open(a.args[1], encoding="utf-8").read()))
            for name, status, detail in res:
                print("%-12s %-11s %s" % (name, status.upper(), detail))
            print("%d balanced, %d unbalanced, %d unchecked" % tuple(sum(1 for r in res if r[1] == s) for s in ("balanced", "unbalanced", "unchecked")))
        else:
            ap.error("give an operation or --selftest")
    except (ValueError, OSError, IndexError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
