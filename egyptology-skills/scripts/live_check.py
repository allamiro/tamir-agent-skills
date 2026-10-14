#!/usr/bin/env python3
"""Run the starter prompts through a real Claude Code session and record what happens (standard library only).

For each case in evals/live_cases.json this installs the skills into a throwaway project, runs
`claude -p` on the skill's starter prompt (the first prompt in prompts/<skill>.md, with any <placeholder>
filled from the case), and records:
  - whether the agent invoked the skill (the Skill tool) and which skills it invoked;
  - whether it ran one of the skill's bundled scripts;
  - whether its final answer matches every regular expression in the case (the key facts from the
    prompt's "a good answer" line);
  - cost, turns and time.

THIS SPENDS API CREDIT. Nothing runs unless you pass --run. Each run is capped by --budget (default
0.80 US dollars), so the worst case is cases x budget; --dry-run prints that. The grading is mechanical
(regular expressions), not a judgement of quality, and whether a skill fires is the model's choice:
a strong model may solve a simple prompt without loading any skill. The result is a measurement of
this model on this day, not a guarantee.

Usage:
  python3 scripts/live_check.py --dry-run
  python3 scripts/live_check.py --run [--only SKILL ...] [--budget 0.80] [--model MODEL] [--out evals/live-results.md]
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CASES = os.path.join(ROOT, "evals", "live_cases.json")


def starter_prompt(skill, number, fill):
    path = os.path.join(ROOT, "prompts", skill + ".md")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^## %d\. .*?$(.*?)(?=^## |\Z)" % number, text, re.M | re.S)
    if not m:
        raise SystemExit("%s: no prompt %d" % (skill, number))
    q = re.search(r"^> (.*)$", m.group(1), re.M)
    prompt = q.group(1).strip()
    for placeholder, value in (fill or {}).items():
        if placeholder not in prompt:
            raise SystemExit("%s: placeholder %r not in the prompt" % (skill, placeholder))
        prompt = prompt.replace(placeholder, value)
    left = re.findall(r"<[^>]{1,40}>", prompt)
    if left:
        raise SystemExit("%s: unfilled placeholder(s) %s: add a 'fill' to the case" % (skill, left))
    return prompt


def run_case(project, case, prompt, budget, model):
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--setting-sources", "project", "--strict-mcp-config",
           "--allowedTools", "Bash(python3:*)", "Read", "Skill",
           "--permission-mode", "dontAsk", "--max-budget-usd", str(budget), "--no-session-persistence"]
    if model:
        cmd += ["--model", model]
    start = time.time()
    try:
        r = subprocess.run(cmd, cwd=project, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return {"error": "timed out after 900 s", "seconds": time.time() - start}
    out = {"seconds": time.time() - start, "skills": [], "scripts": [], "text": "", "cost": None, "turns": None,
           "model": None, "error": None}
    for line in r.stdout.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") == "system" and d.get("subtype") == "init":
            out["model"] = d.get("model")
        elif d.get("type") == "assistant":
            for b in d.get("message", {}).get("content", []):
                if b.get("type") == "tool_use":
                    if b.get("name") == "Skill":
                        out["skills"].append(str(b.get("input", {}).get("skill", "?")))
                    elif b.get("name") == "Bash":
                        for script in re.findall(r"[A-Za-z0-9_]+\.py", str(b.get("input", {}).get("command", ""))):
                            out["scripts"].append(script)
        elif d.get("type") == "result":
            out["text"] = d.get("result") or ""
            out["cost"] = d.get("total_cost_usd")
            out["turns"] = d.get("num_turns")
            if d.get("is_error"):
                out["error"] = d.get("subtype") or "error"
    if not out["text"] and r.returncode:
        out["error"] = (r.stderr or "claude exited %d" % r.returncode).strip()[:200]
    return out


def main():
    ap = argparse.ArgumentParser(description="Run starter prompts through a real Claude Code session.")
    ap.add_argument("--run", action="store_true", help="actually run (spends API credit)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and the worst-case cost")
    ap.add_argument("--only", nargs="*", help="run only these skills")
    ap.add_argument("--budget", type=float, default=0.80, help="maximum US dollars per run (default 0.80)")
    ap.add_argument("--model", default=None)
    ap.add_argument("--baseline", action="store_true", help="run the same prompts with NO skills installed, for comparison")
    ap.add_argument("--out", default=None, help="results file (default evals/live-results.md, or live-results-baseline.md with --baseline)")
    a = ap.parse_args()
    with open(CASES, encoding="utf-8") as fh:
        cases = json.load(fh)["cases"]
    if a.only:
        cases = [c for c in cases if c["skill"] in a.only]
    for c in cases:
        c["_prompt"] = starter_prompt(c["skill"], c.get("prompt", 1), c.get("fill"))
    if a.out is None:
        a.out = os.path.join(ROOT, "evals", "live-results-baseline.md" if a.baseline else "live-results.md")
    if a.dry_run or not a.run:
        print("%d case(s); worst case %.2f US dollars at %.2f per run. Add --run to spend it." % (
            len(cases), len(cases) * a.budget, a.budget))
        for c in cases:
            print("  %-32s %s" % (c["skill"], c["_prompt"][:90].replace("\n", " ")))
        return 0
    version = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()
    rows, total = [], 0.0
    with tempfile.TemporaryDirectory() as project:
        if not a.baseline:
            subprocess.run(["bash", os.path.join(ROOT, "scripts", "install.sh"), "--claude", "--project", project],
                           check=True, capture_output=True)
        for c in cases:
            res = run_case(project, c, c["_prompt"], a.budget, a.model)
            checks = [bool(re.search(rx, res.get("text", ""), re.I | re.S)) for rx in c["answer_regex"]]
            res["checks"] = checks
            total += res.get("cost") or 0.0
            rows.append((c, res))
            print("%-32s skill=%-5s script=%-5s answer=%d/%d cost=%s%s" % (
                c["skill"], c["skill"] in res.get("skills", []), bool(res.get("scripts")), sum(checks), len(checks),
                res.get("cost"), "  ERROR " + res["error"] if res.get("error") else ""))
    fired = sum(1 for c, r in rows if c["skill"] in r.get("skills", []))
    any_skill = sum(1 for c, r in rows if r.get("skills"))
    answered = sum(1 for c, r in rows if r["checks"] and all(r["checks"]))
    models = sorted({r.get("model") for _, r in rows if r.get("model")})
    how = ("NO skills installed, for comparison with live-results.md (`python3 scripts/live_check.py --run --baseline`). "
           if a.baseline else "the skills installed (`python3 scripts/live_check.py --run`). ")
    header = ("Measured on %s with %s, model %s. Each row is one starter prompt run once in a clean project with %s"
              "Grading is by regular expression on the final answer, not a judgement of quality. This is one run per "
              "prompt on one day: it shows what happened, not what always happens."
              % (datetime.date.today().isoformat(), version, ", ".join(models) or "unknown", how))
    lines = [
        "# Live runs, no skills installed (baseline)" if a.baseline else "# Live runs",
        "",
        header,
        "",
        "- The expected skill was invoked in **%d of %d** runs; some skill was invoked in %d." % (fired, len(rows), any_skill),
        "- The answer matched every expected fact in **%d of %d** runs." % (answered, len(rows)),
        "- Total cost %.2f US dollars." % total,
        "",
        "| Skill | Expected skill invoked | Skills invoked | Script run | Facts matched | Cost (USD) | Seconds |",
        "|---|---|---|---|---|---|---|",
    ]
    for c, r in rows:
        lines.append("| `%s` | %s | %s | %s | %d of %d | %s | %d |" % (
            c["skill"], "yes" if c["skill"] in r.get("skills", []) else "no",
            ", ".join(sorted(set(r.get("skills", [])))) or "none", ", ".join("`%s`" % s for s in sorted(set(r.get("scripts", [])))) or "none",
            sum(r["checks"]), len(r["checks"]), "%.2f" % r["cost"] if r.get("cost") is not None else "n/a", r.get("seconds", 0)))
        if r.get("error"):
            lines.append("|  | error: %s | | | | | |" % r["error"].replace("|", "/"))
    lines += ["", "## What the facts were", "", "| Skill | A correct answer matches all of |", "|---|---|"]
    for c, _ in rows:
        lines.append("| `%s` | %s |" % (c["skill"], "; ".join("`%s`" % rx.replace("|", "\\|") for rx in c["answer_regex"])))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote %s; expected skill invoked %d/%d, answers matched %d/%d, cost %.2f" % (a.out, fired, len(rows), answered, len(rows), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
