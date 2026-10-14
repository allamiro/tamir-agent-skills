#!/usr/bin/env python3
"""Validate egyptology-skills (standard library only).

Checks: five expected skills; frontmatter keys; name equals directory; description length;
SKILL.md under 500 lines; required headings; every relative link and `references/...` or
`assets/...` mention resolves; code fences balanced; the sign table (each row has a status,
each code maps to a Unicode character); navigation (claude/, openai/ and prompts/ files exist,
relative links resolve, each skill has its own prompts file, prompt counts match the READMEs,
prompts only use signs from the table, no skill is copied into a platform folder); no source PDF
or source folder is tracked by git; the lookup script self-test passes.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SKILLS = os.path.join(ROOT, "skills")
EXPECTED = ["gardiner-sign-lookup", "transliteration", "text-annotation",
            "hieroglyph-app-builder", "accuracy-review"]
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
    if not (1 <= len(fm.get("description", "")) <= 1024):
        err("%s: description length %d" % (name, len(fm.get("description", ""))))
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
    for sub in os.listdir(d):
        full = os.path.join(d, sub)
        if os.path.isdir(full) and sub in ("references",):
            for f in os.listdir(full):
                if f.endswith(".md") and "references/" + f not in text:
                    err("%s: references/%s is not linked from SKILL.md" % (name, f))

sys.path.insert(0, os.path.join(SKILLS, "gardiner-sign-lookup", "scripts"))
import signs  # noqa: E402

rows = json.load(open(os.path.join(SKILLS, "gardiner-sign-lookup", "references", "common-signs.json"),
                      encoding="utf-8"))["signs"]
for r in rows:
    t = signs.normalize(r["code"])
    if not t or not signs.to_char(t):
        err("sign table: %s has no Unicode character" % r["code"])
    for k in ("label", "role", "gardiner_page", "status"):
        if not r.get(k):
            err("sign table: %s missing %s" % (r["code"], k))
    if r["role"] != "determinative" and not r.get("value"):
        err("sign table: %s has role %s but no value" % (r["code"], r["role"]))
    if r["role"] == "determinative" and r.get("value"):
        err("sign table: determinative %s has a value" % r["code"])

# Navigation: which folder is for which tool, and one prompts file per skill.
NAV = ["README.md", "claude/README.md", "openai/README.md", "prompts/README.md"]
# prompts/gardiner-sign-lookup.md asks about a sign that is deliberately not in the table.
OUTSIDE_TABLE_TESTS = {"A14"}
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
table_codes = {r["code"] for r in rows}


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
    for line in re.findall(r"^> (.*)$", text, re.M):
        for code in re.findall(r"\b[A-Z]{1,2}\d{1,3}[A-Z]?\b", line):
            if code not in table_codes and code not in OUTSIDE_TABLE_TESTS:
                err("prompts/%s.md: sign %s is not in the checked table" % (name, code))

for platform in ("claude", "openai"):
    for dirpath, _dirs, files in os.walk(os.path.join(ROOT, platform)):
        if "SKILL.md" in files:
            err("%s holds a copy of a skill (%s): skills live only in skills/" % (platform, dirpath))

try:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
    for f in out:
        if f.lower().endswith(".pdf") or "/source/" in "/" + f or f.startswith("source/"):
            err("source material is tracked by git: " + f)
except OSError:
    pass

r = subprocess.run([sys.executable, os.path.join(SKILLS, "gardiner-sign-lookup", "scripts", "signs.py"),
                    "--selftest"], capture_output=True, text=True)
if r.returncode:
    err("signs.py self-test failed: " + r.stdout + r.stderr)
else:
    print(r.stdout.strip())

if errors:
    print("FAILED: %d error(s)" % len(errors))
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("OK: %d skills, %d sign-table rows, 0 errors" % (len(EXPECTED), len(rows)))
