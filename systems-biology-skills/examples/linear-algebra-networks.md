# `linear-algebra-networks`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> What is the rank of the matrix with rows (1, 2) and (2, 4), and does the system x + 2y = 3, 2x + 4y = 6 have a unique solution? Use the Rouche-Capelli theorem.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 560 | 801 |
| Input tokens read across all turns (including cached context) | 30,382 | 36,395 |
| Extra input tokens when the skill is installed | | +6,013 |
| Cost, US dollars at list price | 0.071 | 0.124 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 1,700 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
The matrix has **rank 1**, and the system has **infinitely many solutions, so no unique solution**.

**Coefficient matrix and augmented matrix**

$$A = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}, \qquad [A\,|\,b] = \left(\begin{array}{cc|c} 1 & 2 & 3 \\ 2 & 4 & 6 \end{array}\right)$$

**Rank of A**

- det(A) = 1·4 − 2·2 = 0, so the rank is less than 2.
- A has a nonzero entry, so the rank is at least 1.
- Row 2 is 2 × row 1, so rank(A) = 1.

**Rank of [A | b]**

Subtract 2 × row 1 from row 2:

$$\left(\begin{array}{cc|c} 1 & 2 & 3 \\ 0 & 0 & 0 \end{array}\right)$$

The third column is also twice the first row's value (6 = 2·3), so the second row becomes all zeros. That gives rank([A | b]) = 1.

**Rouché–Capelli theorem**

With n = 2 unknowns:
- If rank(A) ≠ rank([A | b]), the system has no solution.
- If rank(A) = rank([A | b]) = n, it has a unique solution.
- If rank(A) = rank([A | b]) < n, it has infinitely many solutions, with n − r free parameters.

Here rank(A) = rank([A | b]) = 1 < 2, so the system is **consistent but underdetermined**. It has infinitely many solutions with 2 − 1 = 1 free parameter.

**Solution set**

Set y = t. Then x = 3 − 2t, so

$$\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 3 \\ 0 \end{pmatrix} + t\begin{pmatrix} -2 \\ 1 \end{pmatrix}, \quad t \in \mathbb{R}$$

Geometrically, the second equation is the first one multiplied by 2. Both describe the same line, so every point on that line is a solution.

If the right-hand side were changed to 7 instead of 6, the augmented matrix would have rank 2 and the coefficient matrix rank 1. The system would then have no solution: two parallel lines that never meet.
````

## Answer without the skill (excerpt)

````text
**The rank of A is 1, and the system has infinitely many solutions, so there is no unique solution.**

**Rank of the coefficient matrix**

A = [[1, 2], [2, 4]]

Row 2 is 2 × Row 1, and det(A) = 1·4 − 2·2 = 0. The matrix has a nonzero entry, so **rank(A) = 1**.

**Augmented matrix**

[A | b] = [[1, 2 | 3], [2, 4 | 6]]

Row 2 is still 2 × Row 1, because 6 = 2·3. Subtracting 2·R1 from R2 gives a zero row:

[[1, 2 | 3], [0, 0 | 0]]

So **rank([A | b]) = 1**.

**Applying the Rouché–Capelli theorem**

- The system is consistent if and only if rank(A) = rank([A | b]). Here 1 = 1, so a solution exists.
- The solution is unique only if the common rank equals the number of unknowns, n = 2. Here the rank is 1, which is less than 2, so there are infinitely many solutions.
- The solution set has n − r = 2 − 1 = 1 free parameter.

**General solution**

Let y = t. Then x = 3 − 2t, so (x, y) = (3 − 2t, t) for any t ∈ ℝ.

Geometrically, the second equation is the first one multiplied by 2. Both equations describe the same line.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
