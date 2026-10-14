#!/usr/bin/env python3
"""Run the commands behind the computable "a good answer" lines in prompts/*.md (standard library only).

The lookup script is the only skill script in this collection, so only prompts/gardiner-sign-lookup.md
has computable answers. For each check this runs signs.py, confirms its output contains the expected
text, and confirms that the prompt's own good-answer paragraph mentions the same fact, so the prose
and the computation cannot drift apart. The other skills' good-answer lines describe behaviour
(ask for sign codes, flag the doubt, separate roles) and need a person or a live agent to grade.

This checks the script and the answer key. It does not run any AI agent.

Usage: python3 scripts/check_answers.py [--verbose]
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SIGNS = os.path.join(ROOT, "skills", "gardiner-sign-lookup", "scripts", "signs.py")

# (prompt file, prompt number, signs.py arguments, text the output must contain, text the prompt must mention)
CHECKS = [
    ("gardiner-sign-lookup", 1, ["G17"], "U+13153", "U+13153"),
    ("gardiner-sign-lookup", 1, ["G17"], "section: Birds", "Birds"),
    ("gardiner-sign-lookup", 1, ["G17"], "[Gardiner p. 469]", "p. 469"),
    ("gardiner-sign-lookup", 2, ["--value", "nfr"], "F35", "F35"),
    ("gardiner-sign-lookup", 2, ["--value", "nfr"], "triliteral    nfr", "triliteral nfr"),
    ("gardiner-sign-lookup", 2, ["--value", "nfr"], "[Gardiner p. 465]", "p. 465"),
    ("gardiner-sign-lookup", 3, ["--mdc", "G17-D21:N35"], "\U00013153", "stacked pair joined"),
    ("gardiner-sign-lookup", 4, ["A14"], "No curated reading", "no curated reading"),
    ("gardiner-sign-lookup", 4, ["A14"], "section: Man and his occupations", "Man and his occupations"),
    ("gardiner-sign-lookup", 5, ["D2"], "biliteral     ḥr", "ḥr"),
    ("gardiner-sign-lookup", 5, ["D2"], "Ideogram for 'face'", "ideogram for \"face\""),
]


def good_answer(stem, number):
    path = os.path.join(ROOT, "prompts", stem + ".md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^## %d\. .*?$(.*?)(?=^## |\Z)" % number, text, re.M | re.S)
    if not m:
        return None
    g = re.search(r"A good answer:(.*)", m.group(1), re.S)
    return " ".join(g.group(1).split()) if g else None


def main():
    ap = argparse.ArgumentParser(description="Check the prompts' computable good-answer lines.")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    failures, passed = [], 0
    for stem, number, args, expected, mention in CHECKS:
        r = subprocess.run([sys.executable, "-I", SIGNS] + args, capture_output=True, text=True, timeout=60)
        out = r.stdout + r.stderr
        prose = good_answer(stem, number)
        label = "%s #%d (signs.py %s)" % (stem, number, " ".join(args))
        if expected not in out:
            why = "output lacks %r: %r" % (expected, out.strip()[:160])
        elif prose is None:
            why = "no 'A good answer' paragraph found"
        elif mention not in prose:
            why = "the prompt's good answer does not mention %r" % mention
        else:
            why = None
        if a.verbose:
            print("%s  %s" % ("PASS" if why is None else "FAIL", label))
        if why is None:
            passed += 1
        else:
            failures.append((label, why))
    for label, why in failures:
        print("FAIL %s: %s" % (label, why))
    print("%d answer checks passed, %d failed" % (passed, len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
