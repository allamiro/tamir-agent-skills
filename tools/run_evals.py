#!/usr/bin/env python3
"""Run and report skill evaluations for a collection (standard library only; needs the `claude` CLI to run).

  run_evals.py plan COLLECTION                       what would run, and a rough worst-case cost (free)
  run_evals.py run COLLECTION [--kind outcome|trigger|both] [--runs 3] [--only SKILL ...] [-j 4]
                              [--model M] [--judge-model M] [--max-cost-usd X]
  run_evals.py report COLLECTION                     rewrite evals/results/*.md from the saved runs (free)
  run_evals.py samples COLLECTION [--feature SKILL]  write examples/ and the README sample section (free)
  run_evals.py pairwise COLLECTION [--judge-model M] a model compares with-skill and no-skill answers, both orders
  run_evals.py sheet COLLECTION [--seed 1]           blind sheet for human graders, plus the answer key
  run_evals.py score COLLECTION --ratings CSV [CSV ...]   score filled-in ratings (win rate, agreement)
  run_evals.py cross-judge COLLECTION [--judge-model M] grade every saved answer once with a different judge model and compare
  run_evals.py rejudge COLLECTION                    add two more judge votes to every saved answer and keep the majority of three
  run_evals.py judge-check COLLECTION [-n 20]        re-grade a sample of saved answers to see how steady the judge is
  run_evals.py codex COLLECTION [--only SKILL ...]   smoke test of the same prompts in OpenAI Codex
  run_evals.py rollup COLLECTION                     rewrite the results tables in TESTING.md from every collection's saved results (free)
  run_evals.py selftest                              unit tests for every module (free)

`run` spends API credit: it launches `claude plugin eval` (Claude Code 2.1.269 or later), which runs every case
several times with the skills and, for outcome cases, again with none, plus a judge model for the rubric
checks. Use `plan` first and `--max-cost-usd` to cap a run. See TESTING.md.
"""
import argparse
import datetime
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from skilleval import cases as cases_mod  # noqa: E402
from skilleval import direct, native, report, stats  # noqa: E402

# rough per-run list-price estimates in US dollars, from the pilot runs (plan only; real cost is reported after a run)
EST = {"outcome_with": 0.20, "outcome_without": 0.12, "judge": 0.03, "trigger": 0.08}


def collection_path(arg):
    path = os.path.abspath(arg)
    if not os.path.isdir(os.path.join(path, "skills")):
        raise SystemExit("%s: not a collection (no skills/ folder)" % arg)
    return path


def cmd_plan(a):
    col = collection_path(a.collection)
    problems = cases_mod.validate(col)
    data = cases_mod.load_cases(col)
    n_out, n_trig = len(data["outcome"]), len(data["trigger"])
    runs = a.runs
    est_out = n_out * runs * (EST["outcome_with"] + EST["outcome_without"] + 2 * EST["judge"])
    est_trig = n_trig * runs * EST["trigger"]
    print("%s: %d outcome cases (%d runs each, with and without skills), %d trigger cases (%d runs each)" % (
        os.path.basename(col), n_out, runs, n_trig, runs))
    print("rough list-price estimate: outcome %.0f, trigger %.0f, total %.0f US dollars (a guess from pilot runs; cap a run with --max-cost-usd)" % (
        est_out, est_trig, est_out + est_trig))
    for p in problems:
        print("PROBLEM:", p)
    return 1 if problems else 0


