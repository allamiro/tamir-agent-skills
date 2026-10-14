#!/usr/bin/env python3
"""Run every free check in the repository (standard library only).

  python3 tools/check_repo.py [--quick]

Runs, for each collection, its validator, its routing or answer checks, and the shared evaluation tool's unit tests,
and confirms that the citation checker copied into four skills is byte-identical in each. It never calls an AI
model and spends nothing. --quick skips the validators that rebuild the ChatGPT bundles.
"""
import argparse
import hashlib
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CHECKS = [
    ("system-design-skills", ["scripts/validate_library.py"]),
    ("system-design-skills", ["scripts/check_routing.py"]),
    ("egyptology-skills", ["scripts/validate_collection.py"]),
    ("egyptology-skills", ["scripts/check_answers.py"]),
    ("bioinformatics-skills", ["scripts/validate_collection.py"]),
    ("bioinformatics-skills", ["scripts/check_routing.py"]),
    ("bioinformatics-skills", ["scripts/check_answers.py"]),
    ("systems-biology-skills", ["scripts/validate_collection.py"]),
    ("systems-biology-skills", ["scripts/check_routing.py"]),
    ("systems-biology-skills", ["scripts/check_answers.py"]),
    (".", ["tools/run_evals.py", "selftest"]),
]
SHARED = ["system-design-skills/skills/systems-literature-reading/scripts/citecheck.py",
          "egyptology-skills/skills/egyptology-literature/scripts/citecheck.py",
          "bioinformatics-skills/skills/literature-search-appraisal/scripts/citecheck.py",
          "systems-biology-skills/skills/systems-biology-literature/scripts/citecheck.py"]


def main():
    ap = argparse.ArgumentParser(description="Run every free check in the repository.")
    ap.add_argument("--quick", action="store_true", help="skip the validators (they rebuild and compare the ChatGPT bundles)")
    a = ap.parse_args()
    failed = []
    for folder, cmd in CHECKS:
        if a.quick and "validate" in cmd[0]:
            continue
        r = subprocess.run([sys.executable] + cmd, cwd=os.path.join(ROOT, folder), capture_output=True, text=True)
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        print("%-4s %-22s %-34s %s" % ("ok" if r.returncode == 0 else "FAIL", folder, " ".join(cmd), tail[:70]))
        if r.returncode:
            failed.append(" ".join(cmd))
    digests = {hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest() for p in SHARED}
    same = len(digests) == 1
    print("%-4s %-22s %-34s %s" % ("ok" if same else "FAIL", "shared script", "citecheck.py copies", "identical" if same else "the copies differ"))
    if not same:
        failed.append("citecheck.py copies")
    print("\n%s" % ("all checks passed" if not failed else "FAILED: " + "; ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
