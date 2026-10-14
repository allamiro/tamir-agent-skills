"""Load a collection's evaluation cases and turn them into a `claude plugin eval` suite (standard library only).

A collection keeps its cases in evals/cases.json:

  {"outcome": [{"skill": "...", "number": 1, "fill": {"<x>": "..."}, "prompt": "literal override",
                "facts": ["regex", ...], "script": "tool.py", "rubric": "text if the prompt has no good-answer line"}],
   "trigger": [{"id": "...", "prompt": "...", "expect": "skill-name" or null, "kind": "implicit|contextual|near-miss|unrelated"}]}

`outcome` cases run with the skills and again without them; their graders are the facts (regular
expressions on the final answer), a rubric judged by a model (the prompt's own "a good answer" line), a
calibration check, and indicators for whether the skill and its script ran. `trigger` cases run with the
skills only and check which skill, if any, the agent invoked.
"""
import json
import os
import re

CALIBRATION = ("PASS if the answer marks specific claims, figures or steps as unverified, assumed or needing confirmation (it names which "
               "ones) and also says what it did check, compute or take from a source. FAIL if it states everything as settled, or offers only a "
               "generic disclaimer such as 'consult a professional' with no specific item marked.")
RUBRIC_TEMPLATE = ("PASS if the answer does what this description of a good answer says: %s FAIL if it misses most of it, "
                   "contradicts it, or states something that is wrong.")
KINDS = {"implicit", "contextual", "near-miss", "unrelated", "explicit"}


def load_cases(collection):
    path = os.path.join(collection, "evals", "cases.json")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def skill_names(collection):
    root = os.path.join(collection, "skills")
    return sorted(d for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, "SKILL.md")))


def get_prompt(collection, skill, number=1):
    """(prompt text, good-answer text or None) for prompt `number` of a skill.

    Looks in prompts/<skill>.md (numbered "## N." sections), then in prompts/README.md under "### `skill`"
    (prompt 1 is the first block quote; later prompts are the bullets under "More prompts")."""
    per_skill = os.path.join(collection, "prompts", skill + ".md")
    if os.path.isfile(per_skill):
        text = open(per_skill, encoding="utf-8").read()
        m = re.search(r"^## %d\. .*?$(.*?)(?=^## |\Z)" % number, text, re.M | re.S)
        if not m:
            raise ValueError("%s: no prompt %d" % (per_skill, number))
        q = re.search(r"^> (.*)$", m.group(1), re.M)
        g = re.search(r"A good answer:(.*)", m.group(1), re.S)
        return q.group(1).strip(), (" ".join(g.group(1).split()) if g else None)
    readme = os.path.join(collection, "prompts", "README.md")
    text = open(readme, encoding="utf-8").read()
    m = re.search(r"^### `%s`\n(.*?)(?=^### |^## |\Z)" % re.escape(skill), text, re.M | re.S)
    if not m:
        raise ValueError("%s: no section for %s" % (readme, skill))
    body = m.group(1)
    g = re.search(r"A good answer:(.*?)(?=\n\[Open the skill\]|\Z)", body, re.S)
    good = " ".join(g.group(1).split()) if g else None
    if number == 1:
        q = re.search(r"^> (.*)$", body, re.M)
        return q.group(1).strip(), good
    bullets = re.findall(r"^- (.*)$", body.split("More prompts:")[-1], re.M) if "More prompts:" in body else []
    if number - 2 >= len(bullets):
        raise ValueError("%s: no prompt %d for %s" % (readme, number, skill))
    return bullets[number - 2].strip(), good


def resolve_outcome(collection, case):
    """(prompt, good answer or None) for an outcome case, filling placeholders and rejecting leftovers."""
    if case.get("prompt"):
        prompt, good = case["prompt"], None
        try:
            _p, good = get_prompt(collection, case["skill"], case.get("number", 1))
        except ValueError:
            pass
    else:
        prompt, good = get_prompt(collection, case["skill"], case.get("number", 1))
    for placeholder, value in (case.get("fill") or {}).items():
        if placeholder not in prompt:
            raise ValueError("%s: placeholder %r not in the prompt" % (case["skill"], placeholder))
        prompt = prompt.replace(placeholder, value)
    left = re.findall(r"<[^>\n]{1,40}>", prompt)
    if left:
        raise ValueError("%s: unfilled placeholder(s) %s: add a fill or a literal prompt" % (case["skill"], left))
    return prompt, good


