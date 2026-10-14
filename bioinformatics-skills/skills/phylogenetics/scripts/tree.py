#!/usr/bin/env python3
"""Distances and distance-based trees from aligned sequences (standard library only).

  tree.py distances ALIGNED.fasta [--model jc|p]   pairwise distance matrix as CSV
  tree.py upgma MATRIX.csv                         rooted tree assuming a molecular clock
  tree.py nj MATRIX.csv                            unrooted neighbour-joining tree
  tree.py jc SEQ1 SEQ2                             p-distance and Jukes-Cantor distance
  tree.py --selftest

MATRIX.csv is a square matrix with a header row and a label column, for example
    ,A,B,C
    A,0,2,4
    B,2,0,4
    C,4,4,0
Output trees are Newick strings with branch lengths. These are distance methods: they build one
tree from summary numbers. They do not search tree space, do not give support values, and
UPGMA is only right when evolution is clock-like. Treat the result as a starting point.
"""
import argparse
import math
import sys


def p_distance(a, b):
    """Proportion of differing sites, using only sites where both sequences have A, C, G or T."""
    if len(a) != len(b):
        raise ValueError("sequences must be aligned and the same length")
    pairs = [(x, y) for x, y in zip(a.upper(), b.upper()) if x in "ACGT" and y in "ACGT"]
    if not pairs:
        raise ValueError("no sites where both sequences have an unambiguous base")
    return sum(1 for x, y in pairs if x != y) / len(pairs)


def jc69(p):
    """Jukes-Cantor distance: expected substitutions per site given the observed proportion p."""
    if not 0 <= p < 0.75:
        raise ValueError("p = %g: Jukes-Cantor distance is undefined at p >= 0.75 (saturation)" % p)
    return -0.75 * math.log(1 - 4.0 * p / 3.0) + 0.0


def fmt(x):
    return format(x + 0.0, ".6g")


def read_matrix(text):
    rows = [ln.split(",") for ln in text.strip().splitlines() if ln.strip()]
    names = [c.strip() for c in rows[0][1:]]
    if len(rows) - 1 != len(names) or len(set(names)) != len(names):
        raise ValueError("need a square matrix with unique labels")
    d = []
    for i, row in enumerate(rows[1:]):
        if row[0].strip() != names[i]:
            raise ValueError("row %d is labelled %r, expected %r" % (i + 1, row[0].strip(), names[i]))
        d.append([float(x) for x in row[1:]])
    check_matrix(names, d)
    return names, d


def check_matrix(names, d):
    n = len(names)
    if any(len(r) != n for r in d):
        raise ValueError("matrix is not square")
    for name in names:
        if not name or name.startswith("#") or any(c in name for c in "(),:;"):
            raise ValueError("label %r is empty, starts with '#', or contains Newick punctuation" % name)
    for i in range(n):
        if abs(d[i][i]) > 1e-12:
            raise ValueError("diagonal entry for %s is not 0" % names[i])
        for j in range(i + 1, n):
            if abs(d[i][j] - d[j][i]) > 1e-9:
                raise ValueError("matrix is not symmetric at %s, %s" % (names[i], names[j]))
            if d[i][j] < 0:
                raise ValueError("negative distance between %s and %s" % (names[i], names[j]))


