# `ngs-pipelines`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> What does SAM FLAG 99 mean, bit by bit, and what flag would its mate normally have?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 817 | 1,009 |
| Input tokens read across all turns (including cached context) | 30,346 | 35,633 |
| Extra input tokens when the skill is installed | | +5,287 |
| Cost, US dollars at list price | 0.076 | 0.122 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 240 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
## FLAG 99 = 64 + 32 + 2 + 1

| Bit | Hex | Decimal | Set? | Meaning |
|---|---|---|---|---|
| 0 | 0x1 | 1 | **yes** | The read is paired (part of a template with more than one segment) |
| 1 | 0x2 | 2 | **yes** | Properly paired: both mates aligned with the orientation and distance the aligner expects |
| 2 | 0x4 | 4 | no | The read is mapped |
| 3 | 0x8 | 8 | no | The mate is mapped |
| 4 | 0x10 | 16 | no | The read is on the **forward** strand |
| 5 | 0x20 | 32 | **yes** | The mate is on the **reverse** strand |
| 6 | 0x40 | 64 | **yes** | This is the **first** read in the pair (R1) |
| 7 | 0x80 | 128 | no | It is not the second read |
| 8 | 0x100 | 256 | no | Primary alignment, not secondary |
| 9 | 0x200 | 512 | no | Passed the vendor QC filter |
| 10 | 0x400 | 1024 | no | Not marked as a PCR or optical duplicate |
| 11 | 0x800 | 2048 | no | Not a supplementary (chimeric) alignment |

**In short:** this is R1 of a properly paired fragment. It maps to the forward strand and its mate maps to the reverse strand. It's the primary alignment, it passed QC, and it isn't a duplicate.

## The mate: FLAG 147

The mate mirrors each pair-related bit:

- 1: paired
- 2: proper pair
- 16: the mate (this record) is on the reverse strand
- 128: it is the second read (R2)

1 + 2 + 16 + 128 = **147**

99/147 is the standard "forward–reverse" (FR) pair from Illumina paired-end libraries, where R1 lies on the forward strand. When the fragment comes from the other strand you get the opposite pair, **83/163**: R1 is reversed (64+16+2+1) and R2 is forward with a reversed mate (128+32+2+1).

Two things can change the mate's flag. If the reads have been through duplicate marking, a duplicate pair has 1024 added to both (99→1123, 147→1171). Secondary or supplementary records for either read add 256 or 2048. To check a flag, run `samtools flags 99`.
````

## Answer without the skill (excerpt)

````text
**FLAG 99 = 64 + 32 + 2 + 1**

| Bit | Hex | Set? | Meaning |
|---|---|---|---|
| 1 | 0x1 | ✅ | Read is paired |
| 2 | 0x2 | ✅ | Read is mapped in a proper pair |
| 4 | 0x4 | ❌ | So the read itself is mapped |
| 8 | 0x8 | ❌ | So the mate is mapped |
| 16 | 0x10 | ❌ | So the read is on the forward strand |
| 32 | 0x20 | ✅ | The mate is on the reverse strand |
| 64 | 0x40 | ✅ | This is the first read in the pair (R1) |
| 128 | 0x80 | ❌ | So it is not the second read |
| 256 | 0x100 | ❌ | So it is the primary alignment |
| 512 | 0x200 | ❌ | So it passed QC |
| 1024 | 0x400 | ❌ | So it is not marked as a duplicate |
| 2048 | 0x800 | ❌ | So it is not a supplementary alignment |

In short, this is R1 of a properly paired read. It maps to the forward strand and its mate maps to the reverse strand. This is the standard forward-reverse ("FR") orientation for Illumina paired-end reads.

**The mate would normally have FLAG 147 = 128 + 16 + 2 + 1:**
- **1 (0x1):** paired
- **2 (0x2):** proper pair
- **16 (0x10):** the mate itself is on the reverse strand
- **128 (0x80):** it is the second read in the pair (R2)
- **32 (0x20) is not set** because its partner (the FLAG 99 read) is on the forward strand

99 and 147 are one of the two standard proper-pair combinations. The other is 83 and 163, where R1 is on the reverse strand and R2 is on the forward strand. You can check any flag with `samtools flags 99`.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
