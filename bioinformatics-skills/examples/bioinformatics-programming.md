# `bioinformatics-programming`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> How do I read a 50 GB compressed FASTA file and compute a statistic for every record without running out of memory?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,440 | 2,445 |
| Input tokens read across all turns (including cached context) | 30,350 | 125,142 |
| Extra input tokens when the skill is installed | | +94,792 |
| Cost, US dollars at list price | 0.088 | 0.192 |
| Skills invoked in the sample run | none | `bioinformatics-programming` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 230 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
The answer is to stream the file. Decompress it as you read, handle one record at a time, write that record's result out straight away, and discard the sequence. Memory then depends on the longest single record, not on the 50 GB file. If you compute the statistic line by line, memory stays nearly constant.

## 1. Check whether an existing tool already computes it

Common per-record statistics such as length, GC content and N count are already built into `seqkit`. It streams gzip input and uses several threads:

```bash
seqkit fx2tab -n -l -g -B N reads.fa.gz > stats.tsv   # name, length, GC%, N%
```

Write your own code only if the statistic isn't available this way.

## 2. Python streaming version

This version doesn't need any libraries:

```python
import gzip, sys

def stream_fasta(path):
    """Yield (header, sequence) one record at a time; plain or .gz."""
    opener = gzip.open if path.endswith(".gz") else open
    header, chunks = None, []
    with opener(path, "rt") as fh:
        for line in fh:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(chunks)   # join once, not += in a loop
                header, chunks = line[1:].split()[0], []
            else:
                chunks.append(line)
        if header is not None:
            yield header, "".join(chunks)

def gc_fraction(seq):
    s = seq.upper()                       # count case-insensitively; soft-masked bases still count
    acgt = sum(s.count(b) for b in "ACGT")
    return (s.count("G") + s.count("C")) / acgt if acgt else float("nan")

out = sys.stdout
for name, seq in stream_fasta(sys.argv[1]):
    out.write(f"{name}\t{len(seq)}\t{gc_fraction(seq):.4f}\n")   # emit immediately, keep nothing
```

Run it with `python3 stats.py reads.fa.gz > stats.tsv`.

Things to get right:
- **Don't call `fh.read()` or `readlines()`, and don't collect records in a list or dict.** Doing any of these loads the whole file into memory.
- **Don't build the sequence with `seq += line`.** Each `+=` copies the string, so the time grows with the square of the record length. Append the lines to a list and join them once, as above.
- **Write each result as soon as you have it.** If you need a summary across all records, keep running totals such as count, sum and sum of squares, not a list of every value.
- **Handle N and other ambiguity codes on purpose.** The code above leaves them out of the GC denominator. Decide whether your statistic should do the same.

## 3. When a single record is huge

A chromosome-scale FASTA can contain single records of hundreds of megabases. If your statistic can be built up a piece at a time (counts, length, GC, k-mer tallies), update it line by line so the sequence is never stored:

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
You need streaming: decompress and parse one record at a time, compute the statistic, write it out, and drop the record. Memory then depends on the size of one record, not the size of the file.

## Python, no dependencies

```python
import gzip, sys

def fasta_records(path):
    """Yield (header, seq) one record at a time."""
    header, chunks = None, []
    with gzip.open(path, "rt") as f:          # decompresses as it reads
        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(chunks)
                header, chunks = line[1:], []
            elif line:
                chunks.append(line)
        if header is not None:
            yield header, "".join(chunks)

out = sys.stdout
for header, seq in fasta_records(sys.argv[1]):
    s = seq.upper()
    gc = (s.count("G") + s.count("C")) / len(s) if s else 0.0
    out.write(f"{header.split()[0]}\t{len(s)}\t{gc:.4f}\n")
```

Write results to a file as you go. Don't collect them in a list or dict.

## If one record is huge (a whole chromosome, for example)

The generator above still builds each full sequence in memory. If a single record can be several GB, update the statistic line by line and never join the sequence:

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
