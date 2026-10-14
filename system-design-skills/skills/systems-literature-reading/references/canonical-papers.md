# Canonical papers by topic

Bibliographic details were checked on 2026-10-14: DOI records on Crossref (publisher metadata) and,
for papers without a DOI, the USENIX and Microsoft Research pages. This is a reading map, not a
ranking. The "does not settle" column is the skill's own analysis and should be checked against the
paper. Read the paper, not this table, before citing a claim from it.

## Time, agreement and failure

| Paper | Good for | Does not settle |
|---|---|---|
| Lamport, L. Time, clocks, and the ordering of events in a distributed system. *Communications of the ACM* 21(7), 558-565, 1978. doi:10.1145/359545.359563 | Logical clocks and the happens-before relation | Failures; the paper assumes processes and messages behave |
| Fischer, M. J., Lynch, N. A., Paterson, M. S. Impossibility of distributed consensus with one faulty process. *Journal of the ACM* 32(2), 374-382, 1985. doi:10.1145/3149.214121 | Why no deterministic protocol guarantees agreement in a fully asynchronous system with a crash fault | How practical systems cope with timeouts, randomness or partial synchrony |
| Lamport, L. Paxos made simple. *ACM SIGACT News* 32(4), 51-58, December 2001 (Microsoft Research publication page) | The core agreement protocol | Production details such as membership change, snapshots and leader leases |
| Ongaro, D., Ousterhout, J. In search of an understandable consensus algorithm. *USENIX ATC 2014*, 305-319 (USENIX record) | A replicated-log consensus protocol designed to be taught and implemented, with membership change and log compaction | Performance under your workload; byzantine faults |

## Consistency and isolation

| Paper | Good for | Does not settle |
|---|---|---|
| Herlihy, M. P., Wing, J. M. Linearizability: a correctness condition for concurrent objects. *ACM TOPLAS* 12(3), 463-492, 1990. doi:10.1145/78969.78972 | The definition of linearizability | Whether a given product delivers it by default |
| Berenson, H., Bernstein, P., Gray, J., Melton, J. A critique of ANSI SQL isolation levels. *SIGMOD 1995* (also *SIGMOD Record* 24(2), 1-10). doi:10.1145/223784.223785 | Why the standard isolation levels are ambiguous; snapshot isolation | How a specific engine implements each level today |
| Bailis, P., Davidson, A., Fekete, A., Ghodsi, A., Hellerstein, J. M., Stoica, I. Highly available transactions: virtues and limitations. *PVLDB* 7(3), 181-192, 2013. doi:10.14778/2732232.2732237 | Which guarantees can be offered without giving up availability | Application-level invariants |
| Gilbert, S., Lynch, N. Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services. *ACM SIGACT News* 33(2), 51-59, 2002. doi:10.1145/564585.564601 | A formal statement and proof of the CAP trade-off for atomic consistency | Everyday latency trade-offs; other meanings of "consistency" |
| Brewer, E. CAP twelve years later: how the "rules" have changed. *IEEE Computer* 45(2), 23-29, 2012. doi:10.1109/MC.2012.37 | Why "pick two of three" over-simplifies | A recipe for choosing a database |

## Industry systems papers

| Paper | Good for | Does not settle |
|---|---|---|
| DeCandia, G. et al. Dynamo: Amazon's highly available key-value store. *SOSP 2007* (also *ACM SIGOPS OSR* 41(6), 205-220). doi:10.1145/1294261.1294281 | An early account of an eventually consistent, partitioned store with versioning and sloppy quorums | How later products by the same company differ |
| Ghemawat, S., Gobioff, H., Leung, S.-T. The Google file system. *SOSP 2003*, 29-43. doi:10.1145/945445.945450 | A file system built around a specific workload and failure assumptions | Workloads that break those assumptions |
| Dean, J., Ghemawat, S. MapReduce: simplified data processing on large clusters. *Communications of the ACM* 51(1), 107-113, 2008. doi:10.1145/1327452.1327492 (conference version at OSDI 2004: VERIFY) | The programming model and its fault-tolerance approach | Interactive or iterative workloads |
| Chang, F. et al. Bigtable: a distributed storage system for structured data. *ACM TOCS* 26(2), 2008. doi:10.1145/1365815.1365816 (conference version at OSDI 2006: VERIFY) | A wide-column data model and its use of a distributed file system | Secondary indexes and general transactions |
| Corbett, J. C. et al. Spanner: Google's globally distributed database. *ACM TOCS* 31(3), 1-22, 2013. doi:10.1145/2491245 (conference version at OSDI 2012: VERIFY) | Externally consistent transactions using bounded clock uncertainty | Whether you have comparable clock infrastructure |

## Method and writing

| Source | Good for |
|---|---|
| Keshav, S. How to read a paper. *ACM SIGCOMM CCR* 37(3), 83-84, 2007. doi:10.1145/1273445.1273458 | A three-pass reading method |
| Georges, A., Buytaert, D., Eeckhout, L. Statistically rigorous Java performance evaluation. *OOPSLA 2007* (also *ACM SIGPLAN Notices* 42(10), 57-76). doi:10.1145/1297027.1297033 | Why single timings mislead and how to report variation |
| Little, J. D. C. A proof for the queuing formula: L = lambda W. *Operations Research* 9(3), 383-387, 1961. doi:10.1287/opre.9.3.383 | The relation between concurrency, arrival rate and time in system |
| Levin, R., Redell, D. D. An evaluation of the ninth SOSP submissions, or how (and how not) to write a good systems paper. Reprinted in *ACM SIGGRAPH Computer Graphics* 22(5), 264-266, 1988. doi:10.1145/378267.378283 (first published 1983: VERIFY) | What systems reviewers look for |
| Smith, A. J. The task of the referee. *IEEE Computer* 23(4), 65-71, 1990. doi:10.1109/2.55470 | What a referee should check |

## Independent evidence worth finding

Independent test reports on a product (for example from the Jepsen project), a system's own current
documentation, and papers that reimplement or measure a published design. URLs and report versions
change, so look them up rather than quoting this file: VERIFY.
