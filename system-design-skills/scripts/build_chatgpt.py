#!/usr/bin/env python3
"""Build self-contained, upload-ready skill bundles for ChatGPT and the OpenAI API.

Why this exists: in this library the specialist skills reference shared templates with
paths such as ../system-design/assets/templates/adr.md. OpenAI skill bundles are a single
top-level folder containing exactly one SKILL.md, so a bundle cannot reach a sibling
skill. This script copies the templates a skill needs into that skill's own
assets/templates/, rewrites the links, adds optional agents/openai.yaml display metadata,
and writes one zip per skill.

Limits enforced (OpenAI developer docs, "Skills" guide, read 2026-10-14):
  - zip contains a single top-level folder
  - exactly one SKILL.md in the bundle
  - at most 500 files per skill; zip <= 50 MB; each file <= 25 MB
Zips are built deterministically (fixed timestamps, sorted entries), so rebuilding an
unchanged skill yields a byte-identical file.

Usage:
  python3 scripts/build_chatgpt.py                 # all skills -> chatgpt/<skill>.zip
  python3 scripts/build_chatgpt.py --skill payment-systems --out /tmp/out
  python3 scripts/build_chatgpt.py --check         # build to a temp dir and verify only
"""
import argparse
import os
import re
import shutil
import stat
import sys
import tempfile
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SKILLS = os.path.join(ROOT, "skills")
TEMPLATES_SRC = os.path.join(SKILLS, "system-design", "assets", "templates")
MAX_FILES, MAX_ZIP, MAX_FILE = 500, 50 * 1024 * 1024, 25 * 1024 * 1024
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
XREF = re.compile(r"\.\./system-design/assets/templates/([A-Za-z0-9_.-]+\.md)")
OTHER_XREF = re.compile(r"\.\./([a-z0-9-]+)/")