def upgma(names, d):
    """UPGMA: repeatedly join the closest pair; a cluster's height is half the joining distance."""
    check_matrix(names, d)
    n = len(names)
    if n < 2:
        raise ValueError("need at least two taxa")
    label = {i: names[i] for i in range(n)}
    height = {i: 0.0 for i in range(n)}
    size = {i: 1 for i in range(n)}
    first = {i: names[i] for i in range(n)}  # alphabetically first leaf, to order siblings the same way every time
    dist = {(i, j): d[i][j] for i in range(n) for j in range(i + 1, n)}
    nxt = n
    while len(label) > 1:
        i, j = min(dist, key=lambda k: (dist[k], k))
        h = dist[(i, j)] / 2.0
        left, right = sorted((i, j), key=lambda c: first[c])
        label[nxt] = "(%s:%s,%s:%s)" % (label[left], fmt(h - height[left]), label[right], fmt(h - height[right]))
        height[nxt], size[nxt], first[nxt] = h, size[i] + size[j], min(first[i], first[j])
        for k in [c for c in label if c not in (i, j, nxt)]:
            dik = dist[(min(i, k), max(i, k))]
            djk = dist[(min(j, k), max(j, k))]
            dist[(k, nxt)] = (size[i] * dik + size[j] * djk) / (size[i] + size[j])
        dist = {k: v for k, v in dist.items() if i not in k and j not in k}
        for gone in (i, j):
            del label[gone]
        nxt += 1
    return next(iter(label.values())) + ";"


def neighbor_joining(names, d):
    """Neighbour-joining. Returns edges as (node, node, length); internal nodes are named '#0', '#1', ..."""
    check_matrix(names, d)
    n = len(names)
    if n < 2:
        raise ValueError("need at least two taxa")
    if n == 2:
        return [(names[0], names[1], d[0][1])]
    dist = {a: {b: d[i][j] for j, b in enumerate(names) if b != a} for i, a in enumerate(names)}
    active, edges, counter = list(names), [], 0
    while len(active) > 3:
        m = len(active)
        r = {a: sum(dist[a][b] for b in active if b != a) for a in active}
        best = None
        for i, a in enumerate(active):
            for b in active[i + 1:]:
                q = (m - 2) * dist[a][b] - r[a] - r[b]
                if best is None or q < best[0] - 1e-12:
                    best = (q, a, b)
        _, a, b = best
        u = "#%d" % counter
        counter += 1
        la = dist[a][b] / 2.0 + (r[a] - r[b]) / (2.0 * (m - 2))
        edges += [(a, u, la), (b, u, dist[a][b] - la)]
        dist[u] = {}
        for k in active:
            if k not in (a, b):
                dist[u][k] = dist[k][u] = (dist[a][k] + dist[b][k] - dist[a][b]) / 2.0
        active = [x for x in active if x not in (a, b)] + [u]
    x, y, z = active
    centre = "#%d" % counter
    lx = (dist[x][y] + dist[x][z] - dist[y][z]) / 2.0
    edges += [(x, centre, lx), (y, centre, dist[x][y] - lx), (z, centre, dist[x][z] - lx)]
    return edges


def _adjacency(edges):
    adj = {}
    for a, b, length in edges:
        adj.setdefault(a, []).append((b, length))
        adj.setdefault(b, []).append((a, length))
    return adj


def leaves_of(edges):
    return sorted(node for node in _adjacency(edges) if not node.startswith("#"))


def path_distances(edges):
    """Distance between every pair of leaves, summed along the tree path."""
    adj = _adjacency(edges)
    out = {}
    for start in leaves_of(edges):
        seen, stack = {start: 0.0}, [start]
        while stack:
            node = stack.pop()
            for nbr, length in adj[node]:
                if nbr not in seen:
                    seen[nbr] = seen[node] + length
                    stack.append(nbr)
        for other in leaves_of(edges):
            if other != start:
                out[(start, other)] = seen[other]
    return out


def splits(edges):
    """The set of leaf bipartitions induced by the internal edges: the topology without lengths."""
    adj = _adjacency(edges)
    every = frozenset(leaves_of(edges))
    result = set()
    for a, b, _ in edges:
        if a.startswith("#") and b.startswith("#"):
            side, stack, seen = set(), [b], {a, b}
            while stack:
                node = stack.pop()
                if not node.startswith("#"):
                    side.add(node)
                for nbr, _l in adj[node]:
                    if nbr not in seen:
                        seen.add(nbr)
                        stack.append(nbr)
            part = frozenset(side)
            result.add(min(part, every - part, key=lambda s: sorted(s)))
    return result


