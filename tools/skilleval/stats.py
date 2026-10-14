"""Statistics for skill evaluations (standard library only).

Small, separately tested functions used by the report and the human-grading kit:
Wilson interval for a pass rate, Newcombe interval for the difference of two pass rates, pass^k and pass@k
estimators for repeated runs, Cohen's kappa for agreement between two graders, an exact sign test, and a
seeded bootstrap interval for a mean.
"""
import math
import random
from statistics import NormalDist, mean, pstdev

_N = NormalDist()


def wilson(k, n, conf=0.95):
    """Wilson score interval for k successes in n trials. Returns (low, high); (0, 1) when n is 0."""
    if n <= 0:
        return 0.0, 1.0
    z = _N.inv_cdf(1 - (1 - conf) / 2)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def newcombe_diff(k1, n1, k2, n2, conf=0.95):
    """Newcombe (hybrid score) interval for p1 - p2. Returns (difference, low, high)."""
    if n1 <= 0 or n2 <= 0:
        return 0.0, -1.0, 1.0
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, conf)
    l2, u2 = wilson(k2, n2, conf)
    d = p1 - p2
    return d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)


def pass_hat_k(successes, n, k):
    """tau-bench style pass^k: the chance that k runs all succeed, estimated from c successes in n runs for
    each task as C(c,k)/C(n,k), averaged over tasks. `successes` is a list of c, one per task."""
    if not successes or k < 1 or k > n:
        raise ValueError("need tasks, 1 <= k <= n")
    return mean(math.comb(c, k) / math.comb(n, k) for c in successes)


def pass_at_k(successes, n, k):
    """pass@k: the chance that at least one of k runs succeeds, 1 - C(n-c,k)/C(n,k), averaged over tasks."""
    if not successes or k < 1 or k > n:
        raise ValueError("need tasks, 1 <= k <= n")
    return mean(1 - math.comb(n - c, k) / math.comb(n, k) for c in successes)


def cohen_kappa(a, b):
    """Cohen's kappa for two equal-length lists of labels. 1 is perfect agreement, 0 is chance level."""
    if len(a) != len(b) or not a:
        raise ValueError("need two non-empty lists of equal length")
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    labels = set(a) | set(b)
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    if pe == 1:
        return 1.0
    return (po - pe) / (1 - pe)


def sign_test(wins, losses):
    """Exact two-sided sign test p-value, ties already removed."""
    n = wins + losses
    if n == 0:
        return 1.0
    low = min(wins, losses)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(low + 1)) / float(2 ** n))


