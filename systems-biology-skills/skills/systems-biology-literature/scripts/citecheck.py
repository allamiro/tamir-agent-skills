#!/usr/bin/env python3
"""Check a reference list for citations that cannot be what they claim (standard library only).

  citecheck.py REFS.txt                 offline: DOI syntax, implausible years, duplicates, entries with no DOI
  citecheck.py REFS.txt --online        also resolve each DOI on Crossref and compare title, year and first author
  citecheck.py REFS.txt --online --search   also search Crossref for entries that have no DOI
  citecheck.py --selftest

REFS.txt holds one reference per line. Blank lines and lines starting with # are ignored.

What a pass means: the DOI resolves to a record whose title words, year and first-author surname
match the line. It does NOT show that the paper says what you cite it for, and a "not found" for a
book, thesis, report or talk is expected, because Crossref indexes mostly journal articles,
proceedings and some books. A DOI that does not exist at all is the strongest sign of an invented
reference. Crossref is queried only with --online or --search; nothing is sent otherwise.
"""
import argparse
import datetime
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>]+")
YEAR_RE = re.compile(r"(?<![\d/.])(1[5-9]\d\d|20\d\d)(?![\d])")
STOP = set("a an the of and or for in on to with from by at as is are its their this that into".split())


def fold(text):
    """Lower-case, strip accents, keep letters and digits as words."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", text.lower())


def clean_doi(raw):
    doi = raw.rstrip(".,;:'\"]>")
    while doi.endswith(")") and doi.count("(") < doi.count(")"):
        doi = doi[:-1].rstrip(".,;:")
    return doi


def extract(line):
    """Return (doi or None, [candidate years], line without DOI or URL)."""
    m = DOI_RE.search(line)
    doi = clean_doi(m.group(0)) if m else None
    rest = DOI_RE.sub(" ", line)
    rest = re.sub(r"https?://\S+", " ", rest)
    paren = [int(y) for y in re.findall(r"\((1[5-9]\d\d|20\d\d)[a-z]?\)", rest)]
    years = paren or [int(y) for y in YEAR_RE.findall(rest)]
    return doi, years, rest


def containment(title, line):
    """Share of the title's content words that appear in the line (1.0 = all of them)."""
    words = [w for w in fold(title) if w not in STOP]
    if not words:
        return 0.0
    have = set(fold(line))
    return sum(1 for w in words if w in have) / len(words)


