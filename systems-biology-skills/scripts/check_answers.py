#!/usr/bin/env python3
"""Run the commands behind the exercises and the prompts' "a good answer" lines (standard library only).

Two kinds of check, both mechanical:
  1. every row of skills/systems-biology-learning-path/references/exercises.md: run its command and
     confirm the output contains the expected text;
  2. the computable "a good answer" lines in prompts/*.md: run the script and confirm the output
     contains the expected text, and that the number quoted in the prompt really appears in the
     prompt's own good-answer paragraph, so the prose and the computation cannot drift apart.

This checks the scripts and the answer key. It does not run any AI agent.

Usage: python3 scripts/check_answers.py [--verbose]
"""
import argparse
import glob
import os
import re
import shlex
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SCRIPTS = {os.path.basename(p): p for p in glob.glob(os.path.join(ROOT, "skills", "*", "scripts", "*.py"))}
EXERCISE_ROW = re.compile(r"^\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*$")

NET = "R1: -> A\nR2: A -> B\nR3: A -> C\nR4: B -> D\nR5: C -> D\nR6: D ->\n"
TOY = "R1: -> A\nR2: A -> B\nR3: A -> C\nR4: B -> D\nR5: C -> 2 D\nR6: D ->\nbounds R1 0 10\nbounds R4 0 3\n"
ENZ = "R1: S_ext + E <-> ES\nR2: ES -> E + P_ext\n"
GLYC = "R1: atp + glc -> adp + g6p\nR2: g6p <-> f6p\nR3: f6p + atp -> fbp + adp\n"
MM_ODE = "var S = 1\npar v0 = 1\npar Vmax = 2\npar Km = 0.5\nd S = v0 - Vmax*S/(Km+S)\n"
OSC_ODE = "var x = 1\nvar y = 0\npar a = 0.2\nd x = y\nd y = -x - a*y\n"
DECAY = "var x = 10\npar k = 0.5\nd x = -k*x\n"
DIRECTED = "X Y\nY Z\nX Z\nZ W\nW X\n"
TREE = "A B\nB C\nC D\nB E\nE F\n"
OMICS = "sample,g1,g2,g3\ns1,1,2,0.5\ns2,2,4,0.4\ns3,3,6,0.6\ns4,4,8,0.5\ns5,5,10,0.45\n"
OMICS_Y = "sample,g1,g2,g3,y\ns1,1,2,0.5,1.1\ns2,2,4,0.4,2.0\ns3,3,6,0.6,3.2\ns4,4,8,0.5,3.9\ns5,5,10,0.45,5.1\n"
ITEMS = "i1,i2,i3,i4\n1,1,0,1\n1,0,0,0\n1,1,1,1\n0,0,0,0\n1,1,1,0\n1,0,1,1\n0,1,0,0\n1,1,1,1\n"
GROUP_A = "5.1\n4.8\n5.6\n5.0\n5.3\n"
GROUP_B = "4.2\n4.6\n4.0\n4.4\n4.3\n"
MODELS = "model,rss,n,k\nA,2.1,12,3\nB,1.6,12,4\nC,1.9,12,4\n"
KIN = "S,v\n0.1,0.9\n0.25,1.9\n0.5,3.4\n1,4.9\n2,6.8\n4,8.0\n8,8.9\n"
PKDATA = "t,C\n0,0\n0.5,2.1\n1,3.0\n2,2.8\n4,1.6\n8,0.5\n12,0.15\n"
RING = "A = not C\nB = A\nC = B\n"
TOGGLE = "A = A and not B\nB = B and not A\n"
BIRTH_DEATH = "init A = 0\nrate R1 10: -> A\nrate R2 0.5: A ->\n"
REACTIONS = "R1: glc + 6 o2 -> 6 co2 + 6 h2o\nR2: pyr + nadh -> lac + nad\nEX_glc: glc ->\n"
FORMULAS = ("glc C6H12O6 0\no2 O2 0\nco2 CO2 0\nh2o H2O 0\npyr C3H3O3 -1\nlac C3H5O3 -1\n"
            "nadh C21H27N7O14P2 -2\nnad C21H26N7O14P2 -1\n")
REFS = "Nobody N (2019). A new result. J Imaginary Biol 5:1-9. doi:10.1000/imaginary.2019.1\n"
PLAN = ("Question: q\nHypothesis: h\nRefuting result: r\n\n## Aim 1: x\nHypothesis: h\nModelling task: m\n"
        "Experiment: e\nMeasurement: r\nAnalysis: a\nAlternative: b\nDeliverable: d\nDepends on: none\n")

