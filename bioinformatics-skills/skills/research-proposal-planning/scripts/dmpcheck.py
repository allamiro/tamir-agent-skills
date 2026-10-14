#!/usr/bin/env python3
"""Check a data management plan for missing elements (standard library only).

  dmpcheck.py PLAN.md [--profile nih|fair]
  dmpcheck.py --selftest

Profiles:
  nih   the six elements that university guides report for an NIH Data Management and Sharing plan:
        data type; related tools, software and code; standards; data preservation, access and
        timelines; access, distribution or reuse considerations; oversight.
  fair  the four FAIR groups (findable, accessible, interoperable, reusable) as listed in the
        FAIR Guiding Principles paper.

This is a keyword check. It tells you which element the text never mentions, plus a few warning signs
(placeholders, "upon request" as the only access route, no volume given, no timeline). It cannot tell
whether an element is adequate or true, and a plan can pass it and still be a poor plan. The element names
come from university guides read on 2026-10-14, not from the funder's notice: check the funder's current
template before submitting. Length guidance varies, and the usual figure of two to three pages is not checked here.
"""
import argparse
import re
import sys

PROFILES = {
    "nih": [
        ("Data type", [r"data types?", r"types? of data", r"\braw\b", r"\bprocessed\b", r"\b\d+(\.\d+)?\s?(KB|MB|GB|TB|PB)\b", r"\bvolume\b", r"\bsamples?\b"]),
        ("Related tools, software and code", [r"software", r"\bcode\b", r"pipeline", r"\btools?\b", r"workflow", r"container", r"github|gitlab|zenodo"]),
        ("Standards", [r"standards?", r"metadata", r"ontolog", r"controlled vocabular", r"\bformat", r"schema"]),
        ("Data preservation, access and timelines", [r"repositor", r"archiv", r"preserv", r"persistent identifier|\bdoi\b|accession", r"deposit", r"\b(years?|months?)\b|publication|end of the award"]),
        ("Access, distribution or reuse considerations", [r"consent", r"privacy", r"restrict", r"controlled[- ]access", r"licen[cs]e", r"embargo", r"de-?identif", r"reuse|re-use"]),
        ("Oversight of data management and sharing", [r"oversight", r"responsib", r"principal investigator|\bPI\b", r"data manager|data steward", r"monitor", r"complian"]),
    ],
    "fair": [
        ("Findable", [r"persistent identifier|\bdoi\b|accession", r"metadata", r"repositor|index|catalog"]),
        ("Accessible", [r"access", r"protocol|https?|open", r"authenticat|authori[sz]|controlled[- ]access", r"metadata.*(remain|persist|available)|(remain|persist|available).*metadata"]),
        ("Interoperable", [r"vocabular|ontolog", r"standard", r"format"]),
        ("Reusable", [r"licen[cs]e", r"provenance", r"community standard|standards?", r"documentation|readme"]),
    ],
}
# An element counts as covered when at least MIN of its patterns match. 'Data type' needs 2, the rest 2 as well,
# except short groups.
MIN_HITS = {"nih": 2, "fair": 2}
PLACEHOLDERS = re.compile(r"\b(TBD|TODO|to be determined|to be decided|\[insert|lorem ipsum|XXX)\b", re.I)
UPON_REQUEST = re.compile(r"upon request|on request|available from the authors|contact the (corresponding )?author", re.I)
VOLUME = re.compile(r"\b\d+(\.\d+)?\s?(KB|MB|GB|TB|PB)\b", re.I)
TIMELINE = re.compile(r"\b(\d+|one|two|three|five|ten)\s+(years?|months?)\b|at (the time of )?publication|end of the award|by (the )?publication", re.I)
REPOSITORY = re.compile(r"repositor|zenodo|figshare|dryad|\bgeo\b|\bsra\b|\bena\b|dbgap|ega\b|arrayexpress|pride|genbank", re.I)


def check(text, profile="nih"):
    """Return (elements, warnings). elements is a list of (name, status, hits) with status 'covered' or 'missing'."""
    if profile not in PROFILES:
        raise ValueError("profile must be nih or fair")
    body = text
    elements = []
    for name, patterns in PROFILES[profile]:
        hits = [p for p in patterns if re.search(p, body, re.I)]
        elements.append((name, "covered" if len(hits) >= MIN_HITS[profile] else "missing", len(hits)))
    warnings = []
    if PLACEHOLDERS.search(body):
        warnings.append("placeholder text remains (TBD, TODO or similar)")
    if UPON_REQUEST.search(body) and not REPOSITORY.search(body):
        warnings.append("access is offered upon request and no repository is named")
    if profile == "nih":
        if not VOLUME.search(body):
            warnings.append("no data volume is given (for example 2 TB)")
        if not TIMELINE.search(body):
            warnings.append("no timeline is given for sharing or retention")
        if re.search(r"https?://", body):
            warnings.append("the plan contains a web address; university guides report that NIH discourages links in the plan: VERIFY")
    words = len(re.findall(r"\w+", body))
    if words < 150:
        warnings.append("only %d words; a real plan is usually longer" % words)
    return elements, warnings


