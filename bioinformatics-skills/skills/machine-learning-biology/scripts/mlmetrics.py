#!/usr/bin/env python3
"""Evaluation metrics and leakage-safe splits for biological machine learning (standard library only).

  mlmetrics.py metrics TRUE PRED            confusion counts, precision, recall, F1, MCC, balanced accuracy
  mlmetrics.py auc TRUE SCORES              area under the ROC curve and average precision
  mlmetrics.py split GROUPS --folds 5       cross-validation folds that keep every group together
  mlmetrics.py similar SEQ_FILE_A SEQ_FILE_B [--k 5] [--min 0.5]   near-duplicates across train and test
  mlmetrics.py --selftest

Labels are 0 or 1 (1 = positive), given as comma-separated values. A "group" is anything whose
members must not be split between training and test data: a protein family, a patient, a
species, a batch, a cluster of near-identical sequences.
"""
import argparse
import math
import random
import sys
from collections import Counter, defaultdict


def _check_labels(y):
    if not y or any(v not in (0, 1) for v in y):
        raise ValueError("labels must be a non-empty list of 0s and 1s")


def confusion(y_true, y_pred):
    _check_labels(y_true)
    _check_labels(y_pred)
    if len(y_true) != len(y_pred):
        raise ValueError("labels and predictions must be the same length")
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    return tp, fp, tn, fn


def _div(a, b):
    return a / b if b else 0.0


def metrics(y_true, y_pred):
    tp, fp, tn, fn = confusion(y_true, y_pred)
    recall = _div(tp, tp + fn)
    specificity = _div(tn, tn + fp)
    precision = _div(tp, tp + fp)
    denom = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return {
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "accuracy": (tp + tn) / len(y_true),
        "precision": precision, "recall": recall, "specificity": specificity,
        "f1": _div(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "mcc": ((tp * tn - fp * fn) / denom) if denom else 0.0,
    }


def auroc(y_true, scores):
    """Area under the ROC curve = P(a random positive scores above a random negative), ties count half."""
    _check_labels(y_true)
    if len(y_true) != len(scores):
        raise ValueError("labels and scores must be the same length")
    pos = [s for t, s in zip(y_true, scores) if t == 1]
    neg = [s for t, s in zip(y_true, scores) if t == 0]
    if not pos or not neg:
        raise ValueError("need at least one positive and one negative")
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):  # average ranks over ties
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2.0 + 1
        i = j + 1
    rank_sum = sum(r for r, t in zip(ranks, y_true) if t == 1)
    return (rank_sum - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg))


def average_precision(y_true, scores):
    """Sum over thresholds of (recall gained) x (precision there). Ties are taken as one threshold."""
    _check_labels(y_true)
    if len(y_true) != len(scores):
        raise ValueError("labels and scores must be the same length")
    total_pos = sum(y_true)
    if total_pos == 0:
        raise ValueError("need at least one positive")
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    tp = seen = 0
    prev_recall = 0.0
    ap = 0.0
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        for k in range(i, j + 1):
            tp += y_true[order[k]]
            seen += 1
        recall = tp / total_pos
        ap += (recall - prev_recall) * (tp / seen)
        prev_recall = recall
        i = j + 1
    return ap


def group_folds(groups, folds, seed=1):
    """Assign each item a fold so that a whole group stays in one fold. Big groups first, each to the
    currently smallest fold. Returns the fold number for each item, in input order."""
    if folds < 2:
        raise ValueError("need at least two folds")
    sizes = Counter(groups)
    if len(sizes) < folds:
        raise ValueError("%d groups cannot fill %d folds" % (len(sizes), folds))
    rng = random.Random(seed)
    names = sorted(sizes)
    rng.shuffle(names)
    names.sort(key=lambda g: -sizes[g])
    load = [0] * folds
    fold_of = {}
    for g in names:
        f = min(range(folds), key=lambda x: (load[x], x))
        fold_of[g] = f
        load[f] += sizes[g]
    return [fold_of[g] for g in groups]


def kmer_set(seq, k):
    seq = seq.upper()
    return {seq[i:i + k] for i in range(len(seq) - k + 1)}


