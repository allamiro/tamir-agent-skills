#!/usr/bin/env python3
"""Critical path and slack for a research plan (standard library only).

  schedule.py PLAN.csv [--deadline WEEKS] [--buffer 0.3]
  schedule.py --selftest

PLAN.csv has columns task,weeks,after where after lists the tasks that must finish first, separated by
semicolons (empty for none). The program finds the earliest finish of every task, the critical path
that sets the total length, and, with --deadline, whether the plan fits once a buffer is added.

The buffer is a fraction added to the total (0.3 adds 30 percent). Plans usually run longer than their
authors expect, so a buffer is a sensible habit, but the right size depends on the project: the default
of 0.3 is an illustration, not a rule. The estimates in the file are yours; the program only does the arithmetic.
"""
import argparse
import csv
import sys


def load(path):
    tasks = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                tasks[r["task"].strip()] = (float(r["weeks"]), [x.strip() for x in (r.get("after") or "").split(";") if x.strip()])
            except (KeyError, ValueError):
                raise SystemExit("%s: need columns task,weeks,after with numeric weeks" % path)
    return tasks


def analyse(tasks):
    """Return (finish times, critical path list, total weeks). Raises ValueError on unknown tasks or a cycle."""
    for name, (_w, deps) in tasks.items():
        for d in deps:
            if d not in tasks:
                raise ValueError("task %r depends on unknown task %r" % (name, d))
        if tasks[name][0] < 0:
            raise ValueError("task %r has negative duration" % name)
    finish, via, state = {}, {}, {}

    def visit(n, stack):
        if state.get(n) == 2:
            return finish[n]
        if state.get(n) == 1:
            raise ValueError("dependency cycle: " + " -> ".join(stack + [n]))
        state[n] = 1
        start, best = 0.0, None
        for d in tasks[n][1]:
            f = visit(d, stack + [n])
            if best is None or f > start:
                start, best = f, d
        finish[n] = start + tasks[n][0]
        via[n] = best
        state[n] = 2
        return finish[n]

    for n in sorted(tasks):
        visit(n, [])
    if not tasks:
        raise ValueError("no tasks")
    last = max(sorted(finish), key=lambda n: finish[n])
    path = []
    while last is not None:
        path.append(last)
        last = via[last]
    return finish, list(reversed(path)), max(finish.values())


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    t = {"A": (2.0, []), "B": (3.0, ["A"]), "C": (1.0, ["A"]), "D": (2.0, ["B", "C"])}
    f, path, total = analyse(t)
    eq("finish times", f, {"A": 2.0, "B": 5.0, "C": 3.0, "D": 7.0})
    eq("critical path", path, ["A", "B", "D"])
    eq("total", total, 7.0)
    eq("independent tasks run in parallel", analyse({"X": (4.0, []), "Y": (6.0, [])})[2], 6.0)
    eq("chain adds up", analyse({"X": (4.0, []), "Y": (6.0, ["X"]), "Z": (1.0, ["Y"])})[2], 11.0)
    eq("path of a chain", analyse({"X": (4.0, []), "Y": (6.0, ["X"]), "Z": (1.0, ["Y"])})[1], ["X", "Y", "Z"])
    eq("zero-length milestone", analyse({"X": (3.0, []), "M": (0.0, ["X"])})[2], 3.0)
    eq("single task", analyse({"X": (2.5, [])})[1], ["X"])
    for bad, label in ((lambda: analyse({"A": (1.0, ["B"]), "B": (1.0, ["A"])}), "cycle"),
                       (lambda: analyse({"A": (1.0, ["Z"])}), "unknown dependency"),
                       (lambda: analyse({}), "empty"),
                       (lambda: analyse({"A": (-1.0, [])}), "negative duration")):
        count[0] += 1
        try:
            bad()
            fails.append("%s should raise" % label)
        except ValueError:
            pass
    if fails:
        print("SELFTEST FAILED")
        for f_ in fails:
            print(" -", f_)
        return 1
    print("schedule selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Critical path and slack for a research plan.")
    ap.add_argument("plan", nargs="?")
    ap.add_argument("--deadline", type=float, help="weeks available")
    ap.add_argument("--buffer", type=float, default=0.3, help="fraction added to the total (default 0.3, an illustration)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.plan:
        ap.error("give a plan file or --selftest")
    try:
        finish, path, total = analyse(load(a.plan))
    except ValueError as e:
        print("error:", e)
        return 2
    for n in sorted(finish, key=lambda x: (finish[x], x)):
        print("  %-30s finishes at week %g%s" % (n, finish[n], "   <- critical path" if n in path else ""))
    print("critical path: %s" % " -> ".join(path))
    buffered = total * (1 + a.buffer)
    print("total %g weeks; with a %d%% buffer %g weeks" % (total, round(a.buffer * 100), buffered))
    if a.deadline is not None:
        slack = a.deadline - buffered
        print("deadline %g weeks: %s by %g weeks" % (a.deadline, "fits with slack" if slack >= 0 else "does NOT fit, short", abs(slack)))
        return 0 if slack >= 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