# (prompt file, prompt number, files to create, command, text the output must contain, text the prompt must mention)
PROMPT_CHECKS = [
    ("quantities-units-balances", 1, {}, "units.py convert 1e6 \"1/(M*s)\" --to \"1/(uM*s)\"", "= 1 1/(uM*s)", "1 1/(µM s)"),
    ("quantities-units-balances", 1, {}, "units.py convert 1e6 \"1/(M*s)\" --to \"1/(mM*s)\"", "= 1000 1/(mM*s)", "1000 1/(mM s)"),
    ("quantities-units-balances", 2, {}, "units.py convert 0.1 1/min --to 1/h", "= 6 1/h", "6 per hour"),
    ("quantities-units-balances", 3, {}, "units.py chemostat --D 0.2 --mumax 0.5 --Ks 0.1 --S0 10 --Y 0.5", "S* = 0.0666667", "0.0667 g/L"),
    ("quantities-units-balances", 3, {}, "units.py chemostat --D 0.2 --mumax 0.5 --Ks 0.1 --S0 10 --Y 0.5", "X* = 4.96667", "4.97 g/L"),
    ("quantities-units-balances", 3, {}, "units.py chemostat --D 0.2 --mumax 0.5 --Ks 0.1 --S0 10 --Y 0.5", "critical D 0.49505", "0.495 per hour"),
    ("linear-algebra-networks", 1, {}, "linalg.py rank \"1,2;2,4\"", "rank 1 of a 2 x 2", "rank 1"),
    ("linear-algebra-networks", 1, {}, "linalg.py solve \"1,2;2,4\" --b \"3,6\"", "infinitely many solutions", "infinitely many solutions"),
    ("linear-algebra-networks", 2, {}, "linalg.py det \"2,1;1,3\"", "determinant 5", "determinant 5"),
    ("linear-algebra-networks", 2, {}, "linalg.py inv \"2,1;1,3\"", "[3/5, -1/5]", "(3/5, −1/5)"),
    ("linear-algebra-networks", 3, {}, "linalg.py eig \"0,1;-2,-3\"", "eigenvalues: -2, -1", "−2 and −1"),
    ("linear-algebra-networks", 4, {}, "linalg.py rref \"1,2,3;4,5,6\"", "[0, 1, 2]", "(0, 1, 2)"),
    ("linear-algebra-networks", 5, {}, "linalg.py null \"1,-1,0;0,1,-1\"", "[1, 1, 1]", "(1, 1, 1)"),
    ("network-analysis", 1, {"g.txt": DIRECTED}, "graphs.py motifs {g.txt}", "1 feed-forward loop(s)", "one feed-forward loop"),
    ("network-analysis", 2, {"u.txt": TREE}, "graphs.py measures {u.txt}", "B                 3      0.714        0.800", "(0.8 normalised)"),
    ("stoichiometric-networks", 1, {"n.txt": NET}, "stoich.py null {n.txt}", "dimension 2", "dimension 2"),
    ("stoichiometric-networks", 1, {"n.txt": NET}, "stoich.py efm {n.txt}", "2 elementary flux mode(s)", "2 elementary flux modes"),
    ("stoichiometric-networks", 2, {"n.txt": NET}, "stoich.py mfa {n.txt} --measured R1=10,R2=4", "system: determined", "R3 = 6, R4 = 4, R5 = 6 and R6 = 10"),
    ("stoichiometric-networks", 2, {"n.txt": NET}, "stoich.py mfa {n.txt} --measured R1=10", "system: underdetermined", "underdetermined"),
    ("stoichiometric-networks", 3, {"e.txt": ENZ}, "stoich.py conserved {e.txt}", "E + ES = constant", "E + ES = constant"),
    ("stoichiometric-networks", 4, {"g.txt": GLYC}, "stoich.py conserved {g.txt}", "atp + adp = constant", "atp + adp is conserved"),
    ("flux-balance-analysis", 1, {"t.txt": TOY}, "fba.py fba {t.txt} --objective R6", "objective R6 = 20", "R6 = 20"),
    ("flux-balance-analysis", 1, {"t.txt": TOY}, "fba.py ko {t.txt} --objective R6", "knock out R3         objective 3", "drops the objective to 3"),
    ("ode-dynamics", 1, {"m.txt": MM_ODE}, "ode.py stability {m.txt}", "eigenvalues: -1", "−Vmax Km/(Km + S)² = −1"),
    ("ode-dynamics", 1, {"m.txt": MM_ODE}, "ode.py sens {m.txt} --t 20", "v0                        2", "2 for v0, −2 for Vmax and 1 for Km"),
    ("ode-dynamics", 2, {"o.txt": OSC_ODE}, "ode.py stability {o.txt}", "-0.1+0.994987i", "−0.1 ± 0.995i"),
    ("ode-dynamics", 3, {"d.txt": DECAY}, "ode.py simulate {d.txt} --t 2 --dt 0.01 --every 100", "2\t3.67879", "3.679"),
    ("control-systems-feedback", 1, {}, "control.py ctrb \"0,1;-2,-3\" \"0;1\"", "controllable", "controllable"),
    ("control-systems-feedback", 1, {}, "control.py obsv \"0,1;-2,-3\" \"1,0\"", "observable", "observable"),
    ("control-systems-feedback", 1, {}, "control.py tf \"1\" \"1,3,2\"", "steady-state gain (s = 0): 0.5", "steady-state gain 0.5"),
    ("control-systems-feedback", 2, {}, "control.py routh \"1,1,2,8\"", "first column: 1, 1, -6, 8", "1, 1, −6, 8"),
    ("control-systems-feedback", 3, {}, "control.py loop --K 4 --tau 10", "closed-loop gain 0.8, time constant 2", "K/(1 + K) = 0.8"),
    ("control-systems-feedback", 4, {}, "control.py second --wn 2 --zeta 0.3", "overshoot_percent    37.2326", "about 37 percent"),
    ("enzyme-kinetics", 1, {"k.csv": KIN}, "kinetics.py fit {k.csv}", "Vmax = 10.0573, Km = 1.01338", "Km ≈ 1.01 mM"),
    ("enzyme-kinetics", 2, {}, "kinetics.py rate competitive --S 2 --Vmax 10 --Km 1 --I 1 --Ki 0.5", "v = 4", "falls from 6.67 to 4"),
    ("pharmacokinetic-modeling", 1, {}, "pk.py iv --dose 100 --V 20 --CL 5 --t 2", "C                            3.03265", "3.03 mg/L"),
    ("pharmacokinetic-modeling", 2, {}, "pk.py oral --dose 100 --F 0.8 --V 20 --CL 5 --ka 1.5 --t 2", "tmax                         1.43341", "1.43 h"),
    ("pharmacokinetic-modeling", 2, {}, "pk.py oral --dose 100 --F 0.8 --V 20 --CL 5 --ka 1.5 --t 2", "Cmax                         2.79531", "2.80 mg/L"),
    ("pharmacokinetic-modeling", 3, {}, "pk.py repeat --dose 100 --F 1 --V 20 --CL 5 --tau 8", "accumulation_ratio           1.15652", "1.16"),
    ("pharmacokinetic-modeling", 4, {"p.csv": PKDATA}, "pk.py auc {p.csv}", "AUC_0_tlast                  14.6", "14.6 mg·h/L"),
    ("pharmacokinetic-modeling", 4, {"p.csv": PKDATA}, "pk.py auc {p.csv} --log-down", "AUC_0_tlast                  13.9332", "about 13.9"),
    ("parameter-estimation-model-selection", 1, {"m.csv": MODELS}, "fitstats.py compare {m.csv}", "A                      -11.9156     0.0000   0.6036", "about 0.60"),
    ("parameter-estimation-model-selection", 1, {"m.csv": MODELS}, "fitstats.py compare {m.csv}", "B                      -10.4646     1.4511", "1.45"),
    ("parameter-estimation-model-selection", 2, {}, "fitstats.py ftest --rss1 4 --k1 2 --rss2 2.5 --k2 3 --n 20", "F = 10.2000 on (1, 17) degrees of freedom, p = 0.005319", "p ≈ 0.005"),
    ("parameter-estimation-model-selection", 4, {}, "fitstats.py ic --rss 1.2 --n 20 --k 3", "AIC -50.2682   AICc -48.7682   BIC -47.2810", "AICc ≈ −48.77"),
    ("stochastic-discrete-models", 1, {"b.txt": BIRTH_DEATH}, "discrete.py ssa {b.txt} --t 50 --runs 300 --seed 1", "mean 19.68", "mean near 20"),
    ("stochastic-discrete-models", 2, {"r.txt": RING}, "discrete.py boolean {r.txt}", "cycle of length 2: 010 -> 101", "cycle of length 2"),
    ("stochastic-discrete-models", 3, {"t.txt": TOGGLE}, "discrete.py boolean {t.txt}", "3 attractor(s)", "three fixed points"),
    ("stochastic-discrete-models", 4, {}, "discrete.py map --r 2.8", "fixed point 0.642857: stable", "0.643"),
    ("stochastic-discrete-models", 4, {}, "discrete.py map --r 3.2 --steps 200", "0.799455, 0.513045", "0.513 and 0.799"),
    ("multivariate-omics", 1, {"o.csv": OMICS}, "multivar.py pca {o.csv} --scale --components 2", "PC1                 2      66.7%", "66.7 percent"),
    ("multivariate-omics", 2, {"o.csv": OMICS_Y}, "multivar.py pls {o.csv} --y y --components 1 --scale", "g2                      0.783    1.224", "about 1.22 each"),
    ("quantitative-research-methods", 1, {"i.csv": ITEMS}, "measure.py alpha {i.csv}", "Cronbach's alpha 0.7139", "alpha ≈ 0.71"),
    ("quantitative-research-methods", 1, {"i.csv": ITEMS}, "measure.py alpha {i.csv}", "i2             alpha if dropped 0.7826   item-rest r 0.269", "about 0.78"),
    ("quantitative-research-methods", 3, {"a.csv": GROUP_A, "b.csv": GROUP_B}, "measure.py effect {a.csv} {b.csv}", "Cohen's d 3.216   Hedges' g 2.905", "Hedges' g ≈ 2.9"),
    ("systems-biology-programming", 1, {"r.txt": REACTIONS, "f.txt": FORMULAS}, "balance.py check {r.txt} {f.txt}", "R2           UNBALANCED  products minus substrates: H +1, charge +1", "H +1 and charge +1"),
    ("systems-biology-literature", 2, {"refs.txt": REFS}, "citecheck.py {refs.txt}", "DOI-SYNTAX-OK", "syntactically valid"),
    ("modeling-research-planning", 3, {"p.md": PLAN}, "plancheck.py {p.md}", "aim 1: missing 'Risk:'", "missing or empty field"),
]


