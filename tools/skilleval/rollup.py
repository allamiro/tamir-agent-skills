"""Cross-collection results table for TESTING.md (standard library only).

Reads each collection's evals/results/*.json and writes one set of tables between the <!-- results:start --> and
<!-- results:end --> markers in TESTING.md, so the numbers on that page are the saved numbers and nothing is retyped.
"""
import json
import os

from . import stats

START, END = "<!-- results:start -->", "<!-- results:end -->"
COLLECTIONS = ["system-design-skills", "egyptology-skills", "bioinformatics-skills"]


def _load(col, name):
    path = os.path.join(col, "evals", "results", name)
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return None


def _p(k, n):
    if not n:
        return "n/a"
    lo, hi = stats.wilson(k, n)
    return "%.0f%% (%.0f-%.0f)" % (100.0 * k / n, 100 * lo, 100 * hi)


def _diff(k1, n1, k2, n2):
    d, lo, hi = stats.newcombe_diff(k1, n1, k2, n2)
    return "%+.0f (%+.0f to %+.0f)" % (100 * d, 100 * lo, 100 * hi)


def build(root, only=None, level=3):
    names = [(c, os.path.join(root, c)) for c in COLLECTIONS if not only or c == only]
    out = []
    rows = []
    for name, path in names:
        o = _load(path, "outcome.json")
        if not o:
            continue
        s, m = o["summary"], o["meta"]
        rows.append((name, s, m))
    if rows:
        out += ["### Outcome runs: starter prompts with and without the skills", "",
                "Share of runs passing each check, with Wilson 95% intervals; the last column is the difference in percentage points with a Newcombe interval. "
                "Rubric and limits are judged by a model.", "",
                "| Collection | Skills | Runs per arm | Facts: skills / none | Rubric: skills / none | Rubric difference | Limits: skills / none | Expected skill invoked |",
                "|---|---|---|---|---|---|---|---|"]
        for name, s, m in rows:
            w, wo = s["overall"]["with"], s["overall"]["without"]
            out.append("| %s | %d | %d / %d | %s / %s | %s / %s | %s | %s / %s | %s |" % (
                name, w["skills"], w["runs"], wo["runs"], _p(w["facts"], w["runs"]), _p(wo["facts"], wo["runs"]), _p(w["rubric"], w["runs"]), _p(wo["rubric"], wo["runs"]),
                _diff(w["rubric"], w["runs"], wo["rubric"], wo["runs"]), _p(w["calibration"], w["runs"]), _p(wo["calibration"], wo["runs"]), _p(w["fired"], w["runs"])))
        flagged_rows = [(name, s, m) for name, s, m in rows if s["neutral"]["with"]["skills"] != s["overall"]["with"]["skills"]]
        if flagged_rows:
            out += ["", "Leaving out the starter prompts that ask for the skill's own table, checker or template:", "",
                    "| Collection | Skills kept | Facts: skills / none | Rubric: skills / none | Rubric difference |", "|---|---|---|---|---|"]
        for name, s, m in flagged_rows:
            nw, nwo = s["neutral"]["with"], s["neutral"]["without"]
            out.append("| %s | %d | %s / %s | %s / %s | %s |" % (name, nw["skills"], _p(nw["facts"], nw["runs"]), _p(nwo["facts"], nwo["runs"]),
                                                               _p(nw["rubric"], nw["runs"]), _p(nwo["rubric"], nwo["runs"]), _diff(nw["rubric"], nw["runs"], nwo["rubric"], nwo["runs"])))
        out += ["", "### Tokens and cost per run (means)", "",
                "| Collection | Output tokens: skills / none | Input tokens read: skills / none | Cost, US dollars: skills / none | Runs with a denied tool call: skills / none |", "|---|---|---|---|---|"]
        for name, s, m in rows:
            w, wo = s["overall"]["with"], s["overall"]["without"]
            out.append("| %s | {:,.0f} / {:,.0f} | {:,.0f} / {:,.0f} | %.3f / %.3f | %d / %d |".format(
                w["mean_out_tokens"] or 0, wo["mean_out_tokens"] or 0, w["mean_in_tokens"] or 0, wo["mean_in_tokens"] or 0) % (
                name, w["mean_cost"] or 0, wo["mean_cost"] or 0, w.get("denied", 0), wo.get("denied", 0)))
        out += [""]
    trows = []
    for name, path in names:
        t = _load(path, "trigger.json")
        if t:
            trows.append((name, t["summary"], t["meta"]))
    if trows:
        out += ["### Trigger runs: does the agent pick the right skill", "",
                "| Collection | Should-trigger runs hit (recall) | Near-miss runs correctly left alone (specificity) | Precision | Unrelated prompts that triggered a skill |", "|---|---|---|---|---|"]
        for name, s, m in trows:
            tp, fn, fp, tn = s["tp"], s["fn"], s["fp"], s["tn"]
            out.append("| %s | %s | %s | %s | %d of %d |" % (name, _p(tp, tp + fn), _p(tn, tn + fp), _p(tp, tp + fp), s["unrelated_false"], s["unrelated_runs"]))
        out += [""]
    prow = []
    for name, path in names:
        p = _load(path, "pairwise.json")
        if p:
            prow.append((name, p["tally"], p["meta"]))
    if prow:
        out += ["### Model-judged pairwise comparison (both orders)", "",
                "| Collection | Skill preferred | Baseline preferred | Tie | Inconsistent across orders | Share preferring the skill, decisive pairs only |", "|---|---|---|---|---|---|"]
        for name, t, m in prow:
            wr = "n/a" if t["win_rate_decisive"] is None else "%.0f%% (%.0f-%.0f)" % (100 * t["win_rate_decisive"], 100 * t["win_rate_ci"][0], 100 * t["win_rate_ci"][1])
            out.append("| %s | %d | %d | %d | %d | %s |" % (name, t["skill"], t["baseline"], t["tie"], t["inconsistent"], wr))
        out += [""]
    crow = []
    for name, path in names:
        c = _load(path, "codex.json")
        if c:
            crow.append((name, c["summary"], c["meta"]))
    if crow:
        out += ["### Codex smoke test (one run per prompt and arm, facts only)", "",
                "| Collection | Every expected fact: skills / none | Expected skill used | Any skill used |", "|---|---|---|---|"]
        for name, recs, m in crow:
            w = [r for r in recs if r["arm"] == "with"]
            wo = [r for r in recs if r["arm"] == "without"]
            out.append("| %s | %d of %d / %d of %d | %d of %d | %d of %d |" % (name, sum(r["all_facts"] for r in w), len(w), sum(r["all_facts"] for r in wo), len(wo),
                                                                              sum(r["fired"] for r in w), len(w), sum(r["any_skill"] for r in w), len(w)))
        out += [""]
    for name, path in names:
        f = os.path.join(path, "evals", "results", "judge-check.md")
        extra = ""
        o = _load(path, "outcome.json")
        rj = (o or {}).get("meta", {}).get("rejudge")
        if rj:
            extra = " Verdicts in the tables are the majority of 3 judge votes; the second and third votes changed %d of %d verdicts." % (rj["changed"], rj["verdicts"])
        if os.path.isfile(f):
            line = [l for l in open(f, encoding="utf-8").read().splitlines() if l.startswith("| Rubric") or l.startswith("| States")]
            if line:
                out += ["Judge self-agreement with a single vote, %s: %s.%s" % (name, "; ".join(l.strip("| ").replace(" | ", ", ") for l in line), extra), ""]
        elif extra:
            out += ["%s:%s" % (name, extra), ""]
    hum = [name for name, path in names if os.path.isfile(os.path.join(path, "evals", "results", "human.md"))]
    out.append("Human grading: %s." % ("scored for " + ", ".join(hum) if hum else "the blind kit is built (`run_evals.py sheet`) but no person has graded any answers yet, so none of the judged results above has been checked against human preference"))
    text = "\n".join(out) + "\n"
    if level != 3:
        text = "\n".join(("#" * (level - 3)) + l if l.startswith("### ") else l for l in text.split("\n"))
    return text


