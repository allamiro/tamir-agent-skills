# Construct modelling: the four building blocks

Paraphrased from the framework described by Wilson and Gochyyev (2013) in Teo's handbook, with examples
adapted to biology and systems biology teaching. No text is quoted.

## 1. Construct map

An ordered description of the property, from low to high, written on two sides: what respondents (or
samples) at each level are like, and what items (or readouts) at each level demand. Writing it forces three
commitments:

- **One dimension at a time** (unidimensionality): each respondent has one location on this map. If two
  properties are mixed, draw two maps.
- **Monotonicity:** a respondent higher on the map is more likely to give higher responses.
- **Theory behind the order:** the levels come from research (for example known misconceptions) and can be
  wrong, which the data will show.

Example (illustrative): understanding of steady state in a network course.

| Level | Student can | Typical item |
|---|---|---|
| 4 | Explain why N v = 0 defines the flux space and when the assumption fails | Critique a model that assumes steady state during a pulse |
| 3 | Compute steady-state fluxes and interpret the null space | Find the flux basis of a small network |
| 2 | Write balances for each metabolite | Set up dA/dt for a three-reaction network |
| 1 | Recognise "steady state" as "nothing changes" | Pick the steady-state graph from four time courses |
| 0 | Confuses steady state with equilibrium | (misconception detected by distractor choice) |

## 2. Items design

Each item targets a region of the map. Distractors in multiple-choice items can be written to match lower
levels (ordered multiple choice), so the wrong answer chosen locates the respondent. For an assay panel,
the analogue is choosing readouts whose dynamic range covers the levels of interest.

## 3. Outcome space

The set of categories responses are sorted into: finite, exhaustive, ordered (at least partially),
well-defined (definitions, exemplars, rater training), research-based and context-specific. Scoring assigns
numbers to the ordered categories so that they relate back to the map.

Missing responses: code "not administered" as missing; consider scoring a run of omitted hard items at the
end differently, and say which rule was used; always look for why responses are missing, because it can
reveal bad items.

## 4. Measurement model

Relates scores back to the map and gives distances between persons and items.

- **Classical test theory:** X = T + E. The true score T is the average over hypothetical repeated testing.
  Supports reliability (for example Cronbach's alpha) of the total score; says little about single items.
- **Rasch model:** P(X = 1 | θ, δ) = exp(θ − δ) / (1 + exp(θ − δ)), with person location θ and item location δ on
  the same scale. Assumes one dimension, equal discrimination for all items and local independence (given θ,
  responses to different items are independent). Fit statistics and residual correlations (Q3) test these.
- **Other IRT models** add discrimination or guessing parameters; more flexible, but persons and items are
  then no longer ordered the same way for every item.

## Listening to respondents

Think-aloud sessions (respondents speak while answering) and exit interviews (asked afterwards) show
whether responses arise from the intended reasoning. Record and document them: they are validity evidence
about response processes.

## Measurement levels and kinds

Nominal, ordinal, interval, ratio (Stevens). The level is a property of a model that fits the data, not
of the numbers themselves. Measurement can be fundamental (a physical concatenation exists, like length),
derived (computed from fundamental measures, like density) or implicit (a latent variable inferred
through a model, like most psychological and many biological constructs such as "pathway activity").