def run(command, files, workdir):
    for name, text in files.items():
        with open(os.path.join(workdir, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    command = re.sub(r"\{([^}]+)\}", lambda m: os.path.join(workdir, m.group(1)), command)
    parts = shlex.split(command)
    script = SCRIPTS.get(parts[0])
    if script is None:
        return None, "no script named %s under skills/*/scripts/" % parts[0]
    r = subprocess.run([sys.executable, "-I", script] + parts[1:], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr, None


def good_answer(stem, number):
    """The 'A good answer:' paragraph of prompt `number` in prompts/<stem>.md, or None."""
    path = os.path.join(ROOT, "prompts", stem + ".md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^## %d\. .*?$(.*?)(?=^## |\Z)" % number, text, re.M | re.S)
    if not m:
        return None
    g = re.search(r"A good answer:(.*)", m.group(1), re.S)
    return " ".join(g.group(1).split()) if g else None


def main():
    ap = argparse.ArgumentParser(description="Check the exercise answers and the prompts' good-answer lines.")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    failures, passed = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        ex_path = os.path.join(ROOT, "skills", "systems-biology-learning-path", "references", "exercises.md")
        rows = []
        with open(ex_path, encoding="utf-8") as fh:
            for line in fh:
                m = EXERCISE_ROW.match(line.rstrip("\n"))
                if m:
                    rows.append((int(m.group(1)), m.group(2), m.group(3)))
        if len(rows) < 20:
            failures.append(("exercises", "found only %d exercise rows in exercises.md" % len(rows)))
        for number, command, expected in rows:
            out, problem = run(command, {}, tmp)
            ok = problem is None and expected in out
            if a.verbose:
                print("exercise %-2d %s  %s" % (number, "PASS" if ok else "FAIL", command))
            if ok:
                passed += 1
            else:
                failures.append(("exercise %d" % number, problem or "output lacks %r: %r" % (expected, out.strip()[:200])))
        for stem, number, files, command, expected, mention in PROMPT_CHECKS:
            label = "%s #%d" % (stem, number)
            out, problem = run(command, files, tmp)
            ok = problem is None and expected in out
            why = problem or ("output lacks %r: %r" % (expected, out.strip()[:200]) if not ok else None)
            if ok and mention:
                prose = good_answer(stem, number)
                if prose is None:
                    ok, why = False, "no 'A good answer' paragraph found for prompt %d" % number
                elif mention not in prose:
                    ok, why = False, "the prompt's good answer does not mention %r" % mention
            if a.verbose:
                print("prompt %-40s %s  %s" % (label, "PASS" if ok else "FAIL", command[:60]))
            if ok:
                passed += 1
            else:
                failures.append((label, why))
    for label, why in failures:
        print("FAIL %s: %s" % (label, why))
    print("%d answer checks passed, %d failed" % (passed, len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
