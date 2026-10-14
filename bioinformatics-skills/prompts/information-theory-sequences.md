# `information-theory-sequences` prompts

Measure how much structure a sequence carries, with the unit, the estimator, and a statement of
what the number does not mean.

- **Give it:** the sequences or alignment columns, the alphabet, and the question (composition,
  local complexity, conservation, dependence between positions, or distance)
- **Skill file:** [`skills/information-theory-sequences/SKILL.md`](../skills/information-theory-sequences/SKILL.md)
- **Formulas and worked values:** [`measures.md`](../skills/information-theory-sequences/references/measures.md)
- **For p-values and null models:** [`sequence-statistics`](sequence-statistics.md)

## 1. Entropy of a short sequence

> What is the Shannon entropy of the base composition of ACGTACGTAACCGGTT, and of its overlapping 2-mers? Give bits, the maximum possible in each case, and say how reliable the estimate is for a sequence this short.

A good answer: 2.0 bits for the bases (the maximum, since each base occurs four times), about
2.82 bits for the fifteen 2-mers against a maximum of 4, and a warning that fifteen observations
spread over sixteen possible 2-mers give a biased-low estimate.

## 2. What a low value does and does not mean

> A window of my genome has 1.2 bits of entropy per base. What does that tell me, what does it not tell me, and what should I compare it with before I call it interesting?

A good answer: composition bias or repeats, not function; a comparison with shuffled sequence of
the same composition and with other windows, and a note that a random sequence has maximal
entropy.

## 3. Diversity numbers

> Compute D0, D1 and D2 for the base frequencies of AACCCGGGGT and explain how they differ and why D0 is never smaller than D1 or D2.

A good answer: D0 = 4, D1 about 3.60, D2 about 3.33, with D1 and D2 weighting the abundant bases
more, and the ordering D0 >= D1 >= D2 explained by Jensen's inequality.

## 4. Do two positions vary together

> Here are two alignment columns, ACGTACGT and ACGTACGA. Compute their mutual information, and tell me why I should be careful trusting it from only eight sequences.

A good answer: about 1.66 bits, and a statement that plug-in mutual information from few
sequences is biased high, since random columns also show positive values.

## 5. Distance by compression

> Measure the compression distance between <sequence 1> and <sequence 2>. State the compressor, and say what limits the result for short sequences or for repeats that are far apart.

A good answer: a value between about 0 and 1, the compressor named (zlib), and the limits: fixed
overhead on short inputs and a window that cannot see distant repeats.

## 6. Bits to name one thing

> How many bits does it take to name one of 3 equally likely kinds, and one of 12? Compare with a case where three of the twelve are more likely than the rest.

A good answer: 1.585 and 3.585 bits, and 2.79 bits for the weighted case, which is lower because
the prior knowledge reduces what the measurement tells you.
