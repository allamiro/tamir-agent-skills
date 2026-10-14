#!/usr/bin/env python3
"""Graph representations and measures for biological networks (standard library only).

  graphs.py matrices EDGES.txt [--directed]    adjacency matrix, incidence matrix and adjacency list
  graphs.py measures EDGES.txt [--directed]    degree, closeness and betweenness centrality, components
  graphs.py path EDGES.txt --from A --to D [--directed]   a shortest path (unweighted)
  graphs.py motifs EDGES.txt                   feed-forward loops (X->Y, Y->Z, X->Z) in a directed graph
  graphs.py --selftest

EDGES.txt has one edge per line, "A B" (an optional third column is a sign or label and is kept for display).
Incidence matrix convention for directed graphs: -1 where an edge leaves a node and +1 where it enters, the same
sign convention as a stoichiometric matrix. Betweenness is Brandes' algorithm on unweighted edges, normalised to
0..1. A feed-forward-loop count says how often the pattern occurs, not whether it is enriched; enrichment needs a
comparison with randomised networks of the same degrees.
"""
import argparse
import sys
from collections import deque


def read_edges(text):
    edges = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            raise ValueError("each edge needs two nodes: %r" % raw)
        edges.append((parts[0], parts[1], parts[2] if len(parts) > 2 else ""))
    if not edges:
        raise ValueError("no edges")
    return edges


def nodes_of(edges):
    out = []
    for a, b, _l in edges:
        for n in (a, b):
            if n not in out:
                out.append(n)
    return out


def adjacency(edges, directed):
    nodes = nodes_of(edges)
    idx = {n: i for i, n in enumerate(nodes)}
    m = [[0] * len(nodes) for _ in nodes]
    for a, b, _l in edges:
        m[idx[a]][idx[b]] = 1
        if not directed:
            m[idx[b]][idx[a]] = 1
    return nodes, m


def incidence(edges, directed):
    nodes = nodes_of(edges)
    idx = {n: i for i, n in enumerate(nodes)}
    m = [[0] * len(edges) for _ in nodes]
    for e, (a, b, _l) in enumerate(edges):
        if directed:
            m[idx[a]][e] -= 1
            m[idx[b]][e] += 1
        else:
            m[idx[a]][e] = 1
            m[idx[b]][e] = 1
    return nodes, m


def neighbours(edges, directed):
    nb = {n: [] for n in nodes_of(edges)}
    for a, b, _l in edges:
        if b not in nb[a]:
            nb[a].append(b)
        if not directed and a not in nb[b]:
            nb[b].append(a)
    return nb


