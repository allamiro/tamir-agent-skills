#!/usr/bin/env python3
"""Description-routing smoke test (standard library only).

Ranks every skill's name + description against the first prompt in each prompts/<skill>.md with a
simple BM25 lexical score. That prompt's own skill must rank first.

This is a lexical proxy for description quality. It does NOT prove an LLM will route correctly;
it catches descriptions that lack the words users actually type.

Usage: python3 scripts/check_routing.py [--root PATH] [--verbose]
"""
import argparse
import math
import os
import re
import sys

STOP = set("a an the and or of to in on for with is are be this that it as at by from we our you your i my how do does should can what which when use used using into over about not no if so but have has had will would".split())


def tokens(text):
    out = []
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        if w in STOP or len(w) < 2:
            continue
        if len(w) > 4 and w.endswith("ing"):
            w = w[:-3]
        elif len(w) > 3 and w.endswith("es"):
            w = w[:-2]
        elif len(w) > 3 and w.endswith("s"):
            w = w[:-1]
        out.append(w)
    return out


def load_skills(root):
    skills = {}
    sroot = os.path.join(root, "skills")
    for name in sorted(os.listdir(sroot)):
        md = os.path.join(sroot, name, "SKILL.md")
        if not os.path.isfile(md):
            continue
        with open(md, encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(r"^description:\s*(.+)$", text, re.M)
        skills[name] = tokens(name.replace("-", " ") + " " + (m.group(1) if m else ""))
    return skills


def bm25(query, docs, k1=1.5, b=0.75):
    n = len(docs)
    avgdl = sum(len(d) for d in docs.values()) / n
    df = {}
    for d in docs.values():
        for t in set(d):
            df[t] = df.get(t, 0) + 1
    scores = {}
    for name, d in docs.items():
        s = 0.0
        for t in set(query):
            if t not in df:
                continue
            tf = d.count(t)
            if tf == 0:
                continue
            idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
            s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avgdl))
        scores[name] = s
    return scores


def first_prompt(path):
    """The first '> ' line of a prompts file: the starter prompt for that skill."""
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("> "):
                return line[2:].strip()
    return None


def main():
    ap = argparse.ArgumentParser(description="Lexical routing smoke test for skill descriptions.")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    docs = load_skills(root)
    failures, passed = [], 0
    for name in sorted(docs):
        path = os.path.join(root, "prompts", name + ".md")
        prompt = first_prompt(path) if os.path.isfile(path) else None
        if prompt is None:
            failures.append((name, "no prompts/%s.md or no prompt in it" % name))
            continue
        ranked = sorted(bm25(tokens(prompt), docs).items(), key=lambda kv: -kv[1])
        ok = ranked[0][0] == name
        if a.verbose:
            print("%-30s %s  %s" % (name, "PASS" if ok else "FAIL",
                                    ", ".join("%s %.1f" % (n, s) for n, s in ranked[:3])))
        if ok:
            passed += 1
        else:
            failures.append((name, "expected it to rank first, got %s" % ", ".join(
                "%s %.1f" % (n, s) for n, s in ranked[:3])))
    for name, why in failures:
        print("FAIL %s: %s" % (name, why))
    print("%d/%d starter prompts route to their own skill" % (passed, len(docs)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
