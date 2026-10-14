# `gene-finding-translation` prompts

Move from DNA to candidate coding regions: reverse complement, composition, translation, and open
reading frames, with the limits of calling a gene from sequence alone.

- **Give it:** the sequence and strand, the organism or domain, the genetic code if it is not the
  standard one, and the minimum protein length you care about
- **Skill file:** [`skills/gene-finding-translation/SKILL.md`](../skills/gene-finding-translation/SKILL.md)
- **References:** [`genetic-code.md`](../skills/gene-finding-translation/references/genetic-code.md) and
  [`gene-finding-methods.md`](../skills/gene-finding-translation/references/gene-finding-methods.md)
- **Before it:** [`sequence-formats`](sequence-formats.md) · **For evidence:** [`sequence-alignment`](sequence-alignment.md)

## 1. Translate a short sequence

> Translate ATGAAATAG in frame 1 under the standard genetic code and tell me what each symbol in the answer means.

A good answer: `MK*`, with M for methionine, K for lysine and `*` for a stop codon.

## 2. Find the ORFs

> Find every open reading frame of at least 2 amino acids in CATGAAATAGCCCC on both strands. Give 1-based coordinates on the forward strand, say whether each includes the stop codon, and give the protein.

A good answer: one ORF on the forward strand at 2 to 10, including the stop, with protein MK.

## 3. Reverse complement with ambiguity codes

> Give the reverse complement of ATGCRY and say what R and Y complement to.

A good answer: RYGCAT, with R (A or G) pairing to Y (C or T) and the other way round.

## 4. Is a long ORF a gene

> I found a 120-codon open reading frame in a genome that is 70% GC. Is that evidence of a gene? Give the chance level and say what else I should look for.

A good answer: under an independent-bases model about 10% of frames stay open that long by
chance in a 70% GC genome, so the frame alone is weak; look for similarity to a known protein,
codon usage like the rest of the genome, and expression.

## 5. Composition

> What are the GC content and the GC skew of GGGCAATT? Define skew, and say what I can and cannot conclude from one short sequence.

A good answer: GC content 0.5 and skew (G - C) / (G + C) = 0.5, with a caution that eight bases
say nothing about a genome.

## 6. Not the standard code

> My sequence comes from human mitochondria. Can I translate it with the standard code? Tell me what differs and where to look it up.

A good answer: not safely; the NCBI page lists vertebrate mitochondrial code differences (AGA and
AGG as stops, ATA as Met, TGA as Trp), and the script supports only the standard table.
