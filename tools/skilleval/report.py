"""Summaries of evaluation runs with confidence intervals (standard library only).

Outcome runs (with and without the skills) are summarised per skill and overall: how often the answer matched
every expected fact, passed the model-judged rubric, and stated its own limits; whether the skill and its script
ran; tokens and cost. Trigger runs are summarised as recall on should-trigger prompts, false-trigger rate on
near-miss and unrelated prompts, and which skill fired when the wrong one did.
"""
import re
from collections import Counter, defaultdict
from statistics import mean

from . import stats


def _pct(k, n):
    return "%d/%d" % (k, n)


def _ci(k, n):
    lo, hi = stats.wilson(k, n)
    return "%.0f%% (%.0f-%.0f)" % (100.0 * k / n if n else 0, 100 * lo, 100 * hi)


def _flags(rec):
    g = rec["graders"]
    facts = [v["passed"] for name, v in g.items() if name.startswith("fact-")]
    return {
        "facts": bool(facts) and all(facts),
        "rubric": bool(g.get("rubric", {}).get("passed")),
        "calibration": bool(g.get("calibration", {}).get("passed")),
        "fired": rec["key"] in rec["skills"],
        "script": bool(g.get("script-run", {}).get("passed")),
        "has_script": "script-run" in g,
        "any_skill": bool(rec["skills"]),
        "denied": bool(rec.get("denied")),
    }


def summarise_outcome(recs, flagged=()):
    """Dict with per-skill and overall counts and means for the 'with' and 'without' arms."""
    by = defaultdict(lambda: {"with": [], "without": []})
    for r in recs:
        if r["kind"] == "outcome":
            by[r["key"]][r["arm"]].append(r)
    out = {"skills": {}, "overall": {}}
    totals = {"with": defaultdict(int), "without": defaultdict(int)}
    cs = {"with": defaultdict(list), "without": defaultdict(list)}   # per-skill success counts, for pass^k
    nruns = {"with": 0, "without": 0}
    for skill in sorted(by):
        entry = {}
        for arm in ("with", "without"):
            rs = by[skill][arm]
            fl = [_flags(r) for r in rs]
            e = {"runs": len(rs)}
            for k in ("facts", "rubric", "calibration", "fired", "script", "any_skill", "denied", "has_script"):
                e[k] = sum(1 for f in fl if f[k])
            e["errors"] = sum(1 for r in rs if r.get("error"))
            for k, field in (("out_tokens", "out_tokens"), ("in_tokens", "in_tokens"), ("cost", "cost"), ("seconds", "seconds")):
                vals = [r[field] for r in rs if r.get(field) is not None]
                e[k] = round(mean(vals), 4) if vals else None
            entry[arm] = e
            nruns[arm] += len(rs)
            for k in ("facts", "rubric", "calibration", "fired", "script", "any_skill", "errors", "denied", "has_script"):
                totals[arm][k] += e[k]
            if rs:
                cs[arm]["facts"].append(e["facts"])
                cs[arm]["rubric"].append(e["rubric"])
        out["skills"][skill] = entry
    for arm in ("with", "without"):
        o = {"runs": nruns[arm], "skills": len(by)}
        o.update(totals[arm])
        n_per = max((len(by[s][arm]) for s in by), default=0)
        o["runs_per_skill"] = n_per
        if n_per:
            same = [c for s, c in zip(sorted(by), cs[arm]["facts"]) if len(by[s][arm]) == n_per]
            o["pass_hat_all_facts"] = round(stats.pass_hat_k(same, n_per, n_per), 4) if same else None
            same = [c for s, c in zip(sorted(by), cs[arm]["rubric"]) if len(by[s][arm]) == n_per]
            o["pass_hat_rubric"] = round(stats.pass_hat_k(same, n_per, n_per), 4) if same else None
        vals = lambda f: [r[f] for s in by for r in by[s][arm] if r.get(f) is not None]
        o["mean_out_tokens"] = round(mean(vals("out_tokens")), 1) if vals("out_tokens") else None
        o["mean_in_tokens"] = round(mean(vals("in_tokens")), 1) if vals("in_tokens") else None
        o["mean_cost"] = round(mean(vals("cost")), 4) if vals("cost") else None
        o["total_cost"] = round(sum(vals("cost")), 2)
        out["overall"][arm] = o
    out["flagged"] = sorted(flagged)
    out["neutral"] = {}
    for arm in ("with", "without"):
        n = {"runs": 0, "facts": 0, "rubric": 0, "calibration": 0, "skills": 0}
        for skill, e in out["skills"].items():
            if skill in flagged:
                continue
            n["skills"] += 1
            for k in ("runs", "facts", "rubric", "calibration"):
                n[k] += e[arm][k]
        out["neutral"][arm] = n
    return out


