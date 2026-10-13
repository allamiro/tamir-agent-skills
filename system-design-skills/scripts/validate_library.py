#!/usr/bin/env python3
"""Validate the system-design-skills library (standard library only).

Checks, per skill directory under skills/:
  - SKILL.md exists with YAML frontmatter; keys limited to the allowed set
  - name matches the directory, spec character rules, <= 64 chars
  - description is 1-1024 chars and non-empty
  - body size: < 500 lines and an approximate token estimate under 5000
  - required section headings are present (the library contract)
  - code fences (``` ) are balanced; mermaid blocks are non-empty
  - every relative Markdown link and every backticked relative file path
    (references/, scripts/, assets/, ../system-design/...) resolves inside skills/
  - SKILL.md never links outside the skills/ tree (so skills install without repo files)
  - Python scripts under scripts/ respond to --help and, if they offer --selftest, pass it
Library-level checks:
  - all 17 expected skills exist, no unexpected ones
  - all 11 templates exist and are non-trivial
  - every skill's Sources block exists

Exit code 0 when everything passes, 1 otherwise.

Usage:
  python3 scripts/validate_library.py [--root PATH] [--skip-scripts]
"""
import argparse
import os
import re
import subprocess
import sys

EXPECTED_SKILLS = [
    "system-design", "requirements-capacity", "architecture-scaling", "api-networking",
    "identity-security", "database-selection", "transactions-consistency",
    "sharding-replication", "caching-performance", "messaging-streaming",
    "storage-systems", "deployment-delivery", "reliability-resilience", "observability",
    "geospatial-design", "payment-systems", "system-design-review",
]
EXPECTED_TEMPLATES = [
    "system-design-document", "adr", "requirements", "capacity-worksheet",
    "technology-selection-matrix", "database-design-review", "failure-analysis",
    "security-architecture-checklist", "observability-reliability-review",
    "production-readiness-checklist", "review-report",
]
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_HEADINGS = [
    r"^## Purpose and activation",
    r"^## Required inputs",
    r"^## Workflow",
    r"^## Decision framework",
    r"^## Architecture and implementation guidance|^## Architecture and implementation",
    r"^## Failure and edge cases",
    r"^## Validation",
    r"^## Expected output",
    r"^## Sources and confidence",
]
# system-design is the coordinator and uses a slightly different shape for two headings.
HEADING_EXCEPTIONS = {"system-design": {r"^## Decision framework": r"^## Decision framework"}}


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text, "missing opening --- frontmatter delimiter"
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text, "missing closing --- frontmatter delimiter"
    block = text[4:end]
    body = text[end + 5:]
    data, cur = {}, None
    for raw in block.split("\n"):
        if not raw.strip():
            continue
        if raw.startswith("  ") and cur is not None:
            k, _, v = raw.strip().partition(":")
            data[cur][k.strip()] = v.strip().strip('"')
            continue
        k, _, v = raw.partition(":")
        k, v = k.strip(), v.strip()
        if v == "":
            data[k] = {}
            cur = k
        else:
            data[k] = v.strip('"')
            cur = None
    return data, body, None


def approx_tokens(text):
    # Rough planning estimate: ~1.3 tokens per word for English prose with code/tables.
    return int(len(re.findall(r"\S+", text)) * 1.3)


def check_links(skill_dir, skills_root, md_path, text, errors):
    base = os.path.dirname(md_path)
    # markdown links
    for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = m.group(1).split("#")[0].strip()
        if not target or re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
            continue
        path = os.path.normpath(os.path.join(base, target))
        if not os.path.exists(path):
            errors.append("%s: broken link -> %s" % (rel(md_path, skills_root), target))
        elif not path.startswith(os.path.normpath(skills_root) + os.sep):
            errors.append("%s: link leaves skills/ tree -> %s" % (rel(md_path, skills_root), target))
    # backticked relative file references
    for m in re.finditer(r"`((?:\.\./)*(?:references|scripts|assets)/[A-Za-z0-9_./-]+|\.\./[a-z-]+/[A-Za-z0-9_./-]+)`", text):
        target = m.group(1)
        if target.endswith("/"):
            continue
        path = os.path.normpath(os.path.join(base, target))
        if "{" in target or "*" in target:
            continue
        if not os.path.exists(path):
            errors.append("%s: referenced path does not exist -> %s" % (rel(md_path, skills_root), target))
    # forbidden repo-level references from skill files
    for bad in ("docs/authoring-guide", "../../references/", "../../../references/", "source-toc.md", "verified-book-notes.md"):
        if bad in text:
            errors.append("%s: references repo-level file (%s) that is not part of skills/" % (rel(md_path, skills_root), bad))


def rel(path, root):
    return os.path.relpath(path, os.path.dirname(root))


def check_fences(path, text, root, errors):
    lines = text.split("\n")
    open_fence, lang, buf = False, "", []
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            if not open_fence:
                open_fence, lang, buf = True, line.strip()[3:].strip(), []
            else:
                if lang == "mermaid" and not any(b.strip() for b in buf):
                    errors.append("%s:%d: empty mermaid block" % (rel(path, root), i))
                open_fence = False
        elif open_fence:
            buf.append(line)
    if open_fence:
        errors.append("%s: unbalanced code fence" % rel(path, root))


