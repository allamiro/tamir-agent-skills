#!/usr/bin/env python3
"""Run the commands behind the exercises and the prompts' "a good answer" lines (standard library only).

Two kinds of check, both mechanical:
  1. every row of skills/bioinformatics-learning-path/references/exercises.md: run its command and
     confirm the output contains the expected text;
  2. the computable "a good answer" lines in prompts/*.md: run the script and confirm the output
     contains the expected text, and that the number quoted in the prompt really appears in the
     prompt's own good-answer paragraph, so the prose and the computation cannot drift apart.

This checks the scripts and the answer key. It does not run any AI agent.

Usage: python3 scripts/check_answers.py [--verbose]
"""
import argparse
import glob
import os
import re
import shlex
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SCRIPTS = {os.path.basename(p): p for p in glob.glob(os.path.join(ROOT, "skills", "*", "scripts", "*.py"))}
EXERCISE_ROW = re.compile(r"^\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*$")

RESULTS9 = "dataset,method,score\n" + "".join("d%d,A,%s\nd%d,B,%s\n" % (i, a, i, b) for i, (a, b) in enumerate(
    [(0.9, 0.8), (0.8, 0.7), (0.7, 0.6), (0.9, 0.7), (0.8, 0.6), (0.7, 0.5), (0.9, 0.85), (0.6, 0.7), (0.5, 0.6)]))
SCHEDULE = "task,weeks,after\ndata access,6,\nquality control,2,data access\nalignment,3,quality control\nstatistics,4,alignment\nwriting,5,statistics\nfigures,2,statistics\n"
THIN_DMP = "We will share the data upon request. TBD.\n"
REFS = "Gardiner, A. H. Egyptian Grammar. Oxford, 1957.\nNobody, N. 2019. A new result. J Imaginary Biol 5:1-9. doi:10.1000/imaginary.2019.1\n"
MATRIX = ",A,B,C,D\nA,0,2,4,6\nB,2,0,4,6\nC,4,4,0,6\nD,6,6,6,0\n"
CONFOUNDED = "sample,group,day\n" + "".join("c%d,control,mon\n" % i for i in range(5)) + "".join("t%d,treated,tue\n" % i for i in range(5))
SHEET12 = "sample,group\n" + "".join("t%d,treated\n" % i for i in range(6)) + "".join("c%d,control\n" % i for i in range(6))
IDS = "NM_000546.6\nNM_000546\nP12345\nzzz\n"
VCF = ("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1\ts2\ts3\n"
       "chr1\t100\t.\tA\tG\t50\tPASS\t.\tGT\t0/0\t0/1\t1/1\n")

