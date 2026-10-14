#!/usr/bin/env python3
"""Check an object's ownership history for gaps and undocumented steps (standard library only).

  provrecord.py check RECORD.json [--gap-years 20]
  provrecord.py --selftest

RECORD.json:
  {"object": {"id": "...", "description": "..."},
   "benchmarks": {"UNESCO 1970 Convention": 1970, "AIA publication policy": 1973},   (optional)
   "events": [
     {"date": "1895", "kind": "excavation", "from": "", "to": "Excavator X", "place": "Egypt",
      "evidence": "document", "ref": "field register"},
     {"date": "1921-05", "kind": "sale", "from": "Excavator X", "to": "Dealer Y", "place": "Cairo",
      "evidence": "publication", "ref": "sale catalogue"}, ...]}

kind is free text (excavation, acquisition, sale, gift, bequest, export, loan, publication, ...).
evidence is one of: document, publication, label, oral, none. Dates are YYYY, YYYY-MM or YYYY-MM-DD,
optionally with a leading ~ or c. for "about".

This flags places a specialist must look. It is NOT a legal opinion, does not establish that an
object is lawful, genuine or looted, and cannot detect a forged document. A clean report means the
record is internally consistent, nothing more. The default benchmark years are the ones a
researcher is likely to meet; confirm what the relevant museum, journal or society requires today.
"""
import argparse
import json
import re
import sys

DEFAULT_BENCHMARKS = {"UNESCO 1970 Convention": 1970, "AIA publication policy (1973)": 1973}
DOCUMENTED = {"document", "publication", "label"}
DATE_RE = re.compile(r"^(?:~|c\.?\s*)?(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$")


def parse_date(text):
    """(year, month or None, day or None, approximate) or None if unreadable."""
    if text is None:
        return None
    t = str(text).strip()
    m = DATE_RE.match(t)
    if not m:
        return None
    approx = t.startswith("~") or t.lower().startswith("c")
    month = int(m.group(2)) if m.group(2) else None
    day = int(m.group(3)) if m.group(3) else None
    if month is not None and not 1 <= month <= 12:
        return None
    if day is not None and not 1 <= day <= 31:
        return None
    return int(m.group(1)), month, day, approx


def sort_key(d):
    return (d[0], d[1] or 0, d[2] or 0)


def check(record, gap_years=20):
    """Return (flags, notes): flags need a specialist, notes are context."""
    flags, notes = [], []
    events = record.get("events") or []
    if not events:
        return [("no-events", "the record has no events")], notes
    benchmarks = record.get("benchmarks") or DEFAULT_BENCHMARKS
    dated = []
    for i, ev in enumerate(events, 1):
        d = parse_date(ev.get("date"))
        ev_ev = ev.get("evidence", "none")
        if d is None:
            flags.append(("undated-event", "event %d (%s) has no usable date: %r" % (i, ev.get("kind", "?"), ev.get("date"))))
        else:
            dated.append((d, i, ev))
        if ev_ev not in DOCUMENTED:
            flags.append(("undocumented-event", "event %d (%s, %s) rests on %s, not a document, publication or label" % (
                i, ev.get("kind", "?"), ev.get("date", "undated"), "oral report" if ev_ev == "oral" else "no evidence")))
        if not ev.get("ref") and ev_ev in DOCUMENTED:
            flags.append(("missing-reference", "event %d claims %s evidence but gives no reference" % (i, ev_ev)))
    # order
    for (d1, i1, _e1), (d2, i2, _e2) in zip(dated, dated[1:]):
        if sort_key(d2) < sort_key(d1):
            flags.append(("out-of-order", "event %d (%s) is dated before event %d (%s)" % (i2, "-".join(map(str, [x for x in d2[:3] if x])), i1, "-".join(map(str, [x for x in d1[:3] if x])))))
    # chain continuity
    for i in range(len(events) - 1):
        to, nxt = (events[i].get("to") or "").strip(), (events[i + 1].get("from") or "").strip()
        if to and nxt and to.lower() != nxt.lower():
            flags.append(("broken-chain", "event %d ends with %r but event %d starts from %r" % (i + 1, to, i + 2, nxt)))
        if not nxt and i + 1 > 0 and events[i + 1].get("kind", "").lower() not in ("excavation", "discovery", "find"):
            flags.append(("unnamed-source", "event %d (%s) does not say who it came from" % (i + 2, events[i + 1].get("kind", "?"))))
    # gaps
    ordered = sorted(dated, key=lambda t: sort_key(t[0]))
    for (d1, i1, _e1), (d2, i2, _e2) in zip(ordered, ordered[1:]):
        if d2[0] - d1[0] > gap_years:
            flags.append(("gap", "%d years between event %d (%d) and event %d (%d)" % (d2[0] - d1[0], i1, d1[0], i2, d2[0])))
    # find spot
    first = events[0]
    if first.get("kind", "").lower() not in ("excavation", "discovery", "find"):
        flags.append(("no-findspot", "the first recorded event is %r, not an excavation or find; the findspot is unknown" % first.get("kind", "?")))
    # benchmarks: is there documentation from before each year?
    documented_years = sorted(d[0] for d, _i, ev in dated if ev.get("evidence") in DOCUMENTED)
    earliest = documented_years[0] if documented_years else None
    for name, year in sorted(benchmarks.items(), key=lambda kv: kv[1]):
        if earliest is None:
            flags.append(("no-documentation", "no documented event at all, so nothing shows the object was documented before %d (%s)" % (year, name)))
        elif earliest > year:
            flags.append(("after-benchmark", "the earliest documented event is %d, after %d (%s)" % (earliest, year, name)))
        else:
            notes.append("documented in %d, before %d (%s); this does not show the object left its country lawfully" % (earliest, year, name))
    return flags, notes


