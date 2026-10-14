#!/usr/bin/env python3
"""Recognise and compare biological database identifiers (standard library only).

  accessions.py classify ID [ID ...]      every database format each identifier fits, and its version
  accessions.py same ID1 ID2              same record? versions compared separately
  accessions.py check FILE                one identifier per line: unversioned or unrecognised ones
  accessions.py --selftest

A string can fit more than one format. P12345 is a valid UniProt accession and also fits the
GenBank "one letter and five digits" nucleotide pattern, so a bare identifier does not say which
database it came from. This script reports every fit and never picks one for you.
Pattern provenance, read 2026-10-14: GenBank nucleotide and protein accession layouts and the
RefSeq underscore rule from NCBI; the Ensembl layout ENS + species + feature + 11 digits from
Ensembl. The remaining patterns (UniProt, PDB, SRA, GEO, the meaning of RefSeq prefixes and of
Ensembl feature letters) are from general knowledge and are marked unverified in the output.
"""
import argparse
import re
import sys

REFSEQ_PREFIX = {  # unverified: the NCBI page holding this table could not be read
    "NC": "chromosome or other complete genomic molecule",
    "NG": "genomic region",
    "NT": "genomic contig",
    "NW": "WGS supercontig",
    "NZ": "WGS project (complete or draft genomes)",
    "NM": "mRNA (curated)",
    "NR": "non-coding RNA (curated)",
    "NP": "protein (curated)",
    "XM": "mRNA (predicted)",
    "XR": "non-coding RNA (predicted)",
    "XP": "protein (predicted)",
    "WP": "non-redundant protein",
}
ENSEMBL_FEATURE = {"G": "gene", "T": "transcript", "P": "protein", "E": "exon"}  # unverified letters

# (database, kind, regex over the unversioned part, verified?)
PATTERNS = [
    ("INSDC (GenBank/ENA/DDBJ)", "nucleotide accession, 1 letter + 5 digits", r"[A-Z]\d{5}", True),
    ("INSDC (GenBank/ENA/DDBJ)", "nucleotide accession, 2 letters + 6 digits", r"[A-Z]{2}\d{6}", True),
    ("INSDC (GenBank/ENA/DDBJ)", "nucleotide accession, 2 letters + 8 digits", r"[A-Z]{2}\d{8}", True),
    ("INSDC (GenBank/ENA/DDBJ)", "protein accession, 3 letters + 5 digits", r"[A-Z]{3}\d{5}", True),
    ("INSDC (GenBank/ENA/DDBJ)", "protein accession, 3 letters + 7 digits", r"[A-Z]{3}\d{7}", True),
    ("UniProtKB", "protein accession", r"(?:[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2})", False),
    ("PDB", "structure entry ID, 4 characters", r"[0-9][A-Za-z0-9]{3}", False),
    ("SRA/ENA/DDBJ", "run, experiment, sample or study", r"[SED]R[RXSP]\d+", False),
    ("GEO", "series, sample, platform or dataset", r"G(?:SE|SM|PL|DS)\d+", False),
]
_REFSEQ = re.compile(r"^([A-Z]{2})_(\d+)$")
_ENSEMBL = re.compile(r"^ENS([A-Z]{0,6}?)([GTPE])(\d{11})$")
_VERSION = re.compile(r"^(.+)\.(\d+)$")


def split_version(identifier):
    """('NM_000546', '6') for 'NM_000546.6'; (id, None) when there is no version suffix."""
    m = _VERSION.match(identifier)
    return (m.group(1), m.group(2)) if m else (identifier, None)


def classify(identifier):
    """List of dicts, one per format the identifier fits. Empty when it fits none."""
    ident = identifier.strip()
    base, version = split_version(ident)
    fits = []
    m = _REFSEQ.match(base)
    if m:
        prefix = m.group(1)
        fits.append({"database": "RefSeq", "kind": "%s_ %s" % (prefix, REFSEQ_PREFIX.get(prefix, "unknown prefix")),
                     "version": version, "verified": False,
                     "note": "underscore in the third position marks RefSeq (verified); the prefix meaning is not"})
    m = _ENSEMBL.match(base)
    if m:
        fits.append({"database": "Ensembl", "kind": "%s%s" % (ENSEMBL_FEATURE.get(m.group(2), "?"),
                     " (species prefix %s)" % m.group(1) if m.group(1) else " (human, no species prefix)"),
                     "version": version, "verified": False,
                     "note": "layout ENS + species + feature + 11 digits is verified; the feature letters are not"})
    if not m and not _REFSEQ.match(base):
        for db, kind, rx, verified in PATTERNS:
            if re.fullmatch(rx, base):
                fits.append({"database": db, "kind": kind, "version": version, "verified": verified,
                             "note": "" if verified else "pattern from general knowledge, unverified"})
    return fits


def same_record(a, b):
    """(same record?, versions differ?). Compares the unversioned parts, case-sensitively."""
    (ba, va), (bb, vb) = split_version(a.strip()), split_version(b.strip())
    return ba == bb, (va != vb)


def check_lines(lines):
    """Problems with a list of identifiers: unrecognised, ambiguous, or missing the version a pin needs."""
    problems = []
    for number, line in enumerate(lines, 1):
        ident = line.strip()
        if not ident or ident.startswith("#"):
            continue
        fits = classify(ident)
        if not fits:
            problems.append((number, ident, "not recognised as any known format"))
            continue
        if len(fits) > 1:
            problems.append((number, ident, "fits %d formats (%s): record which database it came from" % (
                len(fits), "; ".join(f["database"] for f in fits))))
        if split_version(ident)[1] is None and any(f["database"] in ("RefSeq", "Ensembl") or f["database"].startswith("INSDC") for f in fits):
            problems.append((number, ident, "no version suffix: the record can change, so pin the version"))
    return problems


