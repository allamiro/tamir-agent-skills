#!/usr/bin/env python3
"""Allele frequencies, Hardy-Weinberg, linkage disequilibrium and a minimal VCF reader (standard library only).

  popgen.py hwe AA Aa aa                  Hardy-Weinberg chi-square test for one biallelic locus
  popgen.py ld AB Ab aB ab                linkage disequilibrium D and r^2 from haplotype counts
  popgen.py vcf FILE                      genotype counts, allele frequency and HWE p-value per site
  popgen.py --selftest

VCF follows the specification (hts-specs VCFv4.3, read 2026-10-14): POS is 1-based; the genotype
GT field uses 0 for REF and 1 for the first ALT, "/" for unphased and "|" for phased, and "." for
missing. Only biallelic sites with a diploid GT are summarised; multi-allelic sites are reported
as skipped, not forced into two alleles.
The Hardy-Weinberg test is a large-sample chi-square approximation; with small counts an exact
test is the right tool (not implemented here).
"""
import argparse
import math
import sys


def allele_freq(n_aa, n_ab, n_bb):
    """Frequency of allele A from genotype counts AA, Aa, aa."""
    n = n_aa + n_ab + n_bb
    if min(n_aa, n_ab, n_bb) < 0 or n == 0:
        raise ValueError("genotype counts must be non-negative and not all zero")
    return (2 * n_aa + n_ab) / (2.0 * n)


def hwe_expected(n_aa, n_ab, n_bb):
    p = allele_freq(n_aa, n_ab, n_bb)
    n = n_aa + n_ab + n_bb
    return n * p * p, n * 2 * p * (1 - p), n * (1 - p) * (1 - p)


def chi2_sf_1df(x):
    """P(chi-square with 1 degree of freedom >= x) = erfc(sqrt(x / 2))."""
    if x < 0:
        raise ValueError("chi-square statistic cannot be negative")
    return math.erfc(math.sqrt(x / 2.0))


def hwe_test(n_aa, n_ab, n_bb):
    """(chi-square, p-value) against Hardy-Weinberg proportions, 1 degree of freedom.
    Returns (0.0, 1.0) when the locus is monomorphic, since there is nothing to test."""
    exp = hwe_expected(n_aa, n_ab, n_bb)
    if min(exp[0], exp[2]) == 0 and exp[1] == 0:
        return 0.0, 1.0
    obs = (n_aa, n_ab, n_bb)
    chi2 = sum((o - e) ** 2 / e for o, e in zip(obs, exp) if e > 0)
    return chi2, chi2_sf_1df(chi2)


def ld_stats(n_ab_hap, n_a_b, n_a_b2, n_a2_b2):
    """Haplotype counts AB, Ab, aB, ab -> (D, D', r^2)."""
    n = n_ab_hap + n_a_b + n_a_b2 + n_a2_b2
    if min(n_ab_hap, n_a_b, n_a_b2, n_a2_b2) < 0 or n == 0:
        raise ValueError("haplotype counts must be non-negative and not all zero")
    p_ab = n_ab_hap / n
    p_a = (n_ab_hap + n_a_b) / n
    p_b = (n_ab_hap + n_a_b2) / n
    d = p_ab - p_a * p_b
    denom = p_a * (1 - p_a) * p_b * (1 - p_b)
    if denom == 0:
        return d, 0.0, 0.0
    r2 = d * d / denom
    d_max = min(p_a * (1 - p_b), (1 - p_a) * p_b) if d >= 0 else min(p_a * p_b, (1 - p_a) * (1 - p_b))
    return d, (d / d_max if d_max else 0.0), r2


def parse_gt(gt):
    """Alleles of a diploid GT such as '0/1' or '1|1' as ints, None for '.'. Raises for other ploidy."""
    alleles = gt.replace("|", "/").split("/")
    if len(alleles) != 2:
        raise ValueError("only diploid genotypes are handled: %r" % gt)
    out = []
    for a in alleles:
        if a == ".":
            out.append(None)
        elif a.isdigit():
            out.append(int(a))
        else:
            raise ValueError("bad allele %r in genotype %r" % (a, gt))
    return out


