#!/usr/bin/env python3
"""One-compartment pharmacokinetics, non-compartmental AUC and a simple Emax model (standard library only).

  pk.py iv --dose 100 --V 20 --CL 5 --t 2              IV bolus: concentration at t, k, half-life, AUC to infinity
  pk.py oral --dose 100 --F 0.8 --V 20 --CL 5 --ka 1.5 --t 2   first-order absorption (Bateman): C(t), tmax, Cmax
  pk.py repeat --dose 100 --F 1 --V 20 --CL 5 --tau 8   repeated dosing: accumulation ratio and average steady state
  pk.py auc DATA.csv                                     trapezoidal AUC from columns t,C (log-down optional: --log-down)
  pk.py emax --C 2 --E0 0 --Emax 100 --EC50 1 [--n 1]   effect from concentration (sigmoid Emax when n is not 1)
  pk.py --selftest

Use consistent units: if dose is in mg and V in L, concentration comes out in mg/L; CL in L/h gives k in 1/h and
times in h. The model assumes linear (dose-proportional) kinetics and a single well-mixed compartment; real drugs
often need two or more compartments, and the right model is chosen from data, not assumed.
"""
import argparse
import csv
import math
import sys

LN2 = math.log(2)


def iv_bolus(dose, V, CL, t):
    k = CL / V
    return {"C": dose / V * math.exp(-k * t), "k": k, "half_life": LN2 / k, "AUC_inf": dose / CL, "C0": dose / V}


def oral(dose, F, V, CL, ka, t):
    k = CL / V
    if abs(ka - k) < 1e-12:
        c = F * dose / V * k * t * math.exp(-k * t)   # limit when ka == k
        tmax = 1 / k
    else:
        c = F * dose * ka / (V * (ka - k)) * (math.exp(-k * t) - math.exp(-ka * t))
        tmax = math.log(ka / k) / (ka - k)
    cmax = oral_c(dose, F, V, CL, ka, tmax)
    return {"C": c, "k": k, "tmax": tmax, "Cmax": cmax, "AUC_inf": F * dose / CL, "half_life": LN2 / k}


def oral_c(dose, F, V, CL, ka, t):
    k = CL / V
    if abs(ka - k) < 1e-12:
        return F * dose / V * k * t * math.exp(-k * t)
    return F * dose * ka / (V * (ka - k)) * (math.exp(-k * t) - math.exp(-ka * t))


def repeated(dose, F, V, CL, tau):
    k = CL / V
    r = 1 / (1 - math.exp(-k * tau))
    return {"accumulation_ratio": r, "Css_average": F * dose / (CL * tau), "k": k, "half_life": LN2 / k,
            "time_to_90pct_steady_state": math.log(10) / k}


def auc_trapezoid(t, c, log_down=False):
    if len(t) != len(c) or len(t) < 2:
        raise ValueError("need matching t and C with at least two points")
    if any(b <= a for a, b in zip(t, t[1:])):
        raise ValueError("times must increase")
    total = 0.0
    for (t1, c1), (t2, c2) in zip(zip(t, c), zip(t[1:], c[1:])):
        if log_down and c2 < c1 and c2 > 0 and c1 > 0:
            total += (c1 - c2) * (t2 - t1) / math.log(c1 / c2)
        else:
            total += (c1 + c2) / 2 * (t2 - t1)
    return total