def selftest():
    n = [0]

    def check(name, got, want):
        n[0] += 1
        if got != want:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    def dbs(identifier):
        return sorted(f["database"] for f in classify(identifier))

    check("split version", split_version("NM_000546.6"), ("NM_000546", "6"))
    check("no version", split_version("P12345"), ("P12345", None))
    r = classify("NM_000546.6")
    check("RefSeq mRNA", (len(r), r[0]["database"], r[0]["version"]), (1, "RefSeq", "6"))
    check("RefSeq prefix meaning", "mRNA" in r[0]["kind"], True)
    check("RefSeq protein", classify("NP_000537.3")[0]["kind"].startswith("NP_ protein"), True)
    check("RefSeq is recognised by the underscore, not just the table", dbs("ZZ_123456"), ["RefSeq"])
    check("RefSeq is not also INSDC", dbs("NM_000546"), ["RefSeq"])
    check("GenBank 1+5", dbs("U12345"), ["INSDC (GenBank/ENA/DDBJ)"])
    check("GenBank 2+6", dbs("AB123456"), ["INSDC (GenBank/ENA/DDBJ)"])
    check("GenBank 2+8", dbs("AB12345678"), ["INSDC (GenBank/ENA/DDBJ)"])
    check("GenBank protein 3+5", [f["kind"] for f in classify("AAA12345")], ["protein accession, 3 letters + 5 digits"])
    check("a bare P12345 fits two databases", dbs("P12345"), ["INSDC (GenBank/ENA/DDBJ)", "UniProtKB"])
    check("UniProt 10 characters", dbs("A0A022YWF9"), ["UniProtKB"])
    check("UniProt O letter", dbs("O12345"), ["INSDC (GenBank/ENA/DDBJ)", "UniProtKB"])
    check("UniProt Q accession with letters inside", dbs("Q9Y6K9"), ["UniProtKB"])
    check("Ensembl human gene with version", [(f["database"], f["kind"], f["version"]) for f in classify("ENSG00000141510.18")],
          [("Ensembl", "gene (human, no species prefix)", "18")])
    check("Ensembl mouse gene", [f["kind"] for f in classify("ENSMUSG00000000001")], ["gene (species prefix MUS)"])
    check("Ensembl transcript", classify("ENST00000269305")[0]["kind"].startswith("transcript"), True)
    check("Ensembl needs eleven digits", classify("ENSG0000014151"), [])
    check("PDB", dbs("1ABC"), ["PDB"])
    # SRR + seven digits is also three letters + seven digits, the INSDC protein layout: two honest fits.
    check("SRA run also fits the INSDC protein layout", dbs("SRR1234567"), ["INSDC (GenBank/ENA/DDBJ)", "SRA/ENA/DDBJ"])
    check("SRA experiment", dbs("SRX12"), ["SRA/ENA/DDBJ"])
    check("GEO series also fits the INSDC protein layout", dbs("GSE12345"), ["GEO", "INSDC (GenBank/ENA/DDBJ)"])
    check("GEO sample", dbs("GSM1234"), ["GEO"])
    check("not an identifier", classify("hello world"), [])
    check("too short", classify("AB12"), [])
    check("whitespace is trimmed", dbs("  NM_000546.6\n"), ["RefSeq"])
    check("verified flag is set for GenBank layouts", classify("AB123456")[0]["verified"], True)
    check("verified flag is clear for UniProt", [f["verified"] for f in classify("A0A022YWF9")], [False])
    check("same record, same version", same_record("NM_000546.6", "NM_000546.6"), (True, False))
    check("same record, different versions", same_record("NM_000546.5", "NM_000546.6"), (True, True))
    check("different records", same_record("NM_000546.6", "NM_000547.6"), (False, False))
    check("version missing on one side counts as different", same_record("NM_000546", "NM_000546.6"), (True, True))
    problems = check_lines(["NM_000546.6", "NM_000546", "P12345", "# comment", "", "zzz"])
    check("check flags a missing version", (2, "NM_000546") in [(p[0], p[1]) for p in problems], True)
    check("check flags an ambiguous identifier", any(p[1] == "P12345" and "fits 2 formats" in p[2] for p in problems), True)
    check("check flags an unrecognised string", any(p[1] == "zzz" for p in problems), True)
    check("check leaves the good line alone", any(p[1] == "NM_000546.6" for p in problems), False)
    print("accessions.py self-test: %d checks passed" % n[0])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Recognise and compare biological database identifiers.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("classify").add_argument("ids", nargs="+")
    s = sub.add_parser("same")
    s.add_argument("a")
    s.add_argument("b")
    sub.add_parser("check").add_argument("file")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    if a.cmd == "classify":
        for ident in a.ids:
            fits = classify(ident)
            if not fits:
                print("%s: not recognised as any known format" % ident)
            for f in fits:
                print("%s: %s, %s%s%s" % (ident, f["database"], f["kind"],
                                          ", version " + f["version"] if f["version"] else ", no version",
                                          "" if f["verified"] else "  [unverified pattern]"))
    elif a.cmd == "same":
        same, differ = same_record(a.a, a.b)
        print("same record: %s; versions differ: %s" % (same, differ))
    elif a.cmd == "check":
        try:
            with open(a.file, encoding="utf-8") as fh:
                problems = check_lines(fh.read().splitlines())
        except OSError as exc:
            print("error: %s" % exc, file=sys.stderr)
            return 1
        for number, ident, why in problems:
            print("line %d: %s: %s" % (number, ident, why))
        print("%d problem(s)" % len(problems))
        return 1 if problems else 0
    else:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