def render_outcome(summary, meta=None):
    meta = meta or {}
    ov = summary["overall"]
    w, wo = ov["with"], ov["without"]
    lines = []
    lines.append("Each skill's starter prompt was run %d times with the skills installed and %d times with none, each in a fresh Claude Code "
                 "project. Three kinds of check are reported separately: **facts** (regular expressions for the key facts in the answer), "
                 "**rubric** (a model judges the answer against the prompt's own \"a good answer\" description) and **limits stated** (a model "
                 "checks that the answer marks specific items as unverified or assumed and says what it did check). The judge is a model, not a person."
                 % (w.get("runs_per_skill", 0), wo.get("runs_per_skill", 0)))
    lines.append("")
    if meta:
        lines.append("Measured %s with %s." % ((meta.get("startedAt") or "")[:10], meta.get("claudeVersion", "Claude Code")))
        lines.append("")
    lines.append("## Overall")
    lines.append("")
    lines.append("| Check | With the skills | No skills | Difference (95% interval) |")
    lines.append("|---|---|---|---|")
    for label, key in (("Every expected fact present", "facts"), ("Rubric passed", "rubric"), ("States its limits", "calibration")):
        d, lo, hi = stats.newcombe_diff(w[key], w["runs"], wo[key], wo["runs"])
        lines.append("| %s | %s | %s | %+.0f points (%+.0f to %+.0f) |" % (
            label, _ci(w[key], w["runs"]), _ci(wo[key], wo["runs"]), 100 * d, 100 * lo, 100 * hi))
    if summary.get("flagged"):
        nw, nwo = summary["neutral"]["with"], summary["neutral"]["without"]
        lines.append("| **Only prompts that do not presuppose the skill (%d skills)** | | | |" % nw["skills"])
        for label, key in (("Every expected fact present", "facts"), ("Rubric passed", "rubric"), ("States its limits", "calibration")):
            d, lo, hi = stats.newcombe_diff(nw[key], nw["runs"], nwo[key], nwo["runs"])
            lines.append("| %s | %s | %s | %+.0f points (%+.0f to %+.0f) |" % (label, _ci(nw[key], nw["runs"]), _ci(nwo[key], nwo["runs"]), 100 * d, 100 * lo, 100 * hi))
    lines.append("| Expected skill invoked | %s | n/a | |" % _ci(w["fired"], w["runs"]))
    if w.get("has_script"):
        lines.append("| Its script run (skills that ship one, and not denied) | %s | n/a | |" % _ci(w["script"], w["has_script"]))
    lines.append("")
    if summary.get("flagged"):
        lines.append("")
        lines.append("Some starter prompts ask for the skill's own table, checker or template (%s). A run without the skill cannot "
                     "supply those, so the difference on those prompts overstates what the skill adds; the second block leaves them out." % ", ".join("`%s`" % f for f in summary["flagged"]))
    lines.append("")
    lines.append("Cells are the share of runs, with a Wilson 95%% interval. Runs: %d with, %d without (%d skills). "
                 "Runs of the same skill are not independent, so the intervals are narrower than the true uncertainty." % (
                     w["runs"], wo["runs"], w["skills"]))
    lines.append("")
    lines.append("Runs in which the permission mode denied at least one tool call: %d of %d with the skills, %d of %d without. Denied calls "
                 "do not count as a script run." % (w.get("denied", 0), w["runs"], wo.get("denied", 0), wo["runs"]))
    if w.get("pass_hat_all_facts") is not None:
        lines.append("")
        lines.append("Consistency (pass^%d: the chance that all %d runs of a skill pass): facts %.2f with the skills, %.2f without; "
                     "rubric %.2f with, %.2f without." % (
                         w["runs_per_skill"], w["runs_per_skill"], w["pass_hat_all_facts"], wo.get("pass_hat_all_facts") or 0,
                         w.get("pass_hat_rubric") or 0, wo.get("pass_hat_rubric") or 0))
    lines.append("")
    lines.append("Tokens and cost, mean per run: output tokens %s with and %s without; input tokens processed (including cached) "
                 "%s with and %s without; cost %s with and %s without US dollars; total spent on these runs %.2f (agent runs only, "
                 "judge calls excluded)." % (
                     "{:,.0f}".format(w["mean_out_tokens"] or 0), "{:,.0f}".format(wo["mean_out_tokens"] or 0),
                     "{:,.0f}".format(w["mean_in_tokens"] or 0), "{:,.0f}".format(wo["mean_in_tokens"] or 0),
                     "%.3f" % (w["mean_cost"] or 0), "%.3f" % (wo["mean_cost"] or 0), w["total_cost"] + wo["total_cost"]))
    lines.append("")
    lines.append("## By skill")
    lines.append("")
    lines.append("| Skill | Facts with | Facts without | Rubric with | Rubric without | Limits with | Limits without | Skill invoked | Script run |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for skill, e in summary["skills"].items():
        a, b = e["with"], e["without"]
        lines.append("| `%s` | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            skill, _pct(a["facts"], a["runs"]), _pct(b["facts"], b["runs"]), _pct(a["rubric"], a["runs"]), _pct(b["rubric"], b["runs"]),
            _pct(a["calibration"], a["runs"]), _pct(b["calibration"], b["runs"]), _pct(a["fired"], a["runs"]),
            _pct(a["script"], a["has_script"]) if a["has_script"] else "n/a"))
    errs = w["errors"] + wo["errors"]
    if errs:
        lines.append("")
        lines.append("%d run(s) ended with an error such as a turn or time limit; they are graded on what they produced." % errs)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines) + "\n")


