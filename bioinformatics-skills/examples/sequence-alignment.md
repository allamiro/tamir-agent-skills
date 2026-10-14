# `sequence-alignment`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Globally align GCATGCG and GATTACA with match +1, mismatch -1 and gap -1. Show the alignment, the score, and tell me whether the alignment is the only optimal one.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,747 | 1,667 |
| Input tokens read across all turns (including cached context) | 61,865 | 85,910 |
| Extra input tokens when the skill is installed | | +24,046 |
| Cost, US dollars at list price | 0.110 | 0.160 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 210 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
The best score is **0**, and the alignment is **not** the only optimal one. Three different alignments all score 0.

**One optimal alignment**

```
GCA-TGCG
| | |.|.
G-ATTACA
```

`|` is a match, `.` is a mismatch, and a blank is a gap.

Scoring it column by column: G/G +1, C/– −1, A/A +1, –/T −1, T/T +1, G/A −1, C/C +1, G/A −1. That is 4 matches (+4), 2 mismatches (−2) and 2 gaps (−2), for a total of **0**.

**The other two optimal alignments**

```
GCAT-GCG          GCATG-CG
| || .|.          | ||. |.
G-ATTACA          G-ATTACA
```

All three start the same way: G matches G, a gap in GATTACA lines up with the C, then A and T match. They differ only in where the second gap goes, inside GCATGCG. It can go before T, after T or after G, and each placement scores 0. When I traced back through the score table, all three branches came out as optimal.

**Score table** (rows: GCATGCG, columns: GATTACA, with the bottom-right cell holding the final score):

```
       -   G   A   T   T   A   C   A
   -   0  -1  -2  -3  -4  -5  -6  -7
   G  -1   1   0  -1  -2  -3  -4  -5
   C  -2   0   0  -1  -2  -3  -2  -3
   A  -3  -1   1   0  -1  -1  -2  -1
   T  -4  -2   0   2   1   0  -1  -2
   G  -5  -3  -1   1   1   0  -1  -2
   C  -6  -4  -2   0   0   0   1   0
   G  -7  -5  -3  -1  -1  -1   0   0
```

A standard aligner reports only one of the three, depending on how it breaks ties.
````

## Answer without the skill (excerpt)

````text
The best possible score is **0**, and the alignment is **not the only optimal one**: three different alignments all score 0.

**Dynamic-programming score matrix** (rows are GCATGCG, columns are GATTACA, scoring +1 for a match, −1 for a mismatch and −1 for a gap):

```
        -   G   A   T   T   A   C   A
    -   0  -1  -2  -3  -4  -5  -6  -7
    G  -1   1   0  -1  -2  -3  -4  -5
    C  -2   0   0  -1  -2  -3  -2  -3
    A  -3  -1   1   0  -1  -1  -2  -1
    T  -4  -2   0   2   1   0  -1  -2
    G  -5  -3  -1   1   1   0  -1  -2
    C  -6  -4  -2   0   0   0   1   0
    G  -7  -5  -3  -1  -1  -1   0   0
```

**One optimal alignment:**

```
G C A - T G C G
| . | . | . | .
G - A T T A C A
```

There are 4 matches (G, A, T, C) worth +4, 2 gaps worth −2, and 2 mismatches (G/A twice) worth −2. The total is **0**.

**The other optimal alignments.** Tracing back through every tied path in the matrix gives three alignments, each scoring 0:

```
1)  GCA-TGCG     2)  GCAT-GCG     3)  GCATG-CG
    G-ATTACA         G-ATTACA         G-ATTACA
```

All three delete the C from GCATGCG. They differ only in where the extra T of GATTACA goes:
- In alignment 1, the gap sits before GCATGCG's T. That T then matches the second T of TT.
- In alignment 2, the gap sits after GCATGCG's T. That T then matches the first T of TT.
- In alignment 3, the gap moves past the G as well. G/T becomes a mismatch, and A is left facing the gap. This swaps one mismatch for another, so the score stays 0.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
