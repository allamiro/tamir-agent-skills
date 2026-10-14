# Testing scientific code

Scientific code often has no obvious "expected output", so a test needs a source of truth that is
independent of the code under test. Five sources, in rough order of strength.

| Source of truth | Example | Strength |
|---|---|---|
| A hand-computed answer | Entropy of AACC is 1 bit; BED 0-100 is GFF 1-100 | Strong, but only for small cases |
| A second, independent implementation | An exhaustive search over every alignment against the dynamic-programming table | Strong; the two must not share the same logic |
| A property that must hold | Reverse complement twice returns the input; the sum of a distribution is 1; D0 >= D1 >= D2 | Good; catches whole classes of error |
| Synthetic data with a planted answer | Build a tree, derive its distances, check that the method recovers the tree | Strong for methods; shows the method can find the truth |
| A published or fetched reference | A genetic-code table fetched from NCBI compared codon by codon | Good; record the source and date |

## Make the test able to fail

A test that has never failed has not been shown to work. Mutate the code on purpose (flip a sign,
change a comparison, drop a term), rerun, and confirm the test fails. If it still passes, the test
does not cover that line. This collection's scripts were checked this way.

## Patterns that find real bugs

- **Round trip:** convert and convert back; the result must equal the input.
- **Both conventions:** slice a known sequence with 0-based and with 1-based coordinates and compare the bases.
- **Asymmetric inputs:** a palindromic or centred example hides a mirrored coordinate; use an
  off-centre case.
- **Degenerate inputs:** empty sequence, one base, all the same base, a record with nothing in it.
- **Limits:** probability 0 and 1, a distance at the edge of validity, a window longer than the sequence.
- **Order independence:** shuffle the input records; summary results must not change.
- **Scaling:** double every score and check that the answer scales or stays the same as expected.

## Numbers

- Compare floating-point values within a stated tolerance, never with equality, unless the value is
  exact by construction.
- When a source prints rounded values, compare within the rounding. Printed textbook numbers are
  not always rounded the same way.
- Record the tolerance next to the test and keep it as tight as the arithmetic allows.

## Data and randomness

- Use small, fixed test inputs committed with the tests. Do not make the test suite download data.
- Use a fixed seed in tests and a separate multi-seed run for stability.
- For a stochastic method, test the property of the distribution (mean, range, no impossible
  values) rather than one sampled number.

## Reporting what was tested

State the number of checks and what they cover, and state what is not tested. An honest "not
tested: real data, large inputs, compressed files" is more useful than a long list of passing checks.