def newick(edges):
    adj = _adjacency(edges)
    nodes = list(adj)
    if len(nodes) == 2:
        (a, b, length), = edges
        return "(%s:%s,%s:%s);" % (a, fmt(length / 2.0), b, fmt(length / 2.0))
    root = max((nd for nd in nodes if nd.startswith("#")), key=lambda s: int(s[1:]))

    def walk(node, parent):
        kids = sorted(((nbr, length) for nbr, length in adj[node] if nbr != parent), key=lambda t: t[0])
        if not kids:
            return node
        return "(" + ",".join("%s:%s" % (walk(k, node), fmt(length)) for k, length in kids) + ")"

    return walk(root, None) + ";"


def selftest():
    n = [0]

    def check(name, got, want, tol=None):
        n[0] += 1
        ok = abs(got - want) <= tol if tol is not None else got == want
        if not ok:
            raise AssertionError("%s: got %r, want %r" % (name, got, want))

    def raises(name, fn):
        n[0] += 1
        try:
            fn()
        except ValueError:
            return
        raise AssertionError("%s: expected ValueError" % name)

    check("p-distance", p_distance("ACGT", "ACGA"), 0.25)
    check("p-distance skips gaps and N", p_distance("AC-T", "ACGA"), 1 / 3)
    check("Jukes-Cantor at p = 0", jc69(0.0), 0.0)
    check("Jukes-Cantor at p = 0.3 (-0.75 ln 0.6, by hand 0.383119)", jc69(0.3), 0.383119, 1e-6)
    check("Jukes-Cantor exceeds p", jc69(0.1) > 0.1, True)
    raises("Jukes-Cantor saturated", lambda: jc69(0.75))
    raises("p-distance unequal lengths", lambda: p_distance("AC", "ACG"))
    raises("p-distance no comparable sites", lambda: p_distance("NN", "AC"))
    # UPGMA, worked by hand: A,B join at height 1; (AB),C at 2; then D at 3.
    three = ["A", "B", "C"], [[0, 2, 4], [2, 0, 4], [4, 4, 0]]
    check("UPGMA, three taxa", upgma(*three), "((A:1,B:1):1,C:2);")
    four = ["A", "B", "C", "D"], [[0, 2, 4, 6], [2, 0, 4, 6], [4, 4, 0, 6], [6, 6, 6, 0]]
    check("UPGMA, four taxa", upgma(*four), "(((A:1,B:1):1,C:2):1,D:3);")
    # Here the size-weighted average matters: d(ABC, D) = (2*10 + 1*8) / 3 = 9.3333, not (10 + 8) / 2 = 9.
    # The last join is at height 4.66667, so ABC hangs 1.66667 below it and D 4.66667.
    skewed = ["A", "B", "C", "D"], [[0, 2, 6, 10], [2, 0, 6, 10], [6, 6, 0, 8], [10, 10, 8, 0]]
    check("UPGMA weights clusters by size", upgma(*skewed), "(((A:1,B:1):2,C:3):1.66667,D:4.66667);")
    check("UPGMA, two taxa", upgma(["A", "B"], [[0, 5], [5, 0]]), "(A:2.5,B:2.5);")
    # Neighbour-joining must recover a known tree exactly when the distances are additive.
    truth = [("A", "#x", 2), ("B", "#x", 3), ("#x", "#y", 4), ("C", "#y", 1),
             ("#y", "#z", 2), ("D", "#z", 5), ("E", "#z", 1)]
    pd = path_distances(truth)
    for pair, want in ((("A", "B"), 5), (("A", "C"), 7), (("A", "D"), 13), (("D", "E"), 6), (("C", "E"), 4), (("B", "E"), 10)):
        check("hand-computed path %s-%s" % pair, pd[pair], want)
    names = leaves_of(truth)
    matrix = [[0.0 if a == b else pd[(a, b)] for b in names] for a in names]
    got = neighbor_joining(names, matrix)
    check("NJ edge count is 2n-3", len(got), 2 * len(names) - 3)
    check("NJ topology equals the true topology", splits(got), splits(truth))
    check("NJ edge lengths equal the true lengths", sorted(round(l, 9) for _, _, l in got),
          sorted(float(l) for _, _, l in truth))
    for pair, want in path_distances(got).items():
        check("NJ path distance %s-%s" % pair, want, pd[pair], 1e-9)
    # Random additive trees, grown by attaching each new leaf to a random edge.
    state = [99]

    def rnd(k):
        state[0] = (state[0] * 1103515245 + 12345) % (2 ** 31)
        return (state[0] >> 16) % k

    for trial in range(25):
        edges = [("t0", "#0", 1 + rnd(9)), ("t1", "#0", 1 + rnd(9)), ("t2", "#0", 1 + rnd(9))]
        internal = 1
        for leaf in range(3, 5 + rnd(5)):
            i = rnd(len(edges))
            a, b, length = edges.pop(i)
            mid, new = "#%d" % internal, "t%d" % leaf
            internal += 1
            cut = 1 + rnd(9)
            edges += [(a, mid, cut), (mid, b, cut + 1), (new, mid, 1 + rnd(9))]
        tn = leaves_of(edges)
        pdist = path_distances(edges)
        dm = [[0.0 if a == b else pdist[(a, b)] for b in tn] for a in tn]
        rec = neighbor_joining(tn, dm)
        check("random tree %d: topology recovered" % trial, splits(rec), splits(edges))
        for pair, want in path_distances(rec).items():
            check("random tree %d: distance %s-%s" % ((trial,) + pair), want, pdist[pair], 1e-9)
    check("NJ, two taxa", newick(neighbor_joining(["A", "B"], [[0, 5], [5, 0]])), "(A:2.5,B:2.5);")
    check("NJ, three taxa", newick(neighbor_joining(*three)), "(A:1,B:1,C:3);")
    check("matrix text round trip", read_matrix(",A,B\nA,0,2\nB,2,0\n"), (["A", "B"], [[0.0, 2.0], [2.0, 0.0]]))
    raises("asymmetric matrix", lambda: read_matrix(",A,B\nA,0,2\nB,3,0\n"))
    raises("non-zero diagonal", lambda: read_matrix(",A,B\nA,1,2\nB,2,0\n"))
    raises("duplicate labels", lambda: read_matrix(",A,A\nA,0,2\nA,2,0\n"))
    raises("label with punctuation", lambda: upgma(["A(", "B"], [[0, 1], [1, 0]]))
    print("tree.py self-test: %d checks passed" % n[0])