# (prompt file, prompt number, files to create, command, text the output must contain, text the prompt must mention)
PROMPT_CHECKS = [
    ("information-theory-sequences", 1, {}, "seqinfo.py entropy ACGTACGTAACCGGTT", "entropy 2.0000 bits", "2.0 bits"),
    ("information-theory-sequences", 1, {}, "seqinfo.py entropy ACGTACGTAACCGGTT --k 2", "entropy 2.8226 bits", "2.82"),
    ("information-theory-sequences", 3, {}, "seqinfo.py hill AACCCGGGGT", "D0 4.0000  D1 3.5961  D2 3.3333", "3.60"),
    ("information-theory-sequences", 4, {}, "seqinfo.py mi ACGTACGT ACGTACGA", "1.6556 bits", "1.66"),
    ("information-theory-sequences", 6, {}, "seqinfo.py bits 3", "1.5850 bits", "1.585"),
    ("information-theory-sequences", 6, {}, "seqinfo.py bits 12", "3.5850 bits", "3.585"),
    ("sequence-statistics", 1, {}, "seqstats.py sampling 4 2", "unordered, with replacement      10", "16 ordered with replacement"),
    ("sequence-statistics", 1, {}, "seqstats.py sampling 4 2", "ordered, without replacement     12", "12 ordered without"),
    ("sequence-statistics", 2, {}, "seqstats.py expect 1000 GATC --gc 0.4", "3.5892", "3.59"),
    ("sequence-statistics", 2, {}, "seqstats.py binom 997 9 0.0036", "0.0113167", "0.011"),
    ("sequence-statistics", 3, {}, "seqstats.py hypergeom 10 4 3 2", "P(X >= 2) = 0.333333", "1/3"),
    ("sequence-statistics", 4, {}, "seqstats.py adjust 0.01 0.04 0.03 0.005", "0.005 -> 0.02", "0.02, 0.04, 0.04, 0.02"),
    ("sequence-statistics", 4, {}, "seqstats.py adjust 0.01 0.04 0.03 0.005 --method bonferroni", "0.04 -> 0.16", "0.04, 0.16, 0.12, 0.02"),
    ("sequence-statistics", 5, {}, "seqstats.py stationary \"0.9,0.1;0.5,0.5\"", "0.833333, 0.166667", "5/6 and 1/6"),
    ("sequence-alignment", 1, {}, "align.py global GCATGCG GATTACA --match 1 --mismatch=-1 --gap=-1", "score 0", "score of 0"),
    ("sequence-alignment", 2, {}, "align.py local TTACGTT ACGT --match 1 --mismatch=-1 --gap=-1", "score 4", "score of 4"),
    ("sequence-formats", 3, {}, "seqformats.py coords bed2gff 2 5", "3 5", "BED 2-5 is GFF3 3-5"),
    ("sequence-formats", 3, {}, "seqformats.py coords gff2bed 3 5", "2 5", "BED 2-5 is GFF3 3-5"),
    ("gene-finding-translation", 1, {}, "genecode.py translate ATGAAATAG", "MK*", "MK*"),
    ("gene-finding-translation", 2, {}, "genecode.py orfs CATGAAATAGCCCC --min-aa 2", "+ 2-10 2 aa  MK", "2 to 10"),
    ("gene-finding-translation", 3, {}, "genecode.py revcomp ATGCRY", "RYGCAT", "RYGCAT"),
    ("gene-finding-translation", 5, {}, "genecode.py gc GGGCAATT", "GC 0.5000   skew 0.5000", "0.5"),
    ("gene-finding-translation", 4, {}, "genecode.py chance --gc 0.7 --codons 120", "P(120 codons with no stop) = 0.0985", "10%"),
    ("phylogenetics", 1, {}, "tree.py jc ACGTACGTAC ACGTACGTAA", "p-distance 0.100000   Jukes-Cantor 0.107326", "0.107"),
    ("phylogenetics", 2, {"m.csv": MATRIX}, "tree.py upgma {m.csv}", "(((A:1,B:1):1,C:2):1,D:3);", "(((A:1,B:1):1,C:2):1,D:3);"),
    ("phylogenetics", 3, {"m.csv": MATRIX}, "tree.py nj {m.csv}", "((A:1,B:1):1,C:2,D:4);", "((A:1,B:1):1,C:2,D:4);"),
    ("experimental-design", 1, {}, "design.py n --d 0.5", "64 per group", "64 per group"),
    ("experimental-design", 1, {}, "design.py n --d 0.5 --tests 20000", "252 per group", "250 per group"),
    ("experimental-design", 3, {"s.csv": SHEET12}, "design.py assign {s.csv} --batches 3 --seed 1", "sample,group,batch", "2 treated and 2 control"),
    ("experimental-design", 4, {"s.csv": CONFOUNDED}, "design.py confound {s.csv} --group group --batch day", "perfectly confounded: True", "Cramer's V is 1"),
    ("biological-databases", 1, {}, "accessions.py classify NM_000546.6", "version 6", "version 6"),
    ("biological-databases", 2, {}, "accessions.py classify P12345", "UniProtKB", "fits both"),
    ("biological-databases", 3, {"ids.txt": IDS}, "accessions.py check {ids.txt}", "NM_000546: no version suffix", "without a version"),
    ("ngs-pipelines", 1, {}, "ngs.py flags 99", "proper", "1 + 2 + 32 + 64"),
    ("ngs-pipelines", 1, {}, "ngs.py flags 147", "SEQ being reverse complemented", "147"),
    ("ngs-pipelines", 2, {}, "ngs.py cigar 5S10M3D10M2S --pos 100", "end 122", "122"),
    ("ngs-pipelines", 3, {}, "ngs.py coverage --reads 1000000 --length 150 --genome 5000000", "mean depth 30.00x", "30-fold"),
    ("ngs-pipelines", 4, {}, "ngs.py reads-needed --depth 30 --length 150 --genome 5000000", "1000000 reads", "1,000,000"),
    ("variants-population-genetics", 2, {}, "popgen.py hwe 36 48 16", "chi-square 0.000", "chi-square 0"),
    ("variants-population-genetics", 3, {}, "popgen.py hwe 50 0 50", "chi-square 100.000", "chi-square 100"),
    ("variants-population-genetics", 4, {}, "popgen.py ld 40 10 10 40", "D 0.1500  D' 0.6000  r^2 0.3600", "D = 0.15"),
    ("variants-population-genetics", 1, {"t.vcf": VCF}, "popgen.py vcf {t.vcf}", "chr1:100", "1-based"),
    ("protein-analysis", 1, {}, "protein.py mass DRVYIHPF --mono", "1045.5345 Da", "1045.5345"),
    ("machine-learning-biology", 2, {}, "mlmetrics.py auc 0,0,1,1 0.1,0.4,0.35,0.8", "AUROC 0.7500   average precision 0.8333", "0.8333"),
    ("machine-learning-biology", 4, {}, "mlmetrics.py metrics 1,1,1,1,1,1,0,0,0,0 1,1,1,1,1,0,1,0,0,0", "mcc                0.5833", "0.583"),
    ("machine-learning-biology", 1, {}, "mlmetrics.py metrics " + ",".join(["0"] * 98 + ["1"] * 2) + " " + ",".join(["0"] * 100), "accuracy           0.9800", "98%"),
    ("bioinformatics-programming", 2, {}, "bioprog.py logsumexp -1000 -1000", "-999.3068528", "log-sum-exp"),
    ("bioinformatics-programming", 3, {}, "bioprog.py pack ACGTACGTAC", "10 bases in 3 bytes", "3 bytes"),
    ("method-benchmarking", 1, {}, "benchstats.py min-diff --n 200 --acc 0.8", "about 0.112", "11 points"),
    ("method-benchmarking", 2, {}, "benchstats.py chance-gap --n 200 --k 10 --acc 0.8", "the best looks 0.04", "4 points"),
    ("method-benchmarking", 5, {"r.csv": RESULTS9}, "benchstats.py compare {r.csv} --a A --b B", "A better on 7, tied on 0, B better on 2; exact sign test p = 0.1797", "0.18"),
    ("research-proposal-planning", 2, {"p.csv": SCHEDULE}, "schedule.py {p.csv} --deadline 24", "critical path: data access -> quality control -> alignment -> statistics -> writing", "20 weeks"),
    ("research-proposal-planning", 2, {"p.csv": SCHEDULE}, "schedule.py {p.csv} --deadline 24", "total 20 weeks; with a 30% buffer 26 weeks", "26 week"),
    ("research-proposal-planning", 2, {"p.csv": SCHEDULE}, "schedule.py {p.csv} --deadline 24", "does NOT fit, short by 2 weeks", "does not fit"),
    ("research-proposal-planning", 3, {"d.md": THIN_DMP}, "dmpcheck.py {d.md}", "access is offered upon request and no repository is named", "upon request"),
    ("literature-search-appraisal", 2, {"refs.txt": REFS}, "citecheck.py {refs.txt}", "DOI-SYNTAX-OK", "DOI"),
]