def splice(text, block):
    if START not in text or END not in text:
        raise ValueError("no results markers in the file")
    a = text.index(START) + len(START)
    b = text.index(END)
    return text[:a] + "\n\n" + block + "\n" + text[b:]


def main(args):
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    path = os.path.join(root, "TESTING.md")
    text = open(path, encoding="utf-8").read()
    open(path, "w", encoding="utf-8").write(splice(text, build(root)))
    print("updated the results section of TESTING.md")
    for c in COLLECTIONS:
        readme = os.path.join(root, c, "README.md")
        text = open(readme, encoding="utf-8").read()
        if START in text and END in text:
            block = build(root, only=c, level=4)
            open(readme, "w", encoding="utf-8").write(splice(text, block))
            print("updated the results block in %s/README.md" % c)
    return 0


def selftest():
    import tempfile
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    eq("percent cell", _p(5, 10), "50% (24-76)")
    eq("empty cell", _p(0, 0), "n/a")
    eq("difference cell", _diff(80, 100, 60, 100), "+20 (+7 to +32)")
    with tempfile.TemporaryDirectory() as tmp:
        col = os.path.join(tmp, "egyptology-skills", "evals", "results")
        os.makedirs(col)
        arm = lambda f, r, c, fired: {"runs": 10, "skills": 4, "facts": f, "rubric": r, "calibration": c, "fired": fired, "script": 3, "any_skill": fired, "errors": 0,
                                      "denied": 1, "mean_out_tokens": 1000.0, "mean_in_tokens": 90000.0, "mean_cost": 0.2, "total_cost": 2.0}
        summ = {"overall": {"with": arm(9, 8, 9, 10), "without": arm(6, 3, 5, 0)}, "flagged": [], "skills": {},
                "neutral": {"with": {"runs": 10, "facts": 9, "rubric": 8, "calibration": 9, "skills": 4}, "without": {"runs": 10, "facts": 6, "rubric": 3, "calibration": 5, "skills": 4}}}
        json.dump({"meta": {}, "summary": summ}, open(os.path.join(col, "outcome.json"), "w"))
        json.dump({"meta": {}, "summary": {"tp": 9, "fn": 1, "fp": 1, "tn": 9, "unrelated_false": 0, "unrelated_runs": 2, "skills": {}, "confusions": []}}, open(os.path.join(col, "trigger.json"), "w"))
        text = build(tmp)
        eq("outcome table", "| egyptology-skills | 4 | 10 / 10 | 90% (60-98) / 60% (31-83) | 80% (49-94) / 30% (11-60) |" in text, True)
        eq("difference shown", "+50 (" in text, True)
        eq("trigger table", "| egyptology-skills | 90% (60-98) | 90% (60-98) | 90% (60-98) | 0 of 2 |" in text, True)
        eq("human line says none graded", "no person has graded any answers yet" in text, True)
        open(os.path.join(col, "human.md"), "w").write("x")
        eq("human line updates when a file exists", "scored for egyptology-skills" in build(tmp), True)
    doc = "intro\n<!-- results:start -->\nold\n<!-- results:end -->\nrest\n"
    new = splice(doc, "NEW\n")
    eq("splice replaces", ("old" in new, "NEW" in new, new.startswith("intro"), new.endswith("rest\n")), (False, True, True, True))
    eq("splice is repeatable", splice(new, "NEW\n"), new)
    try:
        splice("no markers", "x")
        fails.append("missing markers should raise")
    except ValueError:
        pass
    count[0] += 1
    return fails, count[0]
