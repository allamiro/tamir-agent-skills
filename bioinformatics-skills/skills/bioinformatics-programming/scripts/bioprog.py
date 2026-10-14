#!/usr/bin/env python3
"""Programming building blocks for sequence work (standard library only).

  bioprog.py pack SEQ                  2-bit packing of A, C, G, T: bytes in hex and the size saved
  bioprog.py canonical KMER            the smaller of a k-mer and its reverse complement
  bioprog.py logsumexp X [X ...]       log(sum(exp(x))) without underflow
  bioprog.py gcwin SEQ --size W        GC fraction of each window in one pass
  bioprog.py fasta FILE                stream records from a FASTA file (plain or .gz) one at a time
  bioprog.py --selftest

Each function is the small, tested core of a pattern that causes trouble at scale: memory
(packing, streaming), strand symmetry (canonical k-mers), probabilities that underflow (log space),
and loops that are quadratic when they could be linear (windows).
"""
import argparse
import gzip
import math
import os
import sys
import tempfile

_CODE = {"A": 0, "C": 1, "G": 2, "T": 3}
_BASE = "ACGT"
_COMP = {"A": "T", "C": "G", "G": "C", "T": "A"}


def pack2bit(seq):
    """(bytes, length). A=0, C=1, G=2, T=3, four bases per byte, first base in the high bits.
    N and other codes cannot be stored in two bits: keep them in a separate mask."""
    seq = seq.upper()
    out = bytearray((len(seq) + 3) // 4)
    for i, ch in enumerate(seq):
        if ch not in _CODE:
            raise ValueError("%r cannot be packed in two bits; mask ambiguity codes separately" % ch)
        out[i // 4] |= _CODE[ch] << (6 - 2 * (i % 4))
    return bytes(out), len(seq)


def unpack2bit(data, length):
    if length > 4 * len(data) or length < 0:
        raise ValueError("length does not fit the data")
    return "".join(_BASE[(data[i // 4] >> (6 - 2 * (i % 4))) & 3] for i in range(length))


def kmer_to_int(kmer):
    value = 0
    for ch in kmer.upper():
        if ch not in _CODE:
            raise ValueError("%r is not A, C, G or T" % ch)
        value = (value << 2) | _CODE[ch]
    return value


def int_to_kmer(value, k):
    if value < 0 or value >= 4 ** k:
        raise ValueError("value does not fit in %d bases" % k)
    return "".join(_BASE[(value >> (2 * (k - 1 - i))) & 3] for i in range(k))


def reverse_complement(kmer):
    try:
        return "".join(_COMP[c] for c in reversed(kmer.upper()))
    except KeyError as exc:
        raise ValueError("%r is not A, C, G or T" % exc.args[0])


def canonical(kmer):
    """The same string for a k-mer and its reverse complement: whichever sorts first."""
    kmer = kmer.upper()
    return min(kmer, reverse_complement(kmer))


def logsumexp(values):
    """log(sum(exp(v))) computed around the maximum, so very negative values do not underflow to 0."""
    values = list(values)
    if not values:
        raise ValueError("no values")
    top = max(values)
    if top == -math.inf:
        return -math.inf
    return top + math.log(sum(math.exp(v - top) for v in values))


def gc_windows(seq, size):
    """GC fraction of every window of `size` bases in one pass: add the base entering, remove the one leaving."""
    seq = seq.upper()
    if size < 1 or size > len(seq):
        raise ValueError("window size must be between 1 and the sequence length (%d)" % len(seq))
    gc = sum(ch in "GC" for ch in seq[:size])
    out = [gc / size]
    for i in range(size, len(seq)):
        gc += (seq[i] in "GC") - (seq[i - size] in "GC")
        out.append(gc / size)
    return out


def iter_fasta(lines):
    """Yield (header, sequence) one record at a time from any iterable of lines.
    A record is yielded as soon as the next header is seen, so memory is one record, not the file."""
    header, parts = None, []
    for line in lines:
        line = line.rstrip("\r\n")
        if line.startswith(">"):
            if header is not None:
                yield header, "".join(parts)
            header, parts = line[1:].strip(), []
        elif line.strip():
            if header is None:
                raise ValueError("sequence data before the first '>' header")
            parts.append(line.strip())
    if header is not None:
        yield header, "".join(parts)


def stream_fasta(path):
    """iter_fasta over a plain or gzip-compressed file, opened lazily and closed when exhausted."""
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as fh:
        for record in iter_fasta(fh):
            yield record


def selftest():
    n = [0]

    def check(name, got, want, tol=None):
        n[0] += 1
        ok = (abs(got - want) <= tol) if tol is not None else got == want
        if not ok:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    def raises(name, fn, exc=ValueError):
        n[0] += 1
        try:
            fn()
        except exc:
            return
        raise AssertionError("%s: expected %s" % (name, exc.__name__))

    check("ACGT packs to 0b00011011", pack2bit("ACGT"), (bytes([0b00011011]), 4))
    check("TTTT packs to 0xff", pack2bit("TTTT"), (b"\xff", 4))
    check("a partial byte is padded with zeros", pack2bit("T"), (bytes([0b11000000]), 1))
    check("five bases take two bytes", len(pack2bit("ACGTA")[0]), 2)
    check("empty sequence", pack2bit(""), (b"", 0))
    state = [5]

    def rnd_seq(length):
        out = []
        for _ in range(length):
            state[0] = (state[0] * 1103515245 + 12345) % (2 ** 31)
            out.append("ACGT"[(state[0] >> 16) % 4])
        return "".join(out)

    for length in range(0, 41):
        s = rnd_seq(length)
        data, ln = pack2bit(s)
        check("round trip length %d" % length, unpack2bit(data, ln), s)
        check("size is ceil(n/4) at length %d" % length, len(data), (length + 3) // 4)
    check("lower case accepted", unpack2bit(*pack2bit("acgt")), "ACGT")
    raises("N cannot be packed", lambda: pack2bit("ACNT"))
    raises("length beyond the data", lambda: unpack2bit(b"\x00", 5))
    check("k-mer integer for ACGT", kmer_to_int("ACGT"), 0b00011011)
    check("AAAA is 0", kmer_to_int("AAAA"), 0)
    check("TTTT is 255", kmer_to_int("TTTT"), 255)
    for k in (1, 3, 5):
        for v in range(4 ** k):
            if kmer_to_int(int_to_kmer(v, k)) != v:
                raise AssertionError("k-mer integer round trip failed at k=%d, v=%d" % (k, v))
    n[0] += 1
    raises("value too large for k", lambda: int_to_kmer(16, 2))
    raises("kmer with N", lambda: kmer_to_int("ACN"))
    check("canonical of AAC", canonical("AAC"), "AAC")
    check("canonical of GTT is AAC", canonical("GTT"), "AAC")
    check("a palindromic k-mer is its own canonical form", canonical("ACGT"), "ACGT")
    check("canonical ignores case", canonical("gtt"), "AAC")
    check("canonical is strand-symmetric", all(canonical(m) == canonical(reverse_complement(m))
                                               for m in (int_to_kmer(v, 4) for v in range(256))), True)
    check("canonical forms of all 4-mers: 136 distinct", len({canonical(int_to_kmer(v, 4)) for v in range(256)}), 136)
    check("canonical forms of all 3-mers: 32 distinct", len({canonical(int_to_kmer(v, 3)) for v in range(64)}), 32)
    # Log space.
    check("logsumexp of two equal values", logsumexp([0.0, 0.0]), math.log(2), 1e-12)
    check("logsumexp agrees with the direct sum", logsumexp([-1.0, -2.0, -3.0]),
          math.log(math.exp(-1) + math.exp(-2) + math.exp(-3)), 1e-12)
    check("logsumexp survives underflow", logsumexp([-1000.0, -1000.0]), -1000 + math.log(2), 1e-9)
    raises("the direct sum underflows", lambda: math.log(math.exp(-1000) + math.exp(-1000)))
    check("logsumexp of one value is that value", logsumexp([-3.5]), -3.5, 1e-12)
    check("all minus infinity", logsumexp([-math.inf, -math.inf]), -math.inf)
    raises("logsumexp of nothing", lambda: logsumexp([]))
    # Windows: one pass equals the direct calculation.
    s = rnd_seq(200)
    fast = gc_windows(s, 17)
    direct = [sum(c in "GC" for c in s[i:i + 17]) / 17 for i in range(len(s) - 16)]
    check("incremental GC windows equal direct windows", all(abs(a - b) < 1e-12 for a, b in zip(fast, direct)), True)
    check("window count", len(fast), len(s) - 16)
    check("GC windows of GGCC", gc_windows("GGCCAATT", 4), [1.0, 0.75, 0.5, 0.25, 0.0])
    raises("window too big", lambda: gc_windows("ACGT", 5))
    # Streaming.
    lines = [">a first", "AC", "GT", "", ">b", "TTT", ">c"]
    check("records", list(iter_fasta(lines)), [("a first", "ACGT"), ("b", "TTT"), ("c", "")])
    check("windows line endings", list(iter_fasta([l + "\r\n" for l in lines])), list(iter_fasta(lines)))

    def source():
        yield ">a"
        yield "AC"
        yield ">b"
        raise RuntimeError("the rest of the file was read before the first record was yielded")

    first = next(iter_fasta(source()))
    check("the first record arrives before the rest is read", first, ("a", "AC"))
    raises("data before a header", lambda: list(iter_fasta(["ACGT"])))
    with tempfile.TemporaryDirectory() as d:
        text = ">x\nACGT\nAC\n>y\nGG\n"
        plain, gz = os.path.join(d, "t.fa"), os.path.join(d, "t.fa.gz")
        with open(plain, "w") as fh:
            fh.write(text)
        with gzip.open(gz, "wt") as fh:
            fh.write(text)
        check("plain file", list(stream_fasta(plain)), [("x", "ACGTAC"), ("y", "GG")])
        check("gzip file", list(stream_fasta(gz)), [("x", "ACGTAC"), ("y", "GG")])
    print("bioprog.py self-test: %d checks passed" % n[0])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Programming building blocks for sequence work.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("pack").add_argument("seq")
    sub.add_parser("canonical").add_argument("kmer")
    sub.add_parser("logsumexp").add_argument("values", type=float, nargs="+")
    s = sub.add_parser("gcwin")
    s.add_argument("seq")
    s.add_argument("--size", type=int, required=True)
    sub.add_parser("fasta").add_argument("file")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    try:
        if a.cmd == "pack":
            data, ln = pack2bit(a.seq)
            print("%d bases in %d bytes (%s): %.2f bytes per base, against 1 for text" % (ln, len(data), data.hex(), len(data) / max(ln, 1)))
        elif a.cmd == "canonical":
            print(canonical(a.kmer))
        elif a.cmd == "logsumexp":
            print("%.10g" % logsumexp(a.values))
        elif a.cmd == "gcwin":
            print(" ".join("%.3f" % v for v in gc_windows(a.seq, a.size)))
        elif a.cmd == "fasta":
            count = total = 0
            for header, seq in stream_fasta(a.file):
                count += 1
                total += len(seq)
            print("%d records, %d bases, read one record at a time" % (count, total))
        else:
            ap.print_help()
            return 2
    except (ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
