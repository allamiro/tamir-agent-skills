#!/usr/bin/env python3
"""Read, check and convert common sequence file formats (standard library only).

  seqformats.py fasta FILE                  parse and summarise a FASTA file
  seqformats.py fastq FILE [--limit N]      parse and summarise a 4-line FASTQ file (Phred+33)
  seqformats.py gff3 FILE                   check every line of a GFF3 file
  seqformats.py coords bed2gff START END    BED [start, end) 0-based  ->  1-based closed
  seqformats.py coords gff2bed START END    1-based closed            ->  BED [start, end) 0-based
  seqformats.py --selftest

Read the files whole; for very large files stream them with your own loop over parse_fastq().
FASTQ is read as strict 4-line records. Multi-line FASTQ is not supported.
"""
import argparse
import re
import sys
from collections import Counter, namedtuple

FastaRecord = namedtuple("FastaRecord", "id description seq")
FastqRecord = namedtuple("FastqRecord", "id description seq qual")

DNA = set("ACGTN")
RNA = set("ACGUN")
IUPAC_NUCLEOTIDE = set("ACGTURYKMSWBDHVN")
PROTEIN = set("ACDEFGHIKLMNPQRSTVWYXBZJUO")


class FormatError(ValueError):
    pass


def parse_fasta(text):
    """Records from FASTA text. Header: '>' then an id, then an optional description."""
    records, header, parts = [], None, []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        if line.startswith(">"):
            if header is not None:
                records.append(FastaRecord(header[0], header[1], "".join(parts)))
            fields = line[1:].strip().split(None, 1)
            header = (fields[0] if fields else "", fields[1] if len(fields) > 1 else "")
            parts = []
        elif header is None:
            raise FormatError("line %d: sequence data before the first '>' header" % number)
        else:
            parts.append("".join(line.split()))
    if header is not None:
        records.append(FastaRecord(header[0], header[1], "".join(parts)))
    return records


def possible_alphabets(seq):
    """Every alphabet the letters are consistent with. They overlap: the letters of any DNA
    string are also valid protein letters, so a short string can be more than one thing."""
    chars = set(seq.upper()) - set("-*")
    out = []
    if not chars:
        return out
    if chars <= DNA:
        out.append("dna")
    if chars <= RNA and "U" in chars:
        out.append("rna")
    if chars <= IUPAC_NUCLEOTIDE:
        out.append("iupac-nucleotide")
    if chars <= PROTEIN:
        out.append("protein")
    return out


def classify(seq):
    """The most specific alphabet the letters allow. A guess: use possible_alphabets() to see the doubt."""
    if not (set(seq.upper()) - set("-*")):
        return "empty"
    options = possible_alphabets(seq)
    return options[0] if options else "unknown"


NUCLEOTIDE_ALPHABETS = ("dna", "rna", "iupac-nucleotide")
LIKELY_NUCLEOTIDE_LENGTH = 20


def alphabet_call(seq):
    """(alphabet, confidence). Confidence is 'certain' when only one kind of alphabet fits, 'likely' when
    the letters fit both a nucleotide and a protein alphabet but the string is long, and 'ambiguous'
    when it fits both and is short. A long string made only of A, C, G, T and N is almost surely DNA,
    since a protein would have to avoid fifteen of the twenty amino acids; a short one could be either."""
    options = possible_alphabets(seq)
    if not options:
        return classify(seq), "certain"
    nucleotide = [o for o in options if o in NUCLEOTIDE_ALPHABETS]
    if nucleotide and "protein" in options:
        return nucleotide[0], "likely" if len(seq) >= LIKELY_NUCLEOTIDE_LENGTH else "ambiguous"
    return options[0], "certain"


def fasta_report(records):
    ids = Counter(r.id for r in records)
    lengths = [len(r.seq) for r in records]
    return {
        "records": len(records),
        "residues": sum(lengths),
        "min_length": min(lengths) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
        "duplicate_ids": sorted(i for i, c in ids.items() if c > 1),
        "empty_ids": sum(1 for r in records if not r.id),
        "empty_sequences": [r.id for r in records if not r.seq],
        "alphabets": dict(Counter(classify(r.seq) for r in records)),
        "ambiguous_alphabet": [r.id for r in records if r.seq and alphabet_call(r.seq)[1] == "ambiguous"],
    }