def run(command, files, workdir):
    for name, text in files.items():
        with open(os.path.join(workdir, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    command = re.sub(r"\{([^}]+)\}", lambda m: os.path.join(workdir, m.group(1)), command)
    parts = shlex.split(command)
    script = SCRIPTS.get(parts[0])
    if script is None:
        return None, "no script named %s under skills/*/scripts/" % parts[0]
    r = subprocess.run([sys.executable, "-I", script] + parts[1:], capture_output=True, text=True, timeout=120)
    return r.stdout + r.stderr, None


def good_answer(stem, number):
    """The 'A good answer:' paragraph of prompt `number` in prompts/<stem>.md, or None."""
    path = os.path.join(ROOT, "prompts", stem + ".md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^## %d\. .*?$(.*?)(?=^## |\Z)" % number, text, re.M | re.S)
    if not m:
        return None
    g = re.search(r"A good answer:(.*)", m.group(1), re.S)
    return " ".join(g.group(1).split()) if g else None


def main():
    ap = argparse.ArgumentParser(description="Check the exercise answers and the prompts' good-answer lines.")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    failures, passed = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        ex_path = os.path.join(ROOT, "skills", "bioinformatics-learning-path", "references", "exercises.md")
        rows = []
        with open(ex_path, encoding="utf-8") as fh:
            for line in fh:
                m = EXERCISE_ROW.match(line.rstrip("\n"))
                if m:
                    rows.append((int(m.group(1)), m.group(2), m.group(3)))
        if len(rows) < 20:
            failures.append(("exercises", "found only %d exercise rows in exercises.md" % len(rows)))
        for number, command, expected in rows:
            out, problem = run(command, {}, tmp)
            ok = problem is None and expected in out
            if a.verbose:
                print("exercise %-2d %s  %s" % (number, "PASS" if ok else "FAIL", command))
            if ok:
                passed += 1
            else:
                failures.append(("exercise %d" % number, problem or "output lacks %r: %r" % (expected, out.strip()[:200])))
        for stem, number, files, command, expected, mention in PROMPT_CHECKS:
            label = "%s #%d" % (stem, number)
            out, problem = run(command, files, tmp)
            ok = problem is None and expected in out
            why = problem or ("output lacks %r: %r" % (expected, out.strip()[:200]) if not ok else None)
            if ok and mention:
                prose = good_answer(stem, number)
                if prose is None:
                    ok, why = False, "no 'A good answer' paragraph found for prompt %d" % number
                elif mention not in prose:
                    ok, why = False, "the prompt's good answer does not mention %r" % mention
            if a.verbose:
                print("prompt %-40s %s  %s" % (label, "PASS" if ok else "FAIL", command[:60]))
            if ok:
                passed += 1
            else:
                failures.append((label, why))
    for label, why in failures:
        print("FAIL %s: %s" % (label, why))
    print("%d answer checks passed, %d failed" % (passed, len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