def selftest():
    fails, count = [], [0]

    def eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    def kinds(rec, **kw):
        return sorted(k for k, _m in check(rec, **kw)[0])

    eq("date year", parse_date("1895"), (1895, None, None, False))
    eq("date month", parse_date("1921-05"), (1921, 5, None, False))
    eq("date day", parse_date("1921-05-17"), (1921, 5, 17, False))
    eq("date approx tilde", parse_date("~1900"), (1900, None, None, True))
    eq("date approx c.", parse_date("c. 1900"), (1900, None, None, True))
    eq("date bad month", parse_date("1921-13"), None)
    eq("date text", parse_date("early 1900s"), None)
    eq("date none", parse_date(None), None)

    good = {"events": [
        {"date": "1895", "kind": "excavation", "from": "", "to": "X", "evidence": "document", "ref": "field register"},
        {"date": "1900", "kind": "sale", "from": "X", "to": "Museum M", "evidence": "publication", "ref": "catalogue"}]}
    eq("clean record has no flags", check(good)[0], [])
    eq("clean record notes both benchmarks", len(check(good)[1]), 2)
    eq("empty record", kinds({"events": []}), ["no-events"])

    late = {"events": [
        {"date": "1980", "kind": "purchase", "from": "Dealer", "to": "Collector", "evidence": "document", "ref": "invoice"}]}
    eq("late and no findspot", kinds(late), ["after-benchmark", "after-benchmark", "no-findspot"])
    msgs = [m for k, m in check(late)[0] if k == "after-benchmark"]
    eq("benchmark names reported", sorted(("UNESCO" in m, "AIA" in m) for m in msgs), [(False, True), (True, False)])
    between = {"events": [{"date": "1972", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": "r"}]}
    eq("between benchmarks", sorted(m.split("after ")[-1][:4] for k, m in check(between)[0] if k == "after-benchmark"), ["1970"])
    eq("exactly at benchmark year is not after", kinds({"events": [{"date": "1970", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": "r"}]}), [])

    oral = {"events": [
        {"date": "1900", "kind": "excavation", "from": "", "to": "A", "evidence": "oral", "ref": ""},
        {"date": "1905", "kind": "gift", "from": "A", "to": "B", "evidence": "none", "ref": ""}]}
    eq("oral and none", kinds(oral), ["no-documentation", "no-documentation", "undocumented-event", "undocumented-event"])
    noref = {"events": [{"date": "1900", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": ""}]}
    eq("missing reference", kinds(noref), ["missing-reference"])
    broken = {"events": [
        {"date": "1900", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": "r"},
        {"date": "1910", "kind": "sale", "from": "Z", "to": "B", "evidence": "document", "ref": "r"}]}
    eq("broken chain", kinds(broken), ["broken-chain"])
    eq("chain match is case-insensitive", kinds({"events": [
        {"date": "1900", "kind": "excavation", "from": "", "to": "Smith", "evidence": "document", "ref": "r"},
        {"date": "1910", "kind": "sale", "from": "SMITH", "to": "B", "evidence": "document", "ref": "r"}]}), [])
    unnamed = {"events": [
        {"date": "1900", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": "r"},
        {"date": "1910", "kind": "sale", "from": "", "to": "B", "evidence": "document", "ref": "r"}]}
    eq("unnamed source", kinds(unnamed), ["unnamed-source"])
    gap = {"events": [
        {"date": "1900", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": "r"},
        {"date": "1950", "kind": "sale", "from": "A", "to": "B", "evidence": "document", "ref": "r"}]}
    eq("gap flagged", kinds(gap), ["gap"])
    eq("gap threshold", kinds(gap, gap_years=60), [])
    twenty = {"events": [{"date": "1900", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": "r"},
                         {"date": "1920", "kind": "sale", "from": "A", "to": "B", "evidence": "document", "ref": "r"}]}
    eq("a gap equal to the threshold is not flagged", kinds(twenty), [])
    eq("one year over the threshold is", kinds(twenty, gap_years=19), ["gap"])
    eq("gap message", check(gap)[0][0][1].startswith("50 years between event 1 (1900) and event 2 (1950)"), True)
    order = {"events": [
        {"date": "1950", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": "r"},
        {"date": "1900", "kind": "sale", "from": "A", "to": "B", "evidence": "document", "ref": "r"}]}
    eq("out of order", "out-of-order" in kinds(order), True)
    undated = {"events": [
        {"date": "sometime", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": "r"}]}
    eq("undated", kinds(undated), ["no-documentation", "no-documentation", "undated-event"])
    custom = {"benchmarks": {"My museum rule": 1990}, "events": [
        {"date": "1985", "kind": "excavation", "from": "", "to": "A", "evidence": "document", "ref": "r"}]}
    eq("custom benchmark", check(custom)[0], [])
    eq("custom benchmark note", "My museum rule" in check(custom)[1][0], True)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("provrecord selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Check an object's ownership history for gaps and undocumented steps.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("check")
    c.add_argument("record")
    c.add_argument("--gap-years", type=int, default=20)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd != "check":
        ap.error("give check or --selftest")
    with open(a.record, encoding="utf-8") as fh:
        record = json.load(fh)
    flags, notes = check(record, a.gap_years)
    obj = (record.get("object") or {}).get("id", "(unnamed object)")
    print("Object: %s" % obj)
    for kind, msg in flags:
        print("FLAG  %-18s %s" % (kind, msg))
    for n in notes:
        print("note  %s" % n)
    print("%d flag(s) for specialist review. This is not a legal or authenticity opinion." % len(flags))
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