def crossref_get(url, mailto=None):
    agent = "citecheck (skills repo)" + (" (mailto:%s)" % mailto if mailto else "")
    req = urllib.request.Request(url, headers={"User-Agent": agent})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_doi(doi, mailto=None):
    """Crossref record for a DOI, None if Crossref has no such DOI, raises on network trouble."""
    try:
        return crossref_get("https://api.crossref.org/works/" + urllib.parse.quote(doi), mailto)["message"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def search_text(text, mailto=None):
    params = urllib.parse.urlencode({"query.bibliographic": text[:300], "rows": 1})
    items = crossref_get("https://api.crossref.org/works?" + params, mailto)["message"]["items"]
    return items[0] if items else None


def record_year(rec):
    for key in ("issued", "published-print", "published-online", "created"):
        parts = (rec.get(key) or {}).get("date-parts") or [[None]]
        if parts[0] and parts[0][0]:
            return int(parts[0][0])
    return None


def compare(line, years, rec):
    """List of problems between a line and a Crossref record (empty list = consistent)."""
    problems = []
    title = " ".join(rec.get("title") or [""])
    share = containment(title, line)
    if share < 0.8:
        problems.append("title words %d%% present (record: %r)" % (round(100 * share), title[:70]))
    ry = record_year(rec)
    if years and ry and ry not in years:
        near = any(abs(ry - y) == 1 for y in years)
        problems.append("year %s vs record %s%s" % ("/".join(map(str, years)), ry, " (off by one, may be online-first)" if near else ""))
    authors = rec.get("author") or []
    if authors:
        family = fold(authors[0].get("family") or authors[0].get("name") or "")
        if family and not all(w in set(fold(line)) for w in family):
            problems.append("first author %r not in the line" % " ".join(family))
    return problems


def check_lines(lines, fetch=None, search=None, today=None):
    """Return [(line, status, detail)]. fetch/search are None for an offline run."""
    today = today or datetime.date.today()
    results, seen = [], {}
    for line in lines:
        doi, years, rest = extract(line)
        key = doi.lower() if doi else " ".join(fold(rest))
        if key in seen:
            results.append((line, "DUPLICATE", "same as entry %d" % seen[key]))
            continue
        seen[key] = len(results) + 1
        notes = []
        for y in years:
            if y > today.year + 1:
                notes.append("year %d is in the future" % y)
        if doi is None:
            if "10." in line and "/" in line:
                results.append((line, "BAD-DOI", "looks like a DOI but does not match 10.NNNN/suffix"))
            elif search:
                try:
                    rec = search(rest)
                except (urllib.error.URLError, OSError, ValueError) as e:
                    results.append((line, "ERROR", "network: %s" % e))
                    continue
                if rec and containment(" ".join(rec.get("title") or [""]), line) >= 0.8:
                    problems = compare(line, years, rec)
                    results.append((line, "FOUND" if not problems else "CHECK",
                                    "Crossref has doi %s%s" % (rec["DOI"], "; " + "; ".join(problems) if problems else "")))
                else:
                    results.append((line, "NOT-FOUND", "no close Crossref match; normal for books, theses, reports and talks"))
            else:
                results.append((line, "NO-DOI", "cannot be checked offline; verify against the publisher or library"))
            if notes:
                results[-1] = (results[-1][0], results[-1][1], results[-1][2] + "; " + "; ".join(notes))
            continue
        if fetch is None:
            results.append((line, "DOI-SYNTAX-OK", ("; ".join(notes) + "; " if notes else "") + "not resolved (run with --online)"))
            continue
        try:
            rec = fetch(doi)
        except (urllib.error.URLError, OSError, ValueError) as e:
            results.append((line, "ERROR", "network: %s" % e))
            continue
        if rec is None:
            results.append((line, "DOI-NOT-FOUND", "Crossref has no record of %s; a typo or an invented reference" % doi))
            continue
        problems = compare(line, years, rec) + notes
        results.append((line, "MISMATCH" if problems else "OK", "; ".join(problems) if problems else "title, year and first author agree"))
    return results


BAD = {"DOI-NOT-FOUND", "MISMATCH", "BAD-DOI", "CHECK"}


def selftest():
    fails, count = [], [0]

    def check(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    # DOI extraction and cleaning
    check("doi plain", extract("Lamport L. (1978) Time, clocks. CACM 21(7). doi:10.1145/359545.359563.")[0], "10.1145/359545.359563")
    check("doi url", extract("https://doi.org/10.1371/journal.pcbi.1003285")[0], "10.1371/journal.pcbi.1003285")
    check("doi parens kept", extract("see 10.1016/0041-1647(71)90040-2.")[0], "10.1016/0041-1647(71)90040-2")
    check("doi wrapped", extract("(doi 10.1000/abc123)")[0], "10.1000/abc123")
    check("doi with balanced parentheses kept", extract("see (10.1000/a(b))")[0], "10.1000/a(b)")
    check("doi digits are not read as a year", extract("Smith. Title. J 5, 2020. 10.1000/abc-1999-x")[1], [2020])
    check("no doi", extract("Gardiner A. Egyptian Grammar, 3rd ed., 1957")[0], None)
    # years: parenthesised year wins over page numbers
    check("year paren", extract("Smith A. (2019) Title. J 12:1234-1250")[1], [2019])
    check("year bare", extract("Smith A. Title. J 12, 2019.")[1], [2019])
    check("year none", extract("no year here")[1], [])
    # folding and containment
    check("fold accents", fold("Wörterbuch Ägyptischen"), ["worterbuch", "agyptischen"])
    check("containment all", containment("Time, clocks, and the ordering of events", "Lamport. Time clocks and the ordering of events in a distributed system"), 1.0)
    check("containment half", containment("Alpha beta gamma delta", "alpha beta"), 0.5)
    check("containment stop-only", containment("the of and", "the of and"), 0.0)

    rec = {"title": ["Time, clocks, and the ordering of events in a distributed system"], "DOI": "10.1145/359545.359563",
           "issued": {"date-parts": [[1978, 7]]}, "author": [{"family": "Lamport", "given": "Leslie"}]}
    good = "Lamport, L. (1978). Time, clocks, and the ordering of events in a distributed system. CACM 21(7), 558-565. 10.1145/359545.359563"
    wrong_year = good.replace("1978", "1982")
    wrong_title = "Lamport, L. (1978). Paxos made simple. CACM 21(7). 10.1145/359545.359563"
    wrong_author = good.replace("Lamport", "Fischer")
    off_one = good.replace("(1978)", "(1979)")
    db = {"10.1145/359545.359563": rec}
    fetch = lambda d: db.get(d)
    one = lambda line: check_lines([line], fetch=fetch)[0]   # one line at a time: they share a DOI
    check("online ok", one(good)[1], "OK")
    check("online wrong year", one(wrong_year)[1], "MISMATCH")
    check("online wrong title", one(wrong_title)[1], "MISMATCH")
    check("online wrong author", one(wrong_author)[1], "MISMATCH")
    check("online off by one flagged", "off by one" in one(off_one)[2], True)
    gone = check_lines(["Nobody N. (2020) Invented result. 10.9999/fake.0001"], fetch=fetch)
    check("doi not found", gone[0][1], "DOI-NOT-FOUND")
    check("duplicates", [r[1] for r in check_lines([good, good], fetch=fetch)], ["OK", "DUPLICATE"])
    check("duplicate by text", [r[1] for r in check_lines(["Gardiner A. Egyptian Grammar 1957", "gardiner a. egyptian grammar, 1957."])], ["NO-DOI", "DUPLICATE"])
    check("offline syntax only", check_lines([good])[0][1], "DOI-SYNTAX-OK")
    check("bad doi", check_lines(["Foo. 2020. 10.12/short"])[0][1], "BAD-DOI")
    check("future year", "future" in check_lines(["Foo B. (2099) Title. J."], today=datetime.date(2026, 10, 14))[0][2], True)
    # search path
    srch = lambda text: rec
    found = check_lines(["Lamport L. 1978. Time, clocks, and the ordering of events in a distributed system. CACM."], search=srch)
    check("search found", found[0][1], "FOUND")
    miss = check_lines(["Gardiner A. Egyptian Grammar. Oxford: Griffith Institute, 1957."], search=srch)
    check("search not found", miss[0][1], "NOT-FOUND")

    def boom(_):
        raise urllib.error.URLError("no network")
    check("network error reported", check_lines([good], fetch=boom)[0][1], "ERROR")
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("citecheck selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Check a reference list for citations that cannot be what they claim.")
    ap.add_argument("refs", nargs="?", help="text file, one reference per line")
    ap.add_argument("--online", action="store_true", help="resolve DOIs on Crossref")
    ap.add_argument("--search", action="store_true", help="search Crossref for entries without a DOI")
    ap.add_argument("--mailto", help="contact address sent in the User-Agent, as Crossref asks for polite use")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.refs:
        ap.error("give a references file or --selftest")
    with open(a.refs, encoding="utf-8") as fh:
        lines = [ln.strip() for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]
    fetch = (lambda d: fetch_doi(d, a.mailto)) if a.online else None
    search = (lambda t: search_text(t, a.mailto)) if a.search else None
    results = check_lines(lines, fetch=fetch, search=search)
    for i, (line, status, detail) in enumerate(results, 1):
        print("%2d  %-14s %s" % (i, status, line[:90] + ("..." if len(line) > 90 else "")))
        print("    %s" % detail)
    counts = {}
    for _l, s, _d in results:
        counts[s] = counts.get(s, 0) + 1
    print("\n%d entries: %s" % (len(results), ", ".join("%d %s" % (n, s) for s, n in sorted(counts.items()))))
    return 1 if any(s in BAD for _l, s, _d in results) else 0


if __name__ == "__main__":
    sys.exit(main())
