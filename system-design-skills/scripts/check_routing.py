#!/usr/bin/env python3
"""Description-routing smoke test (standard library only).

Ranks every skill's name + description against each prompt in evals/routing_cases.json
with a simple BM25 lexical score and checks:
  - at least one expected skill appears in the top K
  - no forbidden skill appears in the top K with a score >= 50% of the best score
  (and > 3.0), so rank-3 lexical noise is not counted as misrouting
  - for negative prompts (no expected skills) the best score stays below a threshold,
    meaning no system-design skill looks like a strong match

This is a lexical proxy for description quality. It does NOT prove an LLM will route
correctly; it catches descriptions that lack the words users actually type.

Usage: python3 scripts/check_routing.py [--root PATH] [--verbose]
"""
import argparse
import json
import math
import os
import re
import sys

MIN_SHARE = 0.5
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
        text = open(md, encoding="utf-8").read()
        m = re.search(r"^description:\s*(.+)$", text, re.M)
        desc = m.group(1) if m else ""
        skills[name] = tokens(name.replace("-", " ") + " " + desc)
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


def main():
    ap = argparse.ArgumentParser(description="Lexical routing smoke test for skill descriptions.")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    ap.add_argument("--cases", default=None, help="path to routing_cases.json")
    ap.add_argument("--neg-threshold", type=float, default=6.0,
                    help="max allowed top score for negative prompts (default 6.0)")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    cases_path = a.cases or os.path.join(root, "evals", "routing_cases.json")
    spec = json.load(open(cases_path, encoding="utf-8"))
    k = spec.get("top_k", 3)
    docs = load_skills(root)
    failures, passed = [], 0
    for c in spec["cases"]:
        sc = bm25(tokens(c["prompt"]), docs)
        ranked = sorted(sc.items(), key=lambda kv: -kv[1])
        top = [n for n, _ in ranked[:k]]
        ok, why = True, []
        if c.get("expect_any") and not set(c["expect_any"]) & set(top):
            ok = False
            why.append("none of %s in top %d %s" % (c["expect_any"], k, top))
        top_score = ranked[0][1]
        # A forbidden skill only counts as a routing error when it scores at least
        # MIN_SHARE of the best score; low-scoring rank-3 noise is not misrouting.
        bad = {n for n in set(c.get("forbidden", [])) & set(top)
               if sc[n] >= MIN_SHARE * top_score and sc[n] > 3.0}
        if bad:
            ok = False
            why.append("forbidden in top %d: %s" % (k, sorted(bad)))
        if not c.get("expect_any") and "forbidden_all_above" in c:
            if ranked[0][1] > a.neg_threshold:
                ok = False
                why.append("negative prompt scored %.2f for %s (threshold %.1f)" % (ranked[0][1], ranked[0][0], a.neg_threshold))
        if a.verbose:
            print("%-12s %s top=%s scores=%s" % (c["id"], "PASS" if ok else "FAIL", top,
                                                 ["%.1f" % s for _, s in ranked[:k]]))
        if ok:
            passed += 1
        else:
            failures.append((c["id"], why))
    for cid, why in failures:
        print("FAIL %s: %s" % (cid, "; ".join(why)))
    print("%d/%d routing cases passed" % (passed, len(spec["cases"])))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
