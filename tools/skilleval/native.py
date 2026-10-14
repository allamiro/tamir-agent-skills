"""Run `claude plugin eval` and turn its output into flat run records (standard library only).

The official command runs each case several times with the plugin and, for outcome cases, again without it. It
deletes its temporary files, which hold each run's transcript, so this module keeps them (--keep-temp), reads the
transcript for the final answer, tool calls and token usage, and then removes them.
"""
import json
import os
import re
import shutil
import subprocess
import time


def read_trace(path):
    """Facts from one run's transcript: final answer text, skills invoked, commands run, token usage."""
    info = {"text": "", "skills": [], "commands": [], "usage": {}, "cost": None, "model": None}
    if not path or not os.path.isfile(path):
        return info
    last_text = ""
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") == "system" and d.get("subtype") == "init":
                info["model"] = d.get("model")
            if d.get("type") == "assistant":
                texts = []
                for b in d.get("message", {}).get("content", []):
                    if b.get("type") == "text":
                        texts.append(b.get("text", ""))
                    elif b.get("type") == "tool_use":
                        if b.get("name") == "Skill":
                            info["skills"].append(str(b.get("input", {}).get("skill", "?")).split(":")[-1])
                        elif b.get("name") == "Bash":
                            info["commands"].append(str(b.get("input", {}).get("command", "")))
                if texts:
                    last_text = "".join(texts)
            if "usage" in d and "total_cost_usd" in d:
                info["usage"] = d["usage"]
                info["cost"] = d.get("total_cost_usd")
                if isinstance(d.get("result"), str) and d["result"]:
                    last_text = d["result"]
    info["text"] = last_text
    return info