def check_skill(name, skills_root, errors, warnings):
    d = os.path.join(skills_root, name)
    md = os.path.join(d, "SKILL.md")
    if not os.path.isfile(md):
        errors.append("%s: SKILL.md missing" % name)
        return
    text = open(md, encoding="utf-8").read()
    fm, body, err = parse_frontmatter(text)
    if err:
        errors.append("%s: %s" % (name, err))
        return
    extra = set(fm) - ALLOWED_KEYS
    if extra:
        errors.append("%s: unexpected frontmatter keys %s" % (name, sorted(extra)))
    n = fm.get("name", "")
    if n != name:
        errors.append("%s: name '%s' does not match directory" % (name, n))
    if not NAME_RE.match(n) or len(n) > 64:
        errors.append("%s: invalid name '%s'" % (name, n))
    desc = fm.get("description", "")
    if not desc or len(desc) > 1024:
        errors.append("%s: description length %d not in 1..1024" % (name, len(desc)))
    elif len(desc) < 150:
        warnings.append("%s: description is short (%d chars)" % (name, len(desc)))
    lines = text.count("\n") + 1
    toks = approx_tokens(body)
    if lines >= 500:
        errors.append("%s: SKILL.md has %d lines (limit < 500)" % (name, lines))
    if toks >= 5000:
        errors.append("%s: SKILL.md approx %d tokens (limit < 5000)" % (name, toks))
    for pat in REQUIRED_HEADINGS:
        if not re.search(pat, body, re.M):
            errors.append("%s: missing required heading matching /%s/" % (name, pat))
    if "## Sources and confidence" in body:
        tail = body.split("## Sources and confidence", 1)[1]
        if "Book (direct)" not in tail or "Needs workload validation" not in tail:
            errors.append("%s: Sources block lacks 'Book (direct)' / 'Needs workload validation' lines" % name)
        if len([l for l in tail.strip().split("\n") if l.strip()]) > 12:
            warnings.append("%s: Sources block exceeds 12 lines" % name)
    check_fences(md, text, skills_root, errors)
    check_links(d, skills_root, md, text, errors)
    # referenced files must be linked from SKILL.md (one level deep)
    refdir = os.path.join(d, "references")
    if os.path.isdir(refdir):
        for f in sorted(os.listdir(refdir)):
            if f.endswith(".md") and ("references/" + f) not in text and name != "system-design":
                warnings.append("%s: references/%s is not linked from SKILL.md" % (name, f))
        for f in sorted(os.listdir(refdir)):
            p = os.path.join(refdir, f)
            if f.endswith(".md"):
                t = open(p, encoding="utf-8").read()
                check_fences(p, t, skills_root, errors)
                check_links(d, skills_root, p, t, errors)


def check_scripts(skills_root, errors, notes):
    for name in sorted(os.listdir(skills_root)):
        sd = os.path.join(skills_root, name, "scripts")
        if not os.path.isdir(sd):
            continue
        for f in sorted(os.listdir(sd)):
            if not f.endswith(".py"):
                continue
            p = os.path.join(sd, f)
            r = subprocess.run([sys.executable, p, "--help"], capture_output=True, text=True)
            if r.returncode != 0:
                errors.append("%s/scripts/%s: --help exited %d" % (name, f, r.returncode))
                continue
            src = open(p, encoding="utf-8").read()
            if "--selftest" in src:
                r = subprocess.run([sys.executable, p, "--selftest"], capture_output=True, text=True)
                if r.returncode != 0:
                    errors.append("%s/scripts/%s: --selftest failed: %s" % (name, f, (r.stdout + r.stderr).strip()))
                else:
                    notes.append("%s/scripts/%s --selftest: %s" % (name, f, r.stdout.strip().splitlines()[-1]))


def main():
    ap = argparse.ArgumentParser(description="Validate the system-design-skills library.")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),
                    help="library root containing skills/ (default: parent of scripts/)")
    ap.add_argument("--skip-scripts", action="store_true", help="do not execute bundled scripts")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    skills_root = os.path.join(root, "skills")
    errors, warnings, notes = [], [], []
    if not os.path.isdir(skills_root):
        print("error: %s not found" % skills_root, file=sys.stderr)
        return 2
    present = sorted(d for d in os.listdir(skills_root) if os.path.isdir(os.path.join(skills_root, d)))
    for s in EXPECTED_SKILLS:
        if s not in present:
            errors.append("expected skill missing: %s" % s)
    for s in present:
        if s not in EXPECTED_SKILLS:
            warnings.append("unexpected skill directory: %s" % s)
    for s in EXPECTED_SKILLS:
        if s in present:
            check_skill(s, skills_root, errors, warnings)
    tdir = os.path.join(skills_root, "system-design", "assets", "templates")
    for t in EXPECTED_TEMPLATES:
        p = os.path.join(tdir, t + ".md")
        if not os.path.isfile(p):
            errors.append("template missing: %s.md" % t)
        else:
            txt = open(p, encoding="utf-8").read()
            if len(txt) < 800:
                errors.append("template too thin: %s.md (%d chars)" % (t, len(txt)))
            check_fences(p, txt, skills_root, errors)
    for f in ("book-provenance.md", "modernization-notes.md"):
        if not os.path.isfile(os.path.join(skills_root, "system-design", "references", f)):
            errors.append("missing system-design/references/%s" % f)
    if not a.skip_scripts:
        check_scripts(skills_root, errors, notes)
    for n in notes:
        print("ok:   " + n)
    for w in warnings:
        print("warn: " + w)
    for e in errors:
        print("FAIL: " + e)
    print("\n%d skills checked, %d errors, %d warnings" % (len([s for s in EXPECTED_SKILLS if s in present]), len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