def parse_fastq(text):
    """Records from strict 4-line FASTQ. Never scan for '@': a quality line can begin with it."""
    lines = text.splitlines()
    # Blank lines after the last record are harmless; a final record with an empty read is not.
    while len(lines) % 4 and lines and not lines[-1].strip():
        lines.pop()
    if len(lines) % 4:
        raise FormatError("%d lines is not a multiple of 4: the file is truncated or not 4-line FASTQ" % len(lines))
    records = []
    for i in range(0, len(lines), 4):
        head, seq, plus, qual = lines[i:i + 4]
        where = "record starting at line %d" % (i + 1)
        if not head.startswith("@"):
            raise FormatError("%s: header does not start with '@'" % where)
        if not plus.startswith("+"):
            raise FormatError("%s: third line does not start with '+'" % where)
        if len(seq) != len(qual):
            raise FormatError("%s: %d bases but %d quality characters" % (where, len(seq), len(qual)))
        if any(not 33 <= ord(c) <= 126 for c in qual):
            raise FormatError("%s: quality character outside printable ASCII 33-126" % where)
        fields = head[1:].strip().split(None, 1)
        records.append(FastqRecord(fields[0] if fields else "", fields[1] if len(fields) > 1 else "", seq, qual))
    return records


def phred(qual, offset=33):
    """Quality scores Q from a quality string. Q = ASCII code - offset."""
    scores = [ord(c) - offset for c in qual]
    if any(q < 0 for q in scores):
        raise FormatError("quality character below the offset: wrong offset for this file?")
    return scores


def error_probability(q):
    """Probability that the base call is wrong: 10 ** (-Q / 10)."""
    return 10 ** (-q / 10.0)


def expected_errors(qual, offset=33):
    return sum(error_probability(q) for q in phred(qual, offset))


GFF3_STRANDS = set("+-.?")


def check_gff3_line(line):
    """Problems found in one GFF3 feature line. An empty list means the line looks well formed."""
    fields = line.rstrip("\n").split("\t")
    if len(fields) != 9:
        return ["%d tab-separated columns, expected 9" % len(fields)]
    seqid, _source, ftype, start, end, score, strand, phase, attributes = fields
    problems = []
    if not seqid or re.search(r"\s", seqid):
        problems.append("seqid is empty or contains whitespace")
    if not ftype or ftype == ".":
        problems.append("type is empty")
    s = e = None
    for label, value in (("start", start), ("end", end)):
        if not value.isdigit() or int(value) < 1:
            problems.append("%s %r is not a positive integer (coordinates are 1-based)" % (label, value))
    if start.isdigit() and end.isdigit():
        s, e = int(start), int(end)
        if s > e:
            problems.append("start %d is greater than end %d" % (s, e))
    if score != ".":
        try:
            float(score)
        except ValueError:
            problems.append("score %r is neither '.' nor a number" % score)
    if strand not in GFF3_STRANDS:
        problems.append("strand %r is not one of + - . ?" % strand)
    if phase not in ("0", "1", "2", "."):
        problems.append("phase %r is not 0, 1, 2 or '.'" % phase)
    if ftype == "CDS" and phase == ".":
        problems.append("CDS features require a phase of 0, 1 or 2")
    if attributes != ".":
        for item in filter(None, attributes.split(";")):
            if "=" not in item:
                problems.append("attribute %r is not tag=value" % item)
    return problems


def check_gff3(text):
    """(line number, line, problems) for every bad feature line, plus file-level problems."""
    lines = text.splitlines()
    out = []
    if not lines or not lines[0].startswith("##gff-version 3"):
        out.append((1, lines[0] if lines else "", ["first line should be '##gff-version 3'"]))
    for number, line in enumerate(lines, 1):
        if not line.strip() or line.startswith("#"):
            continue
        problems = check_gff3_line(line)
        if problems:
            out.append((number, line, problems))
    return out


def bed_to_one_based(start, end):
    """BED interval [start, end), 0-based, to a 1-based closed interval [start+1, end]."""
    if start < 0 or end <= start:
        raise ValueError("need 0 <= start < end (a zero-length BED interval has no 1-based closed form)")
    return start + 1, end


def one_based_to_bed(start, end):
    """1-based closed interval [start, end] to a BED interval [start-1, end)."""
    if start < 1 or end < start:
        raise ValueError("need 1 <= start <= end")
    return start - 1, end


