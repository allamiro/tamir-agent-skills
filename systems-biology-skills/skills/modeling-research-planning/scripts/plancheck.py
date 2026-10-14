#!/usr/bin/env python3
"""Check a proposal plan for the fields every aim needs (standard library only).

  plancheck.py PLAN.md       report missing or empty fields per aim, and the plan-level fields
  plancheck.py --selftest

PLAN.md follows assets/templates/proposal-plan.md: plan-level lines "Question:", "Hypothesis:" and "Refuting
result:", and one "## Aim N: title" section per aim with the lines Hypothesis, Modelling task, Experiment,
Measurement, Analysis, Risk, Alternative, Deliverable and Depends on. A field counts as filled when it has text
after the colon. "Depends on" may say "none". The check is structural: it cannot judge whether a hypothesis is
falsifiable or a risk realistic.

It also warns when every aim after the first depends on the one before it (a chain in which one failure stops
the project).
"""
import argparse
import re
import sys

PLAN_FIELDS = ["Question", "Hypothesis", "Refuting result"]
AIM_FIELDS = ["Hypothesis", "Modelling task", "Experiment", "Measurement", "Analysis", "Risk", "Alternative",
              "Deliverable", "Depends on"]


def field(text, name):
    m = re.search(r"^%s:[ \t]*(.*)$" % re.escape(name), text, re.M)
    if not m:
        return None
    return m.group(1).strip()


def check(text):
    problems = []
    head = re.split(r"^## Aim", text, maxsplit=1, flags=re.M)[0]
    for f in PLAN_FIELDS:
        v = field(head, f)
        if v is None:
            problems.append("plan: missing '%s:'" % f)
        elif not v:
            problems.append("plan: '%s' is empty" % f)
    aims = re.findall(r"^## Aim (\d+)[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not aims:
        problems.append("plan: no '## Aim N:' sections")
    deps = []
    for num, body in aims:
        for f in AIM_FIELDS:
            v = field(body, f)
            if v is None:
                problems.append("aim %s: missing '%s:'" % (num, f))
            elif not v:
                problems.append("aim %s: '%s' is empty" % (num, f))
        deps.append((int(num), field(body, "Depends on") or ""))
    if len(deps) >= 3:
        chained = all(re.search(r"\b(aim\s*)?%d\b" % (n - 1), d, re.I) for n, d in deps[1:])
        if chained:
            problems.append("warning: every aim depends on the previous one; one failure would stop the rest")
    return problems, len(aims)


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    full_aim = "Hypothesis: h\nModelling task: m\nExperiment: e\nMeasurement: r\nAnalysis: a\nRisk: k\nAlternative: b\nDeliverable: d\nDepends on: %s\n"
    good = "Question: q\nHypothesis: h\nRefuting result: r\n\n## Aim 1: x\n" + full_aim % "none" + "\n## Aim 2: y\n" + full_aim % "none"
    eq("complete plan has no problems", check(good), ([], 2))
    missing = good.replace("Risk: k\n", "", 1)
    eq("missing risk is reported", check(missing)[0], ["aim 1: missing 'Risk:'"])
    empty = good.replace("Refuting result: r", "Refuting result:")
    eq("empty plan field is reported", check(empty)[0], ["plan: 'Refuting result' is empty"])
    chain = "Question: q\nHypothesis: h\nRefuting result: r\n" + "".join(
        "\n## Aim %d: t\n" % i + full_aim % ("none" if i == 1 else "Aim %d" % (i - 1)) for i in (1, 2, 3))
    eq("a full chain is warned about", check(chain)[0], ["warning: every aim depends on the previous one; one failure would stop the rest"])
    eq("no aims", check("Question: q\nHypothesis: h\nRefuting result: r\n")[0], ["plan: no '## Aim N:' sections"])
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("plancheck selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Check a proposal plan for the fields every aim needs.")
    ap.add_argument("plan", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.plan:
        ap.error("give PLAN.md or --selftest")
    try:
        text = open(a.plan, encoding="utf-8").read()
    except OSError as e:
        print("error:", e)
        return 2
    problems, n = check(text)
    for p in problems:
        print(p)
    hard = [p for p in problems if not p.startswith("warning")]
    print("%d aims, %d missing or empty fields, %d warnings" % (n, len(hard), len(problems) - len(hard)))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