def validate(collection):
    """List of problems with a collection's cases (empty list = fine)."""
    problems = []
    try:
        data = load_cases(collection)
    except (OSError, ValueError) as e:
        return ["cannot read evals/cases.json: %s" % e]
    skills = set(skill_names(collection))
    seen = set()
    for c in data.get("outcome", []):
        s = c.get("skill")
        if s not in skills:
            problems.append("outcome case for unknown skill %r" % s)
            continue
        if s in seen:
            problems.append("two outcome cases for %s" % s)
        seen.add(s)
        if not c.get("facts"):
            problems.append("%s: no facts (regular expressions)" % s)
        for rx in c.get("facts", []):
            try:
                re.compile(rx)
            except re.error as e:
                problems.append("%s: bad regular expression %r: %s" % (s, rx, e))
        try:
            _prompt, good = resolve_outcome(collection, c)
        except ValueError as e:
            problems.append(str(e))
            continue
        if not (c.get("rubric") or good):
            problems.append("%s: no rubric and no 'A good answer' line in its prompt" % s)
        if c.get("script") and not os.path.isfile(os.path.join(collection, "skills", s, "scripts", c["script"])):
            problems.append("%s: script %s not found" % (s, c["script"]))
    for s in sorted(skills - seen):
        problems.append("no outcome case for skill %s" % s)
    ids = set()
    pos, neg = {}, {}
    for t in data.get("trigger", []):
        tid = t.get("id")
        if not tid or tid in ids:
            problems.append("trigger case id missing or repeated: %r" % tid)
        ids.add(tid)
        if t.get("kind") not in KINDS:
            problems.append("%s: kind %r not one of %s" % (tid, t.get("kind"), sorted(KINDS)))
        if not t.get("prompt"):
            problems.append("%s: no prompt" % tid)
        exp = t.get("expect")
        avoid = t.get("avoid")
        if exp is not None and exp not in skills:
            problems.append("%s: expects unknown skill %r" % (tid, exp))
        if avoid is not None and avoid not in skills:
            problems.append("%s: avoids unknown skill %r" % (tid, avoid))
        if exp:
            pos[exp] = pos.get(exp, 0) + 1
        elif avoid:
            neg[avoid] = neg.get(avoid, 0) + 1
    for s in sorted(skills):
        if not pos.get(s):
            problems.append("no should-trigger query for %s" % s)
        if not neg.get(s):
            problems.append("no near-miss (should-not-trigger) query for %s" % s)
    return problems