def summarise_vcf_line(line):
    """Dict for one VCF record, or {'skipped': reason}. Counts are AA (ref/ref), Aa, aa (alt/alt)."""
    f = line.rstrip("\n").split("\t")
    if len(f) < 8:
        return {"skipped": "fewer than 8 columns"}
    chrom, pos, _id, ref, alt = f[0], f[1], f[2], f[3], f[4]
    if not pos.isdigit() or int(pos) < 1:
        return {"skipped": "POS is not a positive integer (it is 1-based)"}
    out = {"chrom": chrom, "pos": int(pos), "ref": ref, "alt": alt, "filter": f[6]}
    if "," in alt:
        out["skipped"] = "multi-allelic site"
        return out
    if len(f) < 10 or "GT" not in f[8].split(":"):
        out["skipped"] = "no genotypes"
        return out
    idx = f[8].split(":").index("GT")
    hom_ref = het = hom_alt = missing = 0
    for sample in f[9:]:
        parts = sample.split(":")
        gt = parts[idx] if idx < len(parts) else "."
        a1, a2 = parse_gt(gt)
        if a1 is None or a2 is None:
            missing += 1
        elif a1 > 1 or a2 > 1:
            out["skipped"] = "allele index above 1 at a biallelic site"
            return out
        elif a1 == a2 == 0:
            hom_ref += 1
        elif a1 == a2 == 1:
            hom_alt += 1
        else:
            het += 1
    called = hom_ref + het + hom_alt
    out.update({"hom_ref": hom_ref, "het": het, "hom_alt": hom_alt, "missing": missing})
    if called:
        out["alt_freq"] = 1 - allele_freq(hom_ref, het, hom_alt)
        out["hwe_p"] = hwe_test(hom_ref, het, hom_alt)[1]
    return out


