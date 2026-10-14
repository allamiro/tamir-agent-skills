"""How steady is the model judge? Re-grade a sample of saved runs and compare with the first verdicts (standard library only).

This measures the judge's agreement with itself, not its accuracy: a judge can be consistently wrong. Accuracy needs
human graders (humankit). Self-agreement is still worth knowing, because a judge that flips on repeat cannot be used to
compare arms.
"""
import json
import os
import random
from concurrent.futures import ThreadPoolExecutor

from . import cases as cases_mod, direct, stats


def resample(records, n, seed=1):
    pool = [r for r in records if r.get("kind") == "outcome" and r.get("text") and "rubric" in r.get("graders", {})]
    rng = random.Random(seed)
    rng.shuffle(pool)
    return pool[:n]


def compare_verdicts(first, second):
    """Agreement and kappa for the two criteria. first/second: lists of (rubric, limits) pairs of booleans."""
    out = {}
    for i, name in enumerate(("rubric", "limits")):
        a = ["PASS" if x[i] else "FAIL" for x in first]
        b = ["PASS" if x[i] else "FAIL" for x in second]
        agree = sum(1 for x, y in zip(a, b) if x == y)
        out[name] = {"n": len(a), "agree": agree, "kappa": stats.cohen_kappa(a, b) if a else None}
    return out


def render(res, meta):
    lines = ["# Judge self-agreement", "",
             "%d saved answers were graded a second time by the same judge (%s) with the same rubric. Agreement with itself says how steady the judge is; "
             "it does not say the judge is right." % (res["rubric"]["n"], meta.get("judge_model", "default")), "",
             "| Criterion | Same verdict twice | Cohen's kappa |", "|---|---|---|"]
    for name, label in (("rubric", "Rubric"), ("limits", "States its limits")):
        r = res[name]
        k = "n/a" if r["kappa"] is None else "%.2f" % r["kappa"]
        lines.append("| %s | %d of %d | %s |" % (label, r["agree"], r["n"], k))
    lines += ["", "Each answer was graded again with one fresh vote and compared with the stored verdict (the majority of three votes once re-judging has been run). "
              "Cohen's kappa is unreliable when almost every verdict is the same, as with a rubric that nearly all answers pass; read the counts first."]
    return "\n".join(lines) + "\n"


def combine(first, extra):
    """Majority of the first verdict and the extra ones (all booleans); an even split counts as FAIL."""
    votes = [first] + list(extra)
    return sum(votes) * 2 > len(votes)


def rejudge(records, info, judge_model, extra=2, runner=None, jobs=4, fresh=()):
    """Add `extra` more judge votes to every saved outcome answer and keep the majority. For skills in `fresh` the earlier verdict
    is discarded and replaced by the majority of `extra + 1` new votes (use it after a rubric was corrected). Returns (records, cost, changed)."""
    todo = [r for r in records if r.get("kind") == "outcome" and r.get("text") and "rubric" in r.get("graders", {})]
    cost = [0.0]
    changed = [0]

    def work(r):
        if r.get("judge_votes", 1) > 1 and r["key"] not in fresh:
            return   # already has several votes
        prompt, rubric = info[r["key"]]
        extra_r, extra_l = [], []
        for _ in range(extra):
            v, _why, c = direct.judge_once(prompt, r["text"], rubric, cases_mod.CALIBRATION, judge_model, runner)
            cost[0] += c
            extra_r.append(bool(v.get("rubric")))
            extra_l.append(bool(v.get("limits")))
        old = (r["graders"]["rubric"]["passed"], r["graders"]["calibration"]["passed"])
        if r["key"] in fresh:
            v, _why, c = direct.judge_once(prompt, r["text"], rubric, cases_mod.CALIBRATION, judge_model, runner)
            cost[0] += c
            extra_r.append(bool(v.get("rubric")))
            extra_l.append(bool(v.get("limits")))
            r["graders"]["rubric"]["passed"] = sum(extra_r) * 2 > len(extra_r)
            r["graders"]["calibration"]["passed"] = sum(extra_l) * 2 > len(extra_l)
        else:
            r["graders"]["rubric"]["passed"] = combine(old[0], extra_r)
            r["graders"]["calibration"]["passed"] = combine(old[1], extra_l)
        r["judge_votes"] = 1 + extra
        if old != (r["graders"]["rubric"]["passed"], r["graders"]["calibration"]["passed"]):
            changed[0] += 1
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        list(pool.map(work, todo))
    return records, cost[0], changed[0]