def jaccard(a, b, k=5):
    sa, sb = kmer_set(a, k), kmer_set(b, k)
    if not sa and not sb:
        return 1.0 if a.upper() == b.upper() else 0.0
    return len(sa & sb) / len(sa | sb)


def near_duplicates(train, test, k=5, minimum=0.5):
    """(train index, test index, Jaccard similarity of their k-mer sets) for pairs at or above `minimum`."""
    return [(i, j, s) for i, a in enumerate(train) for j, b in enumerate(test)
            for s in [jaccard(a, b, k)] if s >= minimum]


def _read_sequences(path):
    seqs, cur = [], []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                if cur:
                    seqs.append("".join(cur))
                cur = []
            elif line:
                cur.append(line)
    if cur:
        seqs.append("".join(cur))
    return seqs


def selftest():
    n = [0]

    def check(name, got, want, tol=None):
        n[0] += 1
        ok = (abs(got - want) <= tol) if tol is not None else got == want
        if not ok:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    def raises(name, fn):
        n[0] += 1
        try:
            fn()
        except ValueError:
            return
        raise AssertionError("%s: expected ValueError" % name)

    check("confusion", confusion([1, 1, 1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 1, 0, 0, 0]), (5, 1, 3, 1))
    m = metrics([1, 1, 1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 1, 0, 0, 0])
    check("MCC = (5*3 - 1*1) / sqrt(6*6*4*4) = 14/24", m["mcc"], 14 / 24, 1e-12)
    check("recall", m["recall"], 5 / 6, 1e-12)
    check("precision", m["precision"], 5 / 6, 1e-12)
    check("specificity", m["specificity"], 3 / 4, 1e-12)
    check("balanced accuracy", m["balanced_accuracy"], (5 / 6 + 3 / 4) / 2, 1e-12)
    check("F1", m["f1"], 5 / 6, 1e-12)
    check("accuracy", m["accuracy"], 0.8, 1e-12)
    # A classifier that always says "negative" on 95 negatives and 5 positives.
    y = [0] * 95 + [1] * 5
    lazy = metrics(y, [0] * 100)
    check("always-negative accuracy looks great", lazy["accuracy"], 0.95, 1e-12)
    check("always-negative MCC is 0", lazy["mcc"], 0.0)
    check("always-negative balanced accuracy is 0.5", lazy["balanced_accuracy"], 0.5, 1e-12)
    # The standard worked example: AUROC 0.75, average precision 0.8333.
    yt, sc = [0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]
    check("AUROC of the worked example", auroc(yt, sc), 0.75, 1e-12)
    check("average precision of the worked example", average_precision(yt, sc), 0.5 * 1 + 0.5 * (2 / 3), 1e-12)
    check("perfect ranking", auroc([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9]), 1.0)
    check("reversed ranking", auroc([0, 0, 1, 1], [0.9, 0.8, 0.2, 0.1]), 0.0)
    check("all scores tied is chance", auroc([0, 1, 0, 1], [0.5, 0.5, 0.5, 0.5]), 0.5)
    check("ties count half", auroc([0, 1], [0.5, 0.5]), 0.5)
    check("AUROC is unchanged by a monotone transform", auroc(yt, [s * 10 + 3 for s in sc]), auroc(yt, sc), 1e-12)
    check("average precision of a perfect ranking", average_precision([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9]), 1.0, 1e-12)
    check("average precision with tied scores uses one threshold", average_precision([0, 1], [0.5, 0.5]), 0.5, 1e-12)
    # AUROC against a brute-force count of positive-negative pairs.
    state = [7]

    def rnd():
        state[0] = (state[0] * 1103515245 + 12345) % (2 ** 31)
        return (state[0] >> 16) % 10

    for _ in range(30):
        ys = [rnd() % 2 for _ in range(12)]
        ss = [rnd() for _ in range(12)]
        if 0 < sum(ys) < len(ys):
            pairs = [(1.0 if p > q else 0.5 if p == q else 0.0) for p, a in zip(ss, ys) if a == 1
                     for q, b in zip(ss, ys) if b == 0]
            check("AUROC equals the pair count", auroc(ys, ss), sum(pairs) / len(pairs), 1e-12)
    raises("one class only", lambda: auroc([1, 1], [0.1, 0.2]))
    raises("bad labels", lambda: metrics([0, 2], [0, 1]))
    raises("length mismatch", lambda: confusion([0, 1], [1]))
    raises("no positives for AP", lambda: average_precision([0, 0], [0.1, 0.2]))
    # Group folds.
    groups = ["f1"] * 6 + ["f2"] * 5 + ["f3"] * 4 + ["f4"] * 3 + ["f5"] * 2
    folds = group_folds(groups, 3, seed=2)
    by_group = defaultdict(set)
    for g, f in zip(groups, folds):
        by_group[g].add(f)
    check("no group is split across folds", all(len(v) == 1 for v in by_group.values()), True)
    sizes = Counter(folds)
    check("folds are balanced to within the largest group", max(sizes.values()) - min(sizes.values()) <= 6, True)
    check("every fold is used", set(folds), {0, 1, 2})
    check("same seed, same folds", group_folds(groups, 3, seed=2), folds)
    raises("more folds than groups", lambda: group_folds(["a", "b"], 3))
    raises("one fold", lambda: group_folds(["a", "b"], 1))
    # Near-duplicates by shared k-mers.
    a = "ACGTTGCAAGCTTAGGCATC"
    check("20-mer has 16 distinct 5-mers", len(kmer_set(a, 5)), 16)
    check("identical sequences", jaccard(a, a), 1.0)
    check("disjoint sequences", jaccard("AAAAAAAAAA", "CCCCCCCCCC"), 0.0)
    b = a[:10] + ("A" if a[10] != "A" else "C") + a[11:]
    check("one change in the middle shares 11 of 21 five-mers", jaccard(a, b), 11 / 21, 1e-12)
    pairs = near_duplicates([a, "TTTTTTTTTTTTTTTT"], [b, "GGGGGGGGGGGGGGGG"], k=5, minimum=0.5)
    check("near-duplicate pair found", [(i, j) for i, j, _ in pairs], [(0, 0)])
    check("nothing above the threshold", near_duplicates([a], ["GGGGGGGGGGGGGGGG"], 5, 0.5), [])
    print("mlmetrics.py self-test: %d checks passed" % n[0])