GOOD = """# Data management and sharing plan
Data type: raw FASTQ files from 120 RNA-seq samples (about 2 TB), processed count matrices and sample metadata.
Software: the pipeline (Snakemake workflow, container image, version-tagged on GitHub and archived on Zenodo) will be released with the data.
Standards: metadata follow the MINSEQE recommendations with controlled vocabulary terms; formats are FASTQ and TSV.
Preservation and access: raw reads will be deposited in SRA and processed data in GEO at the time of publication and kept for at least ten years; each deposit receives an accession.
Reuse: participants consented to data sharing under controlled access; data are de-identified; a license permits reuse after a 12 month embargo.
Oversight: the principal investigator and a named data manager monitor compliance each quarter and are responsible for deposit.
""" + " Additional detail on methods and quality control follows. " * 12

THIN = "We will share the data upon request. TBD."


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    els, warns = check(GOOD)
    eq("good plan covers all six", [s for _n, s, _h in els], ["covered"] * 6)
    eq("good plan has no warnings", warns, [])
    els, warns = check(THIN)
    eq("thin plan misses everything", [s for _n, s, _h in els], ["missing"] * 6)
    eq("thin plan flags upon request", any("upon request" in w for w in warns), True)
    eq("thin plan flags placeholder", any("placeholder" in w for w in warns), True)
    eq("thin plan flags volume", any("volume" in w for w in warns), True)
    eq("thin plan flags timeline", any("timeline" in w for w in warns), True)
    eq("thin plan flags length", any("only" in w and "words" in w for w in warns), True)
    status = dict((n, s) for n, s, _h in check("The data will be kept for ten years. " + "filler " * 60)[0])
    eq("a single keyword signal is not enough", status["Data preservation, access and timelines"], "missing")
    eq("a 100-word plan is flagged as short", any("only 100 words" in w for w in check("word " * 100)[1]), True)
    eq("a 200-word plan is not", any("words" in w and "only" in w for w in check("word " * 200)[1]), False)
    no_oversight = GOOD.replace("Oversight: the principal investigator and a named data manager monitor compliance each quarter and are responsible for deposit.", "")
    els, _w = check(no_oversight)
    eq("missing oversight detected", [n for n, s, _h in els if s == "missing"], ["Oversight of data management and sharing"])
    no_reuse = GOOD.replace("Reuse: participants consented to data sharing under controlled access; data are de-identified; a license permits reuse after a 12 month embargo.", "")
    eq("missing reuse detected", [n for n, s, _h in check(no_reuse)[0] if s == "missing"], ["Access, distribution or reuse considerations"])
    eq("upon request with a repository is not flagged", any("upon request" in w for w in check(GOOD + " Further files are available upon request. ")[1]), False)
    eq("link warning", any("web address" in w for w in check(GOOD + " See https://example.org/plan ")[1]), True)
    els, warns = check(GOOD, "fair")
    eq("good plan on the FAIR profile", [s for _n, s, _h in els], ["covered"] * 4)
    eq("FAIR profile has no volume warning", any("volume" in w for w in warns), False)
    eq("FAIR on thin plan", [s for _n, s, _h in check(THIN, "fair")[0]], ["missing"] * 4)
    count[0] += 1
    try:
        check(GOOD, "other")
        fails.append("unknown profile should raise")
    except ValueError:
        pass
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("dmpcheck selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Check a data management plan for missing elements.")
    ap.add_argument("plan", nargs="?")
    ap.add_argument("--profile", choices=sorted(PROFILES), default="nih")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.plan:
        ap.error("give a plan file or --selftest")
    with open(a.plan, encoding="utf-8") as fh:
        text = fh.read()
    elements, warnings = check(text, a.profile)
    for name, status, hits in elements:
        print("%-45s %-8s (%d signal%s)" % (name, status.upper(), hits, "" if hits == 1 else "s"))
    for w in warnings:
        print("WARNING: " + w)
    missing = sum(1 for _n, s, _h in elements if s == "missing")
    print("%d of %d elements covered by keywords. This does not judge quality." % (len(elements) - missing, len(elements)))
    return 1 if missing or warnings else 0


if __name__ == "__main__":
    sys.exit(main())