def tokens(usage):
    """(output tokens, input tokens processed across all turns, thinking tokens)."""
    out = int(usage.get("output_tokens", 0) or 0)
    inp = sum(int(usage.get(k, 0) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    think = int((usage.get("output_tokens_details") or {}).get("thinking_tokens", 0) or 0)
    return out, inp, think


def parse_result(result_json):
    """Flat list of run records from the command's JSON result (reading each kept transcript)."""
    with open(result_json, encoding="utf-8") as fh:
        d = json.load(fh)
    recs = []
    for case in d.get("cases", []):
        kind, _, key = case["name"].partition("-")
        for arm in ("with", "without"):
            for i, r in enumerate(case.get("arms", {}).get(arm, []), 1):
                tr = read_trace(r.get("tracePath"))
                out_t, in_t, think = tokens(tr["usage"])
                graders = {g["name"]: {"passed": bool(g.get("passed")), "scored": g.get("scored", True),
                                       "explanation": g.get("explanation", "")} for g in r.get("graders", [])}
                text = tr["text"]
                if not text:
                    for g in r.get("graders", []):
                        if g.get("evidence"):
                            text = g["evidence"]
                            break
                recs.append({
                    "case": case["name"], "kind": kind, "key": key, "arm": arm, "run": i,
                    "score": r.get("score"), "graders": graders, "error": r.get("error"),
                    "cost": r.get("costUsd"), "judge_cost": r.get("judgeCostUsd"), "seconds": r.get("durationSeconds"),
                    "turns": r.get("turns"), "skills": tr["skills"], "commands": tr["commands"],
                    "out_tokens": out_t, "in_tokens": in_t, "thinking_tokens": think, "text": text, "model": tr["model"],
                })
    meta = {k: d.get(k) for k in ("claudeVersion", "startedAt", "durationSeconds", "costUsd", "partial", "partialReason")}
    return recs, meta


def kept_dirs(stderr_text):
    return re.findall(r"kept (/\S+?):", stderr_text)


def cleanup(dirs):
    for d in dirs:
        try:
            subprocess.run(["chmod", "-R", "u+rwx", d], capture_output=True)
            shutil.rmtree(d, ignore_errors=True)
        except OSError:
            pass


def run_native(plugin_dir, tag, out_json, runs=3, ablation="with-without", judge_model=None, model=None,
               max_cost=None, concurrency=1, allow_tools=("Bash(python3 *)",), case_glob=None, timeout=None):
    """Run the suite. Returns (records, meta, completed process). Transcripts are read before they are deleted."""
    cmd = ["claude", "plugin", "eval", plugin_dir, "--trust-plugin", "--runs", str(runs), "--ablation", ablation,
           "--no-publish", "--keep-temp", "--json", out_json, "-j", str(concurrency), "--tag", tag]
    if case_glob:
        cmd += ["--case", case_glob]
    if judge_model:
        cmd += ["--judge-model", judge_model]
    if model:
        cmd += ["--model", model]
    if max_cost:
        cmd += ["--max-cost-usd", str(max_cost)]
    if allow_tools:
        cmd += ["--allow-tools"] + list(allow_tools)
    started = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    dirs = kept_dirs(r.stderr + r.stdout)
    try:
        if not os.path.isfile(out_json):
            raise RuntimeError("claude plugin eval wrote no result (exit %s): %s" % (r.returncode, (r.stderr or r.stdout).strip()[-400:]))
        # kept directories are sealed (mode 000); open them so the traces can be read
        for d in dirs:
            subprocess.run(["chmod", "-R", "u+rwx", d], capture_output=True)
        recs, meta = parse_result(out_json)
    finally:
        cleanup(dirs)
    meta["wall_seconds"] = round(time.time() - started)
    meta["exit_code"] = r.returncode
    return recs, meta, r


def selftest():
    import tempfile
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    with tempfile.TemporaryDirectory() as tmp:
        tp = os.path.join(tmp, "trace.jsonl")
        lines = [
            {"type": "system", "subtype": "init", "model": "claude-test-1"},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "demo-skills:alpha"}}]}},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {"command": "python3 scripts/a.py --x"}}]}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "Final "}, {"type": "text", "text": "answer."}]}},
            {"stop_reason": "end_turn", "total_cost_usd": 0.5, "usage": {"input_tokens": 5, "cache_creation_input_tokens": 100,
             "cache_read_input_tokens": 1000, "output_tokens": 70, "output_tokens_details": {"thinking_tokens": 20}}},
        ]
        open(tp, "w").write("\n".join(json.dumps(x) for x in lines) + "\nnot json\n")
        t = read_trace(tp)
        eq("final text", t["text"], "Final answer.")
        eq("skills strip plugin prefix", t["skills"], ["alpha"])
        eq("commands", t["commands"], ["python3 scripts/a.py --x"])
        eq("tokens", tokens(t["usage"]), (70, 1105, 20))
        eq("cost", t["cost"], 0.5)
        eq("model from init", t["model"], "claude-test-1")
        eq("missing trace", read_trace(os.path.join(tmp, "none"))["text"], "")
        eq("tokens of empty usage", tokens({}), (0, 0, 0))
        res = {"claudeVersion": "x", "cases": [{"name": "outcome-alpha", "arms": {
            "with": [{"score": 1, "tracePath": tp, "costUsd": 0.5, "judgeCostUsd": 0.01, "durationSeconds": 9, "turns": 3, "error": None,
                      "graders": [{"name": "fact-1", "passed": True, "scored": True, "explanation": "matched"},
                                  {"name": "skill-fired", "passed": True, "scored": False, "explanation": "Skill called 1x"}]}],
            "without": [{"score": 0.5, "tracePath": os.path.join(tmp, "gone"), "costUsd": 0.2, "turns": 1, "error": None,
                         "graders": [{"name": "fact-1", "passed": False, "scored": True, "explanation": "no match"},
                                     {"name": "rubric", "passed": True, "evidence": "evidence text"}]}]}}]}
        rp = os.path.join(tmp, "r.json")
        json.dump(res, open(rp, "w"))
        recs, meta = parse_result(rp)
        eq("two records", len(recs), 2)
        w = [r for r in recs if r["arm"] == "with"][0]
        eq("kind and key", (w["kind"], w["key"]), ("outcome", "alpha"))
        eq("with-arm graders", sorted(w["graders"]), ["fact-1", "skill-fired"])
        eq("with-arm text and skills", (w["text"], w["skills"]), ("Final answer.", ["alpha"]))
        eq("with-arm tokens", (w["out_tokens"], w["in_tokens"], w["thinking_tokens"]), (70, 1105, 20))
        wo = [r for r in recs if r["arm"] == "without"][0]
        eq("falls back to judge evidence", wo["text"], "evidence text")
        eq("no trace gives zero tokens", wo["out_tokens"], 0)
        eq("kept dirs parsed", kept_dirs("warning kept /private/tmp/e-abc: home/ ... \nkept /private/tmp/e-def: x"), ["/private/tmp/e-abc", "/private/tmp/e-def"])
    return fails, count[0]