def summarise_trigger(recs, cases):
    """cases: the list from cases.json 'trigger'. Returns counts and per-skill results."""
    meta = {t["id"]: t for t in cases}
    res = {"skills": defaultdict(lambda: {"pos_runs": 0, "pos_hit": 0, "neg_runs": 0, "neg_false": 0}),
           "unrelated_runs": 0, "unrelated_false": 0, "confusions": Counter(), "by_kind": defaultdict(lambda: [0, 0])}
    tp = fn = fp = tn = 0
    for r in recs:
        if r["kind"] != "trigger":
            continue
        t = meta.get(r["key"])
        if not t:
            continue
        ok = bool(r["graders"].get("trigger", {}).get("passed"))
        if t.get("expect"):
            s = res["skills"][t["expect"]]
            s["pos_runs"] += 1
            s["pos_hit"] += ok
            tp += ok
            fn += (not ok)
            if not ok and r["skills"]:
                res["confusions"][(t["expect"], r["skills"][0])] += 1
        elif t.get("avoid"):
            s = res["skills"][t["avoid"]]
            s["neg_runs"] += 1
            s["neg_false"] += (not ok)
            fp += (not ok)
            tn += ok
        else:
            res["unrelated_runs"] += 1
            res["unrelated_false"] += (not ok)
        res["by_kind"][t["kind"]][0] += ok
        res["by_kind"][t["kind"]][1] += 1
    res["tp"], res["fn"], res["fp"], res["tn"] = tp, fn, fp, tn
    res["skills"] = dict(res["skills"])
    res["by_kind"] = {k: v for k, v in res["by_kind"].items()}
    res["confusions"] = [[a, b, n] for (a, b), n in res["confusions"].most_common()]
    return res


