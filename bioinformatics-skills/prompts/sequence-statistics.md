# `sequence-statistics` prompts

Put a number on "how surprising is this", with the null model written down, the tail chosen
correctly, and every test counted.

- **Give it:** the observation, the population it came from, what "just chance" means here, how
  many comparisons you made, and the base composition
- **Skill file:** [`skills/sequence-statistics/SKILL.md`](../skills/sequence-statistics/SKILL.md)
- **Null models and testing:** [`null-models-and-testing.md`](../skills/sequence-statistics/references/null-models-and-testing.md)
- **For entropy and conservation:** [`information-theory-sequences`](information-theory-sequences.md)

## 1. Count the possibilities

> How many sequences of length 2 are possible from 4 letters? Give the four counts: ordered or unordered, with or without replacement.

A good answer: 16 ordered with replacement, 12 ordered without, 6 unordered without, and 10
unordered with replacement.

## 2. Is a word over-represented

> The word GATC occurs 9 times in a 1,000-base sequence with 40% GC. How many would chance give, and is 9 surprising? Say which assumption fails for words that can overlap themselves.

A good answer: about 3.59 expected occurrences under independent positions, and an upper-tail
probability of roughly 0.011 for nine or more from the binomial. It notes that GATC cannot
overlap itself, so the overlap caveat is slight here, but would matter for a word such as AAAA or
ACAC, where a shuffle null is safer.

## 3. Drawing without replacement

> Ten genes were measured and four of them are in a gene set. I picked three of the ten and two were in the set. What is the probability of at least two, and which distribution is this?

A good answer: the hypergeometric distribution, P(exactly 2) = 0.30 and P(at least 2) = 1/3.

## 4. Many tests

> I tested four hypotheses and got p-values 0.01, 0.04, 0.03 and 0.005. Adjust them with Benjamini-Hochberg and with Bonferroni, and say which survive 0.05 under each.

A good answer: Benjamini-Hochberg gives 0.02, 0.04, 0.04, 0.02, so all four survive;
Bonferroni gives 0.04, 0.16, 0.12, 0.02, so only the first and fourth survive.

## 5. A Markov chain

> A two-state chain has transition rows (0.9, 0.1) and (0.5, 0.5). What fraction of time does it spend in each state in the long run, and when is that answer valid?

A good answer: 5/6 and 1/6, valid when every state can reach every other and the chain is not
periodic.

## 6. The best of many windows

> I report significant enrichment after trying 20 window sizes and keeping the best one. What is wrong with that, and how do I fix it?

A good answer: twenty looks, one reported, so the real false-positive rate is far above the
nominal one; count all 20 as tests, adjust for them, or choose the window size before looking.
