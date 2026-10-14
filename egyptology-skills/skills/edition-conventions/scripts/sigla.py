#!/usr/bin/env python3
"""Check the editorial brackets in a draft edition and list the key it needs (standard library only).

  sigla.py check FILE [--per-line]    brackets balanced, properly nested, not empty
  sigla.py key FILE                   the sigla that occur, how often, and what each usually marks
  sigla.py --selftest

What the sigla mean is NOT fixed. The table here is the classical Leiden system (agreed at Leiden in
1931 for Greek and Latin texts) plus common Egyptological half brackets and round brackets. Egyptological
publications differ from each other, so the meanings printed by `key` are a draft to be checked
against the key of the publication you follow, never a statement of what a given edition means.

This program checks mechanics only. It cannot tell whether a restoration is right, whether a
parallel supports it, or whether the text is Egyptian.
"""
import argparse
import sys

# opener -> (closer, kind, usual meaning)
PAIRS = {
    "[": ("]", "square", "lost or illegible text; letters inside are the editor's restoration, dots or ... mark an unrestored gap"),
    "⟦": ("⟧", "erasure", "text erased in antiquity (written [[ ]] in plain text)"),
    "⟨": ("⟩", "angle", "omitted by the scribe, supplied by the editor"),
    "〈": ("〉", "angle", "omitted by the scribe, supplied by the editor"),
    "{": ("}", "curly", "superfluous or wrongly written text that the editor removes"),
    "(": (")", "round", "an expansion, or words added for sense in a translation (varies)"),
    "⸢": ("⸣", "half", "partly damaged but legible, or restored with confidence (varies)"),
    "⌈": ("⌉", "half", "as the half brackets above, in another glyph style (varies)"),
}
CLOSERS = {v[0]: k for k, v in PAIRS.items()}
ERASE = "[["
ERASE_END = "]]"


def tokens(text, double_bracket_erasure=True):
    """Yield (kind, symbol, line, col, pos) for each bracket; kind is 'open', 'close' or 'gap', pos is the index in text."""
    line, col, i, n = 1, 0, 0, len(text)
    while i < n:
        ch = text[i]
        col += 1
        if ch == "\n":
            line, col = line + 1, 0
            i += 1
            continue
        if double_bracket_erasure and text.startswith(ERASE, i):
            yield ("open", ERASE, line, col, i)
            i += 2
            col += 1
            continue
        if double_bracket_erasure and text.startswith(ERASE_END, i):
            yield ("close", ERASE_END, line, col, i)
            i += 2
            col += 1
            continue
        if ch in PAIRS:
            yield ("open", ch, line, col, i)
        elif ch in CLOSERS:
            yield ("close", ch, line, col, i)
        elif text.startswith("...", i) or ch == "…":
            yield ("gap", "..." if ch == "." else ch, line, col, i)
            if ch == ".":
                i += 2
                col += 2
        i += 1


def _kind(sym):
    if sym in (ERASE, ERASE_END):
        return "erasure"
    if sym in PAIRS:
        return PAIRS[sym][1]
    return PAIRS[CLOSERS[sym]][1]


def _closer(sym):
    return ERASE_END if sym == ERASE else PAIRS[sym][0]


def check(text, per_line=False, double_bracket_erasure=True):
    """Return a list of (severity, line, col, message). severity is 'error' or 'warning'."""
    problems = []
    chunks = [(text, 0)]
    if per_line:
        chunks = [(ln, i) for i, ln in enumerate(text.split("\n"))]
    for chunk, offset in chunks:
        stack = []   # (symbol, line, col, index just after the opener)
        for kind, sym, line, col, pos in tokens(chunk, double_bracket_erasure):
            line += offset
            if kind == "gap":
                continue
            if kind == "open":
                if any(_kind(s) == _kind(sym) for s, _l, _c, _p in stack):
                    problems.append(("error", line, col, "%s opened inside another %s bracket" % (sym, _kind(sym))))
                stack.append((sym, line, col, pos + len(sym)))
                continue
            if not stack:
                problems.append(("error", line, col, "%s closes a bracket that was never opened" % sym))
                continue
            top, tl, tc, after = stack[-1]
            if _closer(top) == sym:
                stack.pop()
                if not chunk[after:pos].strip():
                    problems.append(("warning", tl, tc, "empty %s%s%s" % (top, sym, ": add the restored text or ..." if _kind(top) == "square" else "")))
            else:
                crossing = [i for i, (s, _l, _c, _p) in enumerate(stack) if _closer(s) == sym]
                if crossing:
                    j = crossing[-1]
                    problems.append(("error", line, col, "%s closes %s opened at %d:%d, but %s from %d:%d is still open (crossing)" % (
                        sym, stack[j][0], stack[j][1], stack[j][2], top, tl, tc)))
                    del stack[j:]
                else:
                    problems.append(("error", line, col, "%s does not match the open %s from %d:%d" % (sym, top, tl, tc)))
        for sym, line, col, _p in stack:
            problems.append(("error", line, col, "%s is never closed" % sym))
    used = {sym for kind, sym, _l, _c, _p in tokens(text, double_bracket_erasure) if kind == "open"}
    if "⸢" in used and "⌈" in used:
        problems.append(("warning", 0, 0, "two half-bracket styles are mixed; use one"))
    if "⟨" in used and "〈" in used:
        problems.append(("warning", 0, 0, "two angle-bracket styles are mixed; use one"))
    if ERASE in used and "⟦" in used:
        problems.append(("warning", 0, 0, "erasure is written both as [[ ]] and as the double-bracket glyphs; use one"))
    return sorted(problems, key=lambda p: (p[1], p[2]))