def bfs(nb, src):
    dist, prev = {src: 0}, {src: None}
    q = deque([src])
    while q:
        u = q.popleft()
        for v in nb[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                prev[v] = u
                q.append(v)
    return dist, prev


def shortest_path(nb, a, b):
    if a not in nb or b not in nb:
        raise ValueError("unknown node")
    dist, prev = bfs(nb, a)
    if b not in dist:
        return None
    path, cur = [], b
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return path[::-1]


def components(nb):
    und = {n: set(v) for n, v in nb.items()}
    for n, vs in nb.items():
        for v in vs:
            und[v].add(n)
    seen, comps = set(), []
    for n in und:
        if n in seen:
            continue
        stack, comp = [n], []
        seen.add(n)
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in und[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        comps.append(sorted(comp))
    return comps


def closeness(nb):
    """Closeness of each node: (reachable - 1) / sum of distances, scaled by the reachable fraction (Wasserman-Faust)."""
    n = len(nb)
    out = {}
    for u in nb:
        dist, _ = bfs(nb, u)
        tot = sum(dist.values())
        r = len(dist) - 1
        out[u] = (r / tot) * (r / (n - 1)) if tot > 0 and n > 1 else 0.0
    return out


def betweenness(nb, directed):
    """Brandes' algorithm, normalised by the number of node pairs that could pass through a node."""
    bc = {v: 0.0 for v in nb}
    for s in nb:
        stack, pred = [], {w: [] for w in nb}
        sigma = {w: 0 for w in nb}
        sigma[s] = 1
        dist = {w: -1 for w in nb}
        dist[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            stack.append(v)
            for w in nb[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    q.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = {w: 0.0 for w in nb}
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += sigma[v] / sigma[w] * (1 + delta[w])
            if w != s:
                bc[w] += delta[w]
    n = len(nb)
    scale = (n - 1) * (n - 2)
    if not directed:
        scale /= 2.0
        bc = {v: x / 2.0 for v, x in bc.items()}
    return {v: (x / scale if scale else 0.0) for v, x in bc.items()}


def feed_forward_loops(edges):
    succ = {}
    for a, b, _l in edges:
        if a != b:
            succ.setdefault(a, set()).add(b)
    loops = []
    for x in succ:
        for y in succ[x]:
            for z in succ.get(y, ()):
                if z != x and z in succ[x] and z != y:
                    loops.append((x, y, z))
    return sorted(loops)


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=None):
        count[0] += 1
        ok = abs(got - want) <= tol if tol is not None else got == want
        if not ok:
            fails.append("%s: got %r, want %r" % (name, got, want))

    e = read_edges("A B\nB C\nA C\nC D  # comment")
    nodes, adj = adjacency(e, True)
    eq("directed adjacency", adj, [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]])
    nodes, inc = incidence(e, True)
    eq("incidence columns sum to zero (directed)", [sum(inc[i][j] for i in range(len(nodes))) for j in range(len(e))], [0, 0, 0, 0])
    eq("incidence sign: A leaves edge 1", inc[0][0], -1)
    nodes, inc = incidence(e, False)
    eq("undirected incidence column sums are 2", [sum(inc[i][j] for i in range(len(nodes))) for j in range(len(e))], [2, 2, 2, 2])
    nb = neighbours(e, True)
    eq("shortest path", shortest_path(nb, "A", "D"), ["A", "C", "D"])
    eq("no path backwards", shortest_path(nb, "D", "A"), None)
    eq("feed-forward loop found", feed_forward_loops(e), [("A", "B", "C")])
    star = read_edges("H A\nH B\nH C\nH D")
    bc = betweenness(neighbours(star, False), False)
    eq("star hub betweenness 1", bc["H"], 1.0, 1e-12)
    eq("star leaf betweenness 0", bc["A"], 0.0, 1e-12)
    path = read_edges("A B\nB C\nC D\nD E")
    bc = betweenness(neighbours(path, False), False)
    eq("path middle betweenness", bc["C"], 4 / 6.0, 1e-12)
    cl = closeness(neighbours(path, False))
    eq("path middle closeness", cl["C"], 4 / 6.0, 1e-12)
    eq("components", components(neighbours(read_edges("A B\nC D"), False)), [["A", "B"], ["C", "D"]])
    eq("self loop ignored in motifs", feed_forward_loops(read_edges("A A\nA B")), [])
    for bad, label in ((lambda: read_edges("A"), "single node line"), (lambda: read_edges("# only a comment"), "no edges"),
                       (lambda: shortest_path(neighbours(e, True), "A", "Z"), "unknown node")):
        count[0] += 1
        try:
            bad()
            fails.append("%s should raise" % label)
        except ValueError:
            pass
    # Added after a mutation test: each case below is hand-computed and covers a path the earlier checks missed.
    def _near(label, got, want, tol=1e-6):
        count[0] += 1
        if not abs(got - want) <= tol:
            fails.append("%s: got %r, want %r" % (label, got, want))

    def _same(label, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (label, got, want))

    def _raises(label, fn):
        count[0] += 1
        try:
            fn()
            fails.append("%s should raise" % label)
        except (ValueError, ZeroDivisionError):
            pass
    _nb = neighbours(read_edges("A B\nB C"), False)
    _cl = closeness(_nb)
    _near("closeness of the middle of a path", _cl["B"], 1.0)
    _near("closeness of an end of a path", _cl["A"], 2 / 3)
    _near("closeness in a split graph is scaled by the reachable share", closeness(neighbours(read_edges("A B\nC D"), False))["A"], 1 / 3)
    _n, _m = adjacency(read_edges("A B\nB C"), False)
    _same("undirected adjacency is symmetric", all(_m[i][j] == _m[j][i] for i in range(3) for j in range(3)), True)
    _bsq = betweenness(neighbours(read_edges("A B\nB C\nC D\nD A"), False), False)
    _near("square: two shortest paths A-C share B and D, betweenness 0.5 / 3", _bsq["B"], 1 / 6)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("graphs selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Graph representations and measures for biological networks.")
    ap.add_argument("op", nargs="?", choices=["matrices", "measures", "path", "motifs"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--directed", action="store_true")
    ap.add_argument("--from", dest="src")
    ap.add_argument("--to", dest="dst")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        e = read_edges(open(a.file, encoding="utf-8").read())
        if a.op == "matrices":
            nodes, adj = adjacency(e, a.directed)
            print("adjacency (rows: from, columns: to):\n  " + " ".join(nodes))
            for n, row in zip(nodes, adj):
                print("%-6s %s" % (n, " ".join(str(x) for x in row)))
            nodes, inc = incidence(e, a.directed)
            print("incidence (rows: nodes, columns: edges %s):" % ", ".join("%s-%s" % (x, y) for x, y, _l in e))
            for n, row in zip(nodes, inc):
                print("%-6s %s" % (n, " ".join("%2d" % x for x in row)))
            print("adjacency list:")
            for n, vs in neighbours(e, a.directed).items():
                print("  %s: %s" % (n, ", ".join(vs) or "-"))
        elif a.op == "measures":
            nb = neighbours(e, a.directed)
            bc, cl = betweenness(nb, a.directed), closeness(nb)
            indeg = {n: 0 for n in nb}
            for x, y, _l in e:
                indeg[y] += 1
            if a.directed:
                print("%-12s %6s %6s %10s %12s" % ("node", "out", "in", "closeness", "betweenness"))
            else:
                print("%-12s %6s %10s %12s" % ("node", "degree", "closeness", "betweenness"))
            for n in sorted(nb, key=lambda v: -bc[v]):
                if a.directed:
                    print("%-12s %6d %6d %10.3f %12.3f" % (n, len(nb[n]), indeg[n], cl[n], bc[n]))
                else:
                    print("%-12s %6d %10.3f %12.3f" % (n, len(nb[n]), cl[n], bc[n]))
            print("%d connected component(s) (ignoring direction)" % len(components(nb)))
        elif a.op == "path":
            p = shortest_path(neighbours(e, a.directed), a.src, a.dst)
            print(" -> ".join(p) if p else "no path")
        elif a.op == "motifs":
            loops = feed_forward_loops(e)
            print("%d feed-forward loop(s)" % len(loops))
            for x, y, z in loops:
                print("  %s -> %s -> %s, and %s -> %s" % (x, y, z, x, z))
        else:
            ap.error("give an operation or --selftest")
    except (ValueError, OSError, TypeError) as e_:
        print("error:", e_)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