def render_trigger(res, meta=None):
    meta = meta or {}
    tp, fn, fp, tn = res["tp"], res["fn"], res["fp"], res["tn"]
    recall = tp / (tp + fn) if tp + fn else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    spec = tn / (tn + fp) if tn + fp else 0.0
    lines = ["Each skill has a should-trigger prompt (written without naming the skill) and a near-miss prompt that shares vocabulary "
             "but belongs elsewhere; there are also unrelated prompts that should trigger nothing. Every prompt was run several times with "
             "the skills installed and the first skill the agent invoked was recorded from its tool calls. "
             "A should-trigger run passes when the expected skill was invoked; a near-miss run passes when the named skill was not.", ""]
    if meta:
        lines += ["Measured %s with %s." % ((meta.get("startedAt") or "")[:10], meta.get("claudeVersion", "Claude Code")), ""]
    lines += ["## Overall", "", "| Measure | Value |", "|---|---|"]
    lines.append("| Recall on should-trigger prompts | %s |" % _ci(tp, tp + fn))
    lines.append("| Specificity on near-miss prompts | %s |" % _ci(tn, tn + fp))
    lines.append("| Precision (invoked when it should be) | %s |" % _ci(tp, tp + fp))
    if res["unrelated_runs"]:
        lines.append("| Unrelated prompts that triggered a skill | %s |" % _pct(res["unrelated_false"], res["unrelated_runs"]))
    lines.append("")
    lines.append("Recall %.2f, precision %.2f, specificity %.2f. Wilson 95%% intervals; runs of one prompt are not independent." % (recall, precision, spec))
    lines += ["", "## By skill", "", "| Skill | Should-trigger runs hit | Near-miss runs that falsely triggered |", "|---|---|---|"]
    for skill in sorted(res["skills"]):
        s = res["skills"][skill]
        lines.append("| `%s` | %s | %s |" % (skill, _pct(s["pos_hit"], s["pos_runs"]), _pct(s["neg_false"], s["neg_runs"])))
    if res["confusions"]:
        lines += ["", "## When the wrong skill fired", "", "| Expected | Fired instead | Runs |", "|---|---|---|"]
        for a, b, n in res["confusions"][:12]:
            lines.append("| `%s` | `%s` | %d |" % (a, b, n))
    return "\n".join(lines) + "\n"


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    def rec(kind, key, arm, run, graders, skills=(), out=100, inp=1000, cost=0.1):
        return {"case": kind + "-" + key, "kind": kind, "key": key, "arm": arm, "run": run,
                "graders": {n: {"passed": p, "scored": True, "explanation": ""} for n, p in graders.items()},
                "skills": list(skills), "out_tokens": out, "in_tokens": inp, "cost": cost, "seconds": 10, "error": None}

    recs = []
    for i in range(1, 4):
        recs.append(rec("outcome", "alpha", "with", i, {"fact-1": True, "fact-2": i != 3, "rubric": True, "calibration": True, "skill-fired": True,
                                                         "script-run": i == 1}, ["alpha"], 200, 3000, 0.2))
        recs.append(rec("outcome", "alpha", "without", i, {"fact-1": True, "fact-2": False, "rubric": i == 1, "calibration": False}, [], 100, 1000, 0.1))
        recs.append(rec("outcome", "beta", "with", i, {"fact-1": True, "rubric": True, "calibration": True}, [], 300, 2000, 0.3))
        recs.append(rec("outcome", "beta", "without", i, {"fact-1": True, "rubric": True, "calibration": True}, [], 300, 1000, 0.1))
    s = summarise_outcome(recs, flagged=["alpha"])
    eq("neutral excludes flagged", (s["neutral"]["with"]["skills"], s["neutral"]["with"]["runs"], s["neutral"]["with"]["facts"]), (1, 3, 3))
    eq("neutral without arm", (s["neutral"]["without"]["facts"], s["flagged"]), (3, ["alpha"]))
    a = s["skills"]["alpha"]
    eq("alpha facts with", (a["with"]["facts"], a["with"]["runs"]), (2, 3))
    eq("alpha facts without", a["without"]["facts"], 0)
    eq("alpha rubric without", a["without"]["rubric"], 1)
    eq("alpha fired", a["with"]["fired"], 3)
    eq("alpha script", (a["with"]["script"], a["with"]["has_script"]), (1, 3))
    eq("beta has no script grader", s["skills"]["beta"]["with"]["has_script"], 0)
    eq("overall script denominator counts only skills with a script", (s["overall"]["with"]["script"], s["overall"]["with"]["has_script"]), (1, 3))
    eq("beta not fired", s["skills"]["beta"]["with"]["fired"], 0)
    eq("beta any skill", s["skills"]["beta"]["with"]["any_skill"], 0)
    eq("tokens mean alpha with", a["with"]["out_tokens"], 200.0)
    eq("overall runs", (s["overall"]["with"]["runs"], s["overall"]["without"]["runs"]), (6, 6))
    eq("overall facts with", s["overall"]["with"]["facts"], 5)
    eq("overall mean out tokens with", s["overall"]["with"]["mean_out_tokens"], 250.0)
    eq("overall total cost", s["overall"]["with"]["total_cost"], 1.5)
    # pass^3 of all facts with the skills: alpha 2 of 3 -> C(2,3)=0; beta 3 of 3 -> 1; mean 0.5
    eq("pass^3 facts with", s["overall"]["with"]["pass_hat_all_facts"], 0.5)
    text = render_outcome(s, {"startedAt": "2026-10-14T10:00:00Z", "claudeVersion": "9.9"})
    eq("render has table row", "| `alpha` | 2/3 | 0/3 |" in text, True)
    eq("render script cells", "| 1/3 |" in text and "| n/a |" in text, True)
    eq("render has difference row", "Every expected fact present" in text and "points" in text, True)
    eq("render has the neutral block", "Only prompts that do not presuppose the skill (1 skills)" in text and "`alpha`" in text, True)
    eq("render mentions the version", "with 9.9." in text, True)

    cases = [{"id": "a-pos", "prompt": "x", "expect": "alpha", "kind": "implicit"}, {"id": "a-neg", "prompt": "y", "expect": None, "avoid": "alpha", "kind": "near-miss"},
             {"id": "none", "prompt": "z", "expect": None, "kind": "unrelated"}]
    trecs = []
    for i in range(1, 4):
        trecs.append(rec("trigger", "a-pos", "with", i, {"trigger": i != 3}, ["alpha"] if i != 3 else ["beta"]))
        trecs.append(rec("trigger", "a-neg", "with", i, {"trigger": i == 1}, [] if i == 1 else ["alpha"]))
        trecs.append(rec("trigger", "none", "with", i, {"trigger": True}, []))
    t = summarise_trigger(trecs, cases)
    eq("tp fn fp tn", (t["tp"], t["fn"], t["fp"], t["tn"]), (2, 1, 2, 1))
    eq("unrelated", (t["unrelated_runs"], t["unrelated_false"]), (3, 0))
    eq("confusion recorded", t["confusions"], [["alpha", "beta", 1]])
    eq("per skill", t["skills"]["alpha"], {"pos_runs": 3, "pos_hit": 2, "neg_runs": 3, "neg_false": 2})
    eq("by kind", t["by_kind"]["near-miss"], [1, 3])
    text = render_trigger(t)
    eq("trigger render recall", "Recall 0.67, precision 0.50, specificity 0.33" in text, True)
    eq("trigger render confusion", "| `alpha` | `beta` | 1 |" in text, True)
    return fails, count[0]