def _ints(text):
    return [int(x) for x in text.split(",")]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Evaluation metrics and leakage-safe splits.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("metrics")
    s.add_argument("true")
    s.add_argument("pred")
    s = sub.add_parser("auc")
    s.add_argument("true")
    s.add_argument("scores")
    s = sub.add_parser("split")
    s.add_argument("groups", help="comma-separated group name for each item")
    s.add_argument("--folds", type=int, default=5)
    s.add_argument("--seed", type=int, default=1)
    s = sub.add_parser("similar")
    s.add_argument("a")
    s.add_argument("b")
    s.add_argument("--k", type=int, default=5)
    s.add_argument("--min", type=float, default=0.5)
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    try:
        if a.cmd == "metrics":
            for k, v in metrics(_ints(a.true), _ints(a.pred)).items():
                print("%-18s %s" % (k, v if isinstance(v, int) else "%.4f" % v))
        elif a.cmd == "auc":
            y, sc = _ints(a.true), [float(x) for x in a.scores.split(",")]
            print("AUROC %.4f   average precision %.4f   (positive rate %.3f: chance AP is about that)" % (
                auroc(y, sc), average_precision(y, sc), sum(y) / len(y)))
        elif a.cmd == "split":
            groups = a.groups.split(",")
            print(",".join(str(f) for f in group_folds(groups, a.folds, a.seed)))
        elif a.cmd == "similar":
            hits = near_duplicates(_read_sequences(a.a), _read_sequences(a.b), a.k, a.min)
            for i, j, s in hits:
                print("A[%d] ~ B[%d]  k-mer Jaccard %.3f" % (i, j, s))
            print("%d pair(s) at or above %.2f: split these together or drop them" % (len(hits), a.min))
            return 1 if hits else 0
        else:
            ap.print_help()
            return 2
    except (ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
