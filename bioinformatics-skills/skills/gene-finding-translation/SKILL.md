---
name: gene-finding-translation
description: Works with DNA sequence at the gene level, covering reverse complement, GC content and skew, k-mer (word) counts, translation under the standard genetic code, six-frame translation, and open reading frames, with the limits of calling a gene from sequence alone. Use for "translate this DNA", "find the ORFs", "what is the reverse complement", "what is the GC content", "which frame is this gene in", "count the codons", "is this a gene". Use sequence-formats for reading the file and coordinates, sequence-alignment to find genes by similarity to known ones, information-theory-sequences for entropy, and sequence-statistics for whether an ORF could arise by chance.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Gene finding and translation

## Purpose and activation

Move from a DNA string to candidate coding regions and their protein sequences, and say how far
the evidence goes. A stretch of sequence with an unbroken reading frame is a candidate, not a gene.
Activate when the user has DNA and asks what it encodes, which strand or frame a gene is on, or how
to compute basic composition.

## Required inputs

The sequence and its strand; the organism or at least its domain, since gene structure and genetic
code differ (bacteria have no introns, eukaryotes do); the genetic code if not the standard one;
the minimum protein length of interest; and whether coordinates are needed and in which convention.

## Workflow

1. **Clean the sequence.** Upper-case, remove whitespace, treat U as T. Keep ambiguity codes.
2. **Describe composition.** `python3 scripts/genecode.py gc SEQ` gives GC fraction and skew.
   Composition changes how often stop codons appear by chance.
3. **Translate.** `translate SEQ --frame 1|2|3 [--strand -] [--to-stop]`. For an unknown frame
   translate all six (three frames on each strand) and look for the long unbroken one.
4. **Find ORFs.** `orfs SEQ --min-aa 100` lists start-to-stop frames on both strands with 1-based
   closed forward-strand coordinates that include the stop. Add `--starts ATG,TTG,CTG` to allow
   alternative starts.
5. **Set the length threshold against chance.** `python3 scripts/genecode.py chance --gc 0.7 --codons 100`
   gives the chance that 100 codons of random sequence hold no stop; `orfs` prints the same for its own
   cutoff and the sequence's GC. In a GC-rich genome long frames occur by chance far more often
   (`references/gene-finding-methods.md`).
6. **Look for support** beyond the frame: similarity to a known protein (`sequence-alignment`),
   a plausible start region and signals, codon usage like the rest of the genome, expression data.
7. **Count words if composition is the question:** `kmers SEQ --k 3` for codons in frame or `--k 4`
   for tetranucleotide bias. Overlapping counts are not codon counts; for codon usage translate in frame.
8. **Report as candidates** with coordinates, strand, length and the evidence level.

## Decision framework

| Situation | Do this |
|---|---|
| Bacterial or viral sequence, no known genes | ORF finding with a length cutoff set for the GC content, then similarity search |
| Eukaryotic genomic DNA | ORFs are fragments (exons); use a spliced-gene method, not this script alone |
| Known mRNA or cDNA | Translate from the first ATG; check the reading frame is long |
| Mitochondrial, some protists, mycoplasma | Not the standard code; look up the table (`references/genetic-code.md`) |
| ORF of a length that chance often gives at this GC content (table in `references/gene-finding-methods.md`) | Keep only with other evidence |
| GC-rich genome | Raise the cutoff; many long ORFs are not genes |
| Sequence may be on either strand | Run both strands; the script does |

## Implementation guidance

- Coordinates are 1-based closed on the forward strand with start less than end, including the stop
  codon; an ORF on the reverse strand is reported with forward coordinates and strand `-`. The
  self-test checks an asymmetric case so a wrong mapping would show.
- The protein printed is the literal translation, so an alternative start such as TTG shows as L.
  In a cell an initiator codon is read as methionine (VERIFY).
- Only the standard code is built in, and its 64 codons are checked in the self-test against the
  NCBI table codon by codon.
- ORFs are reported only when they reach a stop. A frame running off the end of the sequence is not
  listed, which can hide a gene that starts near the end of a contig.

## Failure and edge cases

- **ORF read as gene.** A frame can be open by chance; many genes are also missed.
- **Introns.** In eukaryotes the coding sequence is split; a frame stops at an intron boundary.
- **Overlapping genes and nested starts.** Only the outermost ORF from the first start is listed.
- **Wrong code.** Translating a mitochondrial gene with the standard code gives stops in the middle.
- **Frame shifts** from sequencing errors in homopolymers break one gene into two ORFs.
- **Partial codon at the end,** which the translation drops.
- **Strand confusion** between the gene's strand and the sequence file's.
- **Lower-case masking** removed by cleaning.
- **C-value paradox.** Genome size does not track organism complexity, so a large genome does not
  imply many genes.

## Validation

- `python3 scripts/genecode.py --selftest` must pass.
- Hand check: ATGAAATAG translates to MK*; in CCATGAAATAGCC the ORF is 3-11 on the forward strand.
- Hand check: the reverse complement of an ORF's sequence translates to the same protein when the
  ORF is on the `-` strand.
- Hand check: at 50% GC a codon is a stop with probability 3/64; at 70% GC it is 0.019125. The
  self-test also compares the formula with a simulated random sequence.
- Falsifier: shuffle the sequence; the ORF count at the same cutoff gives the chance level to
  compare against.

## Expected output

The candidate list: strand, 1-based coordinates, length in amino acids, protein sequence, the
evidence for each, the chance level at the cutoff used, and a plain statement that these are
candidates.

## Sources and confidence

- Genetic code table 1 (standard): NCBI genetic codes page, read 2026-10-14; the 64 codons checked
  against it in the self-test. The page marks TTG, CTG and ATG as possible initiators in table 1,
  and lists AGA and AGG as stops, AUA as Met and UGA as Trp in table 2 (vertebrate mitochondrial)
- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: ch. 1.1 (supplied) gives the central dogma,
  DNA to RNA to protein; chs. 10.3 to 10.6, 11.3 to 11.5, 13.1, 13.3 to 13.5 and 13.7 (genome and
  gene structure, DNA and amino acids, gene identification, extrinsic and intrinsic methods,
  nucleotide frequencies, word occurrences): section titles only, from the table of contents
- Chance-ORF figures in `references/gene-finding-methods.md`: computed by `genecode.py chance` from an
  independence model and checked against a simulation; real sequence is not independent
- Gene structure in different domains, initiator behaviour, codon usage: general knowledge, VERIFY
- Not covered: eukaryotic gene prediction, RNA genes, promoter and splice-site models, annotation