def _read_fasta(path):
    names, seqs = [], []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                names.append(line[1:].split()[0] if line[1:].split() else "")
                seqs.append([])
            elif line and seqs:
                seqs[-1].append(line)
    return names, ["".join(s) for s in seqs]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Distances and distance-based trees.")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("distances")
    s.add_argument("fasta")
    s.add_argument("--model", choices=("jc", "p"), default="jc")
    sub.add_parser("upgma").add_argument("matrix")
    sub.add_parser("nj").add_argument("matrix")
    s = sub.add_parser("jc")
    s.add_argument("a")
    s.add_argument("b")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    try:
        if a.cmd == "distances":
            names, seqs = _read_fasta(a.fasta)
            f = jc69 if a.model == "jc" else (lambda p: p)
            print("," + ",".join(names))
            for i, ni in enumerate(names):
                print(ni + "," + ",".join("0" if i == j else fmt(f(p_distance(seqs[i], seqs[j]))) for j in range(len(names))))
        elif a.cmd in ("upgma", "nj"):
            with open(a.matrix, encoding="utf-8") as fh:
                names, d = read_matrix(fh.read())
            print(upgma(names, d) if a.cmd == "upgma" else newick(neighbor_joining(names, d)))
        elif a.cmd == "jc":
            p = p_distance(a.a, a.b)
            print("p-distance %.6f   Jukes-Cantor %.6f" % (p, jc69(p)))
        else:
            ap.print_help()
            return 2
    except (ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
