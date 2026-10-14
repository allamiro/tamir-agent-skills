#!/usr/bin/env python3
"""Validate bioinformatics-skills (standard library only).

Per skill: the twenty-three expected skills exist; frontmatter keys; name equals directory; license;
description length and plain-YAML safety (no ': ' or ' #' when unquoted); SKILL.md under 500 lines; required headings; every relative link and every
backticked `references/...`, `assets/...` or `scripts/...` path resolves; every references/*.md and
every file under assets/ is mentioned in SKILL.md; code fences balanced; every backticked skill
name is a real skill; every script runs --help and passes --selftest, and SKILL.md names it.
Navigation: README.md, claude/README.md, openai/README.md and prompts/README.md exist and their
relative links resolve; each skill has its own prompts file with numbered prompts; prompt counts
match the READMEs; no skill is copied into claude/ or openai/. ChatGPT bundles: openai/chatgpt/ holds
one zip per skill and each is current with its skill (scripts/build_chatgpt.py --fresh). No source
book or PDF is tracked by git.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILLS = os.path.join(ROOT, "skills")
EXPECTED = ["bioinformatics-workflow", "experimental-design", "biological-databases", "data-governance-ethics",
            "sequence-formats", "ngs-pipelines", "sequence-alignment", "gene-finding-translation",
            "protein-analysis", "phylogenetics", "variants-population-genetics", "omics-data-analysis",
            "information-theory-sequences", "sequence-statistics", "machine-learning-biology",
            "bioinformatics-programming", "reproducible-research-code", "research-writing-reporting",
            "bioinformatics-review", "bioinformatics-learning-path",
            "literature-search-appraisal", "method-benchmarking", "research-proposal-planning"]
SIBLING_COLLECTIONS = {"accuracy-review", "system-design-review"}  # named as method precedents
HEADINGS = ["## Purpose and activation", "## Required inputs", "## Workflow", "## Decision framework",
            "## Failure and edge cases", "## Validation", "## Expected output", "## Sources and confidence"]
errors = []


def err(msg):
    errors.append(msg)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).split("\n"):
        if re.match(r"^[a-z]", line) and ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


present = sorted(d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d)))
if present != sorted(EXPECTED):
    err("skills present %s != expected %s" % (present, sorted(EXPECTED)))

script_count = 0
for name in EXPECTED:
    d = os.path.join(SKILLS, name)
    p = os.path.join(d, "SKILL.md")
    if not os.path.isfile(p):
        err("%s: missing SKILL.md" % name)
        continue
    text = open(p, encoding="utf-8").read()
    fm = frontmatter(text)
    if not fm:
        err("%s: bad frontmatter" % name)
        continue
    for k in ("name", "description", "license", "metadata"):
        if k not in fm:
            err("%s: frontmatter missing %s" % (name, k))
    if fm.get("name") != name:
        err("%s: name %r != directory" % (name, fm.get("name")))
    if fm.get("license") != "Apache-2.0":
        err("%s: license is %r, expected Apache-2.0" % (name, fm.get("license")))
    if not (1 <= len(fm.get("description", "")) <= 1024):
        err("%s: description length %d" % (name, len(fm.get("description", ""))))
    desc = fm.get("description", "")
    if desc[:1] not in ("'", '"') and (": " in desc or " #" in desc or desc.endswith(":")):
        err("%s: description has ': ' or ' #' in an unquoted YAML value; rephrase or quote it" % name)
    if text.count("\n") + 1 > 500:
        err("%s: SKILL.md over 500 lines" % name)
    for h in HEADINGS:
        if h not in text:
            err("%s: missing heading %s" % (name, h))
    if text.count("```") % 2:
        err("%s: unbalanced code fence" % name)
    for ref in set(re.findall(r"`((?:references|assets|scripts)/[A-Za-z0-9_./-]+)`", text)):
        if not os.path.exists(os.path.join(d, ref)):
            err("%s: mentioned path not found: %s" % (name, ref))
    for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
        if not re.match(r"^[a-z]+:", target) and not os.path.exists(os.path.normpath(os.path.join(d, target))):
            err("%s: broken link %s" % (name, target))
    for tok in set(re.findall(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`", text)):
        if tok not in EXPECTED and tok not in SIBLING_COLLECTIONS:
            err("%s: `%s` looks like a skill name but no such skill exists" % (name, tok))
    refs = os.path.join(d, "references")
    if os.path.isdir(refs):
        for f in os.listdir(refs):
            if f.endswith(".md") and "references/" + f not in text:
                err("%s: references/%s is not linked from SKILL.md" % (name, f))
    assets = os.path.join(d, "assets")
    for dirpath, _dirs, files in os.walk(assets):
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), d).replace(os.sep, "/")
            if rel not in text:
                err("%s: %s is not mentioned in SKILL.md" % (name, rel))
    scripts = os.path.join(d, "scripts")
    if os.path.isdir(scripts):
        for f in sorted(os.listdir(scripts)):
            if not f.endswith(".py"):
                continue
            script_count += 1
            if "scripts/" + f not in text:
                err("%s: scripts/%s is not mentioned in SKILL.md" % (name, f))
            path = os.path.join(scripts, f)
            for args in (["--help"], ["--selftest"]):
                r = subprocess.run([sys.executable, path] + args, capture_output=True, text=True)
                if r.returncode:
                    err("%s/scripts/%s %s failed: %s" % (name, f, args[0], (r.stdout + r.stderr).strip()[-300:]))
                elif args == ["--selftest"]:
                    print(r.stdout.strip())

# Navigation: which folder is for which tool, and one prompts file per skill.
NAV = ["README.md", "claude/README.md", "openai/README.md", "prompts/README.md"]
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def read_doc(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.isfile(path):
        err("missing file: " + rel)
        return ""
    return open(path, encoding="utf-8").read()


for rel in NAV + ["prompts/%s.md" % n for n in EXPECTED]:
    text = read_doc(rel)
    base = os.path.dirname(os.path.join(ROOT, rel))
    if "PROMPTS.md" in text:
        err("%s: still mentions the old PROMPTS.md" % rel)
    for target in LINK.findall(text):
        if re.match(r"^[a-z]+:", target):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(base, target))):
            err("%s: broken link %s" % (rel, target))

readme, prompts_index = read_doc("README.md"), read_doc("prompts/README.md")
for needed in ("claude/README.md", "openai/README.md", "prompts/README.md"):
    if needed not in readme:
        err("README.md does not link " + needed)
for name in EXPECTED:
    text = read_doc("prompts/%s.md" % name)
    count = len(re.findall(r"^> ", text, re.M))
    headings = len(re.findall(r"^## \d+\. ", text, re.M))
    if count < 3 or count != headings:
        err("prompts/%s.md: %d prompts for %d numbered headings (need 3 or more, equal)" % (name, count, headings))
    if "skills/%s/" % name not in readme:
        err("README.md does not link skills/%s/" % name)
    if "[%d](prompts/%s.md)" % (count, name) not in readme:
        err("README.md prompt count for %s is not %d" % (name, count))
    if "[%d prompts](%s.md)" % (count, name) not in prompts_index:
        err("prompts/README.md prompt count for %s is not %d" % (name, count))

for platform in ("claude", "openai"):
    for dirpath, _dirs, files in os.walk(os.path.join(ROOT, platform)):
        if "SKILL.md" in files:
            err("%s holds a copy of a skill (%s): skills live only in skills/" % (platform, dirpath))

zdir = os.path.join(ROOT, "openai", "chatgpt")
zips = sorted(f[:-4] for f in os.listdir(zdir) if f.endswith(".zip")) if os.path.isdir(zdir) else []
if zips != sorted(EXPECTED):
    err("openai/chatgpt/ has zips for %s, expected %s" % (zips, sorted(EXPECTED)))
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_chatgpt.py"), "--fresh"],
                   capture_output=True, text=True)
if r.returncode:
    err("ChatGPT bundles are invalid or out of date: " + " | ".join(
        ln.strip() for ln in r.stdout.splitlines() if ln.strip().startswith(("FAIL", "-")))[:400])

tools_runner = os.path.join(ROOT, "..", "tools", "run_evals.py")
if not os.path.isfile(os.path.join(ROOT, "evals", "cases.json")):
    err("missing evals/cases.json")
elif os.path.isfile(tools_runner):
    r = subprocess.run([sys.executable, tools_runner, "plan", ROOT], capture_output=True, text=True)
    if r.returncode:
        err("evals/cases.json: " + " | ".join(ln.strip() for ln in r.stdout.splitlines() if ln.startswith("PROBLEM"))[:500])
else:
    print("note: ../tools/run_evals.py not found, evaluation cases were not checked")

try:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
    for f in out:
        if f.lower().endswith(".pdf") or "/source/" in "/" + f or f.startswith("source/"):
            err("source material is tracked by git: " + f)
except OSError:
    pass

if errors:
    print("FAILED: %d error(s)" % len(errors))
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK: %d skills, %d scripts, 0 errors" % (len(EXPECTED), script_count))