def _save(col, kind, recs, meta, summary, markdown, stamp):
    runs_dir = os.path.join(col, "evals", "runs")
    res_dir = os.path.join(col, "evals", "results")
    os.makedirs(runs_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)
    with open(os.path.join(runs_dir, "%s-%s.json" % (stamp, kind)), "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "records": recs}, fh, ensure_ascii=False)
    with open(os.path.join(runs_dir, "latest-%s.json" % kind), "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "records": recs}, fh, ensure_ascii=False)
    with open(os.path.join(res_dir, "%s.json" % kind), "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "summary": summary}, fh, indent=1, ensure_ascii=False, default=lambda o: dict(o))
    with open(os.path.join(res_dir, "%s.md" % kind), "w", encoding="utf-8") as fh:
        fh.write(markdown)


def _title(kind, col, meta):
    models = sorted({r.get("model") for r in meta.get("_records", []) if r.get("model")})
    return "# %s results: %s\n\n" % (kind.capitalize(), os.path.basename(col))


def cmd_run(a):
    col = collection_path(a.collection)
    problems = cases_mod.validate(col)
    if problems:
        for p in problems:
            print("PROBLEM:", p)
        return 1
    data = cases_mod.load_cases(col)
    kinds = ["outcome", "trigger"] if a.kind == "both" else [a.kind]
    stamp = datetime.date.today().isoformat()
    only = set(a.only) if a.only else None
    for kind in kinds:
        name = kind + ("-" + a.label if a.label else "")
        print("running %s cases (%d runs each, engine %s) ..." % (name, a.runs, a.engine), flush=True)
        if a.engine == "direct":
            recs, meta = direct.run_cases(col, kind, runs=a.runs, only=only, jobs=a.jobs, model=a.model, judge_model=a.judge_model,
                                          votes=a.votes, max_cost=a.max_cost_usd)
        else:
            with tempfile.TemporaryDirectory() as tmp:
                cases_mod.build_suite(col, tmp, only=only)
                out_json = os.path.join(tmp, "result-%s.json" % kind)
                recs, meta, _proc = native.run_native(tmp, kind, out_json, runs=a.runs, ablation="with-without" if kind == "outcome" else "none",
                                                      judge_model=a.judge_model, model=a.model, max_cost=a.max_cost_usd, concurrency=a.jobs)
            meta["engine"] = "native"
            meta["agent_model"] = ", ".join(sorted({r["model"] for r in recs if r.get("model")}))
            meta["judge_model"] = a.judge_model or "default"
            meta["runs_per_case"] = a.runs
        meta["_stamp"] = stamp
        if a.merge:
            old_path = os.path.join(col, "evals", "runs", "latest-%s.json" % name)
            if not os.path.isfile(old_path):
                raise SystemExit("--merge needs earlier saved runs")
            old = json.load(open(old_path, encoding="utf-8"))
            replaced = {r["key"] for r in recs}
            kept = [r for r in old["records"] if r["key"] not in replaced]
            meta["costUsd"] = round((old["meta"].get("costUsd") or 0) + (meta.get("costUsd") or 0), 4)
            for k in ("judge_votes", "rejudge", "regraded_after_rubric_correction"):
                if k in old["meta"]:
                    meta.setdefault("previous_" + k, old["meta"][k])
            meta["merged_cases"] = sorted(replaced)
            meta["agent_model"] = old["meta"].get("agent_model", meta.get("agent_model"))
            meta["claudeVersion"] = old["meta"].get("claudeVersion", meta.get("claudeVersion"))
            meta["startedAt"] = old["meta"].get("startedAt", meta.get("startedAt"))
            meta["runs_per_case"] = old["meta"].get("runs_per_case", meta.get("runs_per_case"))
            meta["judge_votes"] = 1
            recs = kept + recs
        if kind == "outcome":
            summary = report.summarise_outcome(recs, _flagged(data))
            body = report.render_outcome(summary, meta)
        else:
            summary = report.summarise_trigger(recs, data["trigger"])
            body = report.render_trigger(summary, meta)
        meta["label"] = a.label or ""
        _save(col, name, recs, meta, summary, _header(kind, col, meta) + body, stamp)
        print("%s: %d run records, cost %.2f US dollars, results in evals/results/%s.md" % (name, len(recs), meta.get("costUsd") or 0, name))
    return 0


def _flagged(data):
    return {c["skill"] for c in data["outcome"] if c.get("presupposes_skill")}


def _header(kind, col, meta):
    cost = ("Cost of this run, agent and judge at list price: %.2f US dollars." % (meta.get("costUsd") or 0)) if kind == "outcome" else \
        "Trigger runs stop at the first skill call, so their cost is not tallied."
    return "# %s results: %s\n\nEngine %s. Agent model %s, judge model %s (%s vote%s per verdict), %s runs per case. %s%s\n\n" % (
        kind.capitalize(), os.path.basename(col), meta.get("engine", "?"), meta.get("agent_model"), meta.get("judge_model"),
        meta.get("judge_votes", 1), "" if meta.get("judge_votes", 1) == 1 else "s", meta.get("runs_per_case"), cost, " The run stopped early at the cost cap, so results are partial." if meta.get("partial") else "")


def cmd_report(a):
    col = collection_path(a.collection)
    data = cases_mod.load_cases(col)
    for kind in ("outcome", "trigger"):
        path = os.path.join(col, "evals", "runs", "latest-%s.json" % kind)
        if not os.path.isfile(path):
            print("no saved %s runs; run `run` first" % kind)
            continue
        saved = json.load(open(path, encoding="utf-8"))
        recs, meta = saved["records"], saved["meta"]
        if kind == "outcome":
            summary = report.summarise_outcome(recs, _flagged(data))
            body = report.render_outcome(summary, meta)
        else:
            summary = report.summarise_trigger(recs, data["trigger"])
            body = report.render_trigger(summary, meta)
        _save(col, kind, recs, meta, summary, _header(kind, col, meta) + body, meta.get("_stamp") or datetime.date.today().isoformat())
        print("rewrote evals/results/%s.md" % kind)
    return 0


def cmd_selftest(_a):
    from skilleval import cases as c, native as n, report as r, stats as s
    total, bad = 0, []
    for name, mod in (("stats", s), ("cases", c), ("native", n), ("direct", direct), ("report", r)):
        f, k = mod.selftest()
        total += k
        bad += ["%s: %s" % (name, x) for x in f]
        print("%-8s %s" % (name, "OK (%d checks)" % k if not f else "FAILED"))
    for extra in ("samples", "humankit", "pairwise", "codex_runner", "judgecheck", "rollup"):
        try:
            mod = __import__("skilleval." + extra, fromlist=["selftest"])
        except ImportError:
            continue
        f, k = mod.selftest()
        total += k
        bad += ["%s: %s" % (extra, x) for x in f]
        print("%-8s %s" % (extra, "OK (%d checks)" % k if not f else "FAILED"))
    if bad:
        print("SELFTEST FAILED")
        for b in bad:
            print(" -", b)
        return 1
    print("all modules OK (%d checks)" % total)
    return 0


def main():
    ap = argparse.ArgumentParser(description="Run and report skill evaluations for a collection.")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("plan")
    p.add_argument("collection")
    p.add_argument("--runs", type=int, default=3)
    r = sub.add_parser("run")
    r.add_argument("collection")
    r.add_argument("--kind", choices=["outcome", "trigger", "both"], default="both")
    r.add_argument("--runs", type=int, default=3)
    r.add_argument("--only", nargs="*")
    r.add_argument("-j", "--jobs", type=int, default=4)
    r.add_argument("--engine", choices=["direct", "native"], default="direct", help="direct: claude -p in a project with the skills installed (default); native: claude plugin eval")
    r.add_argument("--votes", type=int, default=1, help="judge calls per run for the rubric checks (majority wins)")
    r.add_argument("--label", help="save the results under outcome-LABEL / trigger-LABEL instead of overwriting the main ones (for example a second agent model)")
    r.add_argument("--merge", action="store_true", help="replace only the --only skills' records in the saved runs instead of overwriting them")
    r.add_argument("--model")
    r.add_argument("--judge-model")
    r.add_argument("--max-cost-usd", type=float)
    rp = sub.add_parser("report")
    rp.add_argument("collection")
    sub.add_parser("selftest")
    for name in ("samples", "pairwise", "sheet", "score", "codex", "judge-check", "rollup", "rejudge", "cross-judge"):
        q = sub.add_parser(name)
        q.add_argument("collection")
        q.add_argument("--feature")
        q.add_argument("--judge-model")
        q.add_argument("--seed", type=int, default=1)
        q.add_argument("--ratings", nargs="*")
        q.add_argument("--only", nargs="*")
        q.add_argument("--max-cost-usd", type=float)
        q.add_argument("-n", type=int, default=20)
    a = ap.parse_args()
    if a.cmd in ("samples", "pairwise", "sheet", "score", "codex", "judge-check", "rollup", "rejudge", "cross-judge"):
        mod_name = {"samples": "samples", "pairwise": "pairwise", "sheet": "humankit", "score": "humankit", "codex": "codex_runner", "judge-check": "judgecheck", "rollup": "rollup", "rejudge": "judgecheck", "cross-judge": "judgecheck"}[a.cmd]
        try:
            mod = __import__("skilleval." + mod_name, fromlist=["main"])
        except ImportError as e:
            raise SystemExit("%s is not available yet: %s" % (a.cmd, e))
        return mod.main(a)
    handlers = {"plan": cmd_plan, "run": cmd_run, "report": cmd_report, "selftest": cmd_selftest}
    if a.cmd not in handlers:
        ap.print_help()
        return 2
    return handlers[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