def emax(C, E0, Emax, EC50, n=1.0):
    return E0 + Emax * C ** n / (EC50 ** n + C ** n)


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=1e-9):
        count[0] += 1
        if abs(got - want) > tol:
            fails.append("%s: got %r, want %r" % (name, got, want))

    r = iv_bolus(100, 20, 5, 0)
    eq("C0 = dose/V", r["C"], 5)
    eq("half-life ln2 V/CL", r["half_life"], LN2 * 4)
    eq("AUC = dose/CL", r["AUC_inf"], 20)
    eq("one half-life halves C", iv_bolus(100, 20, 5, LN2 * 4)["C"], 2.5)
    o = oral(100, 1, 20, 5, 1.5, 0)
    eq("oral starts at zero", o["C"], 0)
    k = 0.25
    eq("tmax formula", o["tmax"], math.log(1.5 / k) / (1.5 - k))
    eq("Cmax is the maximum", max(oral_c(100, 1, 20, 5, 1.5, i / 100) for i in range(0, 3000)), o["Cmax"], 1e-4)
    eq("ka equal to k uses the limit", oral(100, 1, 20, 5, 0.25, 4)["C"], 100 / 20 * 0.25 * 4 * math.exp(-1), 1e-12)
    eq("ka near k is continuous", oral(100, 1, 20, 5, 0.25 + 1e-7, 4)["C"], oral(100, 1, 20, 5, 0.25, 4)["C"], 1e-5)
    times = [i / 10 for i in range(0, 600)]
    num = auc_trapezoid(times, [oral_c(100, 0.8, 20, 5, 1.5, t) for t in times])
    eq("numerical AUC approaches F dose / CL", num, 0.8 * 100 / 5, 0.01)
    rp = repeated(100, 1, 20, 5, 8)
    eq("accumulation ratio", rp["accumulation_ratio"], 1 / (1 - math.exp(-2)))
    eq("average steady state", rp["Css_average"], 100 / 40)
    eq("about 3.3 half-lives to 90 percent", rp["time_to_90pct_steady_state"] / rp["half_life"], math.log(10) / LN2)
    eq("trapezoid exact for linear decline", auc_trapezoid([0, 2], [4, 0]), 4)
    eq("log-down exact for exponential", auc_trapezoid([0, 1], [8, 4], log_down=True), 4 / LN2)
    eq("Emax at EC50", emax(1, 0, 100, 1), 50)
    eq("sigmoid Emax steeper", emax(2, 0, 100, 1, 3) > emax(2, 0, 100, 1, 1), 1, 0)
    for bad, label in ((lambda: auc_trapezoid([0, 0], [1, 1]), "repeated time"), (lambda: auc_trapezoid([0], [1]), "one point")):
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
    _o = oral(100, 1, 20, 5, 0.25, 4)
    _near("oral with ka = k: C = (F D / V) k t e^(-kt)", _o["C"], 5 * 0.25 * 4 * math.exp(-1))
    _near("oral with ka = k: tmax = 1/k", _o["tmax"], 4)
    _near("oral AUC to infinity = F D / CL", oral(100, 0.8, 20, 5, 1.5, 2)["AUC_inf"], 16)
    _near("log-down AUC: 2 rising + 2/ln 2 falling", auc_trapezoid([0, 1, 2], [0, 4, 2], log_down=True), 2 + 2 / math.log(2))
    _near("linear AUC of the same points", auc_trapezoid([0, 1, 2], [0, 4, 2]), 5)
    _near("log-down with a 2 h interval: 2 + 4/ln 2", auc_trapezoid([0, 1, 3], [0, 4, 2], log_down=True), 2 + 4 / math.log(2))
    _near("oral_c with ka = k and F = 0.5", oral_c(100, 0.5, 20, 5, 0.25, 4), 0.5 * 5 * 0.25 * 4 * math.exp(-1))
    _iv = iv_bolus(100, 20, 5, 2)
    _near("IV half-life ln 2 / 0.25", _iv["half_life"], math.log(2) / 0.25)
    _near("IV AUC dose / CL", _iv["AUC_inf"], 20)
    _near("IV C0 dose / V", _iv["C0"], 5)
    _near("oral half-life", oral(100, 0.8, 20, 5, 1.5, 2)["half_life"], math.log(2) / 0.25)
    if fails:
        print("SELFTEST FAILED")
        for f in fails:
            print(" -", f)
        return 1
    print("pk selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="One-compartment pharmacokinetics, AUC and Emax.")
    ap.add_argument("op", nargs="?", choices=["iv", "oral", "repeat", "auc", "emax"])
    ap.add_argument("file", nargs="?")
    for name in ("dose", "V", "CL", "t", "F", "ka", "tau", "C", "E0", "Emax", "EC50"):
        ap.add_argument("--" + name, type=float)
    ap.add_argument("--n", type=float, default=1.0)
    ap.add_argument("--log-down", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        if a.op == "iv":
            res = iv_bolus(a.dose, a.V, a.CL, a.t or 0.0)
        elif a.op == "oral":
            res = oral(a.dose, a.F if a.F is not None else 1.0, a.V, a.CL, a.ka, a.t or 0.0)
        elif a.op == "repeat":
            res = repeated(a.dose, a.F if a.F is not None else 1.0, a.V, a.CL, a.tau)
        elif a.op == "auc":
            rows = list(csv.DictReader(open(a.file, newline="", encoding="utf-8")))
            res = {"AUC_0_tlast": auc_trapezoid([float(r["t"]) for r in rows], [float(r["C"]) for r in rows], a.log_down)}
        elif a.op == "emax":
            res = {"E": emax(a.C, a.E0 or 0.0, a.Emax, a.EC50, a.n)}
        else:
            ap.error("give an operation or --selftest")
        for k_, v in res.items():
            print("%-28s %.6g" % (k_, v))
    except (ValueError, TypeError, OSError, KeyError, ZeroDivisionError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