def _q(s):
    """A YAML double-quoted scalar (JSON strings are valid YAML)."""
    return json.dumps(s, ensure_ascii=False)


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def build_suite(collection, out_dir, plugin_name=None, only=None):
    """Write a throwaway plugin directory for `claude plugin eval`: manifest, a link to the skills, and one
    case directory per outcome and trigger case. Returns a dict of counts."""
    collection = os.path.abspath(collection)
    data = load_cases(collection)
    name = plugin_name or os.path.basename(collection)
    os.makedirs(os.path.join(out_dir, ".claude-plugin"), exist_ok=True)
    _write(os.path.join(out_dir, ".claude-plugin", "plugin.json"),
           json.dumps({"name": name, "version": "0.0.0", "description": "Evaluation harness for " + name}) + "\n")
    link = os.path.join(out_dir, "skills")
    if not os.path.lexists(link):
        os.symlink(os.path.join(collection, "skills"), link)
    n_out = n_trig = 0
    for c in data.get("outcome", []):
        if only and c["skill"] not in only:
            continue
        prompt, good = resolve_outcome(collection, c)
        base = os.path.join(out_dir, "evals", "outcome-" + c["skill"])
        _write(os.path.join(base, "prompt.md"),
               "---\ntags: [outcome, %s]\nruns: 3\nmax_turns: 14\ntimeout_seconds: 420\nallowed_tools: [Read, Skill]\n---\n\n%s\n" % (c["skill"], prompt))
        for i, rx in enumerate(c["facts"], 1):
            _write(os.path.join(base, "graders", "fact-%d.md" % i),
                   "---\ntype: regex\npattern: %s\nflags: i\nweight: 1\n---\n" % _q(rx))
        _write(os.path.join(base, "graders", "rubric.md"),
               "---\ntype: llm\nfocus: last_message\nweight: 1\n---\n\n%s\n" % (RUBRIC_TEMPLATE % (c.get("rubric") or good)))
        _write(os.path.join(base, "graders", "calibration.md"),
               "---\ntype: llm\nfocus: last_message\nweight: 1\n---\n\n%s\n" % CALIBRATION)
        _write(os.path.join(base, "graders", "skill-fired.md"),
               "---\ntype: tool_used\ntool: Skill\ninput_match: %s\narm: with-only\n---\n" % _q(r'"skill"\s*:\s*"(?:[\w-]+:)?%s"' % re.escape(c["skill"])))
        if c.get("script"):
            _write(os.path.join(base, "graders", "script-run.md"),
                   "---\ntype: tool_used\ntool: Bash\ninput_match: %s\narm: with-only\n---\n" % _q(re.escape(c["script"])))
        n_out += 1
    for t in data.get("trigger", []):
        if only and (t.get("expect") or t.get("avoid")) not in only:
            continue
        base = os.path.join(out_dir, "evals", "trigger-" + t["id"])
        _write(os.path.join(base, "prompt.md"),
               "---\ntags: [trigger, %s]\nruns: 3\nmax_turns: 3\ntimeout_seconds: 180\nallowed_tools: [Skill]\n---\n\n%s\n" % (t["kind"], t["prompt"]))
        if t.get("expect"):
            body = "---\ntype: tool_used\ntool: Skill\ninput_match: %s\nmin: 1\n---\n" % _q(r'"skill"\s*:\s*"(?:[\w-]+:)?%s"' % re.escape(t["expect"]))
        elif t.get("avoid"):
            body = "---\ntype: tool_used\ntool: Skill\ninput_match: %s\nmin: 0\nmax: 0\narm: both\n---\n" % _q(r'"skill"\s*:\s*"(?:[\w-]+:)?%s"' % re.escape(t["avoid"]))
        else:
            body = "---\ntype: tool_used\ntool: Skill\nmin: 0\nmax: 0\narm: both\n---\n"
        _write(os.path.join(base, "graders", "trigger.md"), body)
        n_trig += 1
    return {"outcome": n_out, "trigger": n_trig}


