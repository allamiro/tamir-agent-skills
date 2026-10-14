# `systems-literature-reading`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Read the Raft paper (Ongaro and Ousterhout, USENIX ATC 2014) for me. We run a five-node cluster across three availability zones. Give me the claim record, what the paper assumes about failures and the network, and whether those assumptions hold for us. Say what you read and what you are recalling.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 4,023 | 5,373 |
| Input tokens read across all turns (including cached context) | 103,710 | 248,900 |
| Extra input tokens when the skill is installed | | +145,190 |
| Cost, US dollars at list price | 0.165 | 0.304 |
| Skills invoked in the sample run | none | `systems-literature-reading` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 270 tokens for its name and description, which are in every session where the skill is installed, and about 2,600 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I couldn't read the paper. The PDF fetch from usenix.org needed your permission and didn't get it, there's no local copy in the workspace, and I didn't try to get around that with curl. So everything below about what the paper says is **recalled**, from memory and not checked against the text. I've left out the paper's numbers because I can't point to a page for any of them. If you approve the fetch or drop the PDF in this folder, I'll check each item against the text and add section and figure references.

## What I used

| Source | Mark | Notes |
|---|---|---|
| Ongaro, D., Ousterhout, J. "In Search of an Understandable Consensus Algorithm." USENIX ATC 2014, pp. 305–319 | **seen** for the citation, **recalled** for the content | The citation comes from the reading list bundled with the skill I used, which records it as checked against the USENIX record. I wasn't allowed to run the citation checker. |
| Ongaro's PhD thesis (Stanford, 2014): pre-vote, check-quorum, single-server membership change | **recalled** | |
| The 2015 bug in single-server membership change, reported on raft-dev | **recalled** | This would be the independent cross-check, but it's unverified. It affects the thesis method, not joint consensus in the ATC paper. |

## Claim record (recalled)

- **Main claim:** Raft gives the same safety and roughly the same efficiency as (Multi-)Paxos, and is easier to understand.
- **Mechanisms:**
  - The problem is split into leader election, log replication and safety.
  - The protocol has fewer possible states: one strong leader, and log entries flow only from leader to followers.
  - Election timeouts are randomized.
  - Membership changes use joint consensus.
  - Logs are compacted with snapshots.
- **Evidence:**
  - A user study comparing Raft and Paxos, with quizzes given to students at two universities.
  - A formal specification in TLA+ and a safety proof. The full proof is in the thesis.
  - Leader-election timing experiments on a small cluster with varying amounts of timeout randomization.
- **What the paper does not claim:**
  - Throughput or latency under your workload.
  - Tolerance of Byzantine (arbitrary or malicious) faults.
  - Protection against disk corruption.
  - Behaviour of any particular implementation.

## The paper's assumptions (recalled)

1. **Servers fail by crashing and may recover.** They are not Byzantine. Each server writes its current term, its vote and its log to stable storage before replying.
2. **The network is asynchronous.** Messages can be delayed, lost, duplicated or reordered, and the network can partition. Safety doesn't depend on timing.
3. **Availability does depend on timing:** broadcast time ≪ election timeout ≪ mean time between failures.
4. **Majority quorums.** A cluster of 2f+1 servers tolerates f failures, so five nodes tolerate two.
5. **Clocks aren't needed for safety.** Lease-based read-only requests, the optional optimisation, do assume bounded clock drift. The default read path confirms leadership with a heartbeat round to a majority.
6. **Clients get linearizable results** when they tag each request with a unique serial number so duplicates can be discarded.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
I couldn't read the paper. The fetch of raft.github.io/raft.pdf was blocked because WebFetch permission wasn't granted, and there's no PDF in the working directory. I didn't try another route. **Everything below is from memory, not from reading the paper this session.** The design and assumptions are well known and I'm confident about them. Specific numbers and section placements are where I'm most likely to be off, and I've marked those "(verify)". If you allow WebFetch or drop the PDF in this directory, I'll check it all against the text.

## Claim record (recalled)

| Claim | Evidence the paper gives | Strength |
|---|---|---|
| Raft is as fault tolerant and as fast as (multi-)Paxos | Argued from its structure: a majority quorum, one round trip to commit in the normal case | An argument, not a head-to-head benchmark |
| Raft is easier to understand than Paxos | User study of 43 students (Stanford and Berkeley) using quizzes on both. Most scored higher on Raft (about 33 of 43, mean gap about 4.9 points out of 60) (verify) | Real but narrow: students, one study, run by the authors |
| Raft is safe: once an entry is committed, no server applies a different entry at that index | Election Safety, Log Matching, Leader Completeness and State Machine Safety properties. A TLA+ spec, plus a safety proof in Ongaro's thesis (verify how much was machine-checked) | Strong. The core protocol has held up |

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
