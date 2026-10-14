#!/usr/bin/env python3
"""Look up Gardiner sign codes, Unicode characters and simple MdC code strings.

Standard library only. The Gardiner code <-> Unicode mapping comes from the Unicode
character names (EGYPTIAN HIEROGLYPH A001 ...), not from any book. The reading table
(references/common-signs.json) is a small curated set with a status on every row.

Usage:
  python3 scripts/signs.py D21                  # code -> glyph, Unicode, category, readings
  python3 scripts/signs.py --char 𓂋            # glyph -> code and readings
  python3 scripts/signs.py --mdc "G17-D21:N35"  # code string -> glyphs (with joiners)
  python3 scripts/signs.py --section D          # list the codes of a section that Unicode defines
  python3 scripts/signs.py --value nfr          # signs whose curated reading is nfr
  python3 scripts/signs.py --json D21           # machine-readable output
  python3 scripts/signs.py --selftest
"""
import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "references", "common-signs.json")

# Section headings of Gardiner's sign-list. There is no section J.
SECTIONS = {
    "A": "Man and his occupations", "B": "Woman and her occupations",
    "C": "Anthropomorphic deities", "D": "Parts of the human body", "E": "Mammals",
    "F": "Parts of mammals", "G": "Birds", "H": "Parts of birds",
    "I": "Amphibious animals, reptiles, etc.", "K": "Fishes and parts of fishes",
    "L": "Invertebrata and lesser animals", "M": "Trees and plants",
    "N": "Sky, earth, water", "O": "Buildings, parts of buildings, etc.",
    "P": "Ships and parts of ships", "Q": "Domestic and funerary furniture",
    "R": "Temple furniture and sacred emblems", "S": "Crowns, dress, staves, etc.",
    "T": "Warfare, hunting, butchery", "U": "Agriculture, crafts and professions",
    "V": "Rope, fibre, baskets, bags, etc.", "W": "Vessels of stone and earthenware",
    "X": "Loaves and cakes", "Y": "Writings, games, music",
    "Z": "Strokes, signs derived from hieratic, geometrical figures", "Aa": "Unclassified",
}
# Highest number printed in the sign-list index, and numbers that are absent.
GARDINER_MAX = {"A": 59, "B": 7, "C": 20, "D": 63, "E": 34, "F": 52, "G": 54, "H": 8,
                "I": 15, "K": 7, "L": 7, "M": 44, "N": 42, "O": 51, "P": 11, "Q": 7,
                "R": 25, "S": 45, "T": 35, "U": 41, "V": 39, "W": 25, "X": 8, "Y": 8,
                "Z": 11, "Aa": 32}
GARDINER_GAPS = {"A": set(range(56, 59)), "C": set(range(13, 17))}

VERTICAL_JOINER = "\U00013430"    # EGYPTIAN HIEROGLYPH VERTICAL JOINER (Unicode 15)
HORIZONTAL_JOINER = "\U00013431"  # EGYPTIAN HIEROGLYPH HORIZONTAL JOINER (Unicode 15)

CODE_RE = re.compile(r"^(Aa|AA|[A-IK-Za-ik-z])\s*0*(\d{1,3})([A-Za-z]?)(\*{0,2})$")


def normalize(code):
    """'d21', 'D 21', 'aa1', 'A14*' -> ('D', 21, '', '') style tuple, or None."""
    m = CODE_RE.match(code.strip())
    if not m:
        return None
    sec, num, suffix, stars = m.groups()
    sec = "Aa" if sec.lower() == "aa" else sec.upper()
    return sec, int(num), suffix.upper(), stars


def code_label(t):
    return "%s%d%s%s" % (t[0], t[1], t[2], t[3])


def unicode_name(t):
    sec, num, suffix, _ = t
    return "EGYPTIAN HIEROGLYPH %s%03d%s" % ("AA" if sec == "Aa" else sec, num, suffix)


def to_char(t):
    try:
        return unicodedata.lookup(unicode_name(t))
    except KeyError:
        return None


def char_to_code(ch):
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return None
    m = re.match(r"^EGYPTIAN HIEROGLYPH (AA|[A-Z])(\d{3})([A-Z]?)$", name)
    if not m:
        return None
    sec, num, suffix = m.groups()
    return ("Aa" if sec == "AA" else sec, int(num), suffix, "")


def in_gardiner_list(t):
    sec, num, suffix, stars = t
    if sec not in GARDINER_MAX:
        return False
    return 1 <= num <= GARDINER_MAX[sec] and num not in GARDINER_GAPS.get(sec, set())


def load_readings():
    with open(DATA, encoding="utf-8") as f:
        rows = json.load(f)["signs"]
    by = {}
    for r in rows:
        by.setdefault(r["code"], []).append(r)
    return by


def lookup(code):
    t = normalize(code)
    if t is None:
        return {"input": code, "error": "not a Gardiner sign code (expected e.g. D21, G 43, Aa1)"}
    out = {"input": code, "code": code_label(t), "section": SECTIONS.get(t[0]),
           "in_gardiner_list": in_gardiner_list(t)}
    base = (t[0], t[1], t[2], "")
    ch = to_char(base)
    out["char"] = ch
    out["unicode"] = ("U+%04X" % ord(ch)) if ch else None
    out["unicode_name"] = unicode_name(base)
    notes = []
    if t[3]:
        notes.append("Starred signs (%s) are Gardiner's variant forms. Unicode has no automatic "
                     "equivalent here; the character shown is the unstarred sign. Check the Unicode "
                     "chart for variants." % code_label(t))
    if t[2]:
        notes.append("A letter suffix is a Unicode variant and may not match Gardiner's own variant.")
    if ch is None:
        notes.append("This Python's Unicode data does not define the character (or the code is not in the block).")
    if not out["in_gardiner_list"]:
        notes.append("Not in the printed Gardiner list index; it may come from the extended Unicode set.")
    out["readings"] = load_readings().get("%s%d" % (t[0], t[1]), []) if not t[2] else []
    if not out["readings"]:
        notes.append("No curated reading. Do not guess one: look it up in a sign list and mark it VERIFY.")
    out["notes"] = notes
    return out


