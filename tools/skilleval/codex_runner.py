"""Smoke test of the same starter prompts in OpenAI Codex (standard library only; needs the `codex` CLI to run).

Skills are installed to the project's .agents/skills (the folder Codex documents for repository skills), the prompt is
run with `codex exec --json`, and the answer is graded with the same regular expressions as the Claude runs. A skill
counts as used when the agent reads its SKILL.md in a shell command, the check the OpenAI skills-evaluation post
describes. Codex reports tokens but not cost, and there is no model judge here, so this is a narrower measurement than the
Claude runs: one run per prompt and arm, facts only.
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

from . import cases as cases_mod, stats


def parse_events(lines):
    """Facts from a `codex exec --json` stream: final message, commands run, skills whose SKILL.md was read, tokens."""
    out = {"text": "", "commands": [], "skills": [], "in_tokens": 0, "cached_tokens": 0, "out_tokens": 0, "error": None}
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        t = d.get("type")
        item = d.get("item") or {}
        if t == "item.completed" and item.get("type") == "agent_message":
            out["text"] = item.get("text", out["text"])
        elif t in ("item.started", "item.completed") and item.get("type") == "command_execution":
            cmd = str(item.get("command", ""))
            if t == "item.started" or cmd not in out["commands"]:
                if cmd not in out["commands"]:
                    out["commands"].append(cmd)
            for m in re.finditer(r"\.agents/skills/([a-z0-9-]+)/SKILL\.md", cmd):
                if m.group(1) not in out["skills"]:
                    out["skills"].append(m.group(1))
        elif t == "turn.completed":
            u = d.get("usage") or {}
            out["in_tokens"] += int(u.get("input_tokens", 0) or 0)
            out["cached_tokens"] += int(u.get("cached_input_tokens", 0) or 0)
            out["out_tokens"] += int(u.get("output_tokens", 0) or 0)
        elif t in ("error", "turn.failed"):
            out["error"] = str(d.get("message") or d.get("error") or t)[:200]
    return out


def run_codex(project, prompt, timeout=600, popen=subprocess.Popen):
    cmd = ["codex", "exec", "--json", "--skip-git-repo-check", "--ephemeral", "--ignore-user-config", "-s", "workspace-write", "-C", project, prompt]
    start = time.time()
    p = popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        stdout, _err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        stdout = ""
    res = parse_events(stdout.splitlines())
    res["seconds"] = round(time.time() - start, 1)
    return res


def run_collection(collection, only=None, jobs=3, runner=run_codex, install=None, progress=print):
    collection = os.path.abspath(collection)
    data = cases_mod.load_cases(collection)
    work_items = []
    for c in data["outcome"]:
        if only and c["skill"] not in only:
            continue
        prompt, _good = cases_mod.resolve_outcome(collection, c)
        for arm in ("with", "without"):
            work_items.append((c, prompt, arm))

    def work(item):
        c, prompt, arm = item
        project = tempfile.mkdtemp(prefix="codexeval-")
        try:
            if arm == "with":
                if install:
                    install(collection, project)
                else:
                    r = subprocess.run(["bash", os.path.join(collection, "scripts", "install.sh"), "--codex", "--project", project],
                                       capture_output=True, text=True)
                    if r.returncode:
                        raise RuntimeError("install.sh failed: " + (r.stderr or r.stdout)[-200:])
            res = runner(project, prompt)
        finally:
            shutil.rmtree(project, ignore_errors=True)
        facts = [bool(re.search(rx, res["text"], re.I | re.S)) for rx in c["facts"]]
        rec = {"skill": c["skill"], "arm": arm, "facts": facts, "all_facts": bool(facts) and all(facts), "fired": c["skill"] in res["skills"],
               "any_skill": bool(res["skills"]), "in_tokens": res["in_tokens"], "cached_tokens": res["cached_tokens"],
               "out_tokens": res["out_tokens"], "seconds": res["seconds"], "error": res["error"], "text": res["text"]}
        progress("  codex %-34s %-7s facts %d/%d  skill %s" % (c["skill"], arm, sum(facts), len(facts), "yes" if rec["fired"] else "no"))
        return rec
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        return list(pool.map(work, work_items))


def summarise(recs):
    out = {}
    for arm in ("with", "without"):
        rs = [r for r in recs if r["arm"] == arm]
        out[arm] = {"runs": len(rs), "all_facts": sum(r["all_facts"] for r in rs), "fired": sum(r["fired"] for r in rs),
                    "any_skill": sum(r["any_skill"] for r in rs),
                    "mean_out_tokens": round(sum(r["out_tokens"] for r in rs) / len(rs), 1) if rs else 0,
                    "mean_in_tokens": round(sum(r["in_tokens"] for r in rs) / len(rs), 1) if rs else 0}
    return out


def render(recs, meta):
    s = summarise(recs)
    w, wo = s["with"], s["without"]
    lines = ["# Codex smoke test: %s" % meta.get("collection", ""), "",
             "The same starter prompts were run once with the skills installed in `.agents/skills` and once with none, using `codex exec` "
             "(Codex CLI %s, model %s). Grading is by the same regular expressions as the Claude runs. A skill counts as used when the agent "
             "reads its SKILL.md. Codex reports tokens but not cost, and there is no model judge here, so this checks that the skills are found and "
             "used in Codex, not how good the answers are. One run per prompt and arm." % (meta.get("codex_version", "?"), meta.get("model", "default")), "",
             "| | Every expected fact | Expected skill used | Any skill used | Mean output tokens | Mean input tokens |", "|---|---|---|---|---|---|"]
    for label, x in (("With the skills", w), ("No skills", wo)):
        lines.append("| %s | %d/%d | %s | %s | %s | %s |" % (label, x["all_facts"], x["runs"], ("%d/%d" % (x["fired"], x["runs"])) if label.startswith("With") else "n/a",
                                                                   ("%d/%d" % (x["any_skill"], x["runs"])) if label.startswith("With") else "n/a",
                                                                   "{:,.0f}".format(x["mean_out_tokens"]), "{:,.0f}".format(x["mean_in_tokens"])))
    lines += ["", "| Skill | Facts with | Facts without | Skill used |", "|---|---|---|---|"]
    by = {}
    for r in recs:
        by.setdefault(r["skill"], {})[r["arm"]] = r
    for skill in sorted(by):
        a, b = by[skill].get("with"), by[skill].get("without")
        lines.append("| `%s` | %s | %s | %s |" % (skill, "%d/%d" % (sum(a["facts"]), len(a["facts"])) if a else "", "%d/%d" % (sum(b["facts"]), len(b["facts"])) if b else "",
                                                  "yes" if a and a["fired"] else "no"))
    return "\n".join(lines) + "\n"


def main(args):
    col = os.path.abspath(args.collection)
    problems = cases_mod.validate(col)
    if problems:
        for p in problems:
            print("PROBLEM:", p)
        return 1
    recs = run_collection(col, only=set(args.only) if args.only else None, jobs=3)
    ver = subprocess.run(["codex", "--version"], capture_output=True, text=True).stdout.strip()
    meta = {"collection": os.path.basename(col), "codex_version": ver, "model": "default"}
    os.makedirs(os.path.join(col, "evals", "results"), exist_ok=True)
    os.makedirs(os.path.join(col, "evals", "runs"), exist_ok=True)
    with open(os.path.join(col, "evals", "runs", "latest-codex.json"), "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "records": recs}, fh, ensure_ascii=False)
    summary = [{k: v for k, v in r.items() if k != "text"} for r in recs]
    with open(os.path.join(col, "evals", "results", "codex.json"), "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "summary": summary}, fh, indent=1)
    with open(os.path.join(col, "evals", "results", "codex.md"), "w", encoding="utf-8") as fh:
        fh.write(render(recs, meta))
    print("wrote evals/results/codex.md")
    return 0


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    lines = [json.dumps(x) for x in [
        {"type": "thread.started", "thread_id": "t"},
        {"type": "item.started", "item": {"id": "1", "type": "command_execution", "command": "cat .agents/skills/alpha/SKILL.md"}},
        {"type": "item.completed", "item": {"id": "1", "type": "command_execution", "command": "cat .agents/skills/alpha/SKILL.md", "exit_code": 0}},
        {"type": "item.completed", "item": {"id": "2", "type": "command_execution", "command": "python3 .agents/skills/alpha/scripts/a.py"}},
        {"type": "item.completed", "item": {"id": "3", "type": "agent_message", "text": "The answer."}},
        {"type": "turn.completed", "usage": {"input_tokens": 100, "cached_input_tokens": 40, "output_tokens": 7}},
        {"type": "turn.completed", "usage": {"input_tokens": 50, "cached_input_tokens": 10, "output_tokens": 3}}]] + ["junk"]
    r = parse_events(lines)
    eq("final message", r["text"], "The answer.")
    eq("commands deduplicated", r["commands"], ["cat .agents/skills/alpha/SKILL.md", "python3 .agents/skills/alpha/scripts/a.py"])
    eq("skill read detected, script path alone is not a SKILL.md read", r["skills"], ["alpha"])
    eq("tokens summed over turns", (r["in_tokens"], r["cached_tokens"], r["out_tokens"]), (150, 50, 10))
    eq("error event", parse_events([json.dumps({"type": "error", "message": "boom"})])["error"], "boom")
    eq("empty stream", parse_events([])["text"], "")

    class FakePopen:
        def __init__(self, cmd, **kw):
            self.cmd = cmd

        def communicate(self, timeout=None):
            return "\n".join(lines), ""

        def kill(self):
            pass
    res = run_codex("/tmp", "p", popen=FakePopen)
    eq("run_codex parses stdout", (res["text"], res["skills"]), ("The answer.", ["alpha"]))
    with tempfile.TemporaryDirectory() as tmp:
        col = os.path.join(tmp, "demo-skills")
        for sub in ("skills/alpha", "prompts", "evals"):
            os.makedirs(os.path.join(col, sub))
        open(os.path.join(col, "prompts", "alpha.md"), "w").write("## 1. One\n\n> Do alpha.\n\nA good answer: ok.\n")
        json.dump({"outcome": [{"skill": "alpha", "facts": ["answer", "missing"]}], "trigger": []}, open(os.path.join(col, "evals", "cases.json"), "w"))
        seen = []

        def fake_runner(project, prompt):
            seen.append(prompt)
            return {"text": "The answer.", "skills": ["alpha"] if os.path.isdir(os.path.join(project, ".agents")) else [], "commands": [],
                    "in_tokens": 10, "cached_tokens": 0, "out_tokens": 4, "seconds": 1.0, "error": None}
        recs = run_collection(col, runner=fake_runner, install=lambda c, p: os.makedirs(os.path.join(p, ".agents", "skills")), progress=lambda *_: None)
        eq("two runs", sorted(r["arm"] for r in recs), ["with", "without"])
        w = [r for r in recs if r["arm"] == "with"][0]
        eq("with arm fired and partial facts", (w["fired"], w["facts"], w["all_facts"]), (True, [True, False], False))
        eq("without arm has no skill", [r["fired"] for r in recs if r["arm"] == "without"], [False])
        s = summarise(recs)
        eq("summary", (s["with"]["runs"], s["with"]["fired"], s["without"]["fired"], s["with"]["mean_out_tokens"]), (1, 1, 0, 4.0))
        eq("render lists the skill", "| `alpha` | 1/2 | 1/2 | yes |" in render(recs, {"collection": "demo"}), True)
    return fails, count[0]
