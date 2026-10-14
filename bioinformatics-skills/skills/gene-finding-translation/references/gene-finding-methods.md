# Gene finding methods

## Two families

The source's chapter on genomics separates gene identification into extrinsic and intrinsic
methods (section titles in its table of contents; its text was not supplied).

| Family | Idea | Examples | Needs |
|---|---|---|---|
| Extrinsic | Compare with known sequences | Similarity to proteins, to expressed sequence tags, to other genomes | A reliable reference; database errors carry over |
| Intrinsic | Use the statistics of the sequence itself | Start and stop signals, codon usage, composition, hidden Markov models | Training data from the same organism |
| Minimalist | Use composition only | Nucleotide frequencies, word occurrences | Cheap, but weak evidence on its own |

Combined methods are normal. A candidate with both a long frame and similarity to a known protein
is far stronger than either alone.

## What an ORF finder can say

An open reading frame is a run of codons from a start to the next stop in one frame. It shows that
a frame is unbroken, which is expected of a real protein-coding gene, and nothing else: chance
produces open frames too.

## How often chance gives a long open frame

Model: independent bases with the given GC fraction (A and T equal, C and G equal). The chance that
a codon is a stop is p = P(TAA) + P(TAG) + P(TGA). A frame is open for at least L codons with
probability (1 - p) to the power L. Computed with `genecode.py chance` (the self-test checks the formula
against a simulated random sequence); run it with your own GC content and cutoff:

| GC | P(stop codon) | Mean codons to a stop | P(open for 30 codons) | P(open for 100 codons) |
|---|---|---|---|---|
| 0.3 | 0.0796 | 12.6 | 0.083 | 0.0003 |
| 0.4 | 0.0630 | 15.9 | 0.142 | 0.0015 |
| 0.5 | 0.0469 | 21.3 | 0.237 | 0.0082 |
| 0.6 | 0.0320 | 31.2 | 0.377 | 0.0387 |
| 0.7 | 0.0191 | 52.3 | 0.560 | 0.1450 |

Stop codons are AT-rich, so a GC-rich genome has fewer of them and longer chance frames. A length
cutoff that is safe at 40% GC lets many false ORFs through at 70% GC. Real sequence has structure
(codon bias, dependence between bases), so use these as a guide and confirm with shuffled data.

## Eukaryotes

Genes are split into exons separated by introns, which are removed from the RNA. A frame in the
genomic DNA ends at an intron boundary, so a plain ORF finder returns exon fragments and misses
genes. Use methods that model splice signals, or work from transcript sequence (VERIFY a tool).

## Composition and words

- GC content varies along a genome and between genomes; GC skew, (G - C) / (G + C), changes sign
  around the replication origin and terminus in many bacteria (VERIFY for your organism).
- Word counts (k-mers) describe composition and repeats. Codon usage is a count of in-frame
  triplets, which needs the frame, so translate or step by three, not a sliding window.

## Evidence ladder for a candidate gene

1. Long open frame (weak, especially in GC-rich genomes).
2. Plus start and stop context and codon usage like the rest of the genome.
3. Plus similarity to a protein from another organism.
4. Plus expression evidence for the region.
5. Plus functional evidence.