def selftest():
    n = [0]

    def check(name, got, want):
        n[0] += 1
        if got != want:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    def raises(name, fn, exc=Exception):
        n[0] += 1
        try:
            fn()
        except exc:
            return
        raise AssertionError("%s: expected %s" % (name, exc.__name__))

    text = ">s1 first one\nACGT\nAC\n\n>s2\nacgtn\n>s1 dup\nAAAA\n>empty\n"
    recs = parse_fasta(text)
    check("fasta count", len(recs), 4)
    check("fasta joins wrapped lines", recs[0].seq, "ACGTAC")
    check("fasta id and description", (recs[0].id, recs[0].description), ("s1", "first one"))
    check("fasta header without description", (recs[1].id, recs[1].description), ("s2", ""))
    check("fasta windows line endings", parse_fasta(text.replace("\n", "\r\n")), recs)
    rep = fasta_report(recs)
    check("fasta duplicate ids", rep["duplicate_ids"], ["s1"])
    check("fasta empty sequences", rep["empty_sequences"], ["empty"])
    check("fasta residues", rep["residues"], 6 + 5 + 4)
    between = parse_fasta(">a\n>b\nAC\n")
    check("fasta keeps an empty record that sits between two others", [(r.id, r.seq) for r in between], [("a", ""), ("b", "AC")])
    raises("fasta data before header", lambda: parse_fasta("ACGT\n>x\nAC\n"), FormatError)
    check("fasta empty file", parse_fasta(""), [])
    check("classify dna", classify("ACGTN"), "dna")
    check("classify rna", classify("ACGU"), "rna")
    check("classify protein", classify("MKVLEF*"), "protein")
    check("MKV* is a valid nucleotide string and a valid peptide", possible_alphabets("MKV*"), ["iupac-nucleotide", "protein"])
    check("ACGT is valid DNA and valid protein", possible_alphabets("ACGT"), ["dna", "iupac-nucleotide", "protein"])
    check("no letters, no alphabet", possible_alphabets("--"), [])
    check("classify iupac", classify("ACGTRYK"), "iupac-nucleotide")
    check("classify gaps ignored", classify("AC-GT"), "dna")
    check("classify unknown", classify("AC1T"), "unknown")
    check("a short ACGT string is ambiguous", alphabet_call("ACGTACGTAC"), ("dna", "ambiguous"))
    check("a long ACGT string is likely DNA", alphabet_call("ACGT" * 8), ("dna", "likely"))
    check("the boundary is 20 bases", (alphabet_call("A" * 19)[1], alphabet_call("A" * 20)[1]), ("ambiguous", "likely"))
    check("letters only a protein uses are certain", alphabet_call("MKVLEF"), ("protein", "certain"))
    check("U settles RNA against DNA, but not against protein", alphabet_call("ACGU" * 8), ("rna", "likely"))
    check("junk is certainly not an alphabet", alphabet_call("AC1T"), ("unknown", "certain"))
    amb = fasta_report(parse_fasta(">short\nACGTACGTAC\n>long\n" + "ACGT" * 8 + "\n>pep\nMKVLEF\n>empty\n"))
    check("the report names the ambiguous records", amb["ambiguous_alphabet"], ["short"])
    # FASTQ: the second record's quality line starts with '@' and must not be taken for a header.
    fq = "@r1\nACGT\n+\nIIII\n@r2 desc\nAC\n+r2 desc\n@@\n"
    q = parse_fastq(fq)
    check("fastq count despite '@' quality line", len(q), 2)
    check("fastq second record", (q[1].id, q[1].description, q[1].seq, q[1].qual), ("r2", "desc", "AC", "@@"))
    check("phred I is Q40", phred("IIII"), [40, 40, 40, 40])
    check("phred ! is Q0", phred("!"), [0])
    check("phred @ is Q31", phred("@@"), [31, 31])
    check("error probability Q10", error_probability(10), 0.1)
    check("error probability Q20", abs(error_probability(20) - 0.01) < 1e-12, True)
    check("error probability Q30", abs(error_probability(30) - 0.001) < 1e-12, True)
    check("expected errors for IIII", abs(expected_errors("IIII") - 4e-4) < 1e-12, True)
    raises("fastq length mismatch", lambda: parse_fastq("@r\nACGT\n+\nIII\n"), FormatError)
    raises("fastq truncated", lambda: parse_fastq("@r\nACGT\n+\n"), FormatError)
    raises("fastq missing plus", lambda: parse_fastq("@r\nACGT\nX\nIIII\n"), FormatError)
    raises("fastq missing at", lambda: parse_fastq("r\nACGT\n+\nIIII\n"), FormatError)
    raises("fastq quality below offset", lambda: phred(" "), FormatError)
    check("fastq trailing blank lines ok", len(parse_fastq(fq + "\n\n")), 2)
    empty_read = parse_fastq("@e\n\n+\n\n")
    check("fastq record with an empty read", (empty_read[0].id, empty_read[0].seq, empty_read[0].qual), ("e", "", ""))
    good = "chr1\tsrc\tgene\t100\t200\t.\t+\t.\tID=g1;Name=x"
    check("gff3 good line", check_gff3_line(good), [])
    check("gff3 CDS with phase ok", check_gff3_line("c\ts\tCDS\t1\t9\t.\t+\t0\tID=c1"), [])
    check("gff3 one-base feature (start equals end) is valid", check_gff3_line("c\ts\tSNV\t5\t5\t.\t+\t.\tID=a"), [])
    check("gff3 start after end", bool(check_gff3_line(good.replace("\t100\t200", "\t200\t100"))), True)
    check("gff3 zero start", bool(check_gff3_line(good.replace("\t100\t", "\t0\t"))), True)
    check("gff3 bad strand", bool(check_gff3_line(good.replace("\t+\t", "\tx\t"))), True)
    check("gff3 CDS without phase", bool(check_gff3_line("c\ts\tCDS\t1\t9\t.\t+\t.\tID=c1")), True)
    check("gff3 eight columns", bool(check_gff3_line("a\tb\tc\t1\t2\t.\t+\t.")), True)
    check("gff3 attribute without equals", bool(check_gff3_line(good[:-1] + "x;oops")), True)
    check("gff3 file needs version line", check_gff3("chr1\ts\tgene\t1\t2\t.\t+\t.\tID=a")[0][0], 1)
    check("gff3 clean file", check_gff3("##gff-version 3\n" + good + "\n"), [])
    # Coordinates: BED is 0-based half-open, GFF3 and SAM POS are 1-based.
    check("bed 0-100 to gff", bed_to_one_based(0, 100), (1, 100))
    check("gff 1-100 to bed", one_based_to_bed(1, 100), (0, 100))
    check("one base", (bed_to_one_based(5, 6), one_based_to_bed(6, 6)), ((6, 6), (5, 6)))
    for start in range(0, 6):
        for end in range(start + 1, 8):
            s, e = bed_to_one_based(start, end)
            check("round trip %d-%d" % (start, end), one_based_to_bed(s, e), (start, end))
            check("length preserved %d-%d" % (start, end), e - s + 1, end - start)
    seq = "ACGTACGTAC"
    s, e = bed_to_one_based(2, 5)
    check("same bases from both conventions", seq[2:5], seq[s - 1:e])
    raises("zero-length bed", lambda: bed_to_one_based(3, 3), ValueError)
    raises("gff start zero", lambda: one_based_to_bed(0, 5), ValueError)
    print("seqformats.py self-test: %d checks passed" % n[0])


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read, check and convert sequence file formats.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("fasta").add_argument("file")
    s = sub.add_parser("fastq")
    s.add_argument("file")
    s.add_argument("--limit", type=int, default=0, help="only summarise the first N records")
    sub.add_parser("gff3").add_argument("file")
    s = sub.add_parser("coords")
    s.add_argument("direction", choices=("bed2gff", "gff2bed"))
    s.add_argument("start", type=int)
    s.add_argument("end", type=int)
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    try:
        if a.cmd == "fasta":
            for k, v in fasta_report(parse_fasta(_read(a.file))).items():
                print("%-18s %s" % (k, v))
        elif a.cmd == "fastq":
            recs = parse_fastq(_read(a.file))
            if a.limit:
                recs = recs[:a.limit]
            bases = sum(len(r.seq) for r in recs)
            allq = [q for r in recs for q in phred(r.qual)]
            print("records %d, bases %d" % (len(recs), bases))
            if allq:
                print("mean Q %.2f (an average of Q is not an average error rate)" % (sum(allq) / len(allq)))
                print("expected errors per record, mean %.4f" % (sum(expected_errors(r.qual) for r in recs) / len(recs)))
        elif a.cmd == "gff3":
            bad = check_gff3(_read(a.file))
            for number, line, problems in bad:
                print("line %d: %s" % (number, "; ".join(problems)))
            print("%d line(s) with problems" % len(bad))
            return 1 if bad else 0
        elif a.cmd == "coords":
            fn = bed_to_one_based if a.direction == "bed2gff" else one_based_to_bed
            print("%d %d" % fn(a.start, a.end))
        else:
            ap.print_help()
            return 2
    except (FormatError, ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
