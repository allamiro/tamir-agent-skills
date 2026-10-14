# `variants-population-genetics`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> What do the columns of this VCF line mean, including the genotype codes? chr1    100    .    A    G    50    PASS    .    GT:DP    0/1:12    1|1:9. Is the position 0-based or 1-based?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 968 | 1,467 |
| Input tokens read across all turns (including cached context) | 30,388 | 48,450 |
| Extra input tokens when the skill is installed | | +18,062 |
| Cost, US dollars at list price | 0.079 | 0.141 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 230 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
## Column by column

| # | Column | Value | Meaning |
|---|---|---|---|
| 1 | CHROM | `chr1` | Chromosome or contig name. It must match the reference the calls were made against. `chr1` is UCSC/GRCh-style naming; Ensembl would write `1`. |
| 2 | POS | `100` | Position of the first base of REF on that contig. |
| 3 | ID | `.` | Variant identifier, such as an rsID like `rs12345`. `.` means none was given. |
| 4 | REF | `A` | Reference allele, the base(s) in the reference genome at POS. |
| 5 | ALT | `G` | Alternate allele(s), comma-separated if there are several. This line is a single-nucleotide A→G substitution. |
| 6 | QUAL | `50` | Phred-scaled quality of the claim that an ALT allele is present: P(wrong) = 10^(−50/10) = 10⁻⁵. It applies to the site, not to each sample. |
| 7 | FILTER | `PASS` | `PASS` means every filter in the file was passed. Otherwise it lists the failed filter names, and `.` means no filters were applied. |
| 8 | INFO | `.` | Site-level annotations as `KEY=value;...`, such as AF, DP or AC. `.` means it's empty. |
| 9 | FORMAT | `GT:DP` | The order of the per-sample fields that follow: genotype, then read depth. |
| 10 | Sample 1 | `0/1:12` | GT = `0/1`, DP = 12 |
| 11 | Sample 2 | `1\|1:9` | GT = `1\|1`, DP = 9 |

The sample names aren't in the line itself. They come from the `#CHROM ... FORMAT sample1 sample2` header line.

## Genotype codes

The numbers are allele indices: **0 = REF** (`A`), **1 = the first ALT** (`G`), 2 = the second ALT, and so on. `.` means a missing allele, for example `./.`.

The separator says whether the genotype is phased:
- **`/` = unphased.** The individual carries these alleles, but the data don't say which one is on which parental chromosome.
- **`|` = phased.** The left allele is on haplotype 1 and the right on haplotype 2, consistently across other phased sites in the same phase set.

For this line:
- **Sample 1, `0/1:12`:** heterozygous A/G, unphased, with 12 reads covering the site.
- **Sample 2, `1|1:9`:** homozygous alternate G/G, written as phased, with 9 reads. For a homozygote the phasing is trivial, because both haplotypes carry G either way.

Mixing `/` and `|` in one record is allowed, because phasing is recorded per sample.

DP in FORMAT is per-sample depth after the caller's filtering. That can differ from INFO/DP, which is usually the total across samples. Low depth such as 9–12 reads is often a reason to look at GQ or AD (allelic depths) before trusting a genotype, but this record doesn't include those fields.

## 0-based or 1-based?

**VCF POS is 1-based.** `100` means the 100th base of chr1, the first base being 1. For indels, POS points to the padding base before the event, and that base is included in both REF and ALT.

That's the opposite of BED, which is 0-based and half-open. The same SNP in BED would be `chr1 99 100`. BCF, the binary form of VCF, also stores positions 0-based internally, but tools like bcftools convert them back to 1-based when they display them. Mixing these conventions up is a common cause of off-by-one errors when intersecting VCFs with BED files.
````

## Answer without the skill (excerpt)

````text
**Columns.** A VCF data line has 8 fixed tab-separated columns, then a FORMAT column, then one column per sample:

| # | Column | Value | Meaning |
|---|--------|-------|---------|
| 1 | CHROM | `chr1` | Chromosome or contig name |
| 2 | POS | `100` | Position of the first base in REF |
| 3 | ID | `.` | Variant ID, such as a dbSNP rsID. `.` means missing |
| 4 | REF | `A` | Reference allele |
| 5 | ALT | `G` | Alternate allele(s), separated by commas if there are several |
| 6 | QUAL | `50` | Phred-scaled quality score. 50 means about a 1 in 100,000 chance the variant call is wrong |
| 7 | FILTER | `PASS` | Passed all filters. Otherwise this lists the names of the filters that failed |
| 8 | INFO | `.` | Site-level annotations as `KEY=value;...`. Here it is empty |
| 9 | FORMAT | `GT:DP` | Says how to read each sample column: genotype, then read depth |
| 10 | Sample 1 | `0/1:12` | GT=`0/1`, DP=12 |
| 11 | Sample 2 | `1\|1:9` | GT=`1\|1`, DP=9 |

**Genotype (GT) codes.** Each number is an allele index:
- `0` = REF (A)
- `1` = the first ALT (G)
- `2` would be the second ALT, and so on
- `.` = missing call

The separator tells you about phasing:
- `/` means **unphased**. You know which alleles are present but not which chromosome copy carries each.
- `|` means **phased**. The left allele is on one haplotype and the right allele is on the other, consistently across sites.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