def selftest():
    n = [0]

    def check(name, got, want, tol=None):
        n[0] += 1
        ok = (abs(got - want) <= tol) if tol is not None else got == want
        if not ok:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    def raises(name, fn):
        n[0] += 1
        try:
            fn()
        except ValueError:
            return
        raise AssertionError("%s: expected ValueError" % name)

    check("allele frequency", allele_freq(36, 48, 16), 0.6, 1e-12)
    check("all homozygous A", allele_freq(10, 0, 0), 1.0)
    exp = hwe_expected(36, 48, 16)
    check("expected AA", exp[0], 36.0, 1e-9)
    check("expected Aa", exp[1], 48.0, 1e-9)
    check("expected aa", exp[2], 16.0, 1e-9)
    chi2, p = hwe_test(36, 48, 16)
    check("chi-square at HWE is 0", chi2, 0.0, 1e-9)
    check("p-value at HWE is 1", p, 1.0, 1e-9)
    chi2, p = hwe_test(50, 0, 50)  # p = 0.5: expected 25, 50, 25 -> 25 + 50 + 25
    check("no heterozygotes at all: chi-square 100", chi2, 100.0, 1e-9)
    check("no heterozygotes: tiny p", p < 1e-20, True)
    check("1 df critical value 3.841 gives p = 0.05", chi2_sf_1df(3.841459), 0.05, 1e-5)
    check("1 df critical value 6.635 gives p = 0.01", chi2_sf_1df(6.634897), 0.01, 1e-5)
    check("1 df, chi-square 0 gives p = 1", chi2_sf_1df(0.0), 1.0)
    check("monomorphic locus is not tested", hwe_test(20, 0, 0), (0.0, 1.0))
    raises("negative counts", lambda: allele_freq(-1, 2, 3))
    raises("all zero", lambda: allele_freq(0, 0, 0))
    raises("negative chi-square", lambda: chi2_sf_1df(-0.1))
    # Linkage disequilibrium, hand-computed: pAB = 0.4, pA = pB = 0.5, D = 0.15, r^2 = 0.0225 / 0.0625.
    d, dprime, r2 = ld_stats(40, 10, 10, 40)
    check("D", d, 0.15, 1e-12)
    check("r^2", r2, 0.36, 1e-12)
    check("D' = D / Dmax = 0.15 / 0.25", dprime, 0.6, 1e-12)
    # Unequal allele frequencies (pA = 0.4, pB = 0.5), so D' needs the right D max.
    d, dprime, r2 = ld_stats(30, 10, 20, 40)
    check("D with unequal frequencies", d, 0.10, 1e-12)
    check("D' = 0.10 / min(0.2, 0.3) = 0.5", dprime, 0.5, 1e-12)
    check("r^2 = 0.01 / 0.06", r2, 1 / 6, 1e-12)
    d, dprime, r2 = ld_stats(10, 30, 40, 20)
    check("negative D", d, -0.10, 1e-12)
    check("negative D' = -0.10 / min(0.2, 0.3) = -0.5", dprime, -0.5, 1e-12)
    d, dprime, r2 = ld_stats(25, 25, 25, 25)
    check("independent loci D", d, 0.0, 1e-12)
    check("independent loci r^2", r2, 0.0, 1e-12)
    check("complete LD gives r^2 = 1", ld_stats(50, 0, 0, 50)[2], 1.0, 1e-12)
    check("a fixed locus has no LD", ld_stats(50, 50, 0, 0)[2], 0.0)
    raises("negative haplotypes", lambda: ld_stats(-1, 1, 1, 1))
    # Genotypes and VCF.
    check("unphased het", parse_gt("0/1"), [0, 1])
    check("phased hom alt", parse_gt("1|1"), [1, 1])
    check("missing", parse_gt("./."), [None, None])
    check("half missing", parse_gt("0/."), [0, None])
    raises("haploid", lambda: parse_gt("1"))
    raises("bad allele", lambda: parse_gt("0/x"))
    line = "chr1\t100\trs1\tA\tG\t50\tPASS\t.\tGT:DP\t0/0:10\t0/1:12\t1/1:9\t./.:0\t0|1:11"
    s = summarise_vcf_line(line)
    check("VCF position is kept 1-based", s["pos"], 100)
    check("VCF counts", (s["hom_ref"], s["het"], s["hom_alt"], s["missing"]), (1, 2, 1, 1))
    check("VCF alt frequency", s["alt_freq"], (2 * 1 + 2) / 8.0, 1e-12)
    check("VCF HWE p is a probability", 0 <= s["hwe_p"] <= 1, True)
    check("VCF filter kept", s["filter"], "PASS")
    check("multi-allelic skipped", summarise_vcf_line("chr1\t5\t.\tA\tG,T\t.\t.\t.\tGT\t0/1")["skipped"], "multi-allelic site")
    check("no genotype column skipped", summarise_vcf_line("chr1\t5\t.\tA\tG\t.\t.\t.")["skipped"], "no genotypes")
    check("POS 0 refused", "1-based" in summarise_vcf_line("chr1\t0\t.\tA\tG\t.\t.\t.\tGT\t0/1")["skipped"], True)
    check("GT in the second FORMAT slot", summarise_vcf_line("c\t7\t.\tA\tG\t.\t.\t.\tDP:GT\t5:0/1")["het"], 1)
    check("allele index above 1 refused", "above 1" in summarise_vcf_line("c\t7\t.\tA\tG\t.\t.\t.\tGT\t0/2")["skipped"], True)
    check("all missing: no frequency", "alt_freq" in summarise_vcf_line("c\t7\t.\tA\tG\t.\t.\t.\tGT\t./.\t./."), False)
    print("popgen.py self-test: %d checks passed" % n[0])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Allele frequencies, Hardy-Weinberg, LD and a minimal VCF reader.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("hwe")
    for name in ("AA", "Aa", "aa"):
        s.add_argument(name, type=int)
    s = sub.add_parser("ld")
    for name in ("AB", "Ab", "aB", "ab"):
        s.add_argument(name, type=int)
    sub.add_parser("vcf").add_argument("file")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    try:
        if a.cmd == "hwe":
            counts = (a.AA, a.Aa, a.aa)
            chi2, p = hwe_test(*counts)
            exp = hwe_expected(*counts)
            print("allele A frequency %.4f; expected %.1f %.1f %.1f; chi-square %.3f (1 df), p = %.4g" % (
                allele_freq(*counts), exp[0], exp[1], exp[2], chi2, p))
        elif a.cmd == "ld":
            d, dprime, r2 = ld_stats(a.AB, a.Ab, a.aB, a.ab)
            print("D %.4f  D' %.4f  r^2 %.4f" % (d, dprime, r2))
        elif a.cmd == "vcf":
            with open(a.file, encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("#") or not line.strip():
                        continue
                    s = summarise_vcf_line(line)
                    if "skipped" in s:
                        print("%s:%s skipped (%s)" % (s.get("chrom", "?"), s.get("pos", "?"), s["skipped"]))
                    else:
                        print("%s:%d %s>%s hom_ref %d het %d hom_alt %d missing %d alt_freq %s HWE p %s" % (
                            s["chrom"], s["pos"], s["ref"], s["alt"], s["hom_ref"], s["het"], s["hom_alt"], s["missing"],
                            "%.3f" % s["alt_freq"] if "alt_freq" in s else "n/a",
                            "%.3g" % s["hwe_p"] if "hwe_p" in s else "n/a"))
        else:
            ap.print_help()
            return 2
    except (ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