def section_codes(sec):
    sec = "Aa" if sec.lower() == "aa" else sec.upper()
    codes = []
    for n in range(1, 1000):
        for suffix in [""] + [chr(c) for c in range(65, 91)]:
            t = (sec, n, suffix, "")
            if to_char(t):
                codes.append(code_label(t))
    return codes


def parse_mdc(s):
    """Parse a restricted MdC subset: signs joined by - : * and ! . Returns (groups, problems)."""
    groups, problems = [], []
    for token in re.split(r"-+", s.strip()):
        if token in ("", "!"):
            continue
        token = token.rstrip("!")
        parts = re.split(r"([:*])", token)
        group = []
        for i, p in enumerate(parts):
            if i % 2 == 1:
                group.append(("op", p))
                continue
            t = normalize(p)
            if t is None or to_char((t[0], t[1], t[2], "")) is None:
                problems.append("unsupported token %r" % p)
                group.append(("bad", p))
            else:
                group.append(("sign", code_label(t)))
        groups.append(group)
    return groups, problems


def mdc_to_text(s):
    groups, problems = parse_mdc(s)
    text, shown = [], []
    for g in groups:
        chars = ""
        for kind, v in g:
            if kind == "sign":
                t = normalize(v)
                chars += to_char((t[0], t[1], t[2], ""))
            elif kind == "op":
                chars += VERTICAL_JOINER if v == ":" else HORIZONTAL_JOINER
            else:
                chars += "?"
        text.append(chars)
    return " ".join(text), problems


def selftest():
    ok = 0

    def check(cond, msg):
        nonlocal ok
        if not cond:
            print("FAIL:", msg)
            sys.exit(1)
        ok += 1

    check(normalize("d 21") == ("D", 21, "", ""), "normalize d 21")
    check(normalize("Aa1") == ("Aa", 1, "", ""), "normalize Aa1")
    check(normalize("J1") is None, "no section J")
    check(unicode_name(("Aa", 1, "", "")) == "EGYPTIAN HIEROGLYPH AA001", "Aa name")
    check(to_char(("D", 21, "", "")) == "\U0001308b", "D21 is U+1308B")
    check(to_char(("G", 43, "", "")) == "\U00013171", "G43")
    check(char_to_code("\U0001308b") == ("D", 21, "", ""), "reverse D21")
    check(in_gardiner_list(("A", 59, "", "")) and not in_gardiner_list(("A", 57, "", "")), "A gaps")
    check(not in_gardiner_list(("C", 14, "", "")), "C13-16 gap")
    r = lookup("G17")
    check(r["readings"] and r["readings"][0]["value"] == "m", "G17 reads m")
    check(lookup("D21")["readings"][0]["value"] == "r", "D21 reads r")
    check("error" in lookup("zz"), "bad code")
    rows = load_readings()
    check(all(to_char(normalize(c)) for c in rows), "every curated code has a Unicode character")
    check(all(r["status"] for rs in rows.values() for r in rs), "every row has a status")
    text, problems = mdc_to_text("G17-D21:N35")
    check(not problems and VERTICAL_JOINER in text, "mdc stack")
    _, problems = mdc_to_text("G17-bogus")
    check(problems, "mdc flags bad token")
    print("signs.py self-test: %d checks passed (Unicode %s)" % (ok, unicodedata.unidata_version))


def render(r):
    if "error" in r:
        return r["error"]
    lines = ["%s  %s  %s" % (r["code"], r["char"] or "(no glyph)", r["unicode"] or ""),
             "section: %s%s" % (r["section"], "" if r["in_gardiner_list"] else "  [not in printed list]")]
    for x in r["readings"]:
        v = x["value"] if x["value"] else "(no phonetic value)"
        lines.append("  %-13s %-10s %s  [%s p. %s] %s" % (x["role"], v, x["label"], "Gardiner", x["gardiner_page"], x["note"]))
    for n in r["notes"]:
        lines.append("  note: " + n)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Gardiner sign lookup")
    ap.add_argument("code", nargs="?")
    ap.add_argument("--char")
    ap.add_argument("--mdc")
    ap.add_argument("--section")
    ap.add_argument("--value")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.mdc:
        text, problems = mdc_to_text(a.mdc)
        print(json.dumps({"text": text, "problems": problems}, ensure_ascii=False) if a.json else
              text + ("\nproblems: " + "; ".join(problems) if problems else ""))
        return
    if a.section:
        codes = section_codes(a.section)
        print(json.dumps(codes) if a.json else " ".join(codes))
        return
    if a.value:
        want = a.value.strip()
        hits = [r for rs in load_readings().values() for r in rs if r["value"] == want]
        for r in hits:
            res = lookup(r["code"])
            print(json.dumps(res, ensure_ascii=False) if a.json else render(res))
        if not hits:
            print("no curated sign reads %r (the table is small; absence is not evidence)" % want)
        return
    if a.char:
        t = char_to_code(a.char[0])
        if not t:
            print("not an Egyptian hieroglyph character")
            sys.exit(1)
        a.code = code_label(t)
    if not a.code:
        ap.print_help()
        return
    res = lookup(a.code)
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else render(res))


if __name__ == "__main__":
    main()
