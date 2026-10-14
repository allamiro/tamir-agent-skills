#!/usr/bin/env python3
"""Build self-contained, upload-ready skill bundles for ChatGPT and the OpenAI API.

Why a bundle per skill: an OpenAI skill bundle is a zip with a single top-level folder that holds
exactly one SKILL.md, so a bundle cannot contain a sibling skill. The skills here name each other
but never link into each other's folders, so each skill is packaged as it is, plus optional
agents/openai.yaml display metadata. Upload the skills you need together.

Limits enforced (OpenAI developer docs, "Skills" guide, read 2026-10-14):
  - zip contains a single top-level folder
  - exactly one SKILL.md in the bundle
  - at most 500 files per skill; zip <= 50 MB; each file <= 25 MB
Zips are built deterministically (fixed timestamps, sorted entries). `--fresh` compares the
committed zips with a new build by file name, size and CRC, so a skill edited without rebuilding
is caught even if two compressors would write different bytes.

Usage:
  python3 scripts/build_chatgpt.py                 # all skills -> openai/chatgpt/<skill>.zip
  python3 scripts/build_chatgpt.py --skill NAME --out /tmp/out
  python3 scripts/build_chatgpt.py --check         # build to a temp dir and verify limits only
  python3 scripts/build_chatgpt.py --fresh         # also fail if the committed zips are stale
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
COMMITTED = os.path.join(ROOT, "openai", "chatgpt")
MAX_FILES, MAX_ZIP, MAX_FILE = 500, 50 * 1024 * 1024, 25 * 1024 * 1024
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def read_frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        t = fh.read()
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
    for dp, _, files in os.walk(dst):
        for f in files:
            if f.endswith(".md"):
                with open(os.path.join(dp, f), encoding="utf-8") as fh:
                    text = fh.read()
                if "](../" in text or "`../" in text:
                    raise SystemExit("%s: %s links outside the skill folder with ../, which a bundle cannot follow"
                                     % (name, os.path.join(dp, f)))
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
                if os.path.normpath(os.path.join(base, tgt)).replace(os.sep, "/") not in names:
                    errors.append("%s: broken link %s" % (i.filename, tgt))
            for m in re.finditer(r"`((?:references|scripts|assets)/[A-Za-z0-9_./-]+)`", text):
                tgt = m.group(1)
                if tgt.endswith("/") or "*" in tgt or "{" in tgt:
                    continue
                if (base + "/" + tgt) not in names:
                    errors.append("%s: referenced path missing %s" % (i.filename, tgt))
    size = os.path.getsize(path)
    if size > MAX_ZIP:
        errors.append("zip is %d bytes (limit %d)" % (size, MAX_ZIP))
    return errors, len(infos), size


def fingerprint(path):
    """(name, size, CRC) of every member: what the zip holds, whatever the compressor did."""
    with zipfile.ZipFile(path) as z:
        return sorted((i.filename, i.file_size, i.CRC) for i in z.infolist() if not i.filename.endswith("/"))


def main():
    ap = argparse.ArgumentParser(description="Build ChatGPT/OpenAI-ready skill zips.")
    ap.add_argument("--skill", action="append", help="build only this skill (repeatable)")
    ap.add_argument("--out", default=COMMITTED, help="output directory (default: openai/chatgpt/)")
    ap.add_argument("--check", action="store_true", help="build to a temporary directory and only verify")
    ap.add_argument("--fresh", action="store_true",
                    help="also fail if a committed zip is missing or differs from a new build (implies --check)")
    a = ap.parse_args()
    all_names = sorted(d for d in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md")))
    names = a.skill or all_names
    check = a.check or a.fresh
    out = tempfile.mkdtemp() if check else os.path.abspath(a.out)
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
        if a.fresh:
            committed = os.path.join(COMMITTED, n + ".zip")
            if not os.path.isfile(committed):
                errs.append("committed zip is missing: run scripts/build_chatgpt.py")
            elif fingerprint(committed) != fingerprint(zpath):
                errs.append("committed zip is out of date with skills/%s: run scripts/build_chatgpt.py" % n)
        print("%s %-30s %3d files %7d bytes" % ("ok  " if not errs else "FAIL", n, count, size))
        for e in errs:
            print("      - " + e)
        bad += bool(errs)
    if a.fresh and not a.skill:
        extra = sorted(f for f in (os.listdir(COMMITTED) if os.path.isdir(COMMITTED) else [])
                       if f.endswith(".zip") and f[:-4] not in all_names)
        for f in extra:
            print("FAIL %s: committed zip has no skill" % f)
            bad += 1
    if check:
        shutil.rmtree(out, ignore_errors=True)
    print("\n%d bundle(s), %d failed" % (len(names), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