def bootstrap_mean(xs, n_boot=5000, conf=0.95, seed=1):
    """(mean, low, high) with a percentile bootstrap, seeded."""
    xs = list(xs)
    if len(xs) < 2:
        return (xs[0], xs[0], xs[0]) if xs else (0.0, 0.0, 0.0)
    rng = random.Random(seed)
    n = len(xs)
    reps = sorted(mean(xs[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot))
    lo = (1 - conf) / 2

    def q(f):
        h = (n_boot - 1) * f
        i = int(math.floor(h))
        j = min(i + 1, n_boot - 1)
        return reps[i] + (h - i) * (reps[j] - reps[i])
    return mean(xs), q(lo), q(1 - lo)


def mean_sd(xs):
    xs = list(xs)
    if not xs:
        return 0.0, 0.0
    return mean(xs), (pstdev(xs) if len(xs) > 1 else 0.0)


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=0.0):
        count[0] += 1
        ok = abs(got - want) <= tol if (tol or isinstance(want, float)) else got == want
        if not ok:
            fails.append("%s: got %r, want %r" % (name, got, want))

    lo, hi = wilson(5, 10)
    eq("wilson 5/10 low", lo, 0.2366, 5e-4)
    eq("wilson 5/10 high", hi, 0.7634, 5e-4)
    lo, hi = wilson(0, 10)
    eq("wilson 0/10 low", lo, 0.0, 1e-12)
    eq("wilson 0/10 high", hi, 0.2775, 5e-4)
    lo, hi = wilson(10, 10)
    eq("wilson 10/10 low", lo, 0.7225, 5e-4)
    eq("wilson 10/10 high", hi, 1.0, 1e-12)
    eq("wilson n=0", wilson(0, 0), (0.0, 1.0))
    lo, hi = wilson(50, 100)
    eq("wilson 50/100", (round(lo, 3), round(hi, 3)), (0.404, 0.596))
    eq("wilson narrows with n", wilson(500, 1000)[1] - wilson(500, 1000)[0] < wilson(5, 10)[1] - wilson(5, 10)[0], True)
    d, lo, hi = newcombe_diff(80, 100, 60, 100)
    eq("newcombe diff", d, 0.2, 1e-12)
    eq("newcombe low (statsmodels value)", lo, 0.0731, 5e-4)
    eq("newcombe high (statsmodels value)", hi, 0.3185, 5e-4)
    d, lo, hi = newcombe_diff(5, 10, 5, 10)
    eq("newcombe equal rates are centred on zero", abs(lo + hi) < 1e-12 and d == 0.0, True)
    eq("pass^3", pass_hat_k([3, 3, 0], 3, 3), 2 / 3.0, 1e-12)
    eq("pass^2", pass_hat_k([3, 2, 0], 3, 2), (1 + 1 / 3.0 + 0) / 3, 1e-12)
    eq("pass^1 is the mean rate", pass_hat_k([3, 2, 0], 3, 1), (3 + 2 + 0) / 9.0, 1e-12)
    eq("pass@3", pass_at_k([3, 2, 0], 3, 3), (1 + 1 + 0) / 3.0, 1e-12)
    eq("pass@1 equals pass^1", pass_at_k([3, 2, 0], 3, 1), pass_hat_k([3, 2, 0], 3, 1), 1e-12)
    eq("pass@2", pass_at_k([1], 3, 2), 1 - math.comb(2, 2) / math.comb(3, 2), 1e-12)
    eq("kappa perfect", cohen_kappa(list("ABAB"), list("ABAB")), 1.0, 1e-12)
    a = ["y"] * 25 + ["n"] * 25
    b = ["y"] * 20 + ["n"] * 5 + ["y"] * 10 + ["n"] * 15
    eq("kappa 0.4 example", cohen_kappa(a, b), 0.4, 1e-12)
    eq("kappa chance", cohen_kappa(list("AABB"), list("ABAB")), 0.0, 1e-12)
    eq("kappa single label", cohen_kappa(["a", "a"], ["a", "a"]), 1.0, 1e-12)
    eq("sign 5-0", sign_test(5, 0), 0.0625, 1e-12)
    eq("sign balanced", sign_test(3, 3), 1.0, 1e-12)
    eq("sign none", sign_test(0, 0), 1.0, 1e-12)
    eq("sign symmetric", sign_test(7, 2), sign_test(2, 7), 1e-15)
    eq("sign 7-2", sign_test(7, 2), 2 * (1 + 9 + 36) / 512.0, 1e-12)
    m, lo, hi = bootstrap_mean([0.2] * 6)
    eq("bootstrap constant", tuple(round(x, 12) for x in (m, lo, hi)), (0.2, 0.2, 0.2))
    m, lo, hi = bootstrap_mean([1, 2, 3, 4, 5, 6], 2000)
    eq("bootstrap brackets mean", lo <= m <= hi, True)
    eq("bootstrap seeded", bootstrap_mean([1, 5, 9], 300, seed=7), bootstrap_mean([1, 5, 9], 300, seed=7))
    eq("mean_sd", mean_sd([2, 4, 4, 4, 5, 5, 7, 9]), (5.0, 2.0))
    for bad, label in ((lambda: cohen_kappa([], []), "kappa empty"), (lambda: cohen_kappa(["a"], ["a", "b"]), "kappa lengths"),
                       (lambda: pass_hat_k([], 3, 1), "pass^k empty"), (lambda: pass_hat_k([1], 3, 4), "k>n")):
        count[0] += 1
        try:
            bad()
            fails.append("%s should raise" % label)
        except ValueError:
            pass
    return fails, count[0]