def main_rejudge(args):
    from . import report
    col = os.path.abspath(args.collection)
    path = os.path.join(col, "evals", "runs", "latest-outcome.json")
    saved = json.load(open(path, encoding="utf-8"))
    data = cases_mod.load_cases(col)
    info = {}
    for c in data["outcome"]:
        prompt, good = cases_mod.resolve_outcome(col, c)
        info[c["skill"]] = (prompt, cases_mod.RUBRIC_TEMPLATE % (c.get("rubric") or good))
    model = args.judge_model or saved["meta"].get("judge_model") or "claude-sonnet-5-5"
    fresh = set(args.only or [])
    recs, cost, changed = rejudge(saved["records"], info, model, extra=2, fresh=fresh)
    if fresh:
        saved["meta"]["regraded_after_rubric_correction"] = sorted(fresh)
    saved["meta"]["judge_votes"] = 3
    saved["meta"]["rejudge"] = {"answers": len(recs), "verdicts": 2 * len(recs), "changed": changed}
    saved["meta"]["judge_model"] = model
    saved["meta"]["costUsd"] = round((saved["meta"].get("costUsd") or 0) + cost, 4)
    json.dump(saved, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    flagged = {c["skill"] for c in data["outcome"] if c.get("presupposes_skill")}
    summary = report.summarise_outcome(recs, flagged)
    meta = saved["meta"]
    import importlib
    run_evals = importlib.import_module("run_evals")
    body = run_evals._header("outcome", col, meta) + report.render_outcome(summary, meta)
    run_evals._save(col, "outcome", recs, meta, summary, body, meta.get("_stamp") or "")
    print("added 2 judge votes to %d answers (majority of 3); %d verdicts changed; extra cost %.2f US dollars" % (len(recs), changed, cost))
    return 0


def cross_judge(records, info, judge_model, runner=None, jobs=4):
    """Grade every saved outcome answer once with a second judge. Returns (list of (record, rubric, limits), cost)."""
    todo = [r for r in records if r.get("kind") == "outcome" and r.get("text") and "rubric" in r.get("graders", {})]
    cost = [0.0]

    def work(r):
        prompt, rubric = info[r["key"]]
        v, _why, c = direct.judge_once(prompt, r["text"], rubric, cases_mod.CALIBRATION, judge_model, runner)
        cost[0] += c
        return r, bool(v.get("rubric")), bool(v.get("limits"))
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        return list(pool.map(work, todo)), cost[0]


def cross_summary(graded):
    """Agreement with the stored verdicts and the with/without pass rates under the second judge."""
    out = {"n": len(graded)}
    for i, (name, key) in enumerate((("rubric", "rubric"), ("limits", "calibration"))):
        stored = ["PASS" if r["graders"][key]["passed"] else "FAIL" for r, _a, _b in graded]
        second = ["PASS" if g[1 + i] else "FAIL" for g in graded]
        out[name] = {"agree": sum(1 for x, y in zip(stored, second) if x == y), "kappa": stats.cohen_kappa(stored, second) if graded else None}
        for arm in ("with", "without"):
            sel = [g for g in graded if g[0]["arm"] == arm]
            out[name][arm] = {"runs": len(sel), "stored": sum(1 for g in sel if g[0]["graders"][key]["passed"]), "second": sum(1 for g in sel if g[1 + i])}
    return out


def main_cross(args):
    col = os.path.abspath(args.collection)
    saved = json.load(open(os.path.join(col, "evals", "runs", "latest-outcome.json"), encoding="utf-8"))
    data = cases_mod.load_cases(col)
    info = {}
    for c in data["outcome"]:
        prompt, good = cases_mod.resolve_outcome(col, c)
        info[c["skill"]] = (prompt, cases_mod.RUBRIC_TEMPLATE % (c.get("rubric") or good))
    model = args.judge_model or "claude-opus-5-5"
    graded, cost = cross_judge(saved["records"], info, model)
    summ = cross_summary(graded)
    summ["judge_model"], summ["first_judge_model"], summ["cost"] = model, saved["meta"].get("judge_model"), round(cost, 2)
    os.makedirs(os.path.join(col, "evals", "results"), exist_ok=True)
    json.dump(summ, open(os.path.join(col, "evals", "results", "cross-judge.json"), "w"), indent=1)
    open(os.path.join(col, "evals", "results", "cross-judge.md"), "w", encoding="utf-8").write(render_cross(summ))
    print(render_cross(summ))
    return 0


def render_cross(summ):
    lines = ["# Second judge", "",
             "Every saved answer (%d) was graded once more by %s, a different model from the first judge (%s), with the same rubric and limits check. "
             "The first judge's verdicts are the majority of three votes; this is a single vote. If the second judge agrees with the first and finds the same "
             "difference between the arms, the result does not depend on one judge model. Both are models, not people." % (summ["n"], summ["judge_model"], summ["first_judge_model"]), "",
             "| Check | Same verdict as the first judge | Cohen's kappa | With skills: first / second judge | No skills: first / second judge |", "|---|---|---|---|---|"]
    for name, label in (("rubric", "Rubric"), ("limits", "States its limits")):
        r = summ[name]
        k = "n/a" if r["kappa"] is None else "%.2f" % r["kappa"]
        lines.append("| %s | %d of %d | %s | %d / %d of %d | %d / %d of %d |" % (label, r["agree"], summ["n"], k, r["with"]["stored"], r["with"]["second"], r["with"]["runs"],
                                                                                 r["without"]["stored"], r["without"]["second"], r["without"]["runs"]))
    return "\n".join(lines) + "\n"


def main(args):
    if getattr(args, "cmd", "") == "rejudge":
        return main_rejudge(args)
    if getattr(args, "cmd", "") == "cross-judge":
        return main_cross(args)
    col = os.path.abspath(args.collection)
    path = os.path.join(col, "evals", "runs", "latest-outcome.json")
    if not os.path.isfile(path):
        raise SystemExit("no saved outcome runs: run `run --kind outcome` first")
    recs = json.load(open(path, encoding="utf-8"))["records"]
    data = cases_mod.load_cases(col)
    info = {}
    for c in data["outcome"]:
        prompt, good = cases_mod.resolve_outcome(col, c)
        info[c["skill"]] = (prompt, cases_mod.RUBRIC_TEMPLATE % (c.get("rubric") or good))
    sample = resample(recs, getattr(args, "n", 20) or 20, args.seed)
    model = args.judge_model or "claude-sonnet-5-5"

    def regrade(r):
        v, _why, _c = direct.judge_once(info[r["key"]][0], r["text"], info[r["key"]][1], cases_mod.CALIBRATION, model)
        return (bool(v.get("rubric")), bool(v.get("limits")))
    with ThreadPoolExecutor(max_workers=4) as pool:
        second = list(pool.map(regrade, sample))
    first = [(bool(r["graders"]["rubric"]["passed"]), bool(r["graders"]["calibration"]["passed"])) for r in sample]
    res = compare_verdicts(first, second)
    text = render(res, {"judge_model": model})
    os.makedirs(os.path.join(col, "evals", "results"), exist_ok=True)
    open(os.path.join(col, "evals", "results", "judge-check.md"), "w", encoding="utf-8").write(text)
    print(text)
    return 0


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    recs = [{"kind": "outcome", "text": "t", "graders": {"rubric": {}}, "key": str(i)} for i in range(10)] + [{"kind": "trigger", "text": "t", "graders": {}}, {"kind": "outcome", "text": "", "graders": {"rubric": {}}}]
    s = resample(recs, 5, seed=2)
    eq("sample size and filter", (len(s), all(r["kind"] == "outcome" and r["text"] for r in s)), (5, True))
    eq("sample is seeded", [r["key"] for r in resample(recs, 5, 2)], [r["key"] for r in s])
    eq("sample cannot exceed the pool", len(resample(recs, 50)), 10)
    first = [(True, True), (True, False), (False, False), (True, True)]
    r = compare_verdicts(first, first)
    eq("identical verdicts", (r["rubric"]["agree"], r["rubric"]["kappa"], r["limits"]["agree"]), (4, 1.0, 4))
    second = [(True, True), (False, False), (False, False), (True, False)]
    r = compare_verdicts(first, second)
    eq("partial agreement", (r["rubric"]["agree"], r["limits"]["agree"]), (3, 3))
    eq("kappa below one", r["rubric"]["kappa"] < 1.0, True)
    eq("empty comparison", compare_verdicts([], [])["rubric"]["kappa"], None)
    eq("render", "| Rubric | 3 of 4 |" in render(r, {"judge_model": "m"}), True)
    gr = [({"arm": "with", "graders": {"rubric": {"passed": True}, "calibration": {"passed": True}}}, True, False),
          ({"arm": "with", "graders": {"rubric": {"passed": True}, "calibration": {"passed": False}}}, False, False),
          ({"arm": "without", "graders": {"rubric": {"passed": False}, "calibration": {"passed": False}}}, False, True),
          ({"arm": "without", "graders": {"rubric": {"passed": False}, "calibration": {"passed": True}}}, False, True)]
    cs = cross_summary(gr)
    eq("cross summary agreement", (cs["n"], cs["rubric"]["agree"], cs["limits"]["agree"]), (4, 3, 2))
    eq("cross summary rates by arm", (cs["rubric"]["with"], cs["limits"]["without"]), ({"runs": 2, "stored": 2, "second": 1}, {"runs": 2, "stored": 1, "second": 2}))
    eq("cross render", "| Rubric | 3 of 4 |" in render_cross(dict(cs, judge_model="b", first_judge_model="a")), True)
    cg, cc = cross_judge([{"kind": "outcome", "text": "t", "key": "a", "arm": "with", "graders": {"rubric": {"passed": True}, "calibration": {"passed": True}}}],
                         {"a": ("p", "r")}, None, runner=lambda body: ({"rubric": False, "limits": True}, {}, 0.02), jobs=1)
    eq("cross judge grades once per answer", (len(cg), cg[0][1], cg[0][2], round(cc, 2)), (1, False, True, 0.02))
    eq("combine majority", (combine(True, [True, False]), combine(False, [True, False]), combine(True, [False, False]), combine(False, [True, True])), (True, False, False, True))
    eq("combine even split fails", combine(True, [False]), False)
    rr = [{"kind": "outcome", "text": "t", "key": "a", "graders": {"rubric": {"passed": True}, "calibration": {"passed": False}}},
          {"kind": "outcome", "text": "", "key": "a", "graders": {"rubric": {"passed": True}, "calibration": {"passed": True}}},
          {"kind": "trigger", "text": "x", "key": "b", "graders": {}}]
    votes = iter([({"rubric": False, "limits": True}, {}, 0.01), ({"rubric": False, "limits": True}, {}, 0.01)])
    out, cost, changed = rejudge(rr, {"a": ("p", "r")}, None, extra=2, runner=lambda body: next(votes), jobs=1)
    eq("rejudge flips both when both new votes disagree", (out[0]["graders"]["rubric"]["passed"], out[0]["graders"]["calibration"]["passed"], changed), (False, True, 1))
    eq("rejudge leaves unanswered and trigger records alone", (out[1]["graders"]["rubric"]["passed"], "judge_votes" in out[1], "judge_votes" in out[2]), (True, False, False))
    eq("rejudge cost and vote count", (round(cost, 2), out[0]["judge_votes"]), (0.02, 3))
    fr = [{"kind": "outcome", "text": "t", "key": "a", "graders": {"rubric": {"passed": True}, "calibration": {"passed": True}}}]
    out, cost, changed = rejudge(fr, {"a": ("p", "r")}, None, extra=2, runner=lambda body: ({"rubric": False, "limits": False}, {}, 0.01), jobs=1, fresh={"a"})
    eq("a fresh regrade ignores the earlier verdict", (out[0]["graders"]["rubric"]["passed"], out[0]["graders"]["calibration"]["passed"]), (False, False))
    eq("a fresh regrade uses three new votes", round(cost, 2), 0.03)
    done = [{"kind": "outcome", "text": "t", "key": "a", "judge_votes": 3, "graders": {"rubric": {"passed": True}, "calibration": {"passed": True}}}]
    out, cost, changed = rejudge(done, {"a": ("p", "r")}, None, extra=2, runner=lambda body: ({"rubric": False, "limits": False}, {}, 0.01), jobs=1)
    eq("records that already have several votes are skipped", (out[0]["graders"]["rubric"]["passed"], cost, changed), (True, 0.0, 0))
    return fails, count[0]