def selftest():
    import tempfile
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    with tempfile.TemporaryDirectory() as tmp:
        col = os.path.join(tmp, "demo-skills")
        os.makedirs(os.path.join(col, "skills", "alpha", "scripts"))
        os.makedirs(os.path.join(col, "skills", "beta"))
        os.makedirs(os.path.join(col, "prompts"))
        os.makedirs(os.path.join(col, "evals"))
        for s in ("alpha", "beta"):
            open(os.path.join(col, "skills", s, "SKILL.md"), "w").write("---\nname: %s\n---\n" % s)
        open(os.path.join(col, "skills", "alpha", "scripts", "a.py"), "w").write("")
        open(os.path.join(col, "prompts", "alpha.md"), "w").write(
            "# alpha\n\n## 1. First\n\n> Do the alpha thing with <thing>.\n\nA good answer: names the thing and says what it did not check.\n\n## 2. Second\n\n> Second prompt.\n\nA good answer: second.\n")
        open(os.path.join(col, "prompts", "README.md"), "w").write(
            "# Prompts\n\n## Group\n\n### `beta`\n\n> Beta starter prompt.\n\nMore prompts:\n\n- Beta second.\n- Beta third.\n\nA good answer: beta is covered.\n\n[Open the skill](../skills/beta/SKILL.md)\n")
        cases = {"outcome": [
            {"skill": "alpha", "fill": {"<thing>": "widget"}, "facts": ["widget", "never.*checked"], "script": "a.py"},
            {"skill": "beta", "facts": ["beta"]}],
            "trigger": [
                {"id": "alpha-pos", "prompt": "please alpha", "expect": "alpha", "kind": "implicit"},
                {"id": "alpha-neg", "prompt": "not alpha", "avoid": "alpha", "kind": "near-miss"},
                {"id": "beta-pos", "prompt": "please beta", "expect": "beta", "kind": "contextual"},
                {"id": "beta-neg", "prompt": "not beta", "avoid": "beta", "kind": "near-miss"},
                {"id": "none", "prompt": "write a poem", "expect": None, "kind": "unrelated"}]}
        json.dump(cases, open(os.path.join(col, "evals", "cases.json"), "w"))
        eq("per-skill prompt", get_prompt(col, "alpha", 1)[0], "Do the alpha thing with <thing>.")
        eq("per-skill good answer", get_prompt(col, "alpha", 1)[1], "names the thing and says what it did not check.")
        eq("per-skill prompt 2", get_prompt(col, "alpha", 2)[0], "Second prompt.")
        eq("readme prompt", get_prompt(col, "beta", 1)[0], "Beta starter prompt.")
        eq("readme more prompts", get_prompt(col, "beta", 3)[0], "Beta third.")
        eq("readme good answer", get_prompt(col, "beta", 1)[1], "beta is covered.")
        eq("fill placeholders", resolve_outcome(col, cases["outcome"][0])[0], "Do the alpha thing with widget.")
        eq("valid collection", validate(col), [])
        bad = json.loads(json.dumps(cases))
        bad["outcome"][0]["fill"] = {}
        json.dump(bad, open(os.path.join(col, "evals", "cases.json"), "w"))
        eq("unfilled placeholder caught", any("unfilled" in p for p in validate(col)), True)
        bad = json.loads(json.dumps(cases))
        bad["outcome"][0]["facts"] = ["(unclosed"]
        json.dump(bad, open(os.path.join(col, "evals", "cases.json"), "w"))
        eq("bad regex caught", any("bad regular expression" in p for p in validate(col)), True)
        bad = json.loads(json.dumps(cases))
        bad["trigger"] = bad["trigger"][:2]
        json.dump(bad, open(os.path.join(col, "evals", "cases.json"), "w"))
        eq("missing trigger coverage caught", sorted(p for p in validate(col) if "beta" in p), ["no near-miss (should-not-trigger) query for beta", "no should-trigger query for beta"])
        bad = json.loads(json.dumps(cases))
        bad["outcome"] = bad["outcome"][:1]
        json.dump(bad, open(os.path.join(col, "evals", "cases.json"), "w"))
        eq("missing outcome caught", "no outcome case for skill beta" in validate(col), True)
        json.dump(cases, open(os.path.join(col, "evals", "cases.json"), "w"))
        out = os.path.join(tmp, "suite")
        counts = build_suite(col, out)
        eq("suite counts", counts, {"outcome": 2, "trigger": 5})
        eq("manifest", json.load(open(os.path.join(out, ".claude-plugin", "plugin.json")))["name"], "demo-skills")
        eq("skills linked", os.path.isfile(os.path.join(out, "skills", "alpha", "SKILL.md")), True)
        graders = sorted(os.listdir(os.path.join(out, "evals", "outcome-alpha", "graders")))
        eq("alpha graders", graders, ["calibration.md", "fact-1.md", "fact-2.md", "rubric.md", "script-run.md", "skill-fired.md"])
        eq("beta has no script grader", "script-run.md" in os.listdir(os.path.join(out, "evals", "outcome-beta", "graders")), False)
        fact = open(os.path.join(out, "evals", "outcome-alpha", "graders", "fact-2.md")).read()
        eq("regex is quoted yaml", 'pattern: "never.*checked"' in fact, True)
        rubric = open(os.path.join(out, "evals", "outcome-alpha", "graders", "rubric.md")).read()
        eq("rubric uses the good answer", "names the thing and says what it did not check." in rubric, True)
        neg = open(os.path.join(out, "evals", "trigger-alpha-neg", "graders", "trigger.md")).read()
        eq("negative grader forbids the skill", "max: 0" in neg and "alpha" in neg, True)
        none = open(os.path.join(out, "evals", "trigger-none", "graders", "trigger.md")).read()
        eq("unrelated grader forbids any skill", "input_match" not in none and "max: 0" in none, True)
        only = build_suite(col, os.path.join(tmp, "suite2"), only={"beta"})
        eq("only filter", only, {"outcome": 1, "trigger": 2})
        prompt = open(os.path.join(out, "evals", "outcome-alpha", "prompt.md")).read()
        eq("prompt body", prompt.rstrip().endswith("Do the alpha thing with widget."), True)
    return fails, count[0]
