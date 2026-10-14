# `stoichiometric-networks`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Build the stoichiometric matrix for R1: -> A, R2: A -> B, R3: A -> C, R4: B -> D, R5: C -> D, R6: D ->, give its rank and the steady-state flux space, and enumerate the elementary flux modes.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,517 | 1,605 |
| Input tokens read across all turns (including cached context) | 30,400 | 36,409 |
| Extra input tokens when the skill is installed | | +6,009 |
| Cost, US dollars at list price | 0.090 | 0.140 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I worked this out by hand. I took all reactions as irreversible, since every arrow points one way.

## Stoichiometric matrix N

Rows are metabolites and columns are reactions:

|       | R1 | R2 | R3 | R4 | R5 | R6 |
|-------|----|----|----|----|----|----|
| **A** |  1 | −1 | −1 |  0 |  0 |  0 |
| **B** |  0 |  1 |  0 | −1 |  0 |  0 |
| **C** |  0 |  0 |  1 |  0 | −1 |  0 |
| **D** |  0 |  0 |  0 |  1 |  1 | −1 |

## Rank

**rank(N) = 4**, so the matrix has full row rank.

To show the four rows are independent, suppose αA + βB + γC + δD = 0:
- The R1 column gives α = 0.
- The R6 column gives δ = 0.
- The R4 column gives β = δ = 0.
- The R5 column gives γ = δ = 0.

The consequences:
- **Left null space:** its dimension is 4 − 4 = 0, so the network has **no conservation relations**. This is expected for an open network with an uptake and an excretion reaction.
- **Right null space:** its dimension is 6 − 4 = **2**, so there are 2 independent steady-state fluxes.

## Steady-state flux space (Nv = 0)

The balance for each metabolite is:
- A: v₁ = v₂ + v₃
- B: v₂ = v₄
- C: v₃ = v₅
- D: v₆ = v₄ + v₅

Taking v₂ and v₃ as the free fluxes gives the null-space basis:

```
k1 = (1, 1, 0, 1, 0, 1)ᵀ     route through B
k2 = (1, 0, 1, 0, 1, 1)ᵀ     route through C
```

Every steady-state flux is v = a·k1 + b·k2, so v = (a+b, a, b, a, b, a+b)ᵀ.

Because all reactions are irreversible (v ≥ 0), the feasible fluxes form the convex cone with a, b ≥ 0. Two things always hold in this cone: v₁ = v₆, and the uptake splits between the two branches.

## Elementary flux modes

There are exactly **two** EFMs:

| EFM | Reactions | Vector (R1…R6) | Pathway |
|-----|-----------|----------------|---------|
| **E1** | R1, R2, R4, R6 | (1, 1, 0, 1, 0, 1) | → A → B → D → |
| **E2** | R1, R3, R5, R6 | (1, 0, 1, 0, 1, 1) | → A → C → D → |

Here is why these two are the complete set:
- **Each is elementary.** Removing any reaction from either support leaves no nonzero steady-state flux, so neither support can be made smaller.
- **There are no others.** Any other feasible flux has both a > 0 and b > 0. Its support then strictly contains the support of E1 and of E2, so it is not elementary.

In this network the EFMs are the same as the null-space basis vectors. That happens because the flux cone has only two extreme rays and the basis vectors already point along them. In larger networks the EFMs usually differ from a null-space basis and outnumber it.
````

## Answer without the skill (excerpt)

````text
## Stoichiometric matrix

Rows are metabolites A, B, C, D. Columns are reactions R1 to R6.

```
        R1  R2  R3  R4  R5  R6
   A  [  1  -1  -1   0   0   0 ]
   B  [  0   1   0  -1   0   0 ]
   C  [  0   0   1   0  -1   0 ]
   D  [  0   0   0   1   1  -1 ]
```

## Rank

**rank(S) = 4**, so the rows are linearly independent. To check this, set αA + βB + γC + δD = 0 and read off the columns:
- Column R1 gives α = 0.
- Column R6 gives δ = 0.
- Column R4 gives −β + δ = 0, so β = 0.
- Column R5 gives −γ + δ = 0, so γ = 0.

The null space therefore has dimension 6 − 4 = **2**. This network has no conserved moieties.

## Steady-state flux space

Setting S·v = 0 gives one balance per metabolite:
- A: v₁ = v₂ + v₃
- B: v₂ = v₄
- C: v₃ = v₅
- D: v₆ = v₄ + v₅

Choosing v₂ = a and v₃ = b as the free variables gives:

```
v = a·(1, 1, 0, 1, 0, 1)ᵀ + b·(1, 0, 1, 0, 1, 1)ᵀ
```

If all reactions are irreversible (a, b ≥ 0), the steady-state flux space is a pointed cone with two extreme rays.

## Elementary flux modes (all reactions irreversible)

| EFM | Vector (R1…R6) | Active reactions | Route |
|---|---|---|---|
| EFM1 | (1, 1, 0, 1, 0, 1) | R1, R2, R4, R6 | → A → B → D → |
| EFM2 | (1, 0, 1, 0, 1, 1) | R1, R3, R5, R6 | → A → C → D → |

Both have minimal support: removing any reaction from either one leaves no nonzero steady-state flux. Every feasible flux is a nonnegative combination of these two, written v = a·EFM1 + b·EFM2.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