def read_frontmatter(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", t, re.S)
    d = {}
    if m:
        for line in m.group(1).split("\n"):
            if line and not line.startswith(" ") and ":" in line:
                k, _, v = line.partition(":")
                d[k.strip()] = v.strip()
    return d


def short_desc(desc, limit=120):
    """Short UI summary: first sentence, cut at a clause or word boundary if too long."""
    first = re.split(r"(?<=[.!?])\s", desc, maxsplit=1)[0].rstrip(".")
    if len(first) > limit:
        cut = first[:limit]
        for sep in (" - ", ", ", " "):
            i = cut.rfind(sep)
            if i > 40:
                cut = cut[:i]
                break
        first = cut.rstrip(" ,-") + "..."
    return first.replace('"', "'")


def stage_skill(name, stage_root):
    src = os.path.join(SKILLS, name)
    dst = os.path.join(stage_root, name)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    needed = set()
    for dp, _, files in os.walk(dst):
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            text = open(p, encoding="utf-8").read()
            needed.update(XREF.findall(text))
            for other in OTHER_XREF.findall(text):
                if other not in ("system-design",) and name != other:
                    raise SystemExit("%s: unsupported cross-skill path ../%s/ in %s" % (name, other, p))
            if name != "system-design":
                new = XREF.sub(lambda m: "assets/templates/" + m.group(1), text)
                if new != text:
                    open(p, "w", encoding="utf-8").write(new)
    if name != "system-design":
        tdir = os.path.join(dst, "assets", "templates")
        os.makedirs(tdir, exist_ok=True)
        for t in sorted(needed):
            s = os.path.join(TEMPLATES_SRC, t)
            if not os.path.isfile(s):
                raise SystemExit("%s: referenced template missing: %s" % (name, t))
            shutil.copy(s, os.path.join(tdir, t))
    fm = read_frontmatter(os.path.join(dst, "SKILL.md"))
    display = " ".join(w.capitalize() for w in name.split("-"))
    os.makedirs(os.path.join(dst, "agents"), exist_ok=True)
    with open(os.path.join(dst, "agents", "openai.yaml"), "w", encoding="utf-8") as fh:
        fh.write(
            "interface:\n"
            '  display_name: "%s"\n'
            '  short_description: "%s"\n'
            "policy:\n"
            "  allow_implicit_invocation: true\n" % (display, short_desc(fm.get("description", "")))
        )
    return dst


def write_zip(stage_dir, name, out_path):
    entries = []
    for dp, _, files in os.walk(stage_dir):
        for f in files:
            full = os.path.join(dp, f)
            entries.append((os.path.join(name, os.path.relpath(full, stage_dir)).replace(os.sep, "/"), full))
    entries.sort()
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, full in entries:
            zi = zipfile.ZipInfo(arc, FIXED_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if os.stat(full).st_mode & stat.S_IXUSR else 0o644
            zi.external_attr = (stat.S_IFREG | mode) << 16
            with open(full, "rb") as fh:
                z.writestr(zi, fh.read())


def verify_zip(path, name):
    errors = []
    with zipfile.ZipFile(path) as z:
        infos = [i for i in z.infolist() if not i.filename.endswith("/")]
        tops = {i.filename.split("/")[0] for i in infos}
        if tops != {name}:
            errors.append("expected single top-level folder '%s', found %s" % (name, sorted(tops)))
        skills_md = [i.filename for i in infos if os.path.basename(i.filename).lower() == "skill.md"]
        if skills_md != [name + "/SKILL.md"]:
            errors.append("expected exactly one SKILL.md at %s/SKILL.md, found %s" % (name, skills_md))
        if len(infos) > MAX_FILES:
            errors.append("%d files exceeds %d" % (len(infos), MAX_FILES))
        for i in infos:
            if i.file_size > MAX_FILE:
                errors.append("%s exceeds per-file limit" % i.filename)
        names = {i.filename for i in infos}
        for i in infos:
            if not i.filename.endswith(".md"):
                continue
            text = z.read(i).decode("utf-8")
            base = os.path.dirname(i.filename)
            for m in re.finditer(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]*)?\)", text):
                tgt = m.group(1).strip()
                if re.match(r"^[a-z]+://", tgt) or tgt.startswith("mailto:"):
                    continue
                p = os.path.normpath(os.path.join(base, tgt)).replace(os.sep, "/")
                if p not in names:
                    errors.append("%s: broken link %s" % (i.filename, tgt))
            for m in re.finditer(r"`((?:references|scripts|assets)/[A-Za-z0-9_./-]+)`", text):
                tgt = m.group(1)
                if tgt.endswith("/") or "*" in tgt or "{" in tgt:
                    continue
                if (base + "/" + tgt) not in names:
                    errors.append("%s: referenced path missing %s" % (i.filename, tgt))
            if "../" in text and ("](../" in text or "`../" in text):
                errors.append("%s: still contains a ../ path that leaves the bundle" % i.filename)
    size = os.path.getsize(path)
    if size > MAX_ZIP:
        errors.append("zip is %d bytes (limit %d)" % (size, MAX_ZIP))
    return errors, len(infos), size


def main():
    ap = argparse.ArgumentParser(description="Build ChatGPT/OpenAI-ready skill zips.")
    ap.add_argument("--skill", action="append", help="build only this skill (repeatable)")
    ap.add_argument("--out", default=os.path.join(ROOT, "chatgpt"), help="output directory (default: chatgpt/)")
    ap.add_argument("--check", action="store_true", help="build to a temporary directory and only verify")
    a = ap.parse_args()
    names = a.skill or sorted(d for d in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md")))
    out = tempfile.mkdtemp() if a.check else os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    bad = 0
    for n in names:
        if not os.path.isfile(os.path.join(SKILLS, n, "SKILL.md")):
            print("error: unknown skill %s" % n, file=sys.stderr)
            return 2
        with tempfile.TemporaryDirectory() as tmp:
            stage = stage_skill(n, tmp)
            zpath = os.path.join(out, n + ".zip")
            write_zip(stage, n, zpath)
        errs, count, size = verify_zip(zpath, n)
        status = "ok  " if not errs else "FAIL"
        print("%s %-26s %3d files %7d bytes" % (status, n, count, size))
        for e in errs:
            print("      - " + e)
        bad += bool(errs)
    if a.check:
        shutil.rmtree(out, ignore_errors=True)
    print("\n%d bundle(s), %d failed" % (len(names), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
