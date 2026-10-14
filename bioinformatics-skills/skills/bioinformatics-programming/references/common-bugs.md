# Common bugs

General experience; each item names a check.

| Bug | Symptom | Check |
|---|---|---|
| Off-by-one coordinate | Every feature shifted by one base | Slice a known sequence with both conventions and compare the bases |
| Closed coordinates used as a half-open slice | Features one base too long | Test an interval of length one |
| Mirrored coordinate on the reverse strand | Right size, wrong place | Use an off-centre test case, not a symmetric one |
| Probability underflow | Zero where a tiny positive number belongs, or log of zero | Compare log-space and direct results on a short case |
| Quadratic loop | Fast on the test, hopeless on real data | Time at 1x, 2x, 4x the input and look at the growth |
| Upper-casing the sequence | Soft-masked repeats become unmasked | Keep case, or record the mask separately |
| Reading the whole file | Memory exhaustion or swapping | Watch memory while running on a larger file |
| Unordered collection | Output order changes between runs | Sort before output; seed the hash order where the language allows (VERIFY) |
| Unseeded randomness | Results differ between runs | Seed and record the seed |
| Integer overflow | Counts wrap or go negative in fixed-width types | Use wide enough types; test near the limit |
| Identifiers read as numbers | Leading zeros lost, long numbers in scientific notation | Read identifier columns as text |
| Gene symbols turned into dates | SEPT2 becomes a date after a spreadsheet step | Keep symbols as text and avoid spreadsheets for them |
| Windows line endings | A stray carriage return in sequence or identifiers | Strip line endings in one place; test with a file that has them |
| Mutable default argument or shared state | Results leak between calls | Test the function twice in a row |
| Floating-point equality | A test passes on one machine and fails on another | Compare within a tolerance |
| Ambiguity codes ignored | N counted as a base, or a crash on N | Test with an N in the input |
| Paired files out of sync | Mates do not match after filtering one file | Check read names pairwise after every step |
| Silent truncation | A partial last record is accepted | Fail on a record count or a line count that does not fit |

## How to catch them

1. A hand-computed answer on a small case.
2. An independent implementation compared on many small random inputs.
3. A property that must hold: a round trip, an invariant, a total that must sum.
4. A planted case: put a known difference in and see that the code finds it.
5. A mutation of your own code: break it on purpose and see that a test fails.

These are the checks used in the self-tests of this collection's scripts.