def key(text, double_bracket_erasure=True):
    """List of (symbol pair, count, meaning) for the sigla that occur."""
    counts = {}
    for kind, sym, _l, _c, _p in tokens(text, double_bracket_erasure):
        if kind == "open":
            counts[sym] = counts.get(sym, 0) + 1
        elif kind == "gap":
            counts["..."] = counts.get("...", 0) + 1
    out = []
    for sym, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        if sym == "...":
            out.append(("...", n, "a gap of unknown or approximate length (a dot per sign if the extent is known)"))
        elif sym == ERASE:
            out.append(("[[ ]]", n, "text erased in antiquity"))
        else:
            out.append(("%s %s" % (sym, PAIRS[sym][0]), n, PAIRS[sym][2]))
    return out


def selftest():
    fails, count = [], [0]

    def check_eq(name, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (name, got, want))

    def errs(text, **kw):
        return [p for p in check(text, **kw) if p[0] == "error"]

    def warns(text, **kw):
        return [p for p in check(text, **kw) if p[0] == "warning"]

    check_eq("clean", check("a [b c] d {e} ⟨f⟩ (g)"), [])
    check_eq("clean nested kinds", errs("[a {b} c] (d [e] f)"), [])
    check_eq("unclosed", [p[3] for p in errs("a [b c")], ["[ is never closed"])
    check_eq("unclosed position", errs("ab [c")[0][1:3], (1, 4))
    check_eq("stray closer", [p[3] for p in errs("a b]")], ["] closes a bracket that was never opened"])
    check_eq("mismatch", len(errs("[a (b]")), 1)
    check_eq("crossing detected", "crossing" in errs("[a {b] c}")[0][3], True)
    check_eq("nested same kind", [p[3] for p in errs("[a [b] c]")][0].endswith("opened inside another square bracket"), True)
    check_eq("round inside round", len(errs("(a (b) c)")), 1)
    check_eq("empty square warns", len(warns("a [] b")), 1)
    check_eq("empty curly warns", len(warns("a {} b")), 1)
    check_eq("gap not empty", check("a [...] b"), [])
    check_eq("ellipsis char", check("a […] b"), [])
    check_eq("double bracket erasure", check("a [[b c]] d"), [])
    check_eq("erasure with restoration inside", check("a [[b [c] d]]"), [])
    check_eq("erasure unclosed", [p[3] for p in errs("a [[b")], ["[[ is never closed"])
    check_eq("double bracket off sees nesting", len(errs("a [[b]] c", double_bracket_erasure=False)), 1)
    check_eq("half brackets", check("⸢a b⸣ [c]"), [])
    check_eq("half bracket mix warns", [p[3] for p in warns("⸢a⸣ ⌈b⌉")], ["two half-bracket styles are mixed; use one"])
    check_eq("angle brackets", check("⟨a⟩ and 〈b〉")[0][3], "two angle-bracket styles are mixed; use one")
    check_eq("multi-line balanced overall", check("[a\nb]"), [])
    check_eq("per-line catches span", len(errs("[a\nb]", per_line=True)), 2)
    check_eq("per-line line numbers", sorted(p[1] for p in errs("ok\n[a\nb]", per_line=True)), [2, 3])
    check_eq("sorted by position", [p[1] for p in check("[a\n(b")], [1, 2])
    check_eq("problems found late still sort first", [p[1] for p in check("(a\nb]")], [1, 2])
    k = dict((s, n) for s, n, _m in key("[a] [b] {c} ... [[d]]"))
    check_eq("key counts", (k.get("[ ]"), k.get("{ }"), k.get("..."), k.get("[[ ]]")), (2, 1, 1, 1))
    check_eq("key lists only used", [s for s, _n, _m in key("plain text")], [])
    check_eq("key ordered by count", key("(a) [b] [c]")[0][0], "[ ]")
    check_eq("key meanings present", all(m for _s, _n, m in key("[a] {b} ⟨c⟩ ⸢d⸣")), True)
    check_eq("no false gap from two dots", [s for s, _n, _m in key("a.. b")], [])
    check_eq("three dots outside brackets counted", [s for s, _n, _m in key("a ... b")], ["..."])
    check_eq("ellipsis character counted as a gap", [s for s, _n, _m in key("a \u2026 b")], ["..."])
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("sigla selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Check the editorial brackets in a draft edition.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("check")
    c.add_argument("file")
    c.add_argument("--per-line", action="store_true", help="each line must balance on its own")
    c.add_argument("--no-double-bracket-erasure", action="store_true", help="read [[ and ]] as two nested square brackets")
    k = sub.add_parser("key")
    k.add_argument("file")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.cmd:
        ap.error("give check, key or --selftest")
    with open(a.file, encoding="utf-8") as fh:
        text = fh.read()
    if a.cmd == "check":
        probs = check(text, a.per_line, not a.no_double_bracket_erasure)
        for sev, line, col, msg in probs:
            where = "line %d, col %d: " % (line, col) if line else ""
            print("%s %s%s" % (sev.upper(), where, msg))
        n_err = sum(1 for p in probs if p[0] == "error")
        print("%d error(s), %d warning(s)" % (n_err, len(probs) - n_err))
        return 1 if n_err else 0
    print("Key draft (confirm against the publication you follow):")
    for sym, n, meaning in key(text):
        print("  %-8s x%-3d %s" % (sym, n, meaning))
    return 0


if __name__ == "__main__":
    sys.exit(main())
